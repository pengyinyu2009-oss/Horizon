---
layout: default
title: "Horizon Daily: 2026-06-20 (ZH)"
date: 2026-06-20
lang: zh
period: daily
period_id: 2026-06-20
---

> 从 17 条内容中筛选出 8 条重要资讯。

其中 **3 条 8 分以上**展开详细简报，其余 5 条仅列于索引。

---

1. [GPT-5.5 幻觉率是 MIT 许可的 GLM-5.2 的三倍](#item-1) ⭐️ 8.0/10
2. [时间序列建模需要动力系统视角](#item-2) ⭐️ 8.0/10
3. [开源手册详解大规模 LLM 推理：GPU 内部机制与主流框架](#item-3) ⭐️ 8.0/10
4. [CSSQuake：用 CSS 渲染经典游戏《雷神之锤》](#item-4) ⭐️ 7.0/10
5. [开发者将整个网站存储在一个网站图标中](#item-5) ⭐️ 7.0/10
6. [屏幕无法显示的颜色在哪里](#item-6) ⭐️ 7.0/10
7. [DVD-JEPA：开源可复现的 JEPA 世界模型](#item-7) ⭐️ 7.0/10
8. [全球 PM2.5 预测模型：采用水平对齐架构](#item-8) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [GPT-5.5 幻觉率是 MIT 许可的 GLM-5.2 的三倍](https://arrowtsx.dev/bigger-models/) ⭐️ 8.0/10

一篇博客文章声称 GPT-5.5 的幻觉率是 MIT 许可的开源模型 GLM-5.2 的三倍，挑战了更大模型减少幻觉的假设。 这一说法引发了关于扩大模型规模是否会导致收益递减甚至幻觉增加的辩论，这对人工智能开发和部署的未来方向至关重要。 该比较基于幻觉率分数，但解释起来很棘手，因为它们是模型不知道答案的条件概率。GLM-5.2 是一个纯开源模型，采用 MIT 许可，并拥有 100 万 token 的上下文窗口。

hackernews · oshrimpton · 6月19日 16:11 · [社区讨论](https://news.ycombinator.com/item?id=48600167)

**背景**: 大型语言模型中的幻觉是指生成听起来合理但事实不正确的输出。规模假设认为，拥有更多数据和参数的更大模型应该表现更好，但这篇文章表明，超过某个点后，幻觉可能会增加。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/zai-org/GLM-5">GLM-5.2 & GLM-5.1 & GLM-5 - GitHub</a></li>
<li><a href="https://openlm.ai/glm-5.2/">GLM-5.2 - openlm.ai</a></li>
<li><a href="https://venturebeat.com/technology/z-ais-open-weights-glm-5-2-beats-gpt-5-5-on-multiple-long-horizon-coding-benchmarks-for-1-6th-the-cost">Z.ai's open-weights GLM-5.2 beats GPT-5.5 on multiple ... - VentureBeat</a></li>

</ul>
</details>

**社区讨论**: 社区评论质疑这一说法，指出幻觉率总体上逐年下降。一些人认为 RLVR（基于可验证奖励的强化学习）可以针对幻觉，另一些人指出幻觉率分数是有条件的，可能无法反映日常使用情况。

**标签**: `#LLM`, `#hallucination`, `#scaling`, `#open-source`, `#AI research`

---

<a id="item-2"></a>
## [时间序列建模需要动力系统视角](https://www.reddit.com/r/MachineLearning/comments/1uark0u/time_series_modeling_needs_a_dynamical_systems/) ⭐️ 8.0/10

一篇 ICML 2026 立场论文主张时间序列建模应采用动力系统视角，提出了五项具体建议，包括广义教师强制、在动力系统模拟上预训练以及回归现代 RNN。 这一范式转变可能实现域外泛化和长期预测，解决当前时间序列模型（尤其是基础模型）的根本局限性。 论文指出 Transformer 会丢失关键的动力学信息，并建议使用广义教师强制来减少参数负载。它还强调拓扑变化是时间序列预测中最困难的问题。

reddit · r/MachineLearning · /u/DangerousFunny1371 · 6月20日 08:47

**背景**: 动力系统重建（DSR）从时间序列数据中推断底层动力过程的生成模型。广义教师强制是一种在混沌动力学学习中稳定梯度的训练技术。当前的时间序列基础模型通常无法捕捉长期统计特性。

**社区讨论**: Reddit 讨论中包含实质性评论，有人同意 Transformer 对时间序列并非最优，也有人质疑动力系统方法在处理真实噪声数据时的实用性。

**标签**: `#time series`, `#dynamical systems`, `#machine learning`, `#ICML`, `#foundation models`

---

<a id="item-3"></a>
## [开源手册详解大规模 LLM 推理：GPU 内部机制与主流框架](https://www.reddit.com/r/MachineLearning/comments/1uavduv/an_open_handbook_on_llm_inference_at_scale_gpu/) ⭐️ 8.0/10

一本关于大规模 LLM 推理的开源手册（仍在编写中）已发布，内容涵盖 GPU 执行与内存内部机制、KV 缓存、批处理以及 vLLM、SGLang 和 TensorRT-LLM 等生产级框架。 该资源罕见地深入剖析了 LLM 推理的系统级瓶颈，对于优化部署成本和延迟的工程师至关重要。作者积极征求社区反馈，确保手册能随着实际生产经验不断演进。 该手册包含用于架构可视化的 mermaid 图表，重点解释了推理过程中 GPU 为何大部分时间空闲，以及内存层次结构如何限制吞吐量。项目托管在 GitHub（github.com/harshuljain13/llm-inference-at-scale），欢迎提交问题和拉取请求。

reddit · r/MachineLearning · /u/YouFirst295 · 6月20日 12:27

**背景**: 大规模 LLM 推理是指以低延迟和高吞吐量为众多用户提供大语言模型服务。关键概念包括 KV 缓存（存储中间注意力键值以避免重复计算）、批处理（将多个请求分组以提高 GPU 利用率）以及专用框架如 vLLM（使用 PagedAttention 实现高效内存管理）和 TensorRT-LLM（NVIDIA 的优化工具包）。理解 GPU 内存层次结构和执行模式对于识别瓶颈至关重要。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://developer.nvidia.com/blog/mastering-llm-techniques-inference-optimization/">Mastering LLM Techniques: Inference Optimization | NVIDIA Technical...</a></li>
<li><a href="https://github.com/vllm-project/vllm">GitHub - vllm-project/vllm: A high-throughput and memory-efficient inference and serving engine for LLMs · GitHub</a></li>
<li><a href="https://github.com/NVIDIA/TensorRT-LLM">GitHub - NVIDIA/TensorRT-LLM: TensorRT LLM provides users ...</a></li>

</ul>
</details>

**标签**: `#LLM inference`, `#GPU internals`, `#machine learning`, `#systems`, `#open source`

---

<a id="item-4"></a>
### *（简报）* [CSSQuake：用 CSS 渲染经典游戏《雷神之锤》](https://cssquake.com/) ⭐️ 7.0/10

CSSQuake 完全重现了原版《雷神之锤》的游戏引擎，使用 CSS 而非传统图形 API 进行 3D 渲染。它在网页浏览器中运行，展示了 CSS 可用于复杂的实时 3D 图形。 该项目突破了 CSS 的能力边界，展现了令人印象深刻的技术创意。它还引发了关于 Web 技术演进及其在游戏开发中潜力的讨论。 尽管使用 CSS 进行渲染，CSSQuake 仍然需要 JavaScript 来处理游戏逻辑，并且在现代硬件上运行速度比原版《雷神之锤》慢。部分游戏元素的行为与原版不同，例如按钮和秘密门的触发方式。

---

<a id="item-5"></a>
### *（简报）* [开发者将整个网站存储在一个网站图标中](https://www.timwehrle.de/blog/i-stored-a-website-in-a-favicon/) ⭐️ 7.0/10

一位开发者展示了一种技术，通过将网站数据编码到 16x16 像素的 PNG 网站图标中，并利用一个微小的引导加载程序来解码和渲染内容，从而将整个网站存储在一个网站图标图像中。 这一创意黑客技术展示了 Web 开发中的替代数据存储方法，引发了关于浏览器指纹识别等安全风险以及使用 SVG 或多格式文件进行改进的讨论。 该技术需要一个引导加载程序来解码图像，但评论者指出，使用 HTML/PNG 多格式文件可以消除这一需求。此外，PNG 注释块（tEXt、zTXt、iTXt）提供了一种更简单的方法来嵌入数据，无需像素编码。

---

<a id="item-6"></a>
### *（简报）* [屏幕无法显示的颜色在哪里](https://moultano.wordpress.com/2026/06/19/where-to-find-the-colors-your-screen-cant-show-you/) ⭐️ 7.0/10

文章探讨了超出 sRGB 色域的颜色，特别是饱和的蓝绿色和红色，并解释了屏幕为何无法显示这些颜色。 这很重要，因为它揭示了当前显示技术的根本局限，影响了数字艺术、摄影和色彩关键工作等领域。 文章使用 CIE 1931 色度图来说明 sRGB 三角形，并显示许多可见颜色（尤其是蓝绿色区域）位于其外。

---

<a id="item-7"></a>
### *（简报）* [DVD-JEPA：开源可复现的 JEPA 世界模型](https://www.reddit.com/r/MachineLearning/comments/1uatlzx/dvdjepa_an_opensource_fullyreproducible_jepa/) ⭐️ 7.0/10

DVD-JEPA 是 Yann LeCun 提出的联合嵌入预测架构（JEPA）的最小化、完全可复现的开源实现，在 16×16 网格中弹跳的 DVD 标志上训练。它展示了 JEPA 世界模型无需像素级预测即可学习潜在表征，通过线性探针实现 0.73 像素的位置恢复，并实现 88 倍异常检测信号。 这项工作为 JEPA 提供了一个简单易懂的概念验证，JEPA 是 LeCun 自主机器智能愿景的关键组成部分。通过使架构完全可复现并可在浏览器中运行，它降低了研究人员和开发者实验世界模型和自监督表征学习的门槛。 该模型使用上下文编码器、EMA 目标编码器和潜在预测器，在 32 维表征空间中预测未来观测，训练时不使用解码器。在冻结的潜在向量上进行线性探针，可将标志的 (x,y) 位置恢复至 0.73 像素以内；结合解码器向前滚动预测器，可在约 20 步内正确渲染弹跳动力学，之后出现潜在漂移。

---

<a id="item-8"></a>
### *（简报）* [全球 PM2.5 预测模型：采用水平对齐架构](https://www.reddit.com/r/MachineLearning/comments/1uar4vc/built_a_global_aq_pm25_forecaster_ml_model_p/) ⭐️ 7.0/10

一位实践者构建了一个端到端的 PM2.5 预测管道，覆盖四个国家（美国、英国、印度、澳大利亚），使用了超过 160 万行 OpenAQ 和 NASA 气象数据。关键创新在于采用水平对齐架构，将预测水平解耦以克服方差陷阱，使全局 MASE 低于 1.0。 这项工作解决了时间序列预测中常见的陷阱——方差陷阱，即在混乱环境中朴素预测优于 ML 模型。水平对齐方法提供了一种实用解决方案，可应用于其他波动性预测任务，有望改善空气质量预警和公共卫生响应。 该模型使用 scikit-learn 的无状态梯度提升回归器，具有严格的自回归滞后向量，针对特定水平（h=1、7、14、30）对齐，并包含一个 3 天滚动波动矩阵以防止数据泄漏。在 30 天水平上，它相对于混乱的热力学基线保持了 57%的预测准确率。

---

