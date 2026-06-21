---
layout: default
title: "Horizon Daily: 2026-06-21 (ZH)"
date: 2026-06-21
lang: zh
period: daily
period_id: 2026-06-21
---

> 从 24 条内容中筛选出 13 条重要资讯。

其中 **9 条 8 分以上**展开详细简报，其余 4 条仅列于索引。

---

1. [开发者不理解 CORS：2019 年分析](#item-1) ⭐️ 8.0/10
2. [Loupe iOS 应用揭示原生应用可访问的隐藏数据](#item-2) ⭐️ 8.0/10
3. [Epoll 与 io_uring：Linux I/O 性能深度对比](#item-3) ⭐️ 8.0/10
4. [SMPTE 向公众免费开放全部标准库](#item-4) ⭐️ 8.0/10
5. [开发者拒绝虽能运行但缺乏可维护性的 AI 代码](#item-5) ⭐️ 8.0/10
6. [没有顶级论文的机器学习博士：该毕业吗？](#item-6) ⭐️ 8.0/10
7. [ICML 2026 论文：时间序列建模需要动力系统视角](#item-7) ⭐️ 8.0/10
8. [大规模 LLM 推理开源手册：GPU 内部机制、KV 缓存、批处理及 vLLM/SGLang/TensorRT-LLM](#item-8) ⭐️ 8.0/10
9. [minFLUX：FLUX 扩散模型的精简 PyTorch 实现](#item-9) ⭐️ 8.0/10
10. [慢呼吸调节大脑功能与冒险行为](#item-10) ⭐️ 7.0/10
11. [免费工作坊教你从零构建大语言模型](#item-11) ⭐️ 7.0/10
12. [DVD-JEPA：最小化开源 JEPA 世界模型](#item-12) ⭐️ 7.0/10
13. [机器学习实践者构建全球 PM2.5 预测模型，采用创新架构](#item-13) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [开发者不理解 CORS：2019 年分析](https://fosterelli.co/developers-dont-understand-cors) ⭐️ 8.0/10

Chris Foster 在 2019 年发表的一篇文章指出，许多开发者误解了 CORS，并以 Zoom 本地服务器的一个真实漏洞作为案例研究。文章强调，Zoom 的错误配置允许任何网站与其本地客户端通信，使用户面临潜在攻击。 这很重要，因为 CORS 是基本的 Web 安全机制，但普遍的误解导致了危险的错误配置。Zoom 案例展示了现实世界的影响，而文章的高参与度表明，开发者亟需更好的 CORS 和威胁模型教育。 文章解释，CORS 是一种基于浏览器的机制，它不阻止请求发送，只限制 JavaScript 对响应的访问。Zoom 漏洞涉及一个缺少正确 CORS 头的本地 Web 服务器，允许任何网站读取 Zoom 客户端的响应。

hackernews · toilet · 6月21日 01:35 · [社区讨论](https://news.ycombinator.com/item?id=48614844)

**背景**: CORS（跨源资源共享）是一种安全特性，控制一个源的网页如何请求另一个源的资源。它依赖于像 Access-Control-Allow-Origin 这样的 HTTP 头。一个常见的误解是 CORS 完全阻止跨源请求；实际上，它只阻止请求脚本读取响应，除非服务器明确允许。Zoom 漏洞的发生是因为 Zoom 本地客户端运行了一个没有 CORS 限制的本地服务器，从而允许跨源攻击。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://fosterelli.co/developers-dont-understand-cors">Developers don't understand CORS - Chris Foster</a></li>
<li><a href="https://www.bomberbot.com/cors/exploiting-cors-misconfigurations-a-deep-dive-for-pentesters-and-developers/">Exploiting CORS Misconfigurations: A Deep Dive for Pentesters and Developers - Bomberbot</a></li>
<li><a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS">Cross-Origin Resource Sharing ( CORS ) - HTTP | MDN</a></li>

</ul>
</details>

**社区讨论**: 社区评论显示了对文章 CORS 描述的不同意见。一位评论者（muvlon）指出，文章错误地声称 CORS 限制哪些网站可以与服务器通信，而实际上 CORS 只限制 JavaScript 对响应的访问。其他人指出，许多开发者，尤其是后端开发者，因为日常工作中很少遇到 CORS 而难以理解，并建议参考 MDN 等资源以加深理解。

**标签**: `#CORS`, `#web security`, `#JavaScript`, `#API`, `#developer education`

---

<a id="item-2"></a>
## [Loupe iOS 应用揭示原生应用可访问的隐藏数据](https://github.com/mysk-research/loupe) ⭐️ 8.0/10

Loupe 是一款开源 iOS 应用，它展示了原生应用如何无需用户明确授权即可访问敏感设备信息，例如已安装的应用列表、卷创建日期和剪贴板变更计数。 这提高了人们对 iOS 中尚未广为人知的隐私漏洞的认识，强调即使没有权限提示，应用也能推断用户行为和设备历史，可能被用于指纹识别或跟踪。 该应用在 GitHub 上开源并附有演示视频。它揭示了诸如 iPhone 上次设置或擦除日期等用户难以伪造的数据，表明 iOS 的权限模型并未覆盖所有敏感数据。

hackernews · Cider9986 · 6月20日 12:08 · [社区讨论](https://news.ycombinator.com/item?id=48608645)

**背景**: iOS 应用运行在沙盒中，访问摄像头、麦克风或位置等受保护资源需要用户明确授权。然而，某些系统 API 无需权限即可使用，允许应用收集设备和用户行为的元数据。Loupe 揭示了这些漏洞。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://developer.apple.com/design/human-interface-guidelines/privacy">Privacy | Apple Developer Documentation</a></li>
<li><a href="https://developer.apple.com/documentation/uikit/requesting-access-to-protected-resources">Requesting access to protected resources - Apple Developer</a></li>
<li><a href="https://www.idownloadblog.com/2025/05/12/apple-ios-18-5-security-patches-vulnerabilities-privacy/">Update your iPhone : iOS 18.5 patches 30+ security vulnerabilities</a></li>

</ul>
</details>

**社区讨论**: 评论者对卷创建日期和剪贴板变更计数等具体数据点表示担忧，称其“过分”。一些人指出，虽然 iOS 在某些方面优于 Android，但这仍然构成隐私风险。其他人质疑用户实际能做什么，一位评论者建议唯一的选择是停止使用 iPhone。

**标签**: `#iOS`, `#privacy`, `#security`, `#mobile apps`

---

<a id="item-3"></a>
## [Epoll 与 io_uring：Linux I/O 性能深度对比](https://sibexi.co/posts/epoll-vs-io_uring/) ⭐️ 8.0/10

文章对 Linux 下 epoll 和 io_uring 两种异步 I/O 机制进行了详细的技术对比，分析了它们在性能和架构上的差异。 对于构建高性能网络服务的系统程序员来说，这一对比具有重要意义，因为 io_uring 在长期使用的 epoll 接口基础上提供了潜在的改进，尤其是在同时涉及网络和存储的工作负载中。 文章探讨了系统调用开销、内存共享和 CPU 绑定等性能权衡，并指出 io_uring 支持共享缓冲区和零拷贝操作，而 epoll 则更简单且部署更广泛。

hackernews · Sibexico · 6月20日 23:07 · [社区讨论](https://news.ycombinator.com/item?id=48613872)

**背景**: epoll 是 Linux 内核中用于可扩展 I/O 事件通知的系统调用，广泛应用于高性能网络服务器。io_uring 是 Linux 5.1 引入的较新的异步 I/O API，通过用户空间和内核空间之间的共享环形缓冲区来减少系统调用开销。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Io_uring">io_uring - Wikipedia</a></li>
<li><a href="https://man7.org/linux/man-pages/man7/io_uring.7.html">io_uring (7) - Linux manual page - man7.org</a></li>
<li><a href="https://dev.to/lordsnow/iouring-the-modern-asynchronous-io-revolution-in-linux-46ch">io_uring — The Modern Asynchronous I/O Revolution in Linux</a></li>

</ul>
</details>

**社区讨论**: 社区评论强调了 CPU 绑定和共享缓冲区等实际优化，并提到了 eBPF 和 mimalloc 等相关工具。一些用户指出 io_uring 尚不支持 sendfile，另一些用户则提到了用于 C++ 网络编程的 Boost.Asio。

**标签**: `#Linux`, `#I/O`, `#epoll`, `#io_uring`, `#systems programming`

---

<a id="item-4"></a>
## [SMPTE 向公众免费开放全部标准库](https://www.smpte.org/blog/smpte-makes-its-standards-freely-accessible-openingstandards-library-to-the-global-media-technology-community) ⭐️ 8.0/10

SMPTE 宣布，其包含 800 多项标准、推荐实践和工程指南的完整目录现已向全球媒体技术社区免费开放，包括所有未来发布的标准。 此举消除了获取关键技术标准的经济障碍，加速了媒体和娱乐行业的标准采用、互操作性和创新。 免费访问包括所有已发布的 SMPTE 标准、推荐实践、工程指南和注册披露文档（RDD），以及未来发布的内容。该组织还通过采用 GitHub 工作流和结构化 HTML 编写来现代化其开发流程。

hackernews · zdw · 6月20日 17:01 · [社区讨论](https://news.ycombinator.com/item?id=48610827)

**背景**: SMPTE（电影与电视工程师协会）是一个全球公认的标准组织，已制定了 800 多项运动影像和电视技术标准。此前，获取这些标准需要购买单个文档，成本高昂且阻碍了广泛采用。此举顺应了行业向开放标准发展的趋势，类似于 IETF 长期免费提供其标准的做法。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.smpte.org/setting-the-standards-free">Setting the Standards Free - smpte.org</a></li>
<li><a href="https://www.sportsvideo.org/2026/06/17/smpte-opens-entire-standards-library-to-public-at-no-cost/">SMPTE Opens Entire Standards Library to Public at No Cost</a></li>
<li><a href="https://www.tvtechnology.com/standards/smpte-makes-its-standards-freely-accessible-to-the-global-media-technology-community">SMPTE Makes Its Standards Freely Accessible to the Global Media Technology Community | TV Tech</a></li>

</ul>
</details>

**社区讨论**: 社区普遍对这一举措表示赞赏，评论强调了真正开放标准对创新的重要性，并将其与 IETF 免费标准的成功相提并论。一些人指出某些国家的法律要求对法律引用的标准提供免费访问，而另一些人则回忆起过去获取 SMPTE 文档的困难和成本。

**标签**: `#standards`, `#media technology`, `#open access`, `#SMPTE`, `#industry news`

---

<a id="item-5"></a>
## [开发者拒绝虽能运行但缺乏可维护性的 AI 代码](https://vinibrasil.com/when-i-reject-ai-code-even-if-it-works/) ⭐️ 8.0/10

这凸显了 AI 辅助生产力与传统代码质量标准之间日益紧张的关系，迫使开发者重新思考在 AI 驱动时代什么才是可接受的代码。 作者强调，AI 常常生成过于复杂的抽象或企业级模式，损害了可维护性，拒绝此类代码是软件工程的正常环节，类似于拒绝同事的代码。

hackernews · vnbrs · 6月21日 00:58 · [社区讨论](https://news.ycombinator.com/item?id=48614631)

**背景**: 像 GitHub Copilot 和 Cursor 这样的 AI 编程助手根据训练数据中的模式生成代码，往往倾向于冗长或复杂的解决方案。可维护性——代码被理解、修改和扩展的难易程度——是一个关键的软件工程原则，有时与 AI 提供的速度相冲突。

**社区讨论**: 评论者大多表示赞同，指出拒绝 AI 代码类似于拒绝同事的代码。一些人观察到，使用 AI 往往导致全有或全无的方法，没有中间地带，而部分理解代码是一个艰难的权衡。其他人则认为 AI 适合原型开发，但不适合真正重要的生产代码。

**标签**: `#AI-assisted coding`, `#code quality`, `#software engineering`, `#maintainability`, `#developer experience`

---

<a id="item-6"></a>
## [没有顶级论文的机器学习博士：该毕业吗？](https://www.reddit.com/r/MachineLearning/comments/1uazlhg/would_you_let_an_ml_phd_student_graduate_without/) ⭐️ 8.0/10

Reddit 上一个讨论提出，如果一个机器学习博士生工作扎实、论文方向清晰，但没有在 NeurIPS、ICML、ICLR 或 CVPR 等顶级会议发表论文，是否应该允许其毕业，前提是论文本身质量过硬。 这场辩论凸显了机器学习学术界以发表论文为衡量标准与研究工作内在质量之间的张力，影响毕业政策和博士生的未来职业前景。 该学生有三篇第一作者的 A 级论文，但没有 A*级会议论文。问题假设论文本身质量过硬，聚焦于顶级发表是否应成为毕业的硬性要求。

reddit · r/MachineLearning · /u/Hope999991 · 6月20日 15:36

**背景**: 在机器学习领域，NeurIPS、ICML、ICLR 和 CVPR 等顶级会议被视为 A*级会议，在这些会议上发表论文常被视为研究质量的标志。许多博士项目明示或暗示要求此类发表才能毕业，但这一做法存在争议。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://dev.to/ericwoooo_kr/do-workshop-papers-at-neuripsicml-actually-help-your-phd-application-heres-what-admissions-9dj">Do Workshop Papers at NeurIPS / ICML Actually... - DEV Community</a></li>
<li><a href="https://blog.csdn.net/a1920993165/article/details/137727367">计算机常见的六大会议介绍： CVPR /ICCV/ECCV...</a></li>

</ul>
</details>

**社区讨论**: Reddit 帖子中的观点不一：有人认为扎实的工作和 A 级论文就足够了，而另一些人坚持认为顶级发表对于机器学习博士至关重要。许多评论者强调论文质量比发表场所更重要。

**标签**: `#machine learning`, `#PhD`, `#publications`, `#academia`, `#graduation criteria`

---

<a id="item-7"></a>
## [ICML 2026 论文：时间序列建模需要动力系统视角](https://www.reddit.com/r/MachineLearning/comments/1uark0u/time_series_modeling_needs_a_dynamical_systems/) ⭐️ 8.0/10

一篇 ICML 2026 立场论文主张时间序列建模应采用动力系统重构（DSR）以实现长期预测和域外泛化，并提出了广义教师强制和基于混沌模拟预训练等具体训练技术。 该论文挑战了当前基于 Transformer 的时间序列预测模型的主导地位，倡导范式转变，有望实现更鲁棒、可解释的模型，能够处理拓扑变化和长期动态。 作者建议回归现代 RNN，因为 Transformer 由于粗粒度化会丢失关键的动力学信息。他们还强调，适当的训练技术（如广义教师强制）比模型架构更重要。

reddit · r/MachineLearning · /u/DangerousFunny1371 · 6月20日 08:47

**背景**: 动力系统重构（DSR）旨在从观测时间序列中推断潜在的动力学规则，而不仅仅是预测。Takens 定理为从观测中重构混沌系统提供了理论基础。广义教师强制是一种在训练混沌动力学时稳定梯度的训练方法。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Takens's_theorem">Takens's theorem - Wikipedia</a></li>
<li><a href="https://arxiv.org/abs/2306.04406">[2306.04406] Generalized Teacher Forcing for Learning Chaotic Dynamics</a></li>
<li><a href="https://proceedings.mlr.press/v202/hess23a/hess23a.pdf">Generalized Teacher Forcing for Learning Chaotic Dynamics</a></li>

</ul>
</details>

**社区讨论**: Reddit 上的讨论内容充实，用户对从 Transformer 转向 RNN 以及关注动力系统的提议表现出浓厚兴趣。一些评论者讨论了在实际应用中实施 DSR 的挑战。

**标签**: `#time series`, `#dynamical systems`, `#machine learning`, `#ICML`, `#forecasting`

---

<a id="item-8"></a>
## [大规模 LLM 推理开源手册：GPU 内部机制、KV 缓存、批处理及 vLLM/SGLang/TensorRT-LLM](https://www.reddit.com/r/MachineLearning/comments/1uavduv/an_open_handbook_on_llm_inference_at_scale_gpu/) ⭐️ 8.0/10

一本关于大规模 LLM 推理的开源手册（仍在编写中）已发布，内容涵盖 GPU 内存层次结构、KV 缓存、批处理以及 vLLM、SGLang 和 TensorRT-LLM 等生产框架。最新章节重点讲解 GPU 执行和内存内部机制，解释推理过程中 GPU 为何大部分时间处于空闲状态以及瓶颈所在。 大规模 LLM 推理是部署 AI 系统的关键挑战，这本手册提供了罕见的详细资源，将 GPU 硬件基础与生产优化技术联系起来。它帮助工程师理解和改进推理吞吐量与延迟，直接影响成本和用户体验。 该手册包含用于架构可视化的 mermaid 图表，并作为个人学习项目托管在 GitHub 上。作者积极寻求社区反馈和更正，尤其欢迎有生产推理经验的人士参与。

reddit · r/MachineLearning · /u/YouFirst295 · 6月20日 12:27

**背景**: LLM 推理受内存带宽限制，由于数据移动瓶颈，GPU 通常仅能达到峰值 FLOPs 的 30-50%。KV 缓存是一项关键优化，它存储中间键和值的计算结果，避免自回归生成过程中的冗余重复计算。vLLM 和 TensorRT-LLM 等生产框架通过 PagedAttention 和编译时优化等技术进一步优化推理。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/pdf/1509.02308">1 Dissecting GPU Memory Hierarchy through Microbenchmarking</a></li>
<li><a href="https://medium.com/@indiai/gpu-memory-hierarchy-how-ai-training-actually-works-24f00cc13050">GPU Memory Hierarchy — How AI Training Actually Works | by AIQuest | Medium</a></li>
<li><a href="https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms">Understanding and Coding the KV Cache in LLMs from Scratch</a></li>

</ul>
</details>

**标签**: `#LLM inference`, `#GPU internals`, `#vLLM`, `#TensorRT-LLM`, `#systems optimization`

---

<a id="item-9"></a>
## [minFLUX：FLUX 扩散模型的精简 PyTorch 实现](https://www.reddit.com/r/MachineLearning/comments/1ub1db3/studying_flux_in_diffusers_library_was_hard_so_i/) ⭐️ 8.0/10

一位开发者发布了 minFLUX，这是一个 FLUX 扩散模型的精简 PyTorch 实现，提供了与官方 HuggingFace diffusers 库的逐行映射，以及 FLUX.1 和 FLUX.2 的训练与推理循环。 该项目通过去除官方 diffusers 库的复杂性，使研究 FLUX 扩散模型变得更加容易，让研究人员和从业者能够更轻松地理解和实验核心架构。 minFLUX 包含 VAE 和 Transformer 模型，使用速度 MSE 的流匹配进行训练，并使用欧拉 ODE 求解器进行推理。它还突出了 FLUX.1 和 FLUX.2 之间的架构差异，例如 Transformer 块、调制、FFN、VAE 归一化和位置 ID 的改进。

reddit · r/MachineLearning · /u/Other-Eye-8152 · 6月20日 16:50

**背景**: FLUX 是由 Black Forest Labs 开发的文本到图像扩散模型系列。官方 HuggingFace diffusers 库提供了全面但复杂的实现，对于想要研究底层数学和架构的人来说可能难以应对。流匹配是一种生成建模技术，涵盖了扩散路径，而 RoPE（旋转位置编码）是 Transformer 中使用的一种位置编码方法。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Flux_(text-to-image_model)">Flux (text-to-image model) - Wikipedia</a></li>
<li><a href="https://arxiv.org/abs/2507.09595">[2507.09595] Demystifying Flux Architecture - arXiv.org</a></li>
<li><a href="https://arxiv.org/abs/2210.02747">[2210.02747] Flow Matching for Generative Modeling</a></li>

</ul>
</details>

**社区讨论**: 社区反响积极，用户赞赏该项目的教育价值。一些评论者指出，与官方库的逐行映射对学习特别有帮助。

**标签**: `#diffusion models`, `#FLUX`, `#PyTorch`, `#open source`, `#machine learning`

---

<a id="item-10"></a>
### *（简报）* [慢呼吸调节大脑功能与冒险行为](https://www.cell.com/neuron/fulltext/S0896-6273(26)00339-9) ⭐️ 7.0/10

发表在《Neuron》上的一项研究表明，慢呼吸技巧能够调节大脑活动并增加冒险行为，对焦虑和抑郁具有潜在临床应用价值。 这项研究为慢呼吸的镇静效果提供了神经生物学基础，将其与冒险行为增加联系起来，这在公开演讲等场景中可能有益。同时，它通过呼吸模式调节奖赏处理，为焦虑和抑郁提供了新的治疗思路。 研究发现，延长呼气呼吸能选择性地增强奖赏反应，这对具有不同自主神经特征的临床状况有重要意义。该效应由副交感神经系统激活介导。

---

<a id="item-11"></a>
### *（简报）* [免费工作坊教你从零构建大语言模型](https://www.reddit.com/r/MachineLearning/comments/1uazlnd/hi_reddit_i_posted_my_build_your_own_llm_workshop/) ⭐️ 7.0/10

一场名为“构建你自己的大语言模型”的综合性工作坊已在 YouTube 上线，内容涵盖机器学习基础、Transformer 架构及训练技术，配有代码和 Excel 示例，无需数学基础。 该资源通过消除数学门槛，使更广泛的受众能够接触大语言模型开发，有望加速该领域的学习与创新。 工作坊包含分词、嵌入、注意力机制（MHA、GQA、MQA、MLA）以及预训练/后训练等实操环节，配有幻灯片、Excel 练习和 PyTorch 代码示例。

---

<a id="item-12"></a>
### *（简报）* [DVD-JEPA：最小化开源 JEPA 世界模型](https://www.reddit.com/r/MachineLearning/comments/1uatlzx/dvdjepa_an_opensource_fullyreproducible_jepa/) ⭐️ 7.0/10

DVD-JEPA 是一个最小化的开源联合嵌入预测架构（JEPA）实现，它学习预测 16×16 网格中弹跳 DVD 标志的表示，无需像素级预测。它展示了线性探针可以从冻结的 32 维潜在空间中恢复标志的精确(x,y)位置，误差在 0.73 像素以内，并且预测误差可作为异常信号，在发生瞬移时比基线高出 88 倍。 这项工作为 JEPA 概念提供了一个清晰、可复现的演示，而 JEPA 是 Yann LeCun 关于世界模型和自监督学习愿景的核心。通过展示一个简单的、可在浏览器中运行的实现能够学习有意义的表示并检测异常，它降低了研究人员和爱好者尝试基于 JEPA 方法的门槛。 该模型由一个上下文编码器、一个 EMA 目标编码器和一个潜在预测器组成，所有组件均在无标签且无解码器的情况下训练。整个系统在浏览器客户端运行，训练好的 MLP 用约 40 行 JavaScript 重新实现。当添加可选解码器时，模型可以“梦想”出大约 20 步的正确未来帧，之后会出现潜在漂移。

---

<a id="item-13"></a>
### *（简报）* [机器学习实践者构建全球 PM2.5 预测模型，采用创新架构](https://www.reddit.com/r/MachineLearning/comments/1uar4vc/built_a_global_aq_pm25_forecaster_ml_model_p/) ⭐️ 7.0/10

一位实践者利用超过 160 万行 OpenAQ 和 NASA 气象数据，构建了覆盖美国、英国、印度和澳大利亚的端到端 PM2.5 预测管道。其核心创新是采用“地平线对齐架构”，通过解耦预测时间窗口来克服混沌环境中的方差陷阱。 这项工作解决了时间序列预测中的一个根本性挑战——方差陷阱，即在高方差区域，简单基线模型的表现反而优于机器学习模型。地平线对齐方法提供了一种实用解决方案，有望改善空气质量、金融和能源等混沌领域的预测可靠性。 该模型在全球范围内实现了 MASE 低于 1.0，在 30 天预测窗口上相对于混沌热力学基线的预测准确率达到 57%。技术栈包括后端 Python、Pandas、scikit-learn、FastAPI，前端 Next.js 16、Tailwind v4、Recharts，部署在 Vercel 上。

---

