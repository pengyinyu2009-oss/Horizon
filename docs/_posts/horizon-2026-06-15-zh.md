# Horizon 每日速递 - 2026-06-15

> 从 28 条内容中筛选出 19 条重要资讯。

---

1. [Publishing WASM wheels to PyPI for use with Pyodide](#item-1) ⭐️ 9.0/10
2. [Rio de Janeiro's "homegrown" LLM appears to be a merge of an existing model](#item-2) ⭐️ 8.0/10
3. [Formal methods and the future of programming](#item-3) ⭐️ 8.0/10
4. [Why AI hasn’t replaced software engineers, and won’t](#item-4) ⭐️ 8.0/10
5. [The Verifier Tax: Horizon-Dependent Safety–Success Tradeoffs in Tool-Using LLM Agents (R)](#item-5) ⭐️ 8.0/10
6. [Your ePub Is fine](#item-6) ⭐️ 7.0/10
7. [Show HN: Kage – Shadow any website to a single binary for offline viewing](#item-7) ⭐️ 7.0/10
8. [Mapping SQLite result columns back to their source `table.column`](#item-8) ⭐️ 7.0/10
9. [I built an open-source Knowledge Graph pipeline with hybrid retrieval to improve LLM multi-hop reasoning (P)](#item-9) ⭐️ 7.0/10
10. [PaddleOCR (v3/v4/v5/v6) implemented in C++ with ncnn (P)](#item-10) ⭐️ 7.0/10
11. [Show HN: Trace – Offline Mac meeting transcripts you can flag mid-call](#item-11) ⭐️ 6.0/10
12. [Perlisisms (1982)](#item-12) ⭐️ 6.0/10
13. [Caddy compatibility for zeroserve: 3x throughput and 70% lower latency](#item-13) ⭐️ 6.0/10
14. [Quant firms at ICML 2026 (D)](#item-14) ⭐️ 6.0/10
15. [How does the ML community view evolutionary algorithm research? Career implications of an EA PhD? (D)](#item-15) ⭐️ 6.0/10
16. [I’m building a free bilingual machine-learning notebook course — looking for feedback on structure and coverage (R)](#item-16) ⭐️ 6.0/10
17. [Anomaly Detection vs Classification for Visually Similar Cancer vs Mimics? (P)](#item-17) ⭐️ 6.0/10
18. [Ask HN: What are you working on? (June 2026)](#item-18) ⭐️ 5.0/10
19. [Quoting Julia Evans](#item-19) ⭐️ 4.0/10

---

<a id="item-1"></a>
## [Publishing WASM wheels to PyPI for use with Pyodide](https://simonwillison.net/2026/Jun/13/publishing-wasm-wheels/#atom-everything) ⭐️ 9.0/10

Pyodide 314.0 allows Python package maintainers to publish WASM wheels directly to PyPI, eliminating the need for manual packaging by Pyodide maintainers.

rss · Simon Willison · 6月13日 23:55

**标签**: `#Pyodide`, `#WebAssembly`, `#Python`, `#PyPI`, `#WASM`

---

<a id="item-2"></a>
## [Rio de Janeiro's "homegrown" LLM appears to be a merge of an existing model](https://github.com/nex-agi/Nex-N2/issues/4) ⭐️ 8.0/10

Rio de Janeiro's claimed homegrown LLM is actually a weighted merge of existing models, raising questions about transparency in AI development.

hackernews · unrvl22 · 6月14日 15:37 · [社区讨论](https://news.ycombinator.com/item?id=48528371)

**标签**: `#LLM`, `#open-source`, `#model merging`, `#controversy`, `#AI ethics`

---

<a id="item-3"></a>
## [Formal methods and the future of programming](https://blog.janestreet.com/formal-methods-at-jane-street-index/?from_theconsensus=1) ⭐️ 8.0/10

Jane Street shares their experience using formal methods in production, highlighting how proof automation and type systems can improve code reliability, especially in the age of AI-generated code.

hackernews · eatonphil · 6月14日 12:35 · [社区讨论](https://news.ycombinator.com/item?id=48526633)

**标签**: `#formal methods`, `#programming languages`, `#type systems`, `#verification`, `#software engineering`

---

<a id="item-4"></a>
## [Why AI hasn’t replaced software engineers, and won’t](https://simonwillison.net/2026/Jun/14/why-ai-hasnt-replaced-software-engineers/#atom-everything) ⭐️ 8.0/10

Arvind Narayanan and Sayash Kapoor argue that evidence does not support AI causing mass layoffs in software engineering, and this likely applies to other professions as well.

rss · Simon Willison · 6月14日 23:54

**标签**: `#AI`, `#software engineering`, `#job displacement`, `#labor economics`

---

<a id="item-5"></a>
## [The Verifier Tax: Horizon-Dependent Safety–Success Tradeoffs in Tool-Using LLM Agents (R)](https://www.reddit.com/r/MachineLearning/comments/1u58mkq/the_verifier_tax_horizondependent_safetysuccess/) ⭐️ 8.0/10

This paper identifies a horizon-dependent safety-success tradeoff in tool-using LLM agents, termed the 'Verifier Tax,' and proposes a two-tier verification architecture to mitigate unsafe successes.

reddit · r/MachineLearning · /u/AccomplishedLeg1508 · 6月14日 02:09

**标签**: `#LLM agents`, `#AI safety`, `#verification`, `#tool use`, `#evaluation`

---

<a id="item-6"></a>
## [Your ePub Is fine](https://andreklein.net/your-epub-is-fine-kobo-disagrees-blame-adobe/) ⭐️ 7.0/10

A technical deep-dive into why valid ePub files may render incorrectly on Kobo devices due to Adobe's RMSDK, with community discussion offering solutions like kepub conversion.

hackernews · sohkamyung · 6月14日 22:54 · [社区讨论](https://news.ycombinator.com/item?id=48533848)

**标签**: `#ePub`, `#Kobo`, `#Adobe`, `#e-reader`, `#software quality`

---

<a id="item-7"></a>
## [Show HN: Kage – Shadow any website to a single binary for offline viewing](https://github.com/tamnd/kage) ⭐️ 7.0/10

Kage is a tool that shadows any website into a single binary for offline viewing, generating static snapshots served via a built-in server.

hackernews · tamnd · 6月14日 17:25 · [社区讨论](https://news.ycombinator.com/item?id=48529990)

**标签**: `#offline`, `#archiving`, `#static-site`, `#tool`, `#web`

---

<a id="item-8"></a>
## [Mapping SQLite result columns back to their source `table.column`](https://simonwillison.net/2026/Jun/13/sqlite-column-provenance/#atom-everything) ⭐️ 7.0/10

Simon Willison explores programmatically mapping SQL query result columns back to their source table.column, using Claude Code to find solutions.

rss · Simon Willison · 6月13日 23:05

**标签**: `#SQL`, `#Datasette`, `#query analysis`, `#AI-assisted development`

---

<a id="item-9"></a>
## [I built an open-source Knowledge Graph pipeline with hybrid retrieval to improve LLM multi-hop reasoning (P)](https://www.reddit.com/r/MachineLearning/comments/1u5yyyl/i_built_an_opensource_knowledge_graph_pipeline/) ⭐️ 7.0/10

An open-source pipeline that builds knowledge graphs from text, detects thematic communities, and uses hybrid retrieval to improve LLM multi-hop reasoning.

reddit · r/MachineLearning · /u/Future_Caregiver_643 · 6月14日 22:38

**标签**: `#knowledge graph`, `#hybrid retrieval`, `#LLM`, `#open-source`, `#NLP`

---

<a id="item-10"></a>
## [PaddleOCR (v3/v4/v5/v6) implemented in C++ with ncnn (P)](https://www.reddit.com/r/MachineLearning/comments/1u4hy2x/paddleocr_v3v4v5v6_implemented_in_c_with_ncnn_p/) ⭐️ 7.0/10

A lightweight C++ implementation of PaddleOCR (v3-v6) using ncnn for easier deployment.

reddit · r/MachineLearning · /u/Knok0932 · 6月13日 05:06

**标签**: `#OCR`, `#C++`, `#ncnn`, `#PaddleOCR`, `#deployment`

---

<a id="item-11"></a>
## [Show HN: Trace – Offline Mac meeting transcripts you can flag mid-call](https://traceapp.info/) ⭐️ 6.0/10

Trace is a Mac app for offline meeting transcription activated by a global shortcut, with on-device processing and a one-time purchase.

hackernews · AG342 · 6月13日 20:41 · [社区讨论](https://news.ycombinator.com/item?id=48521236)

**标签**: `#meeting transcription`, `#macOS`, `#offline`, `#productivity`, `#privacy`

---

<a id="item-12"></a>
## [Perlisisms (1982)](https://www.cs.yale.edu/homes/perlis-alan/quotes.html) ⭐️ 6.0/10

A collection of aphorisms by Alan Perlis on programming, languages, and computer science, sparking reflective discussion.

hackernews · tosh · 6月14日 14:56 · [社区讨论](https://news.ycombinator.com/item?id=48527820)

**标签**: `#programming`, `#philosophy`, `#quotes`, `#computer science`

---

<a id="item-13"></a>
## [Caddy compatibility for zeroserve: 3x throughput and 70% lower latency](https://su3.io/posts/zeroserve-caddy-compat) ⭐️ 6.0/10

Zeroserve achieves 3x throughput and 70% lower latency with Caddy compatibility but lacks ACME and plugin support, drawing mixed reactions.

hackernews · losfair · 6月14日 13:43 · [社区讨论](https://news.ycombinator.com/item?id=48527145)

**标签**: `#web server`, `#performance`, `#io_uring`, `#Caddy`, `#Rust`

---

<a id="item-14"></a>
## [Quant firms at ICML 2026 (D)](https://www.reddit.com/r/MachineLearning/comments/1u64rse/quant_firms_at_icml_2026_d/) ⭐️ 6.0/10

A Reddit user notes that quant firms are heavily sponsoring ICML 2026 and asks for reasons.

reddit · r/MachineLearning · /u/Intrepid_Discount_67 · 6月15日 03:09

**标签**: `#ICML`, `#quantitative finance`, `#sponsorship`, `#machine learning`

---

<a id="item-15"></a>
## [How does the ML community view evolutionary algorithm research? Career implications of an EA PhD? (D)](https://www.reddit.com/r/MachineLearning/comments/1u66q3l/how_does_the_ml_community_view_evolutionary/) ⭐️ 6.0/10

A master's student asks about the ML community's perception of evolutionary algorithms and career implications of pursuing a PhD in that area.

reddit · r/MachineLearning · /u/NullRecurrentDad · 6月15日 04:48

**标签**: `#evolutionary algorithms`, `#career advice`, `#machine learning`, `#PhD`

---

<a id="item-16"></a>
## [I’m building a free bilingual machine-learning notebook course — looking for feedback on structure and coverage (R)](https://www.reddit.com/r/MachineLearning/comments/1u4zbld/im_building_a_free_bilingual_machinelearning/) ⭐️ 6.0/10

A free bilingual (English/Persian) Jupyter notebook-based machine learning course is being developed and the author seeks community feedback on structure and coverage.

reddit · r/MachineLearning · /u/abolfazl1363 · 6月13日 19:07

**标签**: `#machine learning`, `#education`, `#open source`, `#bilingual`, `#Jupyter notebooks`

---

<a id="item-17"></a>
## [Anomaly Detection vs Classification for Visually Similar Cancer vs Mimics? (P)](https://www.reddit.com/r/MachineLearning/comments/1u4obgy/anomaly_detection_vs_classification_for_visually/) ⭐️ 6.0/10

A researcher seeks advice on whether to use anomaly detection or supervised classification for distinguishing visually similar cancer from mimics.

reddit · r/MachineLearning · /u/DryHat3296 · 6月13日 11:18

**标签**: `#anomaly detection`, `#classification`, `#medical imaging`, `#machine learning`

---

<a id="item-18"></a>
## [Ask HN: What are you working on? (June 2026)](https://news.ycombinator.com/item?id=48528779) ⭐️ 5.0/10

A monthly thread where HN users share personal projects and ideas, ranging from PCB design to game development.

hackernews · david927 · 6月14日 16:05

**标签**: `#community`, `#projects`, `#hackernews`, `#discussion`

---

<a id="item-19"></a>
## [Quoting Julia Evans](https://simonwillison.net/2026/Jun/15/julia-evans/#atom-everything) ⭐️ 4.0/10

Simon Willison shares Julia Evans' advice to write for a specific person rather than a general audience.

rss · Simon Willison · 6月15日 02:05

**标签**: `#writing`, `#advice`, `#julia-evans`

---

