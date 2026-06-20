---
layout: default
title: "Horizon Daily: 2026-06-20 (ZH)"
date: 2026-06-20
lang: zh
period: daily
period_id: 2026-06-20
---

> 从 19 条内容中筛选出 10 条重要资讯。

其中 **4 条 8 分以上**展开详细简报，其余 6 条仅列于索引。

---

1. [CSSQuake：用纯 CSS 运行《雷神之锤》](#item-1) ⭐️ 8.0/10
2. [时间序列建模需要动力系统视角](#item-2) ⭐️ 8.0/10
3. [大规模 LLM 推理开源手册发布](#item-3) ⭐️ 8.0/10
4. [minFLUX：FLUX 扩散模型的极简 PyTorch 实现](#item-4) ⭐️ 8.0/10
5. [探索屏幕无法显示的颜色](#item-5) ⭐️ 7.0/10
6. [开发者将整个网站存储在一个网站图标中](#item-6) ⭐️ 7.0/10
7. [DVD-JEPA：开源的最小化 JEPA 世界模型](#item-7) ⭐️ 7.0/10
8. [争议：没有顶会论文的机器学习博士生该毕业吗？](#item-8) ⭐️ 7.0/10
9. [免费工作坊：零数学基础教你从头构建大语言模型](#item-9) ⭐️ 7.0/10
10. [全球 PM2.5 预测模型用水平对齐架构解决方差陷阱](#item-10) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [CSSQuake：用纯 CSS 运行《雷神之锤》](https://cssquake.com/) ⭐️ 8.0/10

CSSQuake 是一个技术演示，它仅使用 CSS 和 HTML 重新创建了 1996 年的游戏《雷神之锤》，并由 PolyCSS 3D 引擎驱动。它将游戏渲染为可检查的 HTML 和 CSS 元素，不依赖 Canvas 或 WebGL。 该项目突破了 CSS 所能实现的界限，展示了纯 CSS 进行复杂 3D 渲染的可能性。它激发了创意编程，并展示了 Web 技术不断发展的能力。 该演示需要 JavaScript 来处理游戏逻辑和输入，但渲染完全基于 CSS。社区成员指出，它在现代硬件上运行速度比原版《雷神之锤》慢。

hackernews · msalsas · 6月20日 10:49 · [社区讨论](https://news.ycombinator.com/item?id=48608223)

**背景**: CSS（层叠样式表）主要用于网页样式设计，但现代 CSS 特性如 3D 变换、自定义属性和 clip-path 使得基本 3D 渲染成为可能。之前的项目如 CSS Doom 展示了类似能力，但 CSSQuake 是对完整游戏引擎的更复杂重建。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/LayoutitStudio/cssQuake">GitHub - LayoutitStudio/cssQuake: A port of Quake (1996), powered by the PolyCSS 3D engine. · GitHub</a></li>
<li><a href="https://cssquake.com/">cssQuake - Powered by PolyCSS</a></li>
<li><a href="https://news.ycombinator.com/item?id=48608223">CSSQuake | Hacker News</a></li>

</ul>
</details>

**社区讨论**: 社区对该技术成就印象深刻，但指出与原版《雷神之锤》相比存在性能问题。一些评论者质疑这是完整的引擎重建还是仅渲染器，其他人幽默地将退出游戏比作退出 vim。

**标签**: `#CSS`, `#web development`, `#game engine`, `#creative coding`, `#retro gaming`

---

<a id="item-2"></a>
## [时间序列建模需要动力系统视角](https://www.reddit.com/r/MachineLearning/comments/1uark0u/time_series_modeling_needs_a_dynamical_systems/) ⭐️ 8.0/10

一篇在 ICML 2026 上发表的观点论文主张时间序列建模应采用动力系统重建（DSR）来克服域外泛化和长期预测等局限。论文提出了五项具体建议，包括使用广义教师强制、在模拟动力系统上预训练、以及从 Transformer 转向现代 RNN。 该论文挑战了时间序列预测中主流的基于 Transformer 的范式，主张回归到基于动力系统理论的循环架构。如果被采纳，它可能实现更稳健的长期预测和域外泛化，影响天气预报、金融和神经科学等领域。 论文推荐使用广义教师强制来捕捉长期统计特性并降低模型复杂度，建议在混沌系统而非人工函数上进行预训练。它还指出，Transformer 由于粗粒度化会丢失关键的动力信息，因此不适合捕捉动力规则。

reddit · r/MachineLearning · /u/DangerousFunny1371 · 6月20日 08:47

**背景**: 自然界和工程中的时间序列数据通常来自潜在的动力系统，往往是混沌的。动力系统重建（DSR）旨在从观测数据中推断出控制方程，从而超越单纯的预测实现理解。当前的时间序列模型，尤其是 Transformer，由于忽略了动力学的递归性质，难以处理域外偏移和长期行为。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Teacher_forcing">Teacher forcing - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: Reddit 讨论中包含技术性评论，辩论 Transformer 和 RNN 之间的权衡，一些用户同意 Transformer 对动力系统不是最优选择。其他人质疑 RNN 在大数据集上的可扩展性。总体情绪积极，对提出的具体训练技术表示赞赏。

**标签**: `#time series`, `#dynamical systems`, `#machine learning`, `#ICML`, `#forecasting`

---

<a id="item-3"></a>
## [大规模 LLM 推理开源手册发布](https://www.reddit.com/r/MachineLearning/comments/1uavduv/an_open_handbook_on_llm_inference_at_scale_gpu/) ⭐️ 8.0/10

一本关于大规模 LLM 推理的开源手册（仍在完善中）已发布，内容涵盖 GPU 内部结构、内存层次结构、KV 缓存、批处理以及 vLLM、SGLang 和 TensorRT-LLM 等生产框架。作者添加了 mermaid 图表来展示 GPU 执行和内存瓶颈。 该手册填补了关于 LLM 推理优化的实用知识空白，这对于在生产环境中高效部署模型至关重要。随着 LLM 的普及，理解 GPU 内存瓶颈和推理框架是降低成本和延迟的关键。 该手册是一个个人学习项目，托管在 GitHub 上，积极通过 issue 和 PR 寻求社区反馈和贡献。它详细解释了为什么 GPU 在推理期间大部分时间处于空闲状态，以及内存层次结构如何限制吞吐量。

reddit · r/MachineLearning · /u/YouFirst295 · 6月20日 12:27

**背景**: 大规模 LLM 推理需要仔细优化 GPU 内存和计算。关键技术包括 KV 缓存以避免重复计算注意力键/值、连续批处理以最大化 GPU 利用率，以及实现这些优化的框架如 vLLM、SGLang 和 TensorRT-LLM。GPU 内存层次结构（寄存器、共享内存、全局内存）显著影响推理性能。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://alain-airom.medium.com/from-theory-to-practice-demystifying-the-key-value-cache-in-modern-llms-9674e9f904a5">From Theory to Practice: Demystifying the Key-Value Cache ... | Medium</a></li>
<li><a href="https://www.spheron.network/blog/vllm-vs-tensorrt-llm-vs-sglang-benchmarks/">vLLM vs TensorRT - LLM vs SGLang : H100... | Spheron Blog</a></li>
<li><a href="https://www.w3reference.com/blog/the-hidden-bottleneck-how-gpu-memory-hierarchy-affects-your-computing-experience/">The Hidden Bottleneck: How GPU Memory Hierarchy Affects Your...</a></li>

</ul>
</details>

**标签**: `#LLM Inference`, `#GPU`, `#Machine Learning`, `#Systems Optimization`, `#Open Source`

---

<a id="item-4"></a>
## [minFLUX：FLUX 扩散模型的极简 PyTorch 实现](https://www.reddit.com/r/MachineLearning/comments/1ub1db3/studying_flux_in_diffusers_library_was_hard_so_i/) ⭐️ 8.0/10

一位开发者发布了 minFLUX，这是一个开源的 FLUX 扩散模型（FLUX.1 和 FLUX.2）的极简 PyTorch 实现，提供了与 HuggingFace diffusers 的逐行映射，并包含训练和推理循环。 该项目通过去除官方 diffusers 库的复杂性，使研究 FLUX 扩散模型变得更加容易，让研究人员和从业者能够快速理解核心架构并进行修改实验。 该实现涵盖了 FLUX.1 和 FLUX.2，突出了架构差异，如改进的 Transformer 块、调制、FFN、VAE 归一化和位置 ID。它包含使用流匹配和速度 MSE 的训练循环，以及使用 Euler ODE 求解器的推理循环。

reddit · r/MachineLearning · /u/Other-Eye-8152 · 6月20日 16:50

**背景**: FLUX 是 Black Forest Labs 开发的现代扩散模型架构，基于 Diffusion Transformer（DiT）和流匹配，相比 Stable Diffusion 提供更优的文本理解和图像质量。官方 HuggingFace diffusers 库提供了全面但复杂的实现，使新手难以研究核心组件。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://flux101.com/en/basics/flux-model">Flux Model Introduction - Flux 101</a></li>
<li><a href="https://arxiv.org/abs/2506.02070">[2506.02070] An Introduction to Flow Matching and Diffusion Models</a></li>
<li><a href="https://docs.interstice.cloud/base-models/">Overview of the different diffusion models supported by the plugin</a></li>

</ul>
</details>

**社区讨论**: Reddit 社区反应积极，用户赞赏清晰的逐行映射和对教育价值的关注。一些人讨论了 FLUX.1 和 FLUX.2 之间的架构差异，指出了 Transformer 块和调制方面的改进。

**标签**: `#diffusion models`, `#FLUX`, `#PyTorch`, `#open-source`, `#machine learning`

---

<a id="item-5"></a>
### *（简报）* [探索屏幕无法显示的颜色](https://moultano.wordpress.com/2026/06/19/where-to-find-the-colors-your-screen-cant-show-you/) ⭐️ 7.0/10

一篇文章探讨了超出标准显示色域的颜色，重点关注 sRGB 无法再现的饱和蓝绿色，并讨论了激光投影仪和油漆颜色等实际案例。 这很重要，因为它突显了 sRGB 等常见色域的局限性，影响了我们在数字媒体、摄影和设计中感知和再现颜色的方式。理解这些差距可以推动更宽色域显示器和色彩管理实践的采用。 文章指出，CIE 1931 色度图可能高估了某些蓝绿色的重要性，因为人眼无法区分该区域内的许多颜色。它还提到，现代三色激光投影仪可以超越 Rec. 2020 色域，提供比 P3 大得多的色域。

---

<a id="item-6"></a>
### *（简报）* [开发者将整个网站存储在一个网站图标中](https://www.timwehrle.de/blog/i-stored-a-website-in-a-favicon/) ⭐️ 7.0/10

开发者 Tim Wehrle 展示了一种技术，通过将数据编码到网站图标（favicon）的像素中，再利用一个微小的引导加载器解码并渲染页面，从而将整个网站的内容存储在一个图标图像里。 这一创意黑客技术突破了网页开发和数据存储的边界，引发了社区关于 SVG 图标和多格式文件等替代方法的讨论，同时也提出了基于网站图标的追踪可能带来的安全与隐私问题。 该技术使用 PNG 格式的网站图标，每个像素编码部分数据，需要一个引导加载器（例如一小段 HTML/JavaScript 代码）来提取并显示内容。这种方法对于大型网站并不实用，但展示了一个有趣的概念验证。

---

<a id="item-7"></a>
### *（简报）* [DVD-JEPA：开源的最小化 JEPA 世界模型](https://www.reddit.com/r/MachineLearning/comments/1uatlzx/dvdjepa_an_opensource_fullyreproducible_jepa/) ⭐️ 7.0/10

DVD-JEPA 是 Yann LeCun 提出的联合嵌入预测架构（JEPA）的一个开源、完全可复现的实现。它通过预测未来的表征而非像素来学习世界模型，并在一个 16x16 网格中弹跳的 DVD 标志上进行了演示。 这项工作提供了一个最小化且诚实的 JEPA 演示，JEPA 是世界模型中像素级预测的一种有前途的替代方案。它表明学习未来的表征可以更高效、更鲁棒，并在异常检测和视频预测等领域具有潜在应用。 该模型使用上下文编码器、EMA 目标编码器和潜在预测器进行训练，无需标签或解码器。线性探针可以恢复标志的精确位置，误差在 0.73 像素以内，并且模型可以“想象”未来约 20 步的帧，之后会出现潜在漂移。

---

<a id="item-8"></a>
### *（简报）* [争议：没有顶会论文的机器学习博士生该毕业吗？](https://www.reddit.com/r/MachineLearning/comments/1uazlhg/would_you_let_an_ml_phd_student_graduate_without/) ⭐️ 7.0/10

一位 Reddit 用户提出假设场景：如果博士生论文工作扎实、方向连贯，但没有任何顶级会议（如 NeurIPS、ICML、ICLR、CVPR）或顶级期刊论文，只有三篇第一作者 A 类论文，导师是否应支持其毕业。 这场辩论凸显了机器学习学术界中发表文化与论文质量之间的张力，影响毕业标准、学生心理健康，以及超越会议声望的研究贡献价值。 该学生已在项目中四年，有连贯的论文方向和三篇第一作者 A 类论文，但没有在 NeurIPS、ICML、ICLR 或 CVPR 等顶级会议发表过论文。

---

<a id="item-9"></a>
### *（简报）* [免费工作坊：零数学基础教你从头构建大语言模型](https://www.reddit.com/r/MachineLearning/comments/1uazlnd/hi_reddit_i_posted_my_build_your_own_llm_workshop/) ⭐️ 7.0/10

JustinAngel 在 YouTube 上发布了一个录播工作坊，教授如何从头构建大语言模型（LLM），内容涵盖机器学习基础、Transformer 架构和训练技术，且无需任何数学或机器学习先修知识。 该资源让广泛的受众能够接触到高级 LLM 概念，降低了学习现代 AI 开发的门槛。它填补了动手型学习者的需求缺口，让没有深厚数学背景的人也能理解 LLM 的内部原理。 工作坊包含幻灯片、基于 Excel 的直觉练习以及 PyTorch 代码示例，涵盖从感知机和激活函数到注意力机制和强化学习的主题。它还涉及使用 CUDA 和 Triton 进行 GPU 编程，并利用 torch.compile() 实现算子融合。

---

<a id="item-10"></a>
### *（简报）* [全球 PM2.5 预测模型用水平对齐架构解决方差陷阱](https://www.reddit.com/r/MachineLearning/comments/1uar4vc/built_a_global_aq_pm25_forecaster_ml_model_p/) ⭐️ 7.0/10

一位实践者利用来自 OpenAQ 和 NASA 的 160 万+行数据，构建了一个覆盖美国、英国、印度和澳大利亚的全球 PM2.5 预测模型。他们通过水平对齐架构解耦预测时间范围，解决了方差陷阱问题，使全局 MASE 降至 1.0 以下。 这项工作展示了一种针对时间序列预测常见失败模式（方差陷阱）的实用解决方案——在高方差环境中，简单基线模型可能优于 ML 模型。这种水平对齐方法可应用于其他混沌预测领域，如能源需求或金融市场。 该模型使用无状态梯度提升回归器，具有严格的自回归滞后向量，针对每个时间范围（h=1、7、14、30）对齐，并包含一个在推理边界结束的 3 天滚动波动率矩阵以防止数据泄露。在 30 天时间范围内，模型相对于混沌热力学基线保持了 57%的预测准确率。

---

