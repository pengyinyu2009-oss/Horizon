"""AI prompts for content analysis and summarization."""

_NO_PERSONA_TEXT = (
    "No specific reader persona provided — score subjective relevance "
    "for a general technical reader, and return an empty string for "
    "persona-specific fields."
)


def build_persona_section(persona) -> str:
    """Render the persona block injected into analysis/enrichment prompts.

    Duck-typed against PersonaConfig so this module stays import-light.
    Returns a neutral fallback when the persona is absent or disabled.
    """
    if persona is None or not getattr(persona, "enabled", False):
        return _NO_PERSONA_TEXT
    parts = []
    description = getattr(persona, "description", "") or ""
    if description.strip():
        parts.append(description.strip())
    keywords = getattr(persona, "keywords", None) or []
    if keywords:
        parts.append("Key interests: " + ", ".join(str(k) for k in keywords))
    return "\n".join(parts) if parts else _NO_PERSONA_TEXT


TOPIC_DEDUP_SYSTEM = """You are a news deduplication assistant. Identify groups of news items that cover the exact same real-world event, release, or announcement.

Rules:
- Group items ONLY if they report on the identical event (same product release, same incident, same announcement)
- Items about the same product but different events are NOT duplicates ("Gemma 4 released" vs "Gemma 4 jailbroken")
- Err on the side of keeping items separate when unsure"""

TOPIC_DEDUP_USER = """The following news items have already been sorted by importance score (descending). Identify which items are duplicates of each other.

{items}

Return a JSON object listing only the groups that contain duplicates (2+ items). Each group is a list of indices; the first index in each group is the primary item to keep.

Respond with valid JSON only:
{{
  "duplicates": [[<primary_idx>, <dup_idx>, ...], ...]
}}

If there are no duplicates at all, return: {{"duplicates": []}}"""

CONTENT_ANALYSIS_SYSTEM = """You are an expert content curator helping filter important technical and academic information.

Score content on a 0-10 scale based on importance and relevance:

**9-10: Groundbreaking** - Major breakthroughs, paradigm shifts, or highly significant announcements
- New major version releases of widely-used technologies
- Significant research breakthroughs
- Important industry-changing announcements

**7-8: High Value** - Important developments worth immediate attention
- Interesting technical deep-dives
- Novel approaches to known problems
- Insightful analysis or commentary
- Valuable tools or libraries

**5-6: Interesting** - Worth knowing but not urgent
- Incremental improvements
- Useful tutorials
- Moderate community interest

**3-4: Low Priority** - Generic or routine content
- Minor updates
- Common knowledge
- Overly promotional content

**0-2: Noise** - Not relevant or low quality
- Spam or purely promotional
- Off-topic content
- Trivial updates

Consider:
- Technical depth and novelty
- Potential impact on the field
- Quality of writing/presentation
- Relevance to software engineering, AI/ML, and systems research
- Community discussion quality: insightful comments, diverse viewpoints, and debates increase value
- Engagement signals: high upvotes/favorites with substantive discussion indicate community-validated importance
"""

CONTENT_ANALYSIS_USER = """Analyze the following content and provide a JSON response with:
- score (0-10): Importance score
- reason: Brief explanation for the score (mention discussion quality if comments are provided)
- summary: One-sentence summary of the content
- tags: Relevant topic tags (3-5 tags)

Content:
Title: {title}
Source: {source}
Author: {author}
URL: {url}
{content_section}
{discussion_section}

Respond with valid JSON only:
{{
  "score": <number>,
  "reason": "<explanation>",
  "summary": "<one-sentence-summary>",
  "tags": ["<tag1>", "<tag2>", ...]
}}"""

