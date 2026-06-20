---
layout: default
title: "Horizon Daily: 2026-06-20 (ZH)"
date: 2026-06-20
lang: zh
period: daily
period_id: 2026-06-20
---

> 从 20 条内容中筛选出 13 条重要资讯。

其中 **5 条 8 分以上**展开详细简报，其余 8 条仅列于索引。

---

1. [屏幕无法显示的颜色，去哪里寻找](#item-1) ⭐️ 8.0/10
2. [DVD-JEPA：开源 JEPA 世界模型，线性探针成功恢复位置](#item-2) ⭐️ 8.0/10
3. [时间序列建模需要动力系统视角](#item-3) ⭐️ 8.0/10
4. [开源手册详解大规模 LLM 推理：GPU 内部机制与生产框架](#item-4) ⭐️ 8.0/10
5. [minFLUX：FLUX 扩散模型的极简开源 PyTorch 实现](#item-5) ⭐️ 8.0/10
6. [CSSQuake：纯 CSS 渲染的《雷神之锤》网页版](#item-6) ⭐️ 7.0/10
7. [从 PGP 到 Mythos：加密出口管制无效的历史回顾](#item-7) ⭐️ 7.0/10
8. [Windows 11 新版媒体播放器内存占用增加 3.5 倍，HEVC 解码器需付费](#item-8) ⭐️ 7.0/10
9. [开发者将整个网站存储在网站图标中](#item-9) ⭐️ 7.0/10
10. [MCP 的关键优势：将认证流程隔离在智能体上下文之外](#item-10) ⭐️ 7.0/10
11. [免费工作坊：零数学基础教你从零构建大语言模型](#item-11) ⭐️ 7.0/10
12. [机器学习博士生没有顶会论文能否毕业？](#item-12) ⭐️ 7.0/10
13. [全球 PM2.5 预测机器学习模型解决方差陷阱](#item-13) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [屏幕无法显示的颜色，去哪里寻找](https://moultano.wordpress.com/2026/06/19/where-to-find-the-colors-your-screen-cant-show-you/) ⭐️ 8.0/10

文章探讨了超出典型屏幕色域的颜色，强调了 sRGB 的局限性以及某些饱和色调（尤其是蓝绿色区域）无法再现的问题。 这很重要，因为它揭示了当前显示技术的基本限制，影响了数字艺术、摄影和印刷等对色彩准确性至关重要的领域。 文章使用 CIE 1931 色度图来说明色域，但该图过度强调了蓝绿色区域的重要性，因为人眼无法区分该区域的许多颜色。sRGB 的真正缺陷是无法再现饱和的橙色/红色/紫色。

hackernews · moultano · 6月20日 03:36 · [社区讨论](https://news.ycombinator.com/item?id=48606140)

**背景**: sRGB 是大多数显示器、打印机和网络使用的标准色彩空间。其色域与人眼可见范围甚至 CMYK 印刷相比都有限。这意味着一些鲜艳的颜色，尤其是自然界中的颜色，无法在典型屏幕上显示。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/SRGB">sRGB - Wikipedia</a></li>
<li><a href="https://www.benq.com/en-us/knowledge-center/knowledge/color-gamut-monitor.html">Understanding Color Gamut Monitors – Expert Insights & Video</a></li>
<li><a href="https://www.w3.org/Graphics/Color/sRGB.html">A Standard Default Color Space for the Internet - sRGB</a></li>

</ul>
</details>

**社区讨论**: 评论指出，虽然蓝绿色在理论上无法再现，但实际问题是 sRGB 对饱和橙色/红色/紫色的再现不佳。一位评论者分享说，群青蓝等丙烯颜料颜色在照片中丢失了。另一位提到一台 CRT 电视具有非凡的青色强度，但强调荧光粉屏幕的色域也有限。

**标签**: `#color science`, `#display technology`, `#sRGB`, `#color gamut`, `#visual perception`

---

<a id="item-2"></a>
## [DVD-JEPA：开源 JEPA 世界模型，线性探针成功恢复位置](https://www.reddit.com/r/MachineLearning/comments/1uatlzx/dvdjepa_an_opensource_fullyreproducible_jepa/) ⭐️ 8.0/10

DVD-JEPA 是一个开源、最小化的联合嵌入预测架构（JEPA）世界模型实现，它从弹跳的 DVD 标志视频中学习预测未来表示，并通过线性探针实现了精确的位置恢复。 这项工作提供了一个完全可复现的、简单的 JEPA 演示，JEPA 是一个关键的自我监督学习概念，表明预测表示而非像素可以产生有用的世界模型。它降低了研究人员和实践者实验基于 JEPA 的方法的门槛。 该模型使用上下文编码器、EMA 目标编码器和潜在预测器，在 16×16 像素的弹跳 DVD 标志视频帧上进行训练。线性探针从冻结的 32 维潜在表示中恢复标志的精确(x,y)位置，误差在 0.73 像素以内。整个系统在浏览器客户端运行，仅需约 40 行 JavaScript 代码。

reddit · r/MachineLearning · /u/NielsRogge · 6月20日 10:52

**背景**: 联合嵌入预测架构（JEPA）是 Yann LeCun 于 2022 年提出的自我监督学习框架。与直接预测未来像素的传统视频预测模型不同，JEPA 在潜在空间中预测未来表示，丢弃不可预测的细节。该方法已用于 Meta AI 的 I-JEPA 和 V-JEPA 等模型中。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://medium.com/@tahirbalarabe2/what-is-jepa-085ca776013a">What is JEPA ? Joint Embedding Predictive Architecture ... | Medium</a></li>
<li><a href="https://huggingface.co/learn/computer-vision-course/unit13/i-jepa">Image-based Joint - Embedding Predictive Architecture (I- JEPA )...</a></li>
<li><a href="https://proceedings.mlr.press/v139/radford21a/radford21a-supp.pdf">We provide additional details for linear probe experiments</a></li>

</ul>
</details>

**社区讨论**: Reddit 讨论强调了该项目的巧妙和幽默，用户欣赏其简单性和可复现性。一些评论者指出，虽然环境很简单，但它有效地展示了 JEPA 的核心概念。其他人讨论了扩展到更复杂环境的可能性。

**标签**: `#world model`, `#self-supervised learning`, `#JEPA`, `#video prediction`, `#open-source`

---

<a id="item-3"></a>
## [时间序列建模需要动力系统视角](https://www.reddit.com/r/MachineLearning/comments/1uark0u/time_series_modeling_needs_a_dynamical_systems/) ⭐️ 8.0/10

一篇在 ICML 2026 上发表的观点论文主张时间序列建模应采用动力系统视角，提出了五项具体建议，包括使用广义教师强制、在动力系统模拟上预训练、以及从 Transformer 回归现代 RNN。 这一范式转变可能实现真正的域外泛化和长期预测，解决当前时间序列模型在混沌系统和拓扑变化上的根本局限。 论文比较了定制训练模型和基础模型在时间序列与动力系统重建上的表现，并指出正确的训练技术比模型架构更重要。它还强调拓扑变化是时间序列预测中最困难的问题。

reddit · r/MachineLearning · /u/DangerousFunny1371 · 6月20日 08:47

**背景**: 自然和工程中的时间序列数据通常来自潜在的动力系统，且往往是混沌的。动力系统重建（DSR）旨在推断过程的生成模型，超越单纯的预测。当前的机器学习模型，尤其是 Transformer，常常无法捕捉长期动态和域外泛化。

**标签**: `#time series`, `#dynamical systems`, `#machine learning`, `#ICML`

---

<a id="item-4"></a>
## [开源手册详解大规模 LLM 推理：GPU 内部机制与生产框架](https://www.reddit.com/r/MachineLearning/comments/1uavduv/an_open_handbook_on_llm_inference_at_scale_gpu/) ⭐️ 8.0/10

一本关于大规模 LLM 推理的开源手册已发布，内容涵盖 GPU 内存层次结构、KV 缓存、批处理以及 vLLM、SGLang 和 TensorRT-LLM 等生产框架。作者正在积极寻求社区反馈和贡献。 该手册罕见地深入剖析了 LLM 推理的内部机制，对于优化生产部署中的性能和成本至关重要，有助于弥合理论理解与实际实现之间的差距。 该手册包含用于架构可视化的 mermaid 图表，并托管在 GitHub 上（github.com/harshuljain13/llm-inference-at-scale）。这是一个仍在不断增长的个人学习项目，已完成关于 GPU 执行和内存内部机制的章节。

reddit · r/MachineLearning · /u/YouFirst295 · 6月20日 12:27

**背景**: 大规模 LLM 推理面临诸多挑战，包括 GPU 内存层次结构（HBM 与 SRAM）、KV 缓存管理以及高效批处理。vLLM 和 TensorRT-LLM 等生产框架已被开发出来以应对这些挑战，但理解底层内部机制是有效优化的关键。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://darshanfofadiya.com/llm-inference/gpu-memory.html">GPU Memory for LLM Inference : Why Llama-70B Doesn't Fit</a></li>
<li><a href="https://www.adaline.ai/blog/understanding-gpu-for-inference-in-llms">Understanding GPU for Inference in LLMs | Adaline</a></li>
<li><a href="https://developer.nvidia.com/blog/mastering-llm-techniques-inference-optimization/">Mastering LLM Techniques: Inference Optimization | NVIDIA Technical...</a></li>

</ul>
</details>

**社区讨论**: Reddit 讨论中包含实质性的技术评论，用户赞赏该手册的深度和清晰度。一些评论者建议增加推测解码和量化等主题，另一些人则根据生产经验提供了修正和见解。

**标签**: `#LLM inference`, `#GPU internals`, `#vLLM`, `#TensorRT-LLM`, `#open source`

---

<a id="item-5"></a>
## [minFLUX：FLUX 扩散模型的极简开源 PyTorch 实现](https://www.reddit.com/r/MachineLearning/comments/1ub1db3/studying_flux_in_diffusers_library_was_hard_so_i/) ⭐️ 8.0/10

一位开发者发布了 minFLUX，这是一个 FLUX.1 和 FLUX.2 扩散模型的极简 PyTorch 实现，包含逐行映射到 HuggingFace diffusers、训练和推理循环，以及 RoPE 和时间步嵌入等共享工具。 该项目通过提供清晰易懂的代码库，降低了研究人员和从业者学习和实验 FLUX 扩散模型的门槛，揭示了官方 diffusers 库的复杂性。 minFLUX 包含 FLUX.1 和 FLUX.2 两种实现，突出了架构差异，如改进的 Transformer 块、调制、FFN、VAE 归一化和位置 ID。它使用流匹配（velocity MSE）进行训练，并使用欧拉 ODE 求解器进行推理。

reddit · r/MachineLearning · /u/Other-Eye-8152 · 6月20日 16:50

**背景**: 扩散模型是一种生成模型，通过学习逆转加噪过程来去噪数据。FLUX 是 Black Forest Labs 开发的一系列扩散模型，FLUX.2 在 FLUX.1 的基础上引入了架构改进。HuggingFace diffusers 库为许多扩散模型提供了统一接口，但可能难以理解。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/black-forest-labs/FLUX.1-dev">black-forest-labs/ FLUX .1-dev · Hugging Face</a></li>
<li><a href="https://arxiv.org/abs/2210.02747">[2210.02747] Flow Matching for Generative Modeling</a></li>
<li><a href="https://diffusionflow.github.io/">Diffusion Meets Flow Matching</a></li>

</ul>
</details>

**社区讨论**: Reddit 帖子获得了积极反响，用户赞赏其与 diffusers 的清晰映射以及教育价值。一些评论讨论了 FLUX.1 和 FLUX.2 之间的架构差异，以及极简实现对于学习的实用性。

**标签**: `#diffusion models`, `#PyTorch`, `#FLUX`, `#open-source`, `#machine learning`

---

<a id="item-6"></a>
### *（简报）* [CSSQuake：纯 CSS 渲染的《雷神之锤》网页版](https://cssquake.com/) ⭐️ 7.0/10

CSSQuake 是一个基于网页的《雷神之锤》复刻版，它利用 CSS 和 HTML 渲染整个游戏，由 PolyCSS 驱动。玩家无需安装即可直接在浏览器中体验《雷神之锤》。 该项目展示了现代 CSS 和 Web 技术的惊人能力，突破了浏览器所能实现的界限。它通过将经典游戏带到新平台，唤起怀旧之情，展现了技术创造力和基于 Web 的游戏潜力。 CSSQuake 不仅仅是一个渲染器，它似乎是《雷神之锤》引擎和游戏逻辑的完整复刻，但某些行为与原版不同，例如按钮激活机制。性能可能有所差异，一些用户指出它在现代硬件上运行不如原版流畅。

---

<a id="item-7"></a>
### *（简报）* [从 PGP 到 Mythos：加密出口管制无效的历史回顾](https://techcrunch.com/2026/06/19/encryption-spyware-and-now-mythos-history-shows-why-cyber-export-control-doesnt-work/) ⭐️ 7.0/10

TechCrunch 一篇文章追溯了从 PGP 到 Anthropic 的 Mythos AI 模型的加密出口管制历史，认为此类管制始终未能阻止坚定的行为者，并对其真实目的提出质疑。 该分析质疑当前对 Mythos 等前沿 AI 出口管制的有效性，暗示这些管制可能服务于监控或扼制点目的，而非阻止技术扩散。 文章引用了三个例子：PGP 加密软件、NSO 集团的 Pegasus 等间谍软件，以及 Anthropic 的 Mythos AI 模型。文章指出，尽管 PGP 源代码在管制下仍全球传播，但美国政府成功阻止了其针对的部分间谍软件供应商。

---

<a id="item-8"></a>
### *（简报）* [Windows 11 新版媒体播放器内存占用增加 3.5 倍，HEVC 解码器需付费](https://www.extremetech.com/computing/windows-11s-new-media-player-uses-35x-more-ram-charges-for-popular-video) ⭐️ 7.0/10

Windows 11 新版媒体播放器空闲时内存占用约 377MB，而旧版仅 103MB，增加了 3.5 倍。此外，由于许可费用，微软在 Microsoft Store 中对 HEVC（H.265）视频扩展收费。 这凸显了两个令人担忧的趋势：现代前端技术（JS/TS）导致资源占用增加，以及基本解码器仍需支付许可费用。用户和开发者可能需要重新考虑媒体播放器的选择，转而使用 VLC 或 MPC-HC 等第三方播放器。 内存增加归因于使用 JavaScript/TypeScript 前端框架而非操作系统原生 API。HEVC 扩展在 Microsoft Store 售价 0.99 美元，但可通过 GPU 厂商驱动或第三方播放器免费获得替代方案。

---

<a id="item-9"></a>
### *（简报）* [开发者将整个网站存储在网站图标中](https://www.timwehrle.de/blog/i-stored-a-website-in-a-favicon/) ⭐️ 7.0/10

一位开发者通过将 HTML 数据编码到像素颜色中，将整个网站存储在一个网站图标（favicon）图像里，仅需一个很小的引导加载程序即可解码。 这一创意黑客技术展示了替代性的数据存储方法，并引发了关于基于网站图标进行指纹识别和追踪的安全担忧。 该技术利用像素数据编码来存储网站的 HTML，但评论者指出，使用 SVG 图标或 PNG 注释块（tEXt、zTXt、iTXt）可以更直接地存储数据。

---

<a id="item-10"></a>
### *（简报）* [MCP 的关键优势：将认证流程隔离在智能体上下文之外](https://simonwillison.net/2026/Jun/19/sean-lynch/#atom-everything) ⭐️ 7.0/10

Sean Lynch 指出，模型上下文协议（MCP）相比传统技能或 CLI 工具具有独特优势：它将认证流程隔离在智能体的上下文窗口之外，甚至可能充当专门的认证网关。 这一见解凸显了 MCP 在安全性和架构上的实际优势，通过将认证与智能体的推理循环解耦，可以减少上下文窗口污染并提升安全性，从而简化智能体工具的开发。 Lynch 提出，MCP 的理想形态可能仅仅是 API 的认证网关，仅此一点就已足够有价值。这与技能/CLI 方法形成对比，后者中认证流程常常占用宝贵的上下文窗口空间。

---

<a id="item-11"></a>
### *（简报）* [免费工作坊：零数学基础教你从零构建大语言模型](https://www.reddit.com/r/MachineLearning/comments/1uazlnd/hi_reddit_i_posted_my_build_your_own_llm_workshop/) ⭐️ 7.0/10

Justin Angel 在 YouTube 上发布了一个全面的工作坊视频，教授如何从零开始构建大语言模型（LLM），涵盖机器学习基础、Transformer 架构和训练技术，且无需数学或机器学习先修知识。 该资源填补了学习者深入理解 LLM 但缺乏高等数学背景的关键空白，使前沿 AI 开发更加平易近人。它涵盖了从感知机到强化学习的完整流程，通过代码和 Excel 示例实现动手学习。 工作坊包含分词器（BPE、SentencePiece）、嵌入（RoPE）、注意力机制（MHA、GQA、MLA）以及指令微调和强化学习等训练技术。它使用幻灯片、手动 Excel 练习和代码示例，除了熟悉代码和 Excel 外无需数学基础。

---

<a id="item-12"></a>
### *（简报）* [机器学习博士生没有顶会论文能否毕业？](https://www.reddit.com/r/MachineLearning/comments/1uazlhg/would_you_let_an_ml_phd_student_graduate_without/) ⭐️ 7.0/10

一位 Reddit 用户提出了一个假设性问题：如果一名机器学习博士生工作扎实、论文方向连贯，但没有在 NeurIPS、ICML、ICLR 或 CVPR 等顶级会议上发表过论文，只有三篇第一作者的 A 级论文，导师是否应该支持其毕业。 这场辩论凸显了机器学习博士项目中基于发表论文的指标与研究内在质量之间的张力，影响毕业政策、学生心理健康以及学术评价的未来。 该学生有三篇第一作者论文发表在“A 级”会议（非顶级），论文本身扎实，但缺乏最负盛名的机器学习会议论文。问题在于论文本身是否足以作为毕业依据。

---

<a id="item-13"></a>
### *（简报）* [全球 PM2.5 预测机器学习模型解决方差陷阱](https://www.reddit.com/r/MachineLearning/comments/1uar4vc/built_a_global_aq_pm25_forecaster_ml_model_p/) ⭐️ 7.0/10

一位实践者构建了一个端到端的 PM2.5 预测管道，覆盖美国、英国、印度和澳大利亚四个国家，使用了超过 160 万行 OpenAQ 和 NASA 气象数据。该模型采用水平对齐架构，解耦预测时间范围，并利用自回归滞后和波动矩阵克服方差陷阱，在全球范围内实现了 MASE 低于 1.0。 这项工作解决了时间序列预测中的一个常见陷阱——方差陷阱，即模型在高方差环境中失效的问题。水平对齐架构提供了一种实用的解决方案，可应用于其他波动性预测领域，提高在混乱条件下的可靠性。 该模型使用 scikit-learn 的梯度提升回归器，并计划迁移到 XGBoost 或 LightGBM。管道部署在 Vercel 上，前端使用 Next.js，代码已在 GitHub 上公开。

---

