---
layout: default
title: "Horizon Daily: 2026-06-21 (ZH)"
date: 2026-06-21
lang: zh
period: daily
period_id: 2026-06-21
---

> 从 21 条内容中筛选出 11 条重要资讯。

其中 **8 条 8 分以上**展开详细简报，其余 3 条仅列于索引。

---

1. [开发者不理解 CORS（2019）](#item-1) ⭐️ 8.0/10
2. [Loupe iOS 应用揭示原生应用数据访问情况](#item-2) ⭐️ 8.0/10
3. [Epoll 与 io_uring 对比：深入解析 Linux I/O 性能](#item-3) ⭐️ 8.0/10
4. [慢呼吸调节大脑功能与风险行为](#item-4) ⭐️ 8.0/10
5. [SMPTE 免费开放其标准库](#item-5) ⭐️ 8.0/10
6. [DVD-JEPA：开源 JEPA 世界模型，线性探针精准定位](#item-6) ⭐️ 8.0/10
7. [大规模 LLM 推理开源手册发布](#item-7) ⭐️ 8.0/10
8. [minFLUX：FLUX 扩散模型的精简 PyTorch 实现](#item-8) ⭐️ 8.0/10
9. [Google IPv6 流量占比突破 50%](#item-9) ⭐️ 7.0/10
10. [免费工作坊教你从零构建 LLM，代码与 Excel 结合教学](#item-10) ⭐️ 7.0/10
11. [ML 博士生没有顶会论文能否毕业？](#item-11) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [开发者不理解 CORS（2019）](https://fosterelli.co/developers-dont-understand-cors) ⭐️ 8.0/10

一篇文章指出大多数开发者从根本上误解了 CORS，而评论区本身通过广泛的困惑和错误断言证明了这一点。 这很重要，因为 CORS 是一个关键的 Web 安全机制，广泛的误解会导致不安全的应用程序和浪费调试时间。 文章强调 CORS 并不限制哪些网站可以发送请求，它只控制浏览器是否可以读取响应。许多评论者错误地认为 CORS 会阻止来自其他来源的请求。

hackernews · toilet · 6月21日 01:35 · [社区讨论](https://news.ycombinator.com/item?id=48614844)

**背景**: CORS（跨源资源共享）是一种浏览器机制，允许对位于给定域之外的资源进行受控访问。它扩展了同源策略（SOP），后者默认阻止网页向不同源发起请求。CORS 使用 HTTP 头让服务器指定哪些源被允许读取响应。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS">Cross-Origin Resource Sharing ( CORS ) - HTTP | MDN</a></li>
<li><a href="https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request">Preflight request - Glossary | MDN</a></li>

</ul>
</details>

**社区讨论**: 评论区争议很大，许多用户误解了 CORS，验证了文章的论点。一些评论者指出文章本身也存在不准确之处，而另一些人则推荐 MDN 文档以获得正确理解。

**标签**: `#CORS`, `#web security`, `#developer education`, `#HTTP`, `#browser security`

---

<a id="item-2"></a>
## [Loupe iOS 应用揭示原生应用数据访问情况](https://github.com/mysk-research/loupe) ⭐️ 8.0/10

Loupe 是由 mysk-research 开发的一款 iOS 应用，它揭示了原生应用可以访问哪些数据，包括已安装应用探测和卷创建日期。 该工具凸显了 iOS 用户面临的重大隐私风险，表明即使是原生应用也能访问已安装应用列表和卷创建日期等敏感信息，这些信息可用于指纹识别和用户画像。 Loupe 展示了 iOS 应用可以通过 LSApplicationQueriesSchemes 探测已安装应用，并访问卷创建日期，从而揭示设备首次设置或最后一次擦除的时间。

hackernews · Cider9986 · 6月20日 12:08 · [社区讨论](https://news.ycombinator.com/item?id=48608645)

**背景**: iOS 应用在沙盒环境中运行，但仍可通过 API 访问某些系统信息。苹果已实施限制以防止应用列出所有已安装应用，但应用仍可通过 URL 方案查询特定应用。卷创建日期是文件系统的一个属性，应用可以访问它，从而可能泄露设备使用历史。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.hawkdive.com/ios-app-privacy-snooping-fix-guide/">iOS App Privacy Snooping: How to See What Apps Access - Hawkdive</a></li>
<li><a href="https://developer.apple.com/documentation/foundation/urlresourcevalues/volumecreationdate?language=_2">volumeCreationDate | Apple Developer Documentation</a></li>

</ul>
</details>

**社区讨论**: 评论者对卷创建日期泄露和探测已安装应用的能力表示担忧，有人建议进行操作系统级别的修复。一位评论者指出，iOS 已经将应用探测限制为特定方案，但卷创建日期仍然是一个隐私问题。

**标签**: `#iOS`, `#privacy`, `#security`, `#app permissions`, `#research`

---

<a id="item-3"></a>
## [Epoll 与 io_uring 对比：深入解析 Linux I/O 性能](https://sibexi.co/posts/epoll-vs-io_uring/) ⭐️ 8.0/10

一篇详细的技术文章对比了 Linux 中的两种 I/O 事件通知机制——epoll 和 io_uring，分析了它们在架构上的差异以及对 I/O 密集型应用的性能影响。 这一对比有助于开发者为高性能服务器选择正确的 I/O 模型，因为 io_uring 在现代工作负载下比 epoll 具有更低的开销和更好的可扩展性。 文章指出 io_uring 使用共享环形缓冲区来减少系统调用，而 epoll 依赖事件驱动的回调。io_uring 还支持缓冲区注册和 splice 操作等高级特性。

hackernews · Sibexico · 6月20日 23:07 · [社区讨论](https://news.ycombinator.com/item?id=48613872)

**背景**: epoll 是 Linux 2.5.44 引入的成熟 I/O 事件通知机制，广泛应用于 nginx 等高性能网络服务器。io_uring 是 Linux 5.1 引入的较新的异步 I/O 框架，旨在减少系统调用开销，并为文件和网络 I/O 提供更灵活的接口。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Io_uring">io_uring - Wikipedia</a></li>
<li><a href="https://github.com/axboe/liburing/issues/536">Yet another comparison between io_uring and epoll on network performance · Issue #536 · axboe/liburing</a></li>
<li><a href="https://www.alibabacloud.com/blog/io-uring-vs--epoll-which-is-better-in-network-programming_599544">io_uring vs. epoll – Which Is Better in Network Programming? - Alibaba Cloud Community</a></li>

</ul>
</details>

**社区讨论**: 评论者讨论了 CPU 绑定和 DPDK 等性能优化技术，有人指出 io_uring 在某些场景下可以超越 epoll，但需要仔细调优。其他人分享了在 Rust 和 C 项目中使用 io_uring 的经验，强调了其在零拷贝网络方面的潜力。

**标签**: `#Linux`, `#I/O`, `#epoll`, `#io_uring`, `#performance`

---

<a id="item-4"></a>
## [慢呼吸调节大脑功能与风险行为](https://www.cell.com/neuron/fulltext/S0896-6273(26)00339-9) ⭐️ 8.0/10

《神经元》期刊发表的一项新研究揭示，慢呼吸（尤其是延长呼气）通过副交感神经激活调节大脑功能，并增加冒险行为。 这一发现将呼吸技巧与奖赏处理和风险行为直接联系起来，为通过调节自主神经系统失衡来治疗焦虑、恐慌症和抑郁症提供了潜在可能。 研究特别发现，延长呼气可增强心脏副交感神经调节，并选择性地影响奖赏反应性，这或许解释了慢呼吸为何会增加冒险行为。

hackernews · croes · 6月20日 22:22 · [社区讨论](https://news.ycombinator.com/item?id=48613555)

**背景**: 副交感神经系统负责“休息与消化”活动，对抗“战斗或逃跑”的交感反应。慢呼吸技巧（尤其是延长呼气）已知可通过迷走神经激活副交感神经系统，促进放松。该研究提供了将这种呼吸与风险行为改变联系起来的神经机制。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Parasympathetic_nervous_system">Parasympathetic nervous system - Wikipedia</a></li>
<li><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC10395759/">Slow breathing for reducing stress: The effect of extending exhale - PMC</a></li>
<li><a href="https://www.psychologytoday.com/us/blog/the-athletes-way/201905/longer-exhalations-are-an-easy-way-to-hack-your-vagus-nerve">Longer Exhalations Are an Easy Way to Hack Your Vagus Nerve | Psychology Today</a></li>

</ul>
</details>

**社区讨论**: 社区评论强调了实际应用：慢呼吸通过将谨慎转为自信来帮助新手公开演讲，用户还分享了用协调呼吸缓解焦虑的个人经验。有人对副交感神经激活增加冒险行为表示惊讶，也有人指出这与临床情境的相关性。

**标签**: `#neuroscience`, `#breathing`, `#mental health`, `#risk behavior`, `#autonomic nervous system`

---

<a id="item-5"></a>
## [SMPTE 免费开放其标准库](https://www.smpte.org/blog/smpte-makes-its-standards-freely-accessible-openingstandards-library-to-the-global-media-technology-community) ⭐️ 8.0/10

SMPTE 宣布其全部标准目录（包括所有已发布的标准、推荐实践、工程指南和注册披露文档）现已向全球媒体技术社区免费开放，未来发布的标准也将包含在内。 SMPTE 标准支撑着时间码、帧率等关键媒体技术；取消付费门槛降低了开发者、研究人员和初创企业的障碍，促进创新和互操作性。这符合行业向开放标准发展的趋势。 免费访问涵盖所有已发布的 SMPTE 标准、推荐实践、工程指南和注册披露文档（RDD），以及所有未来版本。SMPTE 还通过采用 GitHub 工作流、结构化 HTML 编写和集成发布管道来现代化其开发流程。

hackernews · zdw · 6月20日 17:01 · [社区讨论](https://news.ycombinator.com/item?id=48610827)

**背景**: SMPTE（电影与电视工程师协会）一个多世纪以来一直制定媒体技术标准，包括广泛使用的 SMPTE 时间码和 24 fps 电影帧率。此前，获取这些标准需要购买单个文档，成本较高。此次变更使它们免费向所有人开放。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.smpte.org/blog/smpte-makes-its-standards-freely-accessible-openingstandards-library-to-the-global-media-technology-community">SMPTE Makes Its Standards Freely Accessible, Opening Standards Library to the Global Media Technology Community</a></li>
<li><a href="https://www.tvtechnology.com/standards/smpte-makes-its-standards-freely-accessible-to-the-global-media-technology-community">SMPTE Makes Its Standards Freely Accessible to the Global Media Technology Community | TV Tech</a></li>
<li><a href="https://en.wikipedia.org/wiki/Society_of_Motion_Picture_and_Television_Engineers">Society of Motion Picture and Television Engineers - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 社区评论普遍持积极态度，许多人称赞此举早该实施。有人将其与 IETF 免费标准的成功相提并论，也有人指出一些国家的法律要求强制标准必须免费提供。少数评论者强调了 SMPTE 的现代化努力，如采用 GitHub 工作流。

**标签**: `#standards`, `#media technology`, `#open access`, `#SMPTE`

---

<a id="item-6"></a>
## [DVD-JEPA：开源 JEPA 世界模型，线性探针精准定位](https://www.reddit.com/r/MachineLearning/comments/1uatlzx/dvdjepa_an_opensource_fullyreproducible_jepa/) ⭐️ 8.0/10

DVD-JEPA 是一个最小化、完全可复现的开源联合嵌入预测架构（JEPA）实现，它学习预测 16×16 网格中弹跳 DVD 标志的表征，通过线性探针实现 0.73 像素内的位置恢复。 这项工作清晰、诚实地展示了 JEPA 的核心思想——预测表征而非像素——并展示了其在异常检测中的实际效用，使该架构更易于研究和教育。 该模型使用上下文编码器、EMA 目标编码器和潜在预测器，无需标签或解码器进行训练。它还可以通过添加解码器并向前滚动预测器来“做梦”，在潜在漂移发生前生成约 20 步的正确未来帧。

reddit · r/MachineLearning · /u/NielsRogge · 6月20日 10:52

**背景**: JEPA（联合嵌入预测架构）由 Yann LeCun 于 2022 年提出，是一种自监督学习方法，它预测未来观测的表征而非原始像素，从而避免了预测不可预测的像素级细节的困难。EMA（指数移动平均）目标编码器通过提供稳定、缓慢更新的目标来防止表征崩溃。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2301.08243">[2301.08243] Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture</a></li>
<li><a href="https://ai.meta.com/blog/yann-lecun-ai-model-i-jepa/">I-JEPA: The first AI model based on Yann LeCun’s vision for more human-like AI</a></li>
<li><a href="https://www.emergentmind.com/topics/linear-probes">Linear Probes: Neural Network Diagnostics</a></li>

</ul>
</details>

**社区讨论**: Reddit 社区称赞该项目清晰且可复现，一些人认为它是理解 JEPA 的极佳教育工具。部分评论者讨论了线性探针结果和异常检测应用，并表示有兴趣将该方法扩展到更复杂的环境。

**标签**: `#world model`, `#JEPA`, `#representation learning`, `#self-supervised learning`, `#video prediction`

---

<a id="item-7"></a>
## [大规模 LLM 推理开源手册发布](https://www.reddit.com/r/MachineLearning/comments/1uavduv/an_open_handbook_on_llm_inference_at_scale_gpu/) ⭐️ 8.0/10

一本关于大规模 LLM 推理的开源手册（仍在完善中）已发布，内容涵盖 GPU 内存层次结构、KV 缓存、批处理以及 vLLM、SGLang 和 TensorRT-LLM 等生产框架。作者最近新增了一章关于 GPU 执行和内存内部机制的章节，并附有 mermaid 图表。 该手册填补了生产级 LLM 推理方面实用、易懂文档的空白，随着模型规模不断扩大，这一领域至关重要。它帮助工程师理解 GPU 空闲时间和内存层次结构等瓶颈，从而实现更高效的部署。 该手册是一个个人学习项目，托管在 GitHub 上，积极寻求社区反馈和贡献。它包含用于架构可视化的 mermaid 图表，并涵盖 KV 缓存优化和连续批处理等主题。

reddit · r/MachineLearning · /u/YouFirst295 · 6月20日 12:27

**背景**: 大规模 LLM 推理涉及高效服务大型语言模型，需要优化 GPU 内存使用、请求批处理和 KV 缓存管理。vLLM 和 TensorRT-LLM 等框架为这些任务提供了专门的实现。GPU 内存层次结构（HBM、L2 缓存、SRAM）显著影响吞吐量和延迟。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.youngju.dev/blog/gpu-cuda/2026-03-17-gpu-memory-inference-optimization-guide.en">GPU Memory Management & LLM Inference Optimization: vLLM ...</a></li>
<li><a href="https://huggingface.co/blog/not-lain/kv-caching">KV Caching Explained: Optimizing Transformer Inference Efficiency</a></li>
<li><a href="https://northflank.com/blog/vllm-vs-tensorrt-llm-and-how-to-run-them">vLLM vs TensorRT-LLM: Key differences, performance, and how ...</a></li>

</ul>
</details>

**社区讨论**: Reddit 讨论中包含了来自从业者的实质性技术评论，一些人称赞手册的解释清晰，并建议增加量化、推测解码等主题。总体情绪积极，社区对开放协作的方式表示赞赏。

**标签**: `#LLM inference`, `#GPU internals`, `#vLLM`, `#TensorRT-LLM`, `#machine learning`

---

<a id="item-8"></a>
## [minFLUX：FLUX 扩散模型的精简 PyTorch 实现](https://www.reddit.com/r/MachineLearning/comments/1ub1db3/studying_flux_in_diffusers_library_was_hard_so_i/) ⭐️ 8.0/10

一位开发者发布了 minFLUX，这是一个精简的开源 PyTorch 实现，涵盖了 FLUX.1 和 FLUX.2 扩散模型，并提供了与 HuggingFace diffusers 的逐行映射，包含训练和推理循环。 该项目降低了 FLUX 扩散模型的学习和实验门槛，简化了官方 diffusers 库的复杂性，使研究人员和爱好者能够理解其核心架构和数学原理。 minFLUX 包含 FLUX.1 和 FLUX.2 的精简实现，包括 VAE 和 Transformer 模型，通过流匹配（flow matching）和速度均方误差（velocity MSE）进行训练，并使用欧拉 ODE 求解器进行推理。它还突出了 FLUX.1 与 FLUX.2 之间的架构差异，例如改进的 Transformer 块和调制方式。

reddit · r/MachineLearning · /u/Other-Eye-8152 · 6月20日 16:50

**背景**: FLUX 是由 Black Forest Labs 开发的一系列基于扩散的文本到图像模型。官方的 HuggingFace diffusers 库提供了实现，但通常复杂且抽象，难以学习。流匹配（flow matching）是一种训练目标，通过学习速度场将噪声转换为数据；欧拉 ODE 求解器是一种简单的数值方法，用于在推理过程中求解微分方程。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Flux_(text-to-image_model)">Flux (text-to-image model) - Wikipedia</a></li>
<li><a href="https://arxiv.org/abs/2507.09595">[2507.09595] Demystifying Flux Architecture - arXiv.org</a></li>
<li><a href="https://arxiv.org/abs/2506.02070">An Introduction to Flow Matching and Diffusion Models</a></li>

</ul>
</details>

**社区讨论**: Reddit 社区反响积极，用户赞赏其教育价值和清晰的映射关系。一些人表示有兴趣贡献代码或使用该项目进行学习。

**标签**: `#diffusion models`, `#FLUX`, `#PyTorch`, `#open-source`, `#machine learning`

---

<a id="item-9"></a>
### *（简报）* [Google IPv6 流量占比突破 50%](https://blog.apnic.net/2026/04/28/google-hits-50-ipv6/) ⭐️ 7.0/10

Google 报告称，其 50% 的用户现在通过 IPv6 访问服务，这是互联网协议采用的一个重要里程碑。 这一里程碑表明 IPv6 的采用正在加速，这对于克服 IPv4 地址枯竭和支持不断增长的联网设备数量至关重要。 各国采用率差异显著，法国达到 85%，而荷兰的 T-Mobile/Odido 等 ISP 仍不支持 IPv6。Cloudflare 观察到超过 40% 的 IPv6 流量，但客户端采用率可能无法反映服务器端的使用情况。

---

<a id="item-10"></a>
### *（简报）* [免费工作坊教你从零构建 LLM，代码与 Excel 结合教学](https://www.reddit.com/r/MachineLearning/comments/1uazlnd/hi_reddit_i_posted_my_build_your_own_llm_workshop/) ⭐️ 7.0/10

Justin Angel 在 YouTube 上发布了名为“Build Your Own LLM”的录播工作坊，内容涵盖机器学习基础、Transformer 架构和训练技术，配有幻灯片、Excel 示例和代码。该工作坊无需数学或机器学习先修知识，只需能通过代码和 Excel 学习即可。 该资源填补了学习者想要深入理解 LLM 但缺乏高等数学背景的空白。通过结合直观的 Excel 练习和实用的 PyTorch 代码，它让注意力机制、反向传播等复杂概念对更广泛的受众变得可理解。 工作坊涵盖的主题包括 SwiGLU 激活函数、带内核融合的 torch.compile、门控残差连接以及多种归一化技术。还包括分词（BPE、SentencePiece）、位置编码（RoPE）和多查询注意力（MQA）等章节。

---

<a id="item-11"></a>
### *（简报）* [ML 博士生没有顶会论文能否毕业？](https://www.reddit.com/r/MachineLearning/comments/1uazlhg/would_you_let_an_ml_phd_student_graduate_without/) ⭐️ 7.0/10

一位 Reddit 用户提出了一个假设场景：一名机器学习博士生在学四年，有扎实的论文和 3 篇第一作者 A 级会议论文，但没有在 NeurIPS、ICML、ICLR 或 CVPR 等顶级会议上发表过文章。问题在于导师是否会支持其毕业。 这场辩论凸显了机器学习学术界在发表指标与真实研究质量之间的张力。它影响着博士项目如何评估学生，并可能改变毕业标准，尤其是在顶级会议竞争日益激烈的背景下。 该学生有 3 篇第一作者 A 级论文，这些论文被认为扎实但非顶级。论文本身被描述为连贯且扎实。该场景特意排除了任何顶级会议发表，以聚焦讨论非顶级工作是否足以毕业。

---

