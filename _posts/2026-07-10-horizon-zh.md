---
layout: default
title: "Horizon Daily: 2026-07-10 (ZH)"
date: 2026-07-10
lang: zh
period: daily
period_id: 2026-07-10
---

> 从 20 条内容中筛选出 10 条重要资讯。

其中 **5 条 8 分以上**展开详细简报，其余 5 条仅列于索引。

---

1. [OpenAI 发布 GPT-5.6，在 ARC-AGI-3 上达到 SOTA](#item-1) ⭐️ 10.0/10
2. [欧盟议会通过聊天控制 1.0，允许大规模扫描私密消息](#item-2) ⭐️ 9.0/10
3. [用 Rust 重写的 Postgres 通过全部回归测试](#item-3) ⭐️ 8.0/10
4. [美军后勤体系面临下一场大战崩溃风险](#item-4) ⭐️ 8.0/10
5. [Meta 推出付费智能体 AI 模型 Muse Spark 1.1](#item-5) ⭐️ 8.0/10
6. [在 32GB 内存笔记本上运行 GLM 5.2：Colibrì项目](#item-6) ⭐️ 7.0/10
7. [腾讯 Hy3：小模型大能力，OpenRouter 上免费使用](#item-7) ⭐️ 7.0/10
8. [2026 年底不增加闰秒，UTC 偏移量保持不变](#item-8) ⭐️ 7.0/10
9. [内部服务 TLS 证书的正确配置指南](#item-9) ⭐️ 7.0/10
10. [IMGNet：通过符号模式匹配进行人脸验证](#item-10) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [OpenAI 发布 GPT-5.6，在 ARC-AGI-3 上达到 SOTA](https://openai.com/index/gpt-5-6/) ⭐️ 10.0/10

OpenAI 发布了其最新旗舰模型 GPT-5.6，提供 Luna、Terra 和 Sol 三种规格。其中 Sol 版本在 ARC-AGI-3 基准测试中取得了 7.8% 的新 SOTA 分数，成为首个击败 ARC-AGI-3 游戏的前沿模型。 GPT-5.6 在 token 效率和成本节约方面有显著提升，Sol 版本每任务成本为 1.04 美元，而 Opus 4.8 为 1.80 美元，Fable 为 2.75 美元。Luna 版本（每任务 0.21 美元）比 GLM 5.2（0.37 美元）更便宜且智能更高，可能重塑 LLM 定价的竞争格局。 模型定价为每 100 万输入/输出 token：Luna 1/6 美元，Terra 2.50/15 美元，Sol 5/30 美元。相比之下，Claude Opus 系列为 5/25 美元，Claude Fable 5 为 10/50 美元。开发者指南强调了改进的意图理解和原始图像尺寸保留功能。

hackernews · logickkk1 · 7月9日 17:04 · [社区讨论](https://news.ycombinator.com/item?id=48849066)

**背景**: ARC-AGI-3 是一个交互式推理基准测试，旨在通过新颖、抽象的回合制环境衡量 AI 智能体的类人智能。Token 效率指的是最大化每个 token 携带的信息量，从而降低 API 成本和推理延迟。GPT-5.6 改进的 token 效率意味着它可以用更少的 token 达到相似或更好的结果。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arcprize.org/arc-agi/3">ARC-AGI-3</a></li>
<li><a href="https://arxiv.org/abs/2603.24621">[2603.24621] ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence</a></li>
<li><a href="https://redis.io/blog/llm-token-optimization-speed-up-apps/">LLM Token Optimization: Cut Costs & Latency in 2026</a></li>

</ul>
</details>

**社区讨论**: 社区评论强调了 GPT-5.6 Sol 相比 Opus 4.8 和 Fable 在 token 效率和每任务成本上的出色表现。一些用户讨论了在 GeneBench 和 LifeSciBench 比较中未包含 Fable 5 的原因，指出它因拒绝回答大多数高级生物学问题而被排除。还有关于从 Claude Code 切换到其他模型的讨论。

**标签**: `#AI`, `#LLM`, `#OpenAI`, `#benchmarks`, `#cost-efficiency`

---

<a id="item-2"></a>
## [欧盟议会通过聊天控制 1.0，允许大规模扫描私密消息](https://www.patrick-breyer.de/en/eu-parliament-greenlights-chat-control-1-0-breyer-our-children-lose-out/) ⭐️ 9.0/10

2026 年 7 月 9 日，欧洲议会通过了聊天控制 1.0 法案，允许美国科技公司在 2028 年前无需授权即可扫描私密消息。尽管该措施在 3 月份已被两次否决，但议会利用程序规则（需要绝对多数才能阻止）使其得以通过。 这项立法大幅扩大了对私人通信的大规模监控，削弱了数百万欧盟公民的加密和隐私权。它为政府强制扫描数字消息开创了先例，对数字权利和在线安全产生重大影响。 投票结果为 314 票反对、276 票赞成、17 票弃权，但否决动议需要 361 票（全体议员的绝对多数），因此未能通过。扫描适用于 Instagram、Discord、Snapchat、Skype、Xbox、Gmail 和 iCloud 等平台上的直接消息，但不包括端到端加密聊天。

hackernews · rapnie · 7月9日 11:03 · [社区讨论](https://news.ycombinator.com/item?id=48843923)

**背景**: 聊天控制是欧盟于 2022 年 5 月提出的一项法规，旨在通过要求平台扫描通信来打击在线儿童性虐待。聊天控制 1.0 是一项临时措施，允许自愿扫描；而聊天控制 2.0 将强制扫描并破坏加密。欧洲议会此前曾在 2026 年 3 月两次否决该措施。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Chat_Control">Chat Control - Wikipedia</a></li>
<li><a href="https://www.techtimes.com/articles/320010/20260709/eu-parliament-passes-chat-control-default-314-meps-couldnt-block-scanning-law.htm">EU Parliament Passes Chat Control by Default: 314 MEPs Couldn't Block ...</a></li>
<li><a href="https://fightchatcontrol.eu/chat-control-overview">Chat Control 1.0 vs 2.0 - Fight Chat Control</a></li>

</ul>
</details>

**社区讨论**: 评论者对通过程序性手段通过该法律表示愤怒，指出投票的多数议员反对该法案，但绝对多数要求阻止了否决。许多人批评欧盟的民主合法性，并警告其滑向极权主义，一些人指出成员国利用欧盟通过不得人心的法律。

**标签**: `#privacy`, `#surveillance`, `#EU legislation`, `#encryption`, `#digital rights`

---

<a id="item-3"></a>
## [用 Rust 重写的 Postgres 通过全部回归测试](https://github.com/malisper/pgrust) ⭐️ 8.0/10

一个名为 pgrust 的项目用 Rust 重写了 PostgreSQL，现已通过官方 PostgreSQL 的全部回归测试。作者使用 LLM 辅助重写，并正在探索现代数据库架构的改进。 这表明用 Rust 这类内存安全语言完全重写像 Postgres 这样成熟的数据库是可行的，有望提升安全性和性能。同时，它也展示了 LLM 在大规模代码生成和重构遗留系统中的应用。 该项目在不到一个月内借助 LLM 生成了 7101 次提交，使得传统代码审查变得困难。许可证从 PostgreSQL 许可证变更为 AGPL，引发了兼容性问题。

hackernews · SweetSoftPillow · 7月9日 06:18 · [社区讨论](https://news.ycombinator.com/item?id=48841676)

**背景**: PostgreSQL 是一个拥有 30 年历史的开源关系型数据库，以可靠性和可扩展性著称。Rust 是一种注重安全性和性能的系统编程语言，常用于重写 C/C++项目。回归测试是一套全面的测试套件，用于验证 SQL 实现及扩展功能。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.postgresql.org/docs/current/regress.html">PostgreSQL: Documentation: 18: Chapter 31. Regression Tests</a></li>

</ul>
</details>

**社区讨论**: 社区讨论非常活跃，获得了 313 个点赞和 342 条评论。主要话题包括审查 LLM 生成代码的可行性、许可证兼容性（PostgreSQL 许可证 vs AGPL）的担忧，以及通过查询镜像在生产负载下测试 Rust 版本的建议。

**标签**: `#PostgreSQL`, `#Rust`, `#LLM`, `#database`, `#rewrite`

---

<a id="item-4"></a>
## [美军后勤体系面临下一场大战崩溃风险](https://mwi.westpoint.edu/the-glass-backbone-why-the-armys-logistics-will-break-in-the-next-war/) ⭐️ 8.0/10

该分析揭示了一个关键弱点，可能削弱美军在未来战争中的效能，尤其是当中国和伊朗等对手历史上研究并利用过此类弱点时。 文章批评陆军过分关注“牙齿与尾巴”比例，优先考虑作战单位而非后勤，并指出准时制后勤虽然成本高效，但在对抗环境中缺乏韧性。

hackernews · baud147258 · 7月9日 13:24 · [社区讨论](https://news.ycombinator.com/item?id=48845442)

**背景**: 准时制后勤旨在通过按需配送来减少库存和成本，但可能因敌方攻击补给线而中断。“牙齿与尾巴”比例衡量作战部队与支援人员的比例；低比例常被视为低效，但现代战争需要强大的后勤支持。美国陆军的后勤现代化计划（LMP）旨在更新其供应链系统，但批评者认为它未能解决根本性弱点。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.dla.mil/About-DLA/News/News-Article-View/Article/4361608/just-enough-logistics-shifts-paradigm-in-military-supply-chain-readiness/">‘Just enough logistics’ shifts paradigm in military supply ...</a></li>
<li><a href="https://combataxis.com/just-in-time-logistics-in-warfare/">Enhancing Warfare Efficiency Through Just-in-Time Logistics ...</a></li>
<li><a href="https://www.dla.mil/About-DLA/News/News-Article-View/Article/4344159/the-joint-logistics-enterprises-modern-contested-logistics-truths/">The Joint Logistics Enterprise’s Modern 'Contested Logistics ...</a></li>

</ul>
</details>

**社区讨论**: 评论者普遍赞同文章观点，并引用历史案例如费边对抗汉尼拔的战略和二战生产能力进行类比。部分人讨论 SpaceX 星舰等新技术对未来后勤的影响，另一些人指出伊朗和中国等对手深知这些弱点。

**标签**: `#military`, `#logistics`, `#defense`, `#strategy`, `#supply chain`

---

<a id="item-5"></a>
## [Meta 推出付费智能体 AI 模型 Muse Spark 1.1](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/) ⭐️ 8.0/10

Meta 发布了 Muse Spark 1.1，这是一个专为智能体任务设计的多模态推理模型，现以付费 API 形式提供，定价为每百万输入 token 1.25 美元、每百万输出 token 4.5 美元。 这标志着 Meta 开始将其前沿 AI 模型商业化，以有竞争力的定价和强劲性能挑战 OpenAI 与 Anthropic，同时引发了关于基准测试有效性和公司开源策略的讨论。 Muse Spark 1.1 拥有 100 万 token 的上下文窗口，在工具使用、计算机操作、编程和多模态理解方面有显著提升。然而，社区对评估报告的分析显示，由于在 Terminal-Bench 2.1 任务中覆盖了资源限制，基准测试结果可能无效。

hackernews · ot · 7月9日 14:10 · [社区讨论](https://news.ycombinator.com/item?id=48846184)

**背景**: 智能体 AI 是指能够自主感知、推理并采取行动以实现目标的系统，不同于需要人工干预的传统模型。Meta 的 Muse Spark 系列正是为此类任务而构建，1.1 版本是原始 Muse Spark 模型的重大升级。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/">Introducing Muse Spark 1.1</a></li>
<li><a href="https://www.datacamp.com/blog/muse-spark-1-1">Muse Spark 1.1: Meta's Agentic Model and API | DataCamp</a></li>
<li><a href="https://ai.meta.com/blog/introducing-muse-spark-msl/">Introducing Muse Spark: Scaling Towards Personal Superintelligence</a></li>

</ul>
</details>

**社区讨论**: 社区评论对基准测试方法表示担忧，有用户指出覆盖 CPU 和内存限制会使 Terminal-Bench 结果无效。另一位用户分享了通过 LLM 插件进行实际集成的例子，其他人则讨论了 Meta 的定价和开源策略，部分人建议 Meta 应专注于通过开放权重将编程模型商品化。

**标签**: `#AI`, `#Meta`, `#agentic model`, `#benchmarking`, `#open source`

---

<a id="item-6"></a>
### *（简报）* [在 32GB 内存笔记本上运行 GLM 5.2：Colibrì项目](https://github.com/JustVugg/colibri) ⭐️ 7.0/10

一位开发者创建了 Colibrì，这是一个轻量级推理引擎，通过 int4 量化和按需磁盘流式传输专家权重，在 32GB 内存笔记本上运行了 744B 参数的 GLM 5.2 模型。 这表明即使是非常大的混合专家模型也可以在无 GPU 的消费级硬件上运行，使最先进的 LLM 对更广泛的用户群体可用，并支持本地私有推理。 Colibrì将密集部分（约 17B 参数）以 int4 格式常驻内存（约 9.9 GB），并按需从磁盘（约 370 GB）流式传输 21,504 个路由专家，在 12 核、25 GB 可用内存的笔记本上达到约 0.1 tok/s。

---

<a id="item-7"></a>
### *（简报）* [腾讯 Hy3：小模型大能力，OpenRouter 上免费使用](https://hy.tencent.com/research/hy3) ⭐️ 7.0/10

腾讯正式发布了 Hy3，这是一个 295B 参数的混合专家（MoE）模型，激活参数为 21B，性能可与 DeepSeek Flash V4 相媲美。在 OpenRouter 上可免费使用至 7 月 21 日。 Hy3 展示了相对较小的模型也能达到与更大旗舰模型相当的性能，可能推动先进 AI 的普及。其在 OpenRouter 上的免费层级降低了开发者和研究人员尝试最先进语言模型的门槛。 Hy3 总参数量为 295B，每个 token 激活 21B 参数，外加 3.8B 的 MTP 层，推理效率高。它略大于 DeepSeek Flash V4（总参数 284B，激活 13B），但据报道在某些基准测试上达到或超过了 V4 Pro。

---

<a id="item-8"></a>
### *（简报）* [2026 年底不增加闰秒，UTC 偏移量保持不变](https://datacenter.iers.org/data/latestVersion/bulletinC.txt) ⭐️ 7.0/10

国际地球自转与参考系统服务（IERS）宣布，2026 年 12 月底不会引入闰秒，当前 UTC-TAI 偏移量-37 秒和 UTC-GPS 偏移量-18 秒将保持不变。 这一决定为依赖可预测 UTC 偏移量的计时系统提供了稳定性，减少了闰秒插入时常伴随的软件错误和同步问题风险。 上一次闰秒添加于 2016 年 12 月 31 日，此后无需进一步调整。IERS 通常提前约六个月宣布闰秒，下一个可能的插入日期是 2027 年 6 月 30 日。

---

<a id="item-9"></a>
### *（简报）* [内部服务 TLS 证书的正确配置指南](https://tuxnet.dev/posts/tls-for-internal-services/) ⭐️ 7.0/10

一篇关于使用 ACME 和 DNS 验证为内部服务配置 TLS 证书的详细指南，并引发了社区关于最佳实践的讨论。 该指南解决了内部网络安全中的一个常见痛点，提供了减少复杂性并改进证书管理的实用建议。 文章建议使用 Let's Encrypt 的 DNS-01 验证和通配符证书，以避免证书透明度日志中的名称泄露。

---

<a id="item-10"></a>
### *（简报）* [IMGNet：通过符号模式匹配进行人脸验证](https://www.reddit.com/r/MachineLearning/comments/1urxvxh/i_built_imgnet_a_face_verification_model_that/) ⭐️ 7.0/10

一种名为 IMGNet 的新型人脸验证模型，用滑动窗口符号模式匹配替代余弦相似度，在 LFW 上达到 96.27%的准确率，模型大小仅 10.58 MB，使用 CASIA-WebFace 训练。 这项工作挑战了人脸验证中默认使用余弦相似度的做法，表明符号模式匹配可以具有竞争力且更稳定。它还表明，符号模式一致性是训练良好的人脸嵌入的一个基本属性。 该模型引入了 SW Block，一种使用素数窗口大小{3,5,7}的多尺度关系操作，以及完全基于符号模式一致性定义的 IMG Sign MSE 损失。当应用于 ArcFace 嵌入而无需重新训练时，IMG Sign Score 在 LFW 上达到 99.58%，仅比 ArcFace+Cosine 低 0.24%。

---

