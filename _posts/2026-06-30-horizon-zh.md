---
layout: default
title: "Horizon Daily: 2026-06-30 (ZH)"
date: 2026-06-30
lang: zh
period: daily
period_id: 2026-06-30
---

> 从 22 条内容中筛选出 12 条重要资讯。

其中 **9 条 8 分以上**展开详细简报，其余 3 条仅列于索引。

---

1. [美国最高法院裁定地理围栏搜查令需受宪法保护](#item-1) ⭐️ 9.0/10
2. [谷歌智能体 AI 审稿人处理约 1 万篇论文，错误检测率提升 34%](#item-2) ⭐️ 9.0/10
3. [火箭实验室历史性收购铱星公司](#item-3) ⭐️ 8.0/10
4. [WATaBoy：将 Game Boy 指令 JIT 编译为 WebAssembly，性能超越原生解释器](#item-4) ⭐️ 8.0/10
5. [深入解析：运行 CUDA 内核时发生了什么](#item-5) ⭐️ 8.0/10
6. [Ornith-1.0：面向智能体编程的自脚手架大语言模型](#item-6) ⭐️ 8.0/10
7. [OpenAI 与 Cerebras 交易导致初创公司推理访问受阻](#item-7) ⭐️ 8.0/10
8. [EML 树被证明是连续函数的通用逼近器](#item-8) ⭐️ 8.0/10
9. [历史剑术爱好者构建开放数据集，以提升 AI 对剑术动作的追踪能力](#item-9) ⭐️ 8.0/10
10. [拟议的 .self 顶级域名旨在通过免费子域名赋能自托管](#item-10) ⭐️ 7.0/10
11. [Qwen 3.6 27B：强大的本地模型，但硬件成本高昂](#item-11) ⭐️ 7.0/10
12. [一项测验揭示 15 个大型语言模型之间的价值观差异](#item-12) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [美国最高法院裁定地理围栏搜查令需受宪法保护](https://www.theguardian.com/us-news/2026/jun/29/supreme-court-geofence-warrants-case-decision) ⭐️ 9.0/10

美国最高法院裁定，允许执法机构获取特定区域内所有设备位置数据的地理围栏搜查令必须遵守第四修正案的保护，需要基于可能原因和具体性的搜查令。 这项里程碑式的裁决极大地限制了无搜查令获取批量位置数据的行为，加强了数字隐私权，并为法院在数字时代处理反向搜查令树立了先例。 该案涉及谷歌的 Sensorvault 数据库，该数据库存储 Android 设备的历史地理位置数据。法院应用“Carpenter 因素”认定，地理围栏搜查令侵犯了合理的隐私期望，即使在公共场所也是如此。

hackernews · cdrnsf · 6月29日 15:54 · [社区讨论](https://news.ycombinator.com/item?id=48720924)

**背景**: 地理围栏搜查令，也称为反向位置搜查令，允许警方在特定地理区域和时间范围内搜索科技公司的数据库，以查找所有设备。第四修正案保护公民免受不合理搜查和扣押，最高法院 2018 年 Carpenter 诉美国案的判决确立了获取历史基站位置数据需要搜查令。本次裁决将类似保护扩展至地理围栏搜查令。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Geofence_warrant">Geofence warrant</a></li>

</ul>
</details>

**社区讨论**: 评论者对该裁决表示强烈支持，一些人提到了历史先例，如通过 IP 地理位置识别 Paula Broadwell。其他人则提出了对其他监控工具（如 Flock 摄像头）的影响问题。阿利托和托马斯大法官的异议受到批评，而巴雷特的异议令一些人感到意外。

**标签**: `#privacy`, `#supreme court`, `#digital rights`, `#fourth amendment`, `#surveillance`

---

<a id="item-2"></a>
## [谷歌智能体 AI 审稿人处理约 1 万篇论文，错误检测率提升 34%](https://www.reddit.com/r/MachineLearning/comments/1uio9rb/googles_agentic_peerreviewer_handled_10k_papers/) ⭐️ 9.0/10

谷歌在顶级计算机科学会议 ICML 和 STOC 上部署了智能体 AI 审稿人，以 30 分钟的周转时间处理了约 10,000 篇论文。正式研究论文显示，与零样本提示相比，它能多检测出 34%的数学错误。 这为在会议规模上实现 AI 自动科学评审开创了先例，有望减轻审稿人负担并提高评审质量。这是将智能体 AI 融入学术同行评审过程的重要一步。 该系统每篇论文的周转时间为 30 分钟，实现了快速反馈。错误检测率提升 34%是相对于零样本提示（即不给 AI 任何示例的基线方法）而言的。

reddit · r/MachineLearning · /u/Justgototheeffinmoon · 6月29日 10:05

**背景**: 同行评审是科学出版的基石，由专家评估论文的质量和正确性。零样本提示是指要求 AI 执行任务时不提供示例，仅依赖其预训练知识。智能体 AI 系统能够自主规划并执行多步骤任务，因此适合处理审稿这类复杂工作流程。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.wired.com/2017/02/ai-can-solve-peer-review-ai-can-solve-anything/">If AI Can Fix Peer Review in Science, AI Can Do Anything | WIRED</a></li>
<li><a href="https://www.datacamp.com/tutorial/zero-shot-prompting">Zero-Shot Prompting: Examples, Theory, Use Cases - DataCamp</a></li>

</ul>
</details>

**社区讨论**: Reddit 社区对 AI 在同行评审中的规模和潜力表示兴奋，一些用户质疑错误检测的质量和偏见风险。其他人则指出正式发表论文对于验证结果的重要性。

**标签**: `#AI`, `#peer review`, `#machine learning`, `#conference`, `#automation`

---

<a id="item-3"></a>
## [火箭实验室历史性收购铱星公司](https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-acquire-iridium-historic-deal-creating-fully) ⭐️ 8.0/10

火箭实验室宣布收购铱星通信公司，这是一项历史性交易，将火箭实验室的发射和卫星制造能力与铱星的卫星网络和发射需求相结合，打造一家完全整合的太空公司。 此次收购使火箭实验室能够利用铱星现有的卫星网络和发射需求作为稳定基线，类似于 SpaceX 利用星链保证以最低成本进行定期发射。同时，铱星星座的替换需求也加入了火箭实验室的订单簿，为应对市场波动提供了重要对冲。 火箭实验室自行制造卫星，现在可以将铱星星座的替换卫星纳入其制造流程。该交易还使火箭实验室能够接入铱星的卫星网络，该网络运行在低地球轨道，提供全球通信服务。

hackernews · everfrustrated · 6月29日 14:09 · [社区讨论](https://news.ycombinator.com/item?id=48719485)

**背景**: 火箭实验室是一家端到端的太空公司，2006 年在新西兰成立，现总部位于美国，为小型卫星提供发射服务和卫星制造。铱星通信公司运营着一个由 75 颗升级版 Iridium NEXT 卫星组成的全球卫星网络，覆盖整个地球。此次收购模仿了 SpaceX 利用星链星座确保稳定发射节奏的策略。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Iridium_satellite_constellation">Iridium satellite constellation - Wikipedia</a></li>
<li><a href="https://www.space.com/rocket-lab.html">Rocket Lab : Private Spaceflight for Tiny Satellites | Space</a></li>

</ul>
</details>

**社区讨论**: 社区评论表达了对太空垃圾和太空商业化的担忧，有用户质疑增加卫星数量的价值。其他人则认为此次收购是明智的战略举措，注意到与 SpaceX 星链杠杆模式的相似之处。一些用户对火箭实验室从新西兰公司转变为美国公司感到惊讶。

**标签**: `#space`, `#acquisition`, `#satellites`, `#Rocket Lab`, `#Iridium`

---

<a id="item-4"></a>
## [WATaBoy：将 Game Boy 指令 JIT 编译为 WebAssembly，性能超越原生解释器](https://humphri.es/blog/WATaBoy/) ⭐️ 8.0/10

一篇博客文章介绍了 WATaBoy，这是一款 Game Boy 模拟器，它使用即时编译（JIT）技术在运行时将 Game Boy 指令翻译成 WebAssembly（WASM），性能超越了原生解释器。 这展示了一种利用 WebAssembly 在浏览器中的 JIT 能力进行模拟的新方法，可能使 iOS 等限制原生 JIT 编译的平台也能实现高性能模拟。 该项目是一项本科生工作，基准测试显示 Firefox 在此工作负载下比 Chrome/Safari 慢约 25%。该方法利用了浏览器中 WebAssembly 引擎已具备 JIT 编译能力的事实。

hackernews · energeticbark · 6月29日 15:02 · [社区讨论](https://news.ycombinator.com/item?id=48720190)

**背景**: Game Boy 模拟器传统上使用解释执行或原生 JIT 编译（动态重编译）来运行游戏。由于安全限制，iOS 上通常禁止原生 JIT，但浏览器被允许对 JavaScript 和 WebAssembly 进行 JIT 编译。WATaBoy 动态生成 WASM 代码，让浏览器的 WASM 引擎优化并高效执行。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/sysprog21/jitboy">GitHub - sysprog21/jitboy: A Game Boy emulator with dynamic recompilation (JIT) · GitHub</a></li>
<li><a href="https://rodrigodd.github.io/2023/09/02/gameroy-jit.html">GameRoy: JIT compilation in High-Accuracy Game Boy Emulation | Rodrigodd</a></li>
<li><a href="https://8bitworkshop.com/docs/posts/2021/webassembly-vs-javascript-emulator-performance.html">Emulator Performance : WebAssembly vs. JavaScript</a></li>

</ul>
</details>

**社区讨论**: 评论者称赞该项目作为本科生作品令人印象深刻。有人指出 WASM 开销（约 20%）远小于解释器开销（约 1000%），解释了性能提升的原因。另一人指出苹果对浏览器的 JIT 例外使得该方法在 iOS 上可行。还提到了 Andrew Kelley 早期关于 NES 代码静态重编译的工作。

**标签**: `#JIT compilation`, `#WebAssembly`, `#emulation`, `#Game Boy`, `#performance`

---

<a id="item-5"></a>
## [深入解析：运行 CUDA 内核时发生了什么](https://fergusfinn.com/blog/what-happens-when-you-run-a-gpu-kernel/) ⭐️ 8.0/10

一篇详细的博客文章完整梳理了启动 CUDA 内核的软件与硬件路径，从 CPU 驱动提交到 GPU 执行，包括对门铃机制和队列管理描述符（QMD）的新颖解释。 这篇深度文章填补了典型 CUDA 教程的空白——通常只讲到内核、块和线程束，而忽略了关键的 CPU 到 GPU 路径。理解这一路径有助于开发者优化性能并调试 GPU 计算中的问题。 文章详细描述了门铃寄存器的写入操作（用于通知 GPU 取任务）以及描述内核参数和网格配置的 QMD 结构。社区评论指出，控制码实际上是通过查表实现的，而不仅仅是控制字中的比特位。

hackernews · mezark · 6月29日 13:11 · [社区讨论](https://news.ycombinator.com/item?id=48718863)

**背景**: CUDA 是 NVIDIA 的并行计算平台，允许开发者在 GPU 上运行代码。内核启动涉及 CPU（主机）通过 CUDA 驱动向 GPU（设备）发送命令，驱动负责设置内存、参数和执行配置。随后 GPU 以线程束（warp）为单位调度和执行线程。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.geeksforgeeks.org/cpp/launching-a-kernel-in-cuda/">Launching a Kernel | CUDA - GeeksforGeeks</a></li>
<li><a href="https://medium.com/@snshyam/cuda-deep-dive-what-happens-when-you-launch-a-kernel-034e23624932">🚀 CUDA Deep Dive: What Happens When You Launch a Kernel? | by Shyam SN | Medium</a></li>

</ul>
</details>

**社区讨论**: 评论者赞赏文章的清晰度，尤其是门铃和 QMD 部分。有人指出，CUDA 在默认流中的隐式同步比 Vulkan 的显式模型更简单。另一位评论者提到了 NVIDIA 的开放 GPU 文档，可进一步了解 QMD 格式。

**标签**: `#CUDA`, `#GPU`, `#systems`, `#deep-dive`, `#NVIDIA`

---

<a id="item-6"></a>
## [Ornith-1.0：面向智能体编程的自脚手架大语言模型](https://simonwillison.net/2026/Jun/29/ornith/#atom-everything) ⭐️ 8.0/10

DeepReinforce 发布了 Ornith-1.0，这是一系列面向智能体编程的开源权重大语言模型（MIT 许可），提供 9B、31B、35B MoE 和 397B MoE 四种规模，基于 Gemma 4 和 Qwen 3.5 构建。它在编程基准测试中达到了同类开源模型的最高水平。 Ornith-1.0 引入了一种自脚手架训练框架，模型在强化学习过程中学会生成自己的智能体工具链，减少了对人工设计脚手架的依赖。这有望加速开源智能体编程能力的发展，并降低开发者的使用门槛。 该模型系列包括一个 397B MoE 变体，据称在 SWE-Bench 上可与 Claude Opus 4.7 媲美；9B 变体的性能超过了三倍于其规模的模型。底层模型（Gemma 4 和 Qwen 3.5）均采用 Apache 2.0 许可，确保了许可证兼容性。

rss · Simon Willison · 6月29日 16:17

**背景**: 智能体编程是指 AI 智能体在最少人工干预下自主规划、编写、测试和修改代码。传统大语言模型依赖手工制作的脚手架（工具链）来引导多步代码生成，而 Ornith-1.0 则学习同时生成解决方案和驱动这些方案的脚手架，这种技术称为自脚手架。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://simonwillison.net/2026/Jun/29/ornith/">Ornith-1.0: Self-Scaffolding LLMs for Agentic Coding</a></li>
<li><a href="https://deep-reinforce.com/ornith_1_0.html">Ornith-1.0: Self-Scaffolding LLMs for Agentic Coding</a></li>
<li><a href="https://github.com/deepreinforce-ai/Ornith-1">GitHub - deepreinforce-ai/Ornith-1</a></li>

</ul>
</details>

**社区讨论**: 社区讨论（Simon Willison 的博客）强调了该模型在初步测试中的强劲表现，例如在代码库中导航和生成图像。作者还提到了许可证兼容性分析，并称赞该模型能够熟练处理大量工具调用。

**标签**: `#LLM`, `#coding`, `#open-source`, `#AI agents`, `#model release`

---

<a id="item-7"></a>
## [OpenAI 与 Cerebras 交易导致初创公司推理访问受阻](https://www.reddit.com/r/MachineLearning/comments/1uiqhiv/cerebras_openai_deal_capacity_has_effectively/) ⭐️ 8.0/10

一家小型 AI 初创公司报告称，OpenAI 与 Cerebras 的交易已预先分配了 Cerebras 大部分推理能力，导致其他用户的 API 等待名单实际上无限延长。 这凸显了大型 AI 公司与专用硬件提供商之间的独家交易如何挤压依赖快速 ASIC 推理的实时产品初创公司。 该初创公司需要每秒 1-2k token 的持续吞吐量来支持实时编码代理，并已等待 Cerebras 等待名单数月。据报道，该交易涉及 OpenAI 购买约 200 亿美元的 Cerebras 芯片。

reddit · r/MachineLearning · /u/Kortopi-98 · 6月29日 12:00

**背景**: Cerebras 制造晶圆级引擎（WSE-3），这是世界上最大的 AI 芯片，拥有 4 万亿个晶体管，专为高吞吐量 AI 训练和推理设计。与 NVIDIA 的 GPU 不同，Cerebras 的 ASIC 架构为特定工作负载提供专用性能。该公司最近上市。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Cerebras">Cerebras - Wikipedia</a></li>
<li><a href="https://www.cerebras.ai/chip">Product - Chip - Cerebras</a></li>
<li><a href="https://inference-docs.cerebras.ai/quickstart">Make your first Cerebras API call in just minutes.</a></li>

</ul>
</details>

**社区讨论**: Reddit 上的社区评论表达了沮丧，并证实了该初创公司的经历，一些人指出独家容量交易在 AI 硬件领域正变得普遍，并对 Cerebras 关于可用性的公开声明提出质疑。

**标签**: `#AI hardware`, `#Cerebras`, `#OpenAI`, `#inference`, `#startup`

---

<a id="item-8"></a>
## [EML 树被证明是连续函数的通用逼近器](https://www.reddit.com/r/MachineLearning/comments/1uipl1t/eml_trees_are_universal_approximators_r/) ⭐️ 8.0/10

一篇新论文证明，通过 EML 算子（exp(x) - ln(y)）的组合表示初等函数的 EML 树，是连续函数和 Sobolev 空间的通用逼近器。 这一结果为使用 EML 树作为神经网络的替代方案进行函数逼近提供了理论基础，可能对机器学习模型设计产生影响。 证明构建了二元运算、多项式和双曲正切的 EML 表示，将它们作为构建块来逼近任何连续函数。解决的一个关键挑战是自然对数对非正输入的定义不良问题，通过基于符号的分解来处理。

reddit · r/MachineLearning · /u/JoeGermany · 6月29日 11:16

**背景**: EML 算子定义为 eml(x, y) = exp(x) - ln(y)，最近被证明能够通过组合表达所有初等函数。通用逼近定理是机器学习的基础，表明某些模型（如神经网络）可以任意精度逼近任何连续函数。Sobolev 空间是包含导数信息的函数空间，在许多数学和工程背景中很重要。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/html/2603.21852v2">All elementary functions from a single operator</a></li>
<li><a href="https://en.wikipedia.org/wiki/Sobolev_space">Sobolev space - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: Reddit 上的讨论包括对证明的意义和局限性的深刻评论，一些用户指出了为复杂函数构建 EML 树的实际挑战。

**标签**: `#universal approximation`, `#EML trees`, `#machine learning theory`, `#function approximation`

---

<a id="item-9"></a>
## [历史剑术爱好者构建开放数据集，以提升 AI 对剑术动作的追踪能力](https://www.reddit.com/r/MachineLearning/comments/1uivddx/i_do_historical_swordfighting_and_noticed_ai/) ⭐️ 8.0/10

一位历史欧洲武术（HEMA）练习者正在构建一个开放的多视角长剑格斗数据集（120-240 帧/秒），旨在挑战 AI 模型在快速运动、遮挡和细长物体追踪方面的能力。数据集模式包含生物力学、计算机视觉难点和帧级关键点的详细标注。 该数据集通过提供现有数据集中缺乏的真实世界极端运动和遮挡场景，有助于缩小具身 AI 中的 Sim2Real 差距。它可能改进机器人技术和运动分析中的姿态估计、轨迹预测和细长物体追踪。 该数据集使用同步多视角相机以 120/240 帧/秒拍摄，标注内容包括剑刃接触帧、步法类型、打击轨迹和遮挡等级。作者非技术背景，借助 AI 辅助设计数据模式，并在 Hugging Face 上托管以收集社区反馈。

reddit · r/MachineLearning · /u/fonssagrives · 6月29日 15:16

**背景**: Sim2Real 差距指的是在模拟环境中训练的 AI 模型因物理和外观差异而在现实世界中表现不佳的现象。细长物体追踪对计算机视觉尤其具有挑战性，因为像剑这样快速移动的狭窄物体常常低于像素分辨率或产生运动模糊。多视角同步相机设置是专业动作捕捉中常用的 3D 姿态重建方法。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2507.05198">[2507.05198] EmbodieDreamer: Advancing Real2Sim2Real Transfer ...</a></li>
<li><a href="https://inferensys.com/glossary/vision-language-action-models/world-models-and-state-representation/sim2real-gap">Sim2Real Gap: Definition & Solutions for AI/ML | Inference ...</a></li>
<li><a href="https://developers.move.ai/docs/multicam-fundamentals/">Multicam fundamentals | Move API</a></li>

</ul>
</details>

**社区讨论**: Reddit 讨论对数据模式提供了技术反馈，建议添加明确的剑格坐标、步法速度指标和更详细的遮挡标注。评论者赞赏这一新颖领域，并鼓励作者考虑多视角一致性检查。

**标签**: `#computer vision`, `#dataset`, `#embodied AI`, `#Sim2Real`, `#motion tracking`

---

<a id="item-10"></a>
### *（简报）* [拟议的 .self 顶级域名旨在通过免费子域名赋能自托管](https://hccf.onmy.cloud/2026/06/21/reclaiming-our-digital-selves-hccfs-vision-for-a-human-centered-top-level-domain/) ⭐️ 7.0/10

一项关于新顶级域名 .self 的提案已发布，旨在通过向个人提供免费子域名并执行反抢注规则来支持自托管。 如果实施，.self 可以通过为每个人提供免费的永久域名用于个人网站或服务，从而民主化在线存在，减少对中心化平台的依赖。然而，关于可持续性、滥用以及像 .tk 这样的免费 TLD 先例的担忧凸显了重大挑战。 该提案包括为所有人提供免费子域名，禁止停放、抢注或转售。资金和执行机制尚未明确，引发了对长期可行性的质疑。

---

<a id="item-11"></a>
### *（简报）* [Qwen 3.6 27B：强大的本地模型，但硬件成本高昂](https://quesma.com/blog/qwen-36-is-awesome/) ⭐️ 7.0/10

Qwen 3.6 27B 是一款新的开源权重模型，在编程基准测试中表现出色，超越了比它大 10 倍的模型，并具备代理式编码和仓库级推理能力，专为本地开发设计。 该模型为希望出于隐私或延迟原因在本地运行强大 LLM 的开发者提供了有吸引力的选择，但高昂的硬件成本（例如，128GB MacBook Pro 起价 6699 美元）使其与云 API 相比在经济上存疑。 本地运行 Qwen 3.6 27B 至少需要 128GB 内存，即便如此，发热和风扇噪音等实际问题使其不适合在笔记本电脑上进行严肃的编程工作。Mac Mini M4 被推荐为更可行的替代方案。

---

<a id="item-12"></a>
### *（简报）* [一项测验揭示 15 个大型语言模型之间的价值观差异](https://www.reddit.com/r/MachineLearning/comments/1uin5ad/i_made_a_quiz_that_tells_you_which_llm_you_align/) ⭐️ 7.0/10

ai-values.com 上的一项新测验将用户个性和价值观映射到 15 个大型语言模型，结果显示 Grok 4.3 和 GPT-4o 等模型在亿万富翁税收和回形针行动等问题上持有独特的伦理立场。 这项工作提供了一种新颖的、经验性的方法来比较 LLM 的价值对齐，突显出模型在伦理推理上存在显著差异，这对 AI 安全和部署具有重要意义。 该测验使用 117 个问题，每个模型至少提问 5 次，并包含大五人格和道德基础等框架。显著发现：只有 Grok 4.3 反对对亿万富翁征税，只有 GPT-4o 认为回形针行动是正当的，所有模型都认为删除有意识的数字心智等同于谋杀。

---

