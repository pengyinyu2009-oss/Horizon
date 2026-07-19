---
layout: default
title: "Horizon Daily: 2026-07-19 (ZH)"
date: 2026-07-19
lang: zh
period: daily
period_id: 2026-07-19
---

> 从 19 条内容中筛选出 8 条重要资讯。

其中 **5 条 8 分以上**展开详细简报，其余 3 条仅列于索引。

---

1. [GPT-5.6 Sol Pro 解决凸优化领域 30 年未解难题](#item-1) ⭐️ 8.0/10
2. [LG 显示器通过 Windows Update 静默安装未经同意的软件](#item-2) ⭐️ 8.0/10
3. [Anthropic 将 Claude Fable 5 永久纳入 Max 和 Team Premium 套餐](#item-3) ⭐️ 8.0/10
4. [涉嫌 AI 垃圾作品赢得 DeepMind Kaggle 2.5 万美元大奖](#item-4) ⭐️ 8.0/10
5. [GPT-2 词元嵌入空间的交互式地图](#item-5) ⭐️ 8.0/10
6. [Fable 5 与 GPT-5.6 Sol 在 NP 难问题上的对决：/goal 指令有效吗？](#item-6) ⭐️ 7.0/10
7. [GPT-2 Small 嵌入几何：'Trump'的离散与连续近邻对比](#item-7) ⭐️ 7.0/10
8. [单细胞 RNA 测序分析的 25 种深度学习方法综述](#item-8) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [GPT-5.6 Sol Pro 解决凸优化领域 30 年未解难题](https://old.reddit.com/r/math/comments/1uxj3cy/after_openais_cdc_proof_announcement_gpt56_used_a/) ⭐️ 8.0/10

GPT-5.6 Sol Pro（OpenAI GPT-5.6 模型的一个变体）通过一个提示词，证明了一个关于在球形域上优化凸 Lipschitz 函数时间复杂度的猜想，从而填补了凸优化领域一个长达 30 年的空白。 这表明大型语言模型能够攻克数学研究中的中等难度问题，可能加速优化理论及相关领域的进展。同时也凸显了人工智能在形式化数学发现中日益重要的作用。 使用的模型是 GPT-5.6 Sol Pro，而非更高级的 Ultra 版本。该猜想虽较为小众，但仍是一项实质性贡献，且证明是通过单次提示词生成，无需迭代优化。

hackernews · mbustamanter · 7月18日 13:00 · [社区讨论](https://news.ycombinator.com/item?id=48957779)

**背景**: 凸优化研究在凸集上最小化凸函数的问题，广泛应用于机器学习、工程和经济学。该开放问题涉及证明在球形域上优化凸 Lipschitz 函数的时间复杂度上界，此前已悬而未决 30 年。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://openrouter.ai/openai/gpt-5.6-sol-pro">GPT-5.6 Sol Pro - API Pricing & Providers | OpenRouter</a></li>
<li><a href="https://en.wikipedia.org/wiki/Convex_optimization">Convex optimization - Wikipedia</a></li>
<li><a href="https://every.to/vibe-check/gpt-5-6-sol">GPT-5.6 Sol Is Our Favorite Model to Collaborate With - Every</a></li>

</ul>
</details>

**社区讨论**: 社区评论指出，该猜想的解决比 OpenAI 之前证明的循环双覆盖猜想更为小众，但仍是一项实质性贡献。有人质疑这是否会让初级研究人员过时，而另一些人则认为 LLM 更适合处理像 abc 猜想那样难以理解的证明。

**标签**: `#AI`, `#mathematics`, `#convex optimization`, `#machine learning`, `#research`

---

<a id="item-2"></a>
## [LG 显示器通过 Windows Update 静默安装未经同意的软件](https://videocardz.com/newz/lg-monitors-silently-install-software-through-windows-update-without-user-consent) ⭐️ 8.0/10

LG 显示器利用 Windows Update，在通过 HDMI 连接时静默安装未经用户同意的未经验证软件，并赋予其完全系统访问权限。 该软件随系统启动运行、拥有网络访问权限，且无需用户任何操作即可安装，构成重大安全与隐私风险，可能影响数百万用户。 只要通过 HDMI 连接 LG 显示器（即使是之前已连接过的旧显示器），安装就会立即触发。该软件未经过沙盒隔离，拥有完全系统访问权限。

hackernews · baranul · 7月18日 10:21 · [社区讨论](https://news.ycombinator.com/item?id=48956688)

**背景**: Windows Update 本用于推送硬件厂商的驱动和软件更新，但该功能被滥用以在用户不知情的情况下安装可能不需要的软件，引发对微软审核流程的担忧。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.fingerlakes1.com/2026/07/18/lg-monitor-software-now-installs-through-windows-update-and-many-users-did-not-expect-it/">LG Monitor Software Now Installs Through Windows Update and ...</a></li>

</ul>
</details>

**社区讨论**: 社区对此强烈批评，用户称该软件为“恶意软件”，并对 LG 表示失望。有用户提供了通过组策略或设备安装设置阻止自动下载制造商应用的解决方法。

**标签**: `#security`, `#Windows`, `#privacy`, `#hardware`, `#LG`

---

<a id="item-3"></a>
## [Anthropic 将 Claude Fable 5 永久纳入 Max 和 Team Premium 套餐](https://simonwillison.net/2026/Jul/18/claude-make-fable-5-permanent/#atom-everything) ⭐️ 8.0/10

Anthropic 宣布，自 2026 年 7 月 20 日起，Claude Fable 5 将永久纳入 Max 和 Team Premium 订阅套餐，使用额度为上限的 50%。这推翻了此前将该模型从订阅中移除、仅通过 API 提供的计划。 此举是受到 OpenAI 的 GPT-5.6 Sol 和 Moonshot AI 的 Kimi 3 的竞争压力推动，这些模型曾威胁到 Anthropic 订阅套餐的吸引力。将 Fable 5 保留在高级套餐中有助于留住订阅用户并保持市场竞争力。 Pro 和 Team Standard 用户将继续通过使用额度访问 Fable 5，并获得一次性 100 美元额度。但每月 20 美元套餐的用户仍无法使用 Fable 5；Max 套餐价格为每月 100 美元和 200 美元。

rss · Simon Willison · 7月18日 06:00

**背景**: Claude Fable 5 是 Anthropic 的 Mythos 级模型，专为自主知识工作和编程设计。最初因计算能力问题计划从订阅中移除，但来自 GPT-5.6 Sol（在编程基准测试中以更低成本超越 Fable 5）以及开源模型 Kimi 3 的竞争压力迫使公司改变了决定。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Claude_Fable_5">Claude Fable 5</a></li>
<li><a href="https://www.anthropic.com/news/claude-fable-5-mythos-5">Claude Fable 5 and Claude Mythos 5 \ Anthropic</a></li>
<li><a href="https://openai-dotcom-git-main-openai.vercel.app/index/gpt-5-6/">GPT - 5 . 6 : Frontier intelligence that scales with your ambition | OpenAI</a></li>

</ul>
</details>

**标签**: `#Anthropic`, `#Claude`, `#AI models`, `#subscription plans`, `#competition`

---

<a id="item-4"></a>
## [涉嫌 AI 垃圾作品赢得 DeepMind Kaggle 2.5 万美元大奖](https://www.reddit.com/r/MachineLearning/comments/1uzyf66/did_blatant_ai_slop_just_win_a_25k_usd_deepmind/) ⭐️ 8.0/10

Reddit 上的一篇帖子声称，在 DeepMind 赞助的 Kaggle 竞赛“衡量通向 AGI 的进展——认知能力”中，一个设计拙劣、毫无意义的提交作品赢得了 2.5 万美元的大奖。 这引发了对高知名度 AI 竞赛评审过程诚信度以及用于衡量 AGI 进展的基准测试质量控制的严重担忧。 该帖子提供了详细证据，包括对论文、方法论、代码和数据的审查，声称获奖作品是一堆“凭感觉拼凑的意大利面条”，忽略了提交格式要求。

reddit · r/MachineLearning · /u/TheWerkmeister · 7月18日 15:10

**背景**: Kaggle 竞赛是机器学习竞赛，参与者提交模型解决特定问题，通常设有现金奖励。DeepMind 竞赛要求参与者设计基于认知科学的新型 AI 基准测试，以衡量通向 AGI 的进展。评审过程通常包括同行评审和组织者评估。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://blog.google/innovation-and-ai/models-and-research/google-deepmind/measuring-agi-cognitive-framework/">Measuring progress toward AGI: A cognitive framework</a></li>
<li><a href="https://medium.com/global-maksimum-data-information-technologies/kaggle-handbook-fundamentals-to-survive-a-kaggle-shake-up-3dec0c085bc8">Kaggle Handbook: Fundamentals to Survive a Kaggle ... | Medium</a></li>

</ul>
</details>

**社区讨论**: Reddit 社区高度关注，许多人对评审过程表示愤怒和怀疑。一些评论者为主办方辩护，认为此类竞赛中主观性不可避免，而另一些人则呼吁提高透明度和加强审查。

**标签**: `#AI ethics`, `#Kaggle`, `#research integrity`, `#benchmarking`, `#DeepMind`

---

<a id="item-5"></a>
## [GPT-2 词元嵌入空间的交互式地图](https://www.reddit.com/r/MachineLearning/comments/1v09muj/interactive_map_of_gpt2s_token_embedding_space/) ⭐️ 8.0/10

一位 Reddit 用户制作了 GPT-2-small 的 32,070 个字母词元嵌入的交互式 t-SNE 地图，边表示最小生成树以展示最近邻关系。用户可以点击任意词元探索其邻居，并搜索特定词元。 该可视化将抽象的嵌入概念变得具体可探索，帮助研究人员和爱好者理解 GPT-2 学到的语义关系。它提供了一种直观的方式，无需运行前向传播即可检查模型如何对相似词元进行分组。 该地图在嵌入表的压缩表示上使用 t-SNE，并通过该空间中的最小生成树计算边。它支持移动设备，可进行双指缩放、点击导航和搜索框查询。

reddit · r/MachineLearning · /u/Limp-Contest-7309 · 7月18日 22:42

**背景**: 词元嵌入是语言模型（如 GPT-2）学习到的词元稠密向量表示。t-SNE 是一种降维技术，可将高维数据投影到二维或三维空间进行可视化。最小生成树以最小总边权连接所有点，揭示最直接的关系。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding">t -distributed stochastic neighbor embedding - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Minimum_spanning_tree">Minimum spanning tree</a></li>
<li><a href="https://analyticalnikita.substack.com/p/how-llms-embeds-input-tokens">How LLMs Embeds Input Tokens ? - by Nikita Prasad</a></li>

</ul>
</details>

**社区讨论**: 社区称赞该工具的清晰度和交互性，一些用户建议添加更多词元或将其整合到教育资源中。少数人讨论了选择 t-SNE 而非 UMAP 的原因，以及使用压缩表示的影响。

**标签**: `#GPT-2`, `#token embeddings`, `#visualization`, `#t-SNE`, `#NLP`

---

<a id="item-6"></a>
### *（简报）* [Fable 5 与 GPT-5.6 Sol 在 NP 难问题上的对决：/goal 指令有效吗？](https://charlesazam.com/blog/fable-5-gpt-5-6-sol-goal/) ⭐️ 7.0/10

一篇博客文章将 Anthropic 的 Claude Fable 5 与 OpenAI 的 GPT-5.6 Sol 在 NP 难问题上进行了比较，测试 /goal 指令是否能提升性能。评估显示 /goal 对两个模型都有帮助，但 GPT-5.6 Sol 整体表现优于 Fable 5。 这项比较为两个领先 AI 模型在挑战性问题上的编码和推理能力提供了实用见解。研究结果有助于开发者为复杂任务选择合适的模型和提示策略。 所使用的 NP 难问题很可能是一个组合优化任务。/goal 指令是一种提示技术，指示模型在多次交互中保持特定目标，从而提升专注度和一致性。

---

<a id="item-7"></a>
### *（简报）* [GPT-2 Small 嵌入几何：'Trump'的离散与连续近邻对比](https://www.reddit.com/r/MachineLearning/comments/1v07xai/gpt2_smalls_embedding_geometry_around_trump/) ⭐️ 7.0/10

一项可视化研究比较了 GPT-2 Small 静态嵌入表中'Trump'令牌的离散化与连续最近邻，发现离散化产生通用政治术语，而连续嵌入则捕获更具体的关系，如家庭成员和对手。 这项分析揭示了嵌入离散化如何影响语义分组，对于理解大型语言模型中静态嵌入的可解释性和特性至关重要。 该可视化使用 t-SNE 投影了 32,070 个字母令牌，并比较了两种表示下的最近邻：离散化（阈值化坐标）和连续（原始坐标）。不涉及提示或文本生成，结果直接来自 GPT-2 Small 学习到的令牌嵌入。

---

<a id="item-8"></a>
### *（简报）* [单细胞 RNA 测序分析的 25 种深度学习方法综述](https://www.reddit.com/r/MachineLearning/comments/1v06nc1/deep_learning_tackles_singlecell_analysis_a/) ⭐️ 7.0/10

一篇综述论文将用于单细胞 RNA 测序分析的 25 种深度学习方法分为 6 个子类别，并用详细表格总结了每种方法的目的、架构、指标和创新点。 该综述为 scRNA-seq 分析中的深度学习方法提供了结构化概述，帮助研究人员快速识别适用于聚类、插补和轨迹推断等任务的方法，从而加速计算生物学研究。 这些方法被分为表示学习、聚类、插补、基因调控网络推断等类别。每种方法都根据准确性、可扩展性和鲁棒性等指标进行评估，并突出了其具体创新点。

---

