---
layout: default
title: "Horizon Daily: 2026-10-17 (ZH)"
date: 2026-10-17
lang: zh
period: daily
period_id: 2026-10-17
---

> 从 19 条内容中筛选出 12 条重要资讯。

其中 **3 条 8 分以上**展开详细简报，其余 7 条仅列于索引。另有 **2 条🎯猜你感兴趣**（按画像主观分入选）。

---

1. [Claude 破解 NIST 椭圆曲线种子来源：源自 lrand48 时间戳](#item-1) ⭐️ 8.0/10 · 相关 4/10
2. [越狱 PS5 原生运行 llama.cpp，可加载任意 GGUF 模型](#item-2) ⭐️ 8.0/10 · 相关 8/10
3. [ORL 让扩散语言模型在单张 RTX 5090 上达到 2788 tokens/s](#item-3) ⭐️ 8.0/10 · 相关 7/10
4. [特斯拉发布搭载冷气推进器与火箭选装的新款 Roadster 演示](#item-4) ⭐️ 7.0/10 · 相关 3/10
5. [博客从联想记忆推导 Transformer 原理，引发 HN 热议](#item-5) ⭐️ 7.0/10 · 相关 6/10
6. [苹果 MLX 新增分布式推理，可在 Mac Studio 集群上运行近万亿参数模型](#item-6) ⭐️ 7.0/10 · 相关 8/10
7. [Jake Archibald 深度对比 JPEG XL 与 AVIF，引发社区热议](#item-7) ⭐️ 7.0/10 · 相关 4/10
8. [Anthropic 的 Claude Code 团队公开其 AI 驱动的代码审查流程](#item-8) ⭐️ 7.0/10 · 相关 6/10
9. [Mercor 研究：美国 90%的工作时间缺乏 AI 基准覆盖](#item-9) ⭐️ 7.0/10 · 相关 3/10
10. [Home Assistant 默认进行 Pwned 密码检查引发隐私争议](#item-10) ⭐️ 7.0/10 · 相关 6/10
11. 🎯 [CS 学生的 Rust 框架 DenseCore 在 nanoGPT 上逐位复现 PyTorch](#item-11) ⭐️ 7.0/10 · 相关 6/10
12. 🎯 [研究者利用 OpenBSD 内核中潜伏 37 年的漏洞](#item-12) ⭐️ 7.0/10 · 相关 5/10

---

<a id="item-1"></a>
## [Claude 破解 NIST 椭圆曲线种子来源：源自 lrand48 时间戳](https://www.anthropic.com/research/ecdsa-curve-origins) ⭐️ 8.0/10 · 相关 4/10

Anthropic 发布研究称，Claude 在不到半小时内就找出了 NIST P-192、P-224、P-256、P-384 和 P-521 椭圆曲线种子的来源：它们并非由任何哈希算法生成，而是 C 标准库中 lrand48 随机数生成器以 Unix 时间戳作为种子产生的输出。 这一发现终结了长达十余年的猜测——即美国国家安全局（NSA）可能故意挑选这些曲线以植入后门；同时它也表明，AI 模型如今已能对长期悬而未决的开放问题开展有价值的密码学侦查工作。 按照 ANSI X9.62 规范，这些种子本应通过 SHA-1 对任意种子做哈希来“可验证地随机”生成，但 Claude 发现实际输入来自以 Unix 时间戳播种的 lrand48；第五个二进制种子 B-163 仍无法用任何尝试解释，至今成谜。

hackernews · ahlCVA · 10月16日 18:55 · [社区讨论](https://news.ycombinator.com/item?id=50122800)

**背景**: ECDSA 是应用最广泛的椭圆曲线密码标准，其 NIST 曲线于 2000 年在 FIPS 186-2 中发布。由于原始种子值从未公开，包括 Neal Koblitz 和 Alfred Menezes 在内的密码学家长期争论这些曲线是否暗藏人为弱点，而 Dual_EC_DRBG 事件更放大了这种担忧。

**对中国影响**: 在 TLS、安全芯片以及国产密码方案中使用 NIST P-256 等曲线的中国开发者和安全研究者，如今可以引用这一确切的来源结论；此事也凸显了用 AI 辅助分析来审计国外密码标准的价值。

**对我有什么用**: 对电子工程师或硬件开发者而言，这更像是一则密码学与 AI 工具链的新闻，而非可直接动手复刻的硬件项目；但它展示了如何借助 AI 助手逆向分析固件、安全启动链或嵌入式加密库中不透明的参数。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.anthropic.com/research/ecdsa-curve-origins">Claude reveals ECDSA curve origins \ Anthropic</a></li>
<li><a href="https://modernorange.io/item/37784499">NIST Elliptic Curves Seeds Bounty | Modern Orange</a></li>
<li><a href="https://www.cs.ait.ac.th/~on/O/oreilly/tcpip/puis/ch23_07.htm">[Chapter 23] 23.7 UNIX Pseudo- Random Functions</a></li>

</ul>
</details>

**社区讨论**: Hacker News 上的评论者把这一结果称为“13 年阴谋论的终结”，但也有人指出它只证实了生成方法，并不能证明曲线未被刻意挑选，因为被丢弃的候选值无法被观察到。还有人推测，无法解释的 B-163 种子可能只是公布数值时打错了一位数字。

**标签**: `#cryptography`, `#ECDSA`, `#AI-assisted-research`, `#NIST`, `#random-number-generator`

---

<a id="item-2"></a>
## [越狱 PS5 原生运行 llama.cpp，可加载任意 GGUF 模型](https://github.com/cobanov/PS5LM) ⭐️ 8.0/10 · 相关 8/10

开发者发布了 PS5LM 项目，让 llama.cpp 能在越狱后的 PlayStation 5 上原生运行，从而加载任意 GGUF 格式的量化模型进行本地推理。该项目托管在 GitHub 上，并在 Hacker News 上引发热议（163 分、44 条评论）。 这表明搭载强大定制芯片的封闭消费级硬件可以被改造成通用的边缘 AI 计算机，挑战了“本地大模型推理必须依赖专用 PC 或服务器”的固有认知。它还可能激励在其他游戏主机和精简版 APU 板卡上开展类似的破解与自制软件项目。 据称演示中运行的是 2 bit 量化的 Qwen 3.8 27B 模型，质量虽一般，但足以胜任长时间、低复杂度的任务，例如监控服务器错误率或审查安防录像。主机持续运行的电力成本约为每天 70 美分，每天可产出约 200 万个输出 token。

hackernews · Anon84 · 10月16日 18:32 · [社区讨论](https://news.ycombinator.com/item?id=50122431)

**背景**: llama.cpp 是一个独立的 C++ 运行时，无需 Python 依赖即可执行 GGUF 格式的量化模型，而 GGUF 已成为分发本地大模型的事实标准。PS5 采用 AMD 定制芯片，近期的“Relapse”等越狱漏洞几乎适用于所有固件版本，可解锁自制软件甚至 PS2 模拟。边缘 AI 指的是将 AI 模型直接部署在游戏主机、物联网传感器、嵌入式系统等设备上，而非云端。

**对中国影响**: 中国拥有庞大的 llama.cpp 与 GGUF 用户群体以及活跃的二手硬件市场，这类低成本边缘推理方案对希望搭建廉价本地大模型设备的国内开发者颇具吸引力。它也可能为基于再利用芯片或国产 APU 的国内边缘 AI 探索增添动力，不过越狱本身的法律灰色地带限制了其商业化应用。

**对我有什么用**: 对电子工程师/硬件开发者而言，这是一个很有吸引力的可复刻项目：它展示了如何把高性能定制 APU 改用于本地大模型推理，同样的技术思路也可迁移到更便宜的 BC250 板卡或其他嵌入式平台。它还是研究如何把 llama.cpp 移植到非标准硬件、以及低比特量化在常驻边缘任务中取舍的实用案例。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GGUF">GGUF - Wikipedia</a></li>
<li><a href="https://www.techspot.com/news/114037-new-ps5-jailbreak-works-almost-every-firmware-version.html">A new PS5 jailbreak works on almost every firmware version ...</a></li>

</ul>
</details>

**社区讨论**: 评论者总体热情高涨：有人表示，看到黑客把封闭设备变成通用计算机后，自己都开始考虑买一台 PS5；还有人认为同样的思路可以用于基于 AMD 精简版“Cyan Skillfish” APU 的廉价二手矿板 BC250。法律风险是被反复提及的担忧，有评论者认为项目不该托管在 GitHub 上，因为索尼随时可能让页面下架。其他人则看好游戏中的 LLM 驱动 NPC 以及常驻监控等实际用途。

**标签**: `#llama.cpp`, `#PS5`, `#边缘AI`, `#开源硬件`, `#GGUF`

---

<a id="item-3"></a>
## [ORL 让扩散语言模型在单张 RTX 5090 上达到 2788 tokens/s](https://www.reddit.com/r/MachineLearning/comments/1x7qgr0/research_2788_tokenss_on_a_single_rtx_5090_with_a/) ⭐️ 8.0/10 · 相关 7/10

研究者提出面向扩散语言模型的训练方法 ORL（On-Policy Residual Learning，在策略残差学习），并配套自研推理引擎 dlmrt，在单张 RTX 5090 上以 LLaDA-2.1-mini + ORL 的 NVFP4 配置实现 2788 tokens/s，在 8 张 B200 上以 DiffusionGemma 26B MoE + ORL 达到 7708 tokens/s。模型、训练代码、评估流程与推理引擎均已完全开源。 扩散语言模型可以并行细化多个 token，但收敛速度慢一直使其在实际吞吐上远落后于自回归模型；ORL 在提升生成质量的同时大幅缩小了这一差距，有望让扩散解码成为对延迟敏感场景下可行的替代方案。由于整套技术栈完全开源，其他团队可以立即复现并在此基础上继续开发。 所有数据均为特定基准上的单请求（batch size 1）峰值结果，而非任意提示词下的平均值；在 QwenDLM-4B 上，ORL 将每次前向生成的 token 数最多提升 6.2 倍、端到端吞吐提升约 6.9 倍，HumanEval pass@1 从 82.9% 提升到 89.6%。LLaDA-2.1-mini 仅需 420 万自生成训练 token 和 36 个 H100 GPU 小时的后训练，且 dlmrt 在单张 H100 对比中比 SGLang/vLLM 快 1.2–1.6 倍。

reddit · r/MachineLearning · /u/arty_photography · 10月16日 20:03

**背景**: 自回归大模型从左到右一次生成一个 token，而扩散语言模型从完全掩码或加噪的序列出发，利用双向上下文并行地对所有位置迭代去噪。其短板在于往往需要很多去噪步才能收敛，导致单 token 延迟和吞吐都不理想。ORL 的做法是在模型自身新生成的残差轨迹上训练（即“在策略”），并引入相邻熵收缩目标，促使每一步去噪更快降低不确定性；dlmrt 则把整个去噪循环捕获进 CUDA graph 在 GPU 上执行，并支持面向 NVIDIA Blackwell GPU 的 4 位浮点格式 NVFP4。

**对中国影响**: 该工作完全开源，且 RTX 5090 是在中国可广泛买到的消费级显卡，因此国内开发者与硬件团队无需受出口管制的数据中心加速卡即可复现结果；这也为国内 AI 工具链项目提供了扩散模型推理引擎的新参考实现。

**对我有什么用**: 对电子工程师/硬件开发者而言，这是少有的能在消费级硬件上本地跑高速扩散语言模型的机会：RTX 5090 的 NVFP4 路径与开源的 dlmrt 引擎可在单卡工作站上复现，其中的 CUDA graph 捕获与量化技术也可直接迁移到其他嵌入式或边缘 AI 加速项目中。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/html/2610.20687v1">On-Policy Residual Learning for Diffusion Language Models</a></li>
<li><a href="https://github.com/Introspective-Diffusion/ORL/blob/main/">ORL: On-Policy Residual Learning for Diffusion Language Models</a></li>
<li><a href="https://www.emergentmind.com/topics/diffusion-based-large-language-models-dllms">Diffusion -based LLMs</a></li>

</ul>
</details>

**标签**: `#diffusion-LLM`, `#inference-optimization`, `#open-source`, `#AI-toolchain`, `#NVFP4`

---

<a id="item-4"></a>
### *（简报）* [特斯拉发布搭载冷气推进器与火箭选装的新款 Roadster 演示](https://www.tesla.com/roadster) ⭐️ 7.0/10 · 相关 3/10

特斯拉发布了重新设计的新款 Roadster 演示，搭载由 SpaceX 开发的冷气推进器以及可选装的火箭发动机套件，视频中展示了推进器驱动的起步、空中翻滚以及倒挂坡道特技。该车提供两种模式：一种使用冷气推进器以增强前向加速，另一种为仅限受邀用户购买的真实燃烧火箭发动机版本。 这次演示突破了量产电动超跑的性能边界，将航天器推进技术与消费级汽车工程相结合，并引发了关于技术可行性、安全性和商业伦理的激烈讨论。它表明特斯拉仍愿意追求以视觉奇观为导向的工程尝试，尽管这些尝试未必能转化为商业上可行的产品。 冷气推进器通过高压惰性气体膨胀产生推力，不涉及燃烧，因此结构更简单、成本更低，但推力远小于燃烧火箭发动机；火箭版本仅限受邀用户购买，且可能永远不会量产。特斯拉要求支付 25 万美元的预订押金，并且公司已表示无法保证预订车辆最终交付。

---

<a id="item-5"></a>
### *（简报）* [博客从联想记忆推导 Transformer 原理，引发 HN 热议](https://alexwang.ai/posts/associative-memory/) ⭐️ 7.0/10 · 相关 6/10

Alex Wang 发表博客文章《You could have invented transformers from memory》，从联想记忆和 Hopfield 网络出发重新推导 Transformer 架构，提供了从零理解注意力机制的直观解释。该文在 Hacker News 上获得 112 分和 30 条评论，通信工程师与 AI 学习者在评论区讨论了信道容量与模型容量之间的类比。 文章将现代大语言模型背后的主流架构 Transformer 重新解释为一种内容可寻址的联想记忆，为其他领域的工程师提供了熟悉的切入点来理解 AI 内部机制。评论区的讨论凸显出通信/电子工程与机器学习之间日益增强的交叉融合，这可能加速从业者对模型容量与干扰等概念的理解。 文章将 Transformer 的注意力机制与现代 Hopfield 网络（稠密联想记忆）联系起来，后者通过能量函数存储模式，容量远高于经典 Hopfield 网络。有评论者指出，Transformer 只需一步就能检索到合适的记忆，而普通 Hopfield 网络需要多次迭代才能收敛。

---

<a id="item-6"></a>
### *（简报）* [苹果 MLX 新增分布式推理，可在 Mac Studio 集群上运行近万亿参数模型](https://machinelearning.apple.com/research/mlx-distributed-inference) ⭐️ 7.0/10 · 相关 8/10

苹果发布了支持分布式推理的新版 MLX 框架，使四台 Mac Studio 组成的集群能够以超过 36 tokens/s 的速度运行近万亿参数的 Muse Spark Open 模型。苹果在其机器学习研究博客上公布了这一结果，展示了模型从单台配备最高 512GB 统一内存的 Mac Studio 起步，再横向扩展到多台机器的过程。 这是本地大模型推理的重要进展，开发者可以在消费级苹果硬件上运行前沿级别的开源权重模型，而不必租用云端 GPU。这也增强了苹果在端侧 AI 工具链竞争中相对 CUDA 阵营及其他本地推理方案的地位。 官方宣传的 36 tokens/s 是在 8,192 token 上下文长度下测得的，有评论者指出这对如今的长上下文任务来说偏短；此外基准测试中 Meta 的模型使用 4-bit 量化，而 Qwen 仅以原生 BF16 对比。MLX 是苹果为 Apple Silicon 统一内存架构优化的开源数组框架，其分布式特性可将模型拆分到多台 Mac 上联合推理。

---

<a id="item-7"></a>
### *（简报）* [Jake Archibald 深度对比 JPEG XL 与 AVIF，引发社区热议](https://jakearchibald.com/2026/jpeg-xl-vs-avif/) ⭐️ 7.0/10 · 相关 4/10

Jake Archibald 发表了一篇针对 Web 场景的 JPEG XL 与 AVIF 深度对比文章，涵盖压缩效率、编码速度和画质表现。文章包含实用的 ffmpeg 参数以及 Butteraugli 等感知指标，在 Hacker News 上获得 184 分和 142 条评论。 该对比为 Web 开发者提供了在两种下一代图像格式之间做选择的具体数据，直接影响页面加载性能和带宽成本。社区讨论凸显了 AVIF 的感知质量问题（如高光丢失）和 JPEG XL 的编码速度慢等关键权衡，可能影响这两种格式在 Web 上的采用。 文章指出，libjxl 的最高压缩档位对照片可再减小 2–7%，对截图和插画可减小约 25%，但耗时 9–46 秒（比默认设置慢 50–180 倍），这主要源于使用 Butteraugli 感知指标的迭代评估优化循环。评论者还指出，像 jixel 这样更好的编码器能在几秒内达到类似效果，而 AVIF 会抹除 F1 赛车等图像中的精细高光。

---

<a id="item-8"></a>
### *（简报）* [Anthropic 的 Claude Code 团队公开其 AI 驱动的代码审查流程](https://claude.dev/blog/solving-code-review-at-anthropic/) ⭐️ 7.0/10 · 相关 6/10

Anthropic 的 Claude Code 团队发布博客，介绍了他们如何对每一个 pull request 都运行自动化的 AI 审查，并结合按风险分级的审批流程与合并队列，据称回滚（revert）数量下降了 40% 以上。文章还提到，文档、文案以及藏在功能开关后的内部功能等低风险改动，只要自动化审查和安全检查通过，就可以无需人工审查直接合并。 这是大型 AI 实验室首次较为详细地公开自己在高代码量下“自用”AI 代码审查的实践，因此成为其他团队决定保留多少人工审查的重要参考。它也加剧了一个更广泛的争论：AI 审查能否被信任来处理文档和低风险代码，以及每行代码的真实成本究竟有多高。 该流程对每个 PR 都运行 AI 审查，然后按风险分级处理：文档、文案、藏在功能开关后的内部功能等低风险改动，只要自动化审查与安全检查通过就无需人工签字；风险较高的改动仍需人工介入。团队表示，他们的优化目标是找到“不增加回滚或事故的最少人工审查时间”，并且审查器的评测集（eval）会随着每一次事故而扩充。

---

<a id="item-9"></a>
### *（简报）* [Mercor 研究：美国 90%的工作时间缺乏 AI 基准覆盖](https://www.mercor.com/research/labor-index/benchmark-map/) ⭐️ 7.0/10 · 相关 3/10

Mercor 发布的劳动力指数（Labor Index）研究显示，美国约 90%的工作时间花在现有 AI 基准几乎或完全没有覆盖的任务上；即便在控制 AI 暴露度之后，来自高薪职业的 O*NET 任务在基准提示词中仍被显著过度代表。 这揭示了 AI 能力评估方式与人们实际从事工作之间的严重脱节：基准分数可能无法反映真实岗位表现，并可能误导 AI 投资方向与自动化政策。 该研究基于 O*NET 职业任务数据和工资总额加权；有评论者指出“覆盖良好”的定义过于宽松，例如“社会工作者与护理——为育儿问题提供家长咨询”这一类别仅凭 13 条提示词就被算作覆盖良好。

---

<a id="item-10"></a>
### *（简报）* [Home Assistant 默认进行 Pwned 密码检查引发隐私争议](https://github.com/home-assistant/home-assistant.io/issues/49314) ⭐️ 7.0/10 · 相关 6/10

在 home-assistant.io 仓库的一个 GitHub issue 中，用户指责 Home Assistant 在未明确获得用户同意（opt-in）的情况下，将用户密码数据发送给 Have I Been Pwned（HIBP）服务。Home Assistant 开发者 frenck 公开为其最初敷衍的回复道歉，并说明可以通过命令 `ha security options --pwned=false` 关闭该检查。 这一事件凸显了开源与智能家居软件中主动安全功能与用户知情同意之间的日益紧张的矛盾，也说明一个默认设置就可能侵蚀用户对广泛使用平台的信任。同时，它也表明当涉及隐私的默认行为受到质疑时，开发者保持尊重、坦诚的沟通至关重要。 该检查已在 Home Assistant Supervisor 中存在多年，仅针对被标记为密码的应用选项；它只发送密码 SHA-1 哈希值的前 5 个字符（k-匿名机制），从不发送密码本身。最近一次版本更新修复了触发该检查的警告提示，这正是用户现在才注意到它的原因。

---

## 🎯 猜你感兴趣

以下 2 条未进客观分前 10，但与你的兴趣画像高度相关。

---

<a id="item-11"></a>
## [CS 学生的 Rust 框架 DenseCore 在 nanoGPT 上逐位复现 PyTorch](https://www.reddit.com/r/MachineLearning/comments/1x7ojxo/p_my_rust_framework_trains_nanogpt_with_the_exact/) ⭐️ 7.0/10 · 相关 6/10

一名计算机科学专业的学生用 Rust 编写了一个小型深度学习框架 DenseCore，并提供类似 PyTorch 的 Python API。他演示了在不修改 Karpathy 的 nanoGPT 代码的情况下，训练结果与 PyTorch 逐位完全一致：manual_seed 生成的初始权重、损失、梯度、权重在全部 50 个测试步骤中都相同，即使开启 dropout 也一样。 与 PyTorch 实现逐位数值一致极为罕见，需要对未公开的实现细节进行逆向工程。因此这项工作对研究数值可复现性、跨框架兼容性以及轻量级训练/推理运行时的人来说，是一个很有价值的案例。 作者发现 PyTorch 的 CPU attention 并非教科书公式，而是 flash attention 内核，并且在开启 dropout 时会切换到另一条代码路径；Adam 由于编译器对尾部循环的融合，在每个线程分块的末尾元素上舍入方式不同；clip_grad_norm_ 内部实际计算的是 reciprocal() * max_norm 而非除法。该框架体积仅约 2 MB，而 PyTorch 约 580 MB；由于 PyTorch 自身在不同机器上都无法逐位一致（macOS 与 Linux x86 之间 26 个算子只有 1 个结果相同），DenseCore 目前只能在 Apple Silicon Mac 上与 PyTorch 完全一致。

reddit · r/MachineLearning · /u/Mental-Feature-2377 · 10月16日 18:49

**背景**: nanoGPT 是 Andrej Karpathy 编写的极简、易读的 GPT Transformer 实现，常被用作教学和基准测试的参考。Flash attention 是一种融合注意力内核，通过分块计算避免在内存中生成完整的 N×N 注意力矩阵，从而提升速度和内存效率。逐位可复现意味着两次运行产生完全相同的浮点结果，连最后一位都一致；这很难做到，因为浮点运算对顺序敏感，编译器、库和硬件可能以不同方式重排或融合运算。

**对中国影响**: 中国的 AI 工具链生态正在积极构建 PyTorch 的国产替代方案，如 PaddlePaddle 和 MindSpore，而这项工作凸显了与 PyTorch 实现逐位兼容的难度；它可以为追求 PyTorch 无缝替换或国产硬件上可复现训练的中国框架开发者提供参考。

**对我有什么用**: 对电子工程师或硬件开发者而言，这个项目是一个紧凑、可复刻的数值可复现性与轻量级运行时案例：2 MB 的框架可以启发为嵌入式或 CI 环境构建类似的逐位一致工具，而逆向出的 PyTorch 实现细节也有助于排查为什么不同硬件上的两次训练结果会不一致。

**入选理由**: 该项目属于AI工具链/框架开发，与读者关注的AI模型与开发工具链有一定关联，但并非其核心的开源硬件、嵌入式或EDA方向，属于可了解但非直接可复刻或日常使用的技术内容。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://grokipedia.com/page/nanoGPT">nanoGPT</a></li>
<li><a href="https://github.com/Dao-AILab/flash-attention">GitHub - Dao-AILab/flash-attention: Fast and memory-efficient ...</a></li>
<li><a href="https://blog.csdn.net/m0_46702604/article/details/121852450">torch.nn.utils. clip _ grad _ norm _()函数详解_ grad norm 函数-CSDN博客</a></li>

</ul>
</details>

**标签**: `#Rust`, `#深度学习框架`, `#PyTorch`, `#数值一致性`, `#AI工具链`

---

<a id="item-12"></a>
## [研究者利用 OpenBSD 内核中潜伏 37 年的漏洞](https://calif.io/research/big-fish) ⭐️ 7.0/10 · 相关 5/10

一位安全研究者披露并成功利用了一个在 OpenBSD 内核中存活了 37 年的漏洞，并以《Big Fish》为题发布了完整分析。该漏洞在 OpenBSD 以严格著称的代码审计下存活数十年，引发外界对模糊测试与静态分析能否发现此类问题的讨论。 OpenBSD 一向被视为最重视安全、审计最严格的系统之一，因此一个存活 37 年且可被利用的内核漏洞，动摇了“仅靠人工代码审计即可保证内核安全”的假设。这一案例有力说明，人类对漏洞利用原语的推理仍能发现自动化工具难以覆盖的一类缺陷。 该漏洞据称可追溯到 BSD 血统继承下来的老代码，有评论者指出 NetBSD 在 1999 年 8 月重写相关代码时无意中修掉了它。文章将该缺陷描述为一种需要人类洞察才能发现的“利用原语”，而非例行模糊测试或静态分析能够轻易暴露的问题。

hackernews · rs_rs_rs_rs_rs · 10月16日 14:44 · [社区讨论](https://news.ycombinator.com/item?id=50118977)

**背景**: OpenBSD 是由 Theo de Raadt 于 1995 年从 NetBSD 1.0 分叉出来的、以安全为核心的自由类 Unix 操作系统，并从 1996 年夏天起由一支小型专职团队开创了系统化的源代码审计。内核模糊测试与静态分析是发现内存安全和逻辑缺陷的两大自动化手段，但内核模糊测试因环境配置复杂、内核代码具有状态性而格外困难。这使得长期潜伏、触发路径隐蔽的漏洞即便在成熟项目中也是持续难题。

**对中国影响**: 这条新闻没有直接的中国相关角度，但国内基于 BSD 系（包括 OpenBSD 及其衍生）构建网络设备、防火墙和嵌入式产品的厂商，可以借此机会排查自家内核中继承自老代码的隐患。

**对我有什么用**: 对电子工程师或硬件开发者而言，这条新闻只有间接关联：它是内核安全案例，而非开源硬件或嵌入式项目。不过它提醒我们，固件与嵌入式 Linux/BSD 系统常常继承数十年前的老代码，因此审计继承来的驱动和 BSP 代码是值得投入的工作。

**入选理由**: 属于操作系统内核安全漏洞研究，与硬件/嵌入式开发者的核心兴趣（开源硬件、EDA、嵌入式、鸿蒙）仅间接相关；但涉及 OpenBSD 内核与底层系统知识，对关注系统安全的工程师有一定参考价值。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/OpenBSD">OpenBSD - Wikipedia</a></li>
<li><a href="https://www.openbsd.org/security.html">OpenBSD : Security</a></li>
<li><a href="https://arxiv.org/pdf/2501.16165">A Survey of Operating System Kernel Fuzzing - arXiv.org</a></li>

</ul>
</details>

**社区讨论**: 评论者称赞了文章采用的 OpenBSD “Release” 风格配图，并开玩笑期待主题曲，但真正有分量的讨论集中在：一个漏洞为何能在审计最严格的代码库中存活 37 年。有评论者指出 NetBSD 在 1999 年重写代码时无意中修复了它；另一位则追问，模糊测试或静态分析是否真能发现这一类漏洞，还是必须依靠人类去思考利用原语。

**标签**: `#OpenBSD`, `#kernel-security`, `#vulnerability`, `#fuzzing`, `#static-analysis`

---