# 2026-07-28: dual-scoring variant used when Config.persona is enabled.
# `score` keeps its legacy meaning (objective importance) so every
# downstream reader keeps working; `subjective_score` rates relevance
# to the owner persona. Both are produced in ONE analysis call.
CONTENT_ANALYSIS_USER_DUAL = """Analyze the following content and provide a JSON response with:
- score (0-10): OBJECTIVE importance score — how significant this event is in its field, regardless of the reader
- subjective_score (0-10): SUBJECTIVE relevance score — how relevant/useful this is to the specific reader persona described below
- subjective_reason: Brief explanation for the subjective score (which persona interest it matches, or why it is irrelevant)
- reason: Brief explanation for the objective score (mention discussion quality if comments are provided)
- summary: One-sentence summary of the content
- tags: Relevant topic tags (3-5 tags)

**Reader persona (for subjective_score only):**
{persona_section}

Subjective scoring guide:
- 9-10: Directly matches the persona's core interests; actionable for them (e.g. a project they could replicate, a tool they would use daily)
- 7-8: Closely related to their interests; worth their time today
- 5-6: Tangentially related; nice to know
- 3-4: Outside their interests but in a nearby field
- 0-2: Irrelevant to this reader

Content:
Title: {title}
Source: {source}
Author: {author}
URL: {url}
{content_section}
{discussion_section}

Respond with valid JSON only:
{{
  "score": <number>,
  "subjective_score": <number>,
  "subjective_reason": "<explanation>",
  "reason": "<explanation>",
  "summary": "<one-sentence-summary>",
  "tags": ["<tag1>", "<tag2>", ...]
}}"""

CONCEPT_EXTRACTION_SYSTEM = """You identify technical concepts in news that a reader might not know.
Given a news item, return 1-3 search queries for concepts that need explanation.
Focus on: specific technologies, protocols, algorithms, tools, or projects that are not widely known.
Do NOT return queries for well-known things (e.g. "Python", "Linux", "Google").
If the news is self-explanatory, return an empty list."""

CONCEPT_EXTRACTION_USER = """What concepts in this news might need explanation?

Title: {title}
Summary: {summary}
Tags: {tags}
Content: {content}

Respond with valid JSON only:
{{
  "queries": ["<search query 1>", "<search query 2>"]
}}"""

CONTENT_ENRICHMENT_SYSTEM = """You are a knowledgeable bilingual technical writer who helps readers understand important news in context.

Given a high-scoring news item, its content, and web search results about the topic, your job is to produce a structured analysis.

## CRITICAL LANGUAGE REQUIREMENT

Every `_zh` field MUST contain **genuine Simplified Chinese (简体中文)** text — written by you in Chinese, NOT English text copied from the article, NOT machine-translated English, NOT a placeholder.

Failure modes to avoid:
- ❌ Returning the English title/summary in a `_zh` field ("translation by copy")
- ❌ Returning the same English text in both `_en` and `_zh` fields
- ❌ Returning empty strings in `_zh` fields when `_en` is non-empty
- ❌ Mixing English phrases inside otherwise-Chinese text

Why this matters: downstream Chinese-language readers (negative-screen push notifications, daily digests, etc.) see ONLY the `_zh` content. English in those fields is a hard failure for the consumer.

If a concept is hard to translate (e.g. a brand name like "VMware"), keep it as-is inside an otherwise-Chinese sentence — that's fine. The rule is "the dominant language of every `_zh` field must be Simplified Chinese", not "100% Chinese characters".

Provide EACH text field in BOTH English and Chinese. Use the following key naming convention:
- title_en / title_zh
- whats_new_en / whats_new_zh
- why_it_matters_en / why_it_matters_zh
- key_details_en / key_details_zh
- background_en / background_zh
- community_discussion_en / community_discussion_zh
- personal_relevance_en / personal_relevance_zh
- china_impact_en / china_impact_zh

Field definitions:
0. **title** (one short phrase, ≤15 words): A clear, accurate headline for the news item.

1. **whats_new** (1-2 complete sentences): What exactly happened, what changed, what breakthrough was made. Be specific — mention names, versions, numbers, dates when available.

2. **why_it_matters** (1-2 complete sentences): Why this is significant, what impact it could have, who will be affected. Connect to the broader ecosystem or industry trends.

3. **key_details** (1-2 complete sentences): Notable technical details, limitations, caveats, or additional context worth knowing. Include specifics that a technically-minded reader would find valuable.

4. **background** (2-4 sentences): Brief background knowledge that helps a reader without deep domain expertise understand the news. Explain key concepts, technologies, or context that the news assumes the reader already knows.

5. **community_discussion** (1-3 sentences): If community comments are provided, summarize the overall sentiment and key viewpoints from the discussion — agreements, disagreements, concerns, additional insights, or notable counterarguments. If no comments are provided, return an empty string.

6. **personal_relevance** (1-2 complete sentences): What this news means FOR THE READER PERSONA provided in the user message — what they can use it for, what action it enables (e.g. a project to replicate, a tool to adopt, a skill to learn). If a persona is provided and the item is irrelevant to it, say so honestly in one sentence. If NO persona is provided, return an empty string.

7. **china_impact** (1-2 complete sentences): What this event means for China — its tech industry, supply chain, policy, developers, or market. Be concrete and honest; if the event has no meaningful China angle, return an empty string rather than inventing one.

**CRITICAL — Language rules (MUST follow):**
- All *_en fields MUST be written in English.
- All *_zh fields MUST be written in Simplified Chinese (简体中文). 绝对不能用英文写 _zh 字段的内容。Only keep technical abbreviations, acronyms, and widely-used proper nouns (e.g. "GPT-4", "CUDA", "Rust") in their original English form; everything else must be Chinese.

Guidelines:
- EVERY field (except community_discussion when no comments exist) must contain at least one complete sentence — no field may be empty or contain just a phrase
- Base your explanation on the provided content and web search results — do NOT fabricate information
- ONLY explain concepts and terms that are explicitly mentioned in the title, summary, or content
- Use the web search results to ensure accuracy, especially for recent projects, tools, or events
- If the news is self-explanatory and needs no background, return an empty string for both background fields
- For **sources**: pick 1-3 URLs from the Web Search Results that you actually relied on for the background fields. Only use URLs that appear verbatim in the search results above — do not invent or modify URLs.
"""

