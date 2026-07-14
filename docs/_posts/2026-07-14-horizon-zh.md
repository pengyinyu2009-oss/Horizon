---
layout: default
title: "Horizon Daily: 2026-07-14 (ZH)"
date: 2026-07-14
lang: zh
period: daily
period_id: 2026-07-14
---

> 从 20 条内容中筛选出 12 条重要资讯。

其中 **8 条 8 分以上**展开详细简报，其余 4 条仅列于索引。

---

1. [Telegram 的 t.me 域名被暂停，全球链接失效](#item-1) ⭐️ 8.0/10
2. [三星健康应用威胁：拒绝 AI 训练将删除用户数据](#item-2) ⭐️ 8.0/10
3. [开放数据行动恢复被政府移除的气候.gov 数据](#item-3) ⭐️ 8.0/10
4. [DOOMQL：完全由 SQLite 查询驱动的类 Doom 游戏](#item-4) ⭐️ 8.0/10
5. [思维链是规模陷阱；潜在推理兴起](#item-5) ⭐️ 8.0/10
6. [GPUHedge 将无服务器 GPU 冷启动 p95 延迟从 117 秒降至 30 秒](#item-6) ⭐️ 8.0/10
7. [开源工具利用大语言模型为研究者筛选 arXiv 论文](#item-7) ⭐️ 8.0/10
8. [Jacobian Lens 工作空间熵在 Qwen3-4B 上作为错误预测器的测试](#item-8) ⭐️ 8.0/10
9. [无需打开 Xcode 即可构建和发布 Mac 与 iOS 应用](#item-9) ⭐️ 7.0/10
10. [苹果 SpeechAnalyzer API 基准测试：速度更快但准确度略逊于 Whisper](#item-10) ⭐️ 7.0/10
11. [Sega CD 版《Silpheed》的艺术与工程](#item-11) ⭐️ 7.0/10
12. [Datasette 代码频率图展示 AI 代理影响](#item-12) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [Telegram 的 t.me 域名被暂停，全球链接失效](https://www.whois.com/whois/t.me) ⭐️ 8.0/10

Telegram 的 t.me 域名被设置为 serverHold 状态，导致所有 t.me 链接无法解析。此次暂停很可能是由法律或监管行动引发，域名注册商为 GoDaddy。 这影响了数百万依赖 t.me 链接访问用户名、频道和机器人的 Telegram 用户。域名暂停可能中断通信，并凸显依赖单一域名和注册商的风险。 域名状态显示为 serverHold，阻止 DNS 解析。.me 注册局执行了该操作，表明是注册局级别的行动。Telegram 也使用 telegram.me 作为备用域名，但目前尚不清楚该域名是否受影响。

hackernews · Tiberium · 7月13日 19:52 · [社区讨论](https://news.ycombinator.com/item?id=48897878)

**背景**: Telegram 使用 t.me 作为其用户资料、频道和机器人的官方短链接域名。.me 注册局（黑山国家域名）与 Telegram 有合作关系。serverHold 状态通常由注册局在法律纠纷、滥用调查或违反注册局政策时施加。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://domainnamewire.com/2026/07/13/telegrams-t-me-domain-suspended-leading-to-outages/">Telegram’s t.me domain suspended, leading to outages</a></li>
<li><a href="https://www.namepros.com/articles/telegrams-t-me-domain-suspended-leading-to-outages.1392680/unread">news Telegram’s t.me domain suspended, leading to outages</a></li>
<li><a href="https://greekcitytimes.com/2026/07/14/telegram-t-me-domain-serverhold-links-down/">BREAKING: Telegram’s t.me Domain Placed on ServerHold – All ...</a></li>

</ul>
</details>

**社区讨论**: 社区评论对 Telegram 使用 GoDaddy 作为注册商表示惊讶，因为 GoDaddy 以缺乏透明度著称。一些用户指出 Telegram 正面临俄罗斯、法国和印度的法律调查，其中印度是最新且财务影响最大的。其他用户强调使用重定向而非直接链接的重要性，以降低此类风险。

**标签**: `#Telegram`, `#domain suspension`, `#ICANN`, `#GoDaddy`, `#regulatory`

---

<a id="item-2"></a>
## [三星健康应用威胁：拒绝 AI 训练将删除用户数据](https://neow.in/cWsyMTV3) ⭐️ 8.0/10

三星健康应用推出新的同意政策，要求用户允许其健康数据用于 AI 训练，否则同步的健康数据将被删除。该政策涵盖睡眠、用药、医疗记录和周期追踪数据。 该政策引发严重的隐私担忧，因为它迫使用户在丢失健康数据或允许三星将敏感医疗信息用于 AI 训练之间做出选择。这为健康科技领域的数据权利树立了一个令人担忧的先例。 选择退出的用户将无法将健康数据与三星账户同步，现有数据将被删除，除非法律要求保留。该政策适用于健康记录、用药、睡眠、活动和周期追踪等数据类别。

hackernews · bundie · 7月13日 20:01 · [社区讨论](https://news.ycombinator.com/item?id=48897991)

**背景**: 三星健康是一款与 Galaxy Watch 等三星可穿戴设备配合使用的流行健康追踪应用。科技公司利用用户数据进行 AI 训练以改进服务是常见做法，但以数据删除作为惩罚的强制性同意是一种激进的策略，引发了强烈反对。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://cybernews.com/news/samsung-health-ai-training-delete-user-data/">Opt out of Samsung AI training, lose health data | Cybernews</a></li>
<li><a href="https://www.androidauthority.com/samsung-health-train-ai-data-3686684/">Samsung will kill your health data if you don't consent to AI training - Android Authority</a></li>
<li><a href="https://9to5google.com/2026/07/13/samsung-health-ai-training-data-consent/">Samsung Health will delete your data unless you hand it over for AI training</a></li>

</ul>
</details>

**社区讨论**: 社区评论表达了沮丧和怀疑。用户质疑如果拒绝则失去设备功能的公平性，有些人讽刺地指出删除数据可能是一种隐私好处。其他人将该政策与谷歌的类似做法进行比较，批评这种对用户不友好的方式。

**标签**: `#privacy`, `#Samsung`, `#AI training`, `#data rights`, `#health tech`

---

<a id="item-3"></a>
## [开放数据行动恢复被政府移除的气候.gov 数据](https://werd.io/climate-gov-was-destroyed-open-data-saved-it/) ⭐️ 8.0/10

在特朗普政府移除 climate.gov 后，一个非营利组织利用存档的开放数据重新上线了该网站，保留了 15 年的气候新闻、报告和数据集。 这一事件凸显了政府托管公共数据在政治变动面前的脆弱性，并强调了开放数据和社区存档在确保纳税人资助信息长期可获取方面的关键作用。 恢复后的网站包含 climate.gov 的全部新闻、专家博客、气候指标和数据路径，但其可持续性依赖捐赠而非税收。

hackernews · benwerd · 7月13日 19:57 · [社区讨论](https://news.ycombinator.com/item?id=48897945)

**背景**: Climate.gov 是美国政府提供权威气候数据和资源的网站。2025 年，特朗普政府从多个联邦网站移除气候信息，促使存档者和非营利组织下载并保存数据。开放数据倡议主张政府产生的数据应免费向公众开放。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arstechnica.com/science/2026/06/uss-climate-gov-site-taken-down-by-trump-relaunched-by-nonprofit/">US’s climate.gov site, taken down by Trump, relaunched by ...</a></li>
<li><a href="https://nsarchive.gwu.edu/briefing-book/climate-change-transparency-project-foia/2025-02-06/disappearing-data-trump">Disappearing Data: Trump Administration Removing Climate ...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Open_data">Open data - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 评论者担忧依赖捐赠的存档的长期可持续性，主张政府数据默认应为公共领域，并建议使用 IPFS 等去中心化系统发布政府出版物以防止未来被移除。

**标签**: `#open data`, `#government transparency`, `#data preservation`, `#climate`, `#archiving`

---

<a id="item-4"></a>
## [DOOMQL：完全由 SQLite 查询驱动的类 Doom 游戏](https://simonwillison.net/2026/Jul/13/doomql/#atom-everything) ⭐️ 8.0/10

Peter Gostev 创建了 DOOMQL，这是一个可玩的终端第一人称射击游戏，其中 SQLite 处理所有游戏逻辑——移动、碰撞、敌人、战斗和渲染——全部通过 SQL 查询实现，包括使用递归 CTE 实现的射线追踪器。该游戏作为 Python 终端脚本运行，并在 GPT-5.6 Sol 的辅助下构建。 DOOMQL 展示了 SQLite 的非传统创造性用途，突破了数据库引擎在数据存储之外的能力边界。它展示了 SQL 在复杂计算和渲染方面的强大能力，为游戏开发和创意编程提供了新的思路。 该游戏包含一个使用递归 CTE 在 SQL 中实现的完整射线追踪器，游戏状态存储在 SQLite 数据库中，可通过 Datasette 进行探索。Simon Willison 创建了一个 Datasette 应用，每秒刷新一次，显示游戏视图和战术小地图。

rss · Simon Willison · 7月13日 22:34

**背景**: SQLite 是一个自包含、无服务器的 SQL 数据库引擎，广泛应用于各类应用中。DOOMQL 的灵感来源于使用 SQL 处理游戏逻辑的概念，类似于早期的 DuckDB DOOM 等项目，但它更进一步，让 SQLite 成为所有游戏系统的唯一引擎。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/petergpt/doomql/tree/main/">GitHub - petergpt/doomql: A playable terminal FPS whose ...</a></li>
<li><a href="https://simonwillison.net/2026/Jul/13/doomql/">DOOMQL - simonwillison.net</a></li>
<li><a href="https://www.sqlite.org/">SQLite Home Page</a></li>

</ul>
</details>

**标签**: `#SQLite`, `#game development`, `#creative coding`, `#AI-assisted development`

---

<a id="item-5"></a>
## [思维链是规模陷阱；潜在推理兴起](https://www.reddit.com/r/MachineLearning/comments/1uviru5/chain_of_thought_is_a_scaling_trap_the_next_wave/) ⭐️ 8.0/10

一篇 Reddit 帖子认为，思维链（CoT）推理由于忠实性和成本问题是一个规模陷阱，而像 Coconut、HRM 和 RecursiveMAS 这样的潜在推理方法代表了下一波浪潮。该帖子还讨论了黑箱可解释性墙，并提出了用于验证的外循环治理层。 这一分析挑战了 LLM 推理中占主导地位的 CoT 范式，指出了在忠实性和成本方面的根本限制，这些限制可能阻碍规模化。向潜在推理的转变可能提高效率，但为高风险应用带来了关键的可解释性问题。 该帖子指出了 CoT 的两个实际问题：忠实性（痕迹可能与实际计算脱钩）和系统成本（更长的痕迹增加延迟和成本）。像 Coconut、HRM 和 RecursiveMAS 这样的潜在推理方法将内循环转移到潜在空间，但失去了 CoT 的可解释性窗口。

reddit · r/MachineLearning · /u/meowsterpieces · 7月13日 17:50

**背景**: 思维链（CoT）是一种提示 LLM 以自然语言输出中间推理步骤的技术，能提升复杂任务的表现。但它将推理序列化为 token，增加了成本和延迟。像 Coconut 这样的潜在推理方法允许模型在连续隐藏状态中推理而不生成文本，而 HRM 将慢规划与快执行分离。RecursiveMAS 使用潜在空间递归进行多智能体协作。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/html/2412.06769v1?trk=article-ssr-frontend-pulse_little-text-block">Training Large Language Models to Reason in a Continuous Latent ...</a></li>
<li><a href="https://arxiv.org/abs/2506.21734">[2506.21734] Hierarchical Reasoning Model</a></li>
<li><a href="https://recursivemas.github.io/">Recursive Multi-Agent Systems</a></li>

</ul>
</details>

**社区讨论**: Reddit 上的讨论内容充实，评论者就 CoT 的忠实性和成本以及潜在推理的权衡进行了辩论。一些人同意 CoT 是一种权宜之计，而另一些人则警告潜在方法牺牲了可解释性。帖子作者与评论者互动，澄清了 BDH（Dragon Hatchling）作为结合潜在计算与可解释性钩子的模型的作用。

**标签**: `#LLM reasoning`, `#chain-of-thought`, `#latent reasoning`, `#interpretability`, `#scaling`

---

<a id="item-6"></a>
## [GPUHedge 将无服务器 GPU 冷启动 p95 延迟从 117 秒降至 30 秒](https://www.reddit.com/r/MachineLearning/comments/1uvlb6h/gpuhedge_hedging_serverless_gpu_providers/) ⭐️ 8.0/10

GPUHedge 是一个开源对冲库，通过跨多个提供商投机性地分发请求，将无服务器 GPU 推理的 p95 冷启动延迟从 116.6 秒降低到 29.4 秒。 冷启动延迟是无服务器 GPU 推理的主要痛点，大型模型通常会增加 40-90 秒。GPUHedge 的对冲方法提供了一种实用的、与提供商无关的解决方案，可以显著改善用户体验并降低成本。 该库采用投机执行策略：在主提供商上启动请求，监控作业生命周期，并在可配置的超时（例如 10 秒）后有条件地在第二个提供商上启动备份请求。第一个通过验证器的结果获胜，失败的作业通过提供商的 API 取消。在基准测试中，RunPod → Cerebrium 对冲将超过 60 秒的请求从 11/36 减少到 0/36，并将建模的活动计算成本从每个请求 0.0114 美元降低到 0.0083 美元。

reddit · r/MachineLearning · /u/Putrid_Construction3 · 7月13日 19:20

**背景**: 无服务器 GPU 提供商在空闲时缩放到零，导致新请求到达时出现冷启动。这涉及将模型加载到 GPU 内存，可能需要几十秒。对冲是一种分布式系统技术，通过发送多个冗余请求来缓解尾部延迟；使用第一个成功的响应，并取消其他请求。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://tianpan.co/blog/2026-04-10-ai-agents-serverless-cold-start-latency">The Cold Start Tax on Serverless AI Agents</a></li>
<li><a href="https://www.spheron.network/blog/gpu-cold-start-llm-inference-2026/">GPU Cold Start on Serverless LLM Inference: 4 Fixes... | Spheron Blog</a></li>
<li><a href="https://en.wikipedia.org/wiki/Speculative_execution">Speculative execution - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: Reddit 上的讨论内容丰富，用户询问成本影响和提供商支持。作者回应了关于取消保证和验证器设计的技术问题。总体情绪积极，用户对添加更多提供商和集成到现有工作流感兴趣。

**标签**: `#serverless GPU`, `#cold start`, `#hedging`, `#latency optimization`, `#open source`

---

<a id="item-7"></a>
## [开源工具利用大语言模型为研究者筛选 arXiv 论文](https://www.reddit.com/r/MachineLearning/comments/1uvcdf7/hundreds_of_papers_hit_arxiv_every_day_and_maybe/) ⭐️ 8.0/10

一位开发者发布了 Research Radar，这是一个开源工具，利用大语言模型每天根据用户的研究兴趣获取、评分并总结 arXiv 论文，提供个性化摘要。 该工具解决了研究人员每天花费大量时间浏览无关论文的痛点，每天可节省 30-60 分钟，并确保他们不会错过自己领域的重要工作。 该工具采用两轮评分系统：先用轻量模型进行初步筛选，再用强模型对高分论文进行深度阅读。它支持多种后端，包括 Claude Code、兼容 OpenAI 的端点以及通过 Ollama/vLLM 运行的本地模型。

reddit · r/MachineLearning · /u/usedtobreath · 7月13日 13:59

**背景**: arXiv 是一个预印本仓库，拥有超过 200 万篇论文，涵盖多个科学领域，每月新增约 24,000 篇。研究人员常常难以从海量论文中筛选出相关文献。大语言模型越来越多地被用作文本评估的自动裁判，但校准问题仍然具有挑战性。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/ArXiv_(identifier)">ArXiv (identifier)</a></li>
<li><a href="https://info.arxiv.org/help/api/index.html">arXiv API Access - arXiv info</a></li>
<li><a href="https://arxiv.org/abs/2601.03444">[2601.03444] Grading Scale Impact on LLM-as-a-Judge: Human ...</a></li>

</ul>
</details>

**社区讨论**: Reddit 社区反应积极，评论称赞该工具的实用性和开源特性。用户要求增加与其他平台的集成功能，并讨论了如何校准大语言模型裁判的相关性评分。

**标签**: `#arXiv`, `#research tools`, `#LLM`, `#paper filtering`, `#open-source`

---

<a id="item-8"></a>
## [Jacobian Lens 工作空间熵在 Qwen3-4B 上作为错误预测器的测试](https://www.reddit.com/r/MachineLearning/comments/1uv5l75/evaluating_jspace_entropy_as_an_error_predictor/) ⭐️ 8.0/10

一项研究在 Qwen3-4B 上使用约 11,400 个样本，跨越 7 个数据集评估了 Jacobian Lens 工作空间熵作为错误预测器的效果，发现它能在事实检索中补充输出置信度，但无法可靠检测内部化误解，且校准高度依赖任务。 这项工作对一种有前景的可解释性方法进行了细致的实证评估，表明内部熵并非通用的幻觉检测器，但可能作为自信错误事实答案的补充信号，对 AI 安全和模型可靠性具有重要意义。 该研究使用了 Qwen3-4B 和包括 TriviaQA、PopQA、NQ-Open、TruthfulQA、HotpotQA、GSM8K 和 CommonSenseQA 在内的数据集。主要发现：在 PopQA 上，工作空间熵提高了高置信度答案的错误路由精度，但在 TruthfulQA 上弱于输出置信度；在 TriviaQA 上校准的阈值在 GSM8K 上失效，因为数学推理的基线熵更高。

reddit · r/MachineLearning · /u/dasjomsyeet · 7月13日 08:27

**背景**: Jacobian Lens 是 Anthropic 开发的一种可解释性技术，通过计算 logits 相对于激活的 Jacobian 来检查语言模型内部的可言语化表示。工作空间熵指的是这些内部表示的熵，被假设为指示不确定性。本研究在特定模型和多个数据集上检验了这一假设。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.lesswrong.com/posts/T3u6Hctes6vkawsib/reading-into-vlm-hallucinations-using-the-jacobian-lens">Reading into VLM hallucinations using the Jacobian lens — LessWrong</a></li>
<li><a href="https://explainx.ai/blog/what-is-j-lens-jacobian-lens-claude-interpretability-2026">What Is the J- Lens ? Anthropic Jacobian Lens Guide | explainx.ai</a></li>

</ul>
</details>

**社区讨论**: Reddit 帖子目前没有评论，但作者邀请对实验设计提供反馈。社区可能会讨论单模型研究的局限性以及该方法的任务依赖性。

**标签**: `#interpretability`, `#LLM`, `#error detection`, `#Jacobian Lens`, `#AI safety`

---

<a id="item-9"></a>
### *（简报）* [无需打开 Xcode 即可构建和发布 Mac 与 iOS 应用](https://scottwillsey.com/building-and-shipping-mac-and-ios-apps-without-ever-opening-xcode/) ⭐️ 7.0/10

一位开发者展示了如何完全通过命令行和 CI/CD 流水线构建、签名、公证并发布 Mac 与 iOS 应用，彻底绕过 Xcode 的图形界面。该方法利用 Xcode 内置的命令行工具、XcodeGen 生成项目文件以及自动化脚本。 这一工作流使开发者能够将 Apple 应用构建集成到自动化 CI/CD 系统中，减少对臃肿 IDE 的依赖，并支持 AI 辅助编码代理在无需人工干预的情况下构建和发布应用。它挑战了“Xcode 是 Apple 平台开发必备工具”的传统观念。 该流程要求安装 Xcode（以使用其工具链），但无需打开它。关键步骤包括在终端中使用 `xcodebuild`、用 `xcrun` 进行签名和公证，以及通过 XcodeGen 从 YAML 规范生成 `.xcodeproj` 文件。作者还展示了如何用脚本自动化整个链路，并在出错时大声报错。

---

<a id="item-10"></a>
### *（简报）* [苹果 SpeechAnalyzer API 基准测试：速度更快但准确度略逊于 Whisper](https://get-inscribe.com/blog/apple-speech-api-benchmark.html) ⭐️ 7.0/10

一项新的基准测试将苹果在 iOS 26 中引入的 SpeechAnalyzer API 与 OpenAI 的 Whisper 及旧版 SFSpeechRecognizer 进行了对比，结果显示 SpeechAnalyzer 速度更快，但准确度略低于 Whisper。 这项基准测试首次独立评估了苹果新的语音转文本能力，可能影响依赖转录服务的开发者和用户。社区讨论凸显了对第三方 Whisper 封装应用未来的担忧。 该基准测试在数学讲座上进行，SpeechAnalyzer 的速度远快于 Whisper-Large-V2，但准确度仅略逊一筹。苹果的新 API 取代了 SFSpeechRecognizer，且缺少可提高关键词准确度的自定义词汇功能。

---

<a id="item-11"></a>
### *（简报）* [Sega CD 版《Silpheed》的艺术与工程](https://fabiensanglard.net/silpheed/index.html) ⭐️ 7.0/10

Fabien Sanglard 发表了一篇详细的技术分析，揭示了 Sega CD 版《Silpheed》如何利用预渲染的全动态视频（FMV）和巧妙的编程，在没有 3D 能力的硬件上模拟出 3D 图形效果。 这篇深度分析展示了复古游戏开发者克服硬件限制的创造力，为现代系统编程和游戏开发爱好者提供了宝贵的经验。 Sega CD 没有帧缓冲，因此渲染需要将 768 个 8x8 像素的图块绘制到图块映射中，形成 256x224 的图像。游戏使用 FMV 背景配合精灵叠加来营造 3D 错觉。

---

<a id="item-12"></a>
### *（简报）* [Datasette 代码频率图展示 AI 代理影响](https://simonwillison.net/2026/Jul/13/datasette-code-frequency/#atom-everything) ⭐️ 7.0/10

Simon Willison 分享了他的 Datasette 项目的 GitHub 代码频率图，显示 2026 年代码增删量出现巨大峰值，他将其归因于使用编码代理和 Opus 4.5 等模型。 这提供了一个数据驱动的可视化例证，展示了 AI 辅助开发工具如何显著提升个人开发者生产力，为 AI 增强编码的趋势提供了具体案例。 图表显示 2026 年单周新增代码达 37,022 行，删除 9,528 行，远超此前活动水平。Willison 还提到 Opus 4.8、GPT-5.5、Fable 5 和 GPT-5.6 Sol 等模型也做出了贡献。

---