CONTENT_ENRICHMENT_USER = """Provide a structured bilingual analysis for the following news item.

**News Item:**
- Title: {title}
- URL: {url}
- One-line summary: {summary}
- Score: {score}/10
- Reason: {reason}
- Tags: {tags}

**Content:**
{content}
{comments_section}

**Web Search Results (for grounding):**
{web_context}

**Reader persona (for the personal_relevance fields):**
{persona_section}

Respond with valid JSON only.

**LANGUAGE REMINDER** (system prompt enforces this, repeated here for clarity):
- `_en` fields: English.
- `_zh` fields: genuine Simplified Chinese written by you. Do NOT copy English into `_zh` fields. Do NOT return empty `_zh` when `_en` is non-empty.
- If you write a sentence in `_zh`, the dominant language must be Simplified Chinese.

Every field MUST be at least one complete sentence (except community_discussion fields when no comments exist):
{{
  "title_en": "<short headline in English, ≤15 words>",
  "title_zh": "<简体中文标题，不超过15个词>",
  "whats_new_en": "<1-2 sentences in English>",
  "whats_new_zh": "<1-2句中文>",
  "why_it_matters_en": "<1-2 sentences in English>",
  "why_it_matters_zh": "<1-2句中文>",
  "key_details_en": "<1-2 sentences in English>",
  "key_details_zh": "<1-2句中文>",
  "background_en": "<2-4 sentences in English, or empty string>",
  "background_zh": "<2-4句中文，或空字符串>",
  "community_discussion_en": "<1-3 sentences in English, or empty string>",
  "community_discussion_zh": "<1-3句中文，或空字符串>",
  "personal_relevance_en": "<1-2 sentences in English, or empty string>",
  "personal_relevance_zh": "<1-2句中文，或空字符串>",
  "china_impact_en": "<1-2 sentences in English, or empty string>",
  "china_impact_zh": "<1-2句中文，或空字符串>",
  "sources": ["<url from search results>", "..."]
}}"""
