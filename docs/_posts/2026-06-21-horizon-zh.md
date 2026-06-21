---
layout: default
title: "Horizon Daily: 2026-06-21 (ZH)"
date: 2026-06-21
lang: zh
period: daily
period_id: 2026-06-21
---

> 从 15 条内容中筛选出 8 条重要资讯。

其中 **4 条 8 分以上**展开详细简报，其余 4 条仅列于索引。

---

1. [Epoll 与 io_uring：Linux I/O 性能深度对比](#item-1) ⭐️ 8.0/10
2. [开发者不理解 CORS（2019）](#item-2) ⭐️ 8.0/10
3. [发布 GPT-2 中等规模的免 Softmax 注意力模型](#item-3) ⭐️ 8.0/10
4. [minFLUX：FLUX 扩散模型的极简 PyTorch 实现](#item-4) ⭐️ 8.0/10
5. [Google IPv6 流量全球占比达 50%](#item-5) ⭐️ 7.0/10
6. [慢呼吸调节大脑功能与风险行为](#item-6) ⭐️ 7.0/10
7. [免费 YouTube 工作坊：从零开始构建大语言模型](#item-7) ⭐️ 7.0/10
8. [机器学习博士生没有顶会论文能否毕业？](#item-8) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [Epoll 与 io_uring：Linux I/O 性能深度对比](https://sibexi.co/posts/epoll-vs-io_uring/) ⭐️ 8.0/10

一篇详细的技术文章对比了 epoll 和 io_uring 在高性能网络服务器中的表现，分析了它们的性能特性和实际影响。 这一对比有助于开发者为构建高效网络服务器选择合适的 I/O 模型，尤其是在 io_uring 从最初的文件 I/O 扩展到网络 I/O 领域并日益受到关注的背景下。 文章探讨了性能权衡，包括 io_uring 在降低延迟和减少系统调用方面的潜力，但也指出 epoll 在许多工作负载下仍具竞争力。社区评论讨论了 CPU 绑定、零拷贝以及 kTLS 和 eBPF 等相关技术。

hackernews · Sibexico · 6月20日 23:07 · [社区讨论](https://news.ycombinator.com/item?id=48613872)

**背景**: epoll 是 Linux 内核中用于可扩展 I/O 事件通知的系统调用，广泛应用于高性能网络服务器。io_uring 是一种较新的异步 I/O 接口，通过用户空间与内核空间之间的共享环形缓冲区来减少开销并提升性能，最初为文件 I/O 设计，现在也支持网络 I/O。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Io_uring">io_uring - Wikipedia</a></li>
<li><a href="https://developers.redhat.com/articles/2023/04/12/why-you-should-use-iouring-network-io">Why you should use io_uring for network I/O | Red Hat Developer</a></li>
<li><a href="https://github.com/axboe/liburing/issues/536">Yet another comparison between io_uring and epoll on network ... - GitHub</a></li>

</ul>
</details>

**社区讨论**: 评论强调了 CPU 绑定和零拷贝等实际优化，并提到了 concurrencykit 和 mimalloc 等相关项目。一些用户分享了在 Rust 和 kTLS 中使用 io_uring 的经验，指出 io_uring 尚不支持 sendfile。

**标签**: `#Linux`, `#I/O`, `#performance`, `#epoll`, `#io_uring`

---

<a id="item-2"></a>
## [开发者不理解 CORS（2019）](https://fosterelli.co/developers-dont-understand-cors) ⭐️ 8.0/10

一篇博客文章指出大多数开发者误解了 CORS，随后 Hacker News 上的讨论（267 分，202 条评论）讽刺地证明了这一点，因为许多评论本身就是错误的。 CORS 是基本的 Web 安全机制，但普遍的误解导致不安全的实现和开发者的挫败感。这篇文章及其讨论凸显了开发者教育中的关键缺口。 文章解释 CORS 是由浏览器而非服务器强制执行的，错误配置可能使应用程序易受攻击。HN 评论显示了对预检请求和实际威胁模型的困惑。

hackernews · toilet · 6月21日 01:35 · [社区讨论](https://news.ycombinator.com/item?id=48614844)

**背景**: CORS（跨源资源共享）是一种浏览器机制，允许从不同源受控访问资源。它使用 Access-Control-Allow-Origin 等 HTTP 头告诉浏览器允许哪些源。对于非简单请求，浏览器会发送预检请求（OPTIONS）来检查服务器权限。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request">Preflight request - Glossary | MDN</a></li>

</ul>
</details>

**社区讨论**: 评论从通过服务器端实现学习 CORS 的人，到指出文章本身曲解 CORS 的人。有人称这是他们见过的最无知的 HN 评论区，而其他人则指出威胁模型普遍被误解。

**标签**: `#CORS`, `#web security`, `#developer education`, `#HTTP`

---

<a id="item-3"></a>
## [发布 GPT-2 中等规模的免 Softmax 注意力模型](https://www.reddit.com/r/MachineLearning/comments/1ubmybr/i_released_a_softmaxfree_attention_model_at_gpt2/) ⭐️ 8.0/10

一个 GPT-2 中等规模（约 3.54 亿参数，在 115 亿 token 上训练）的免 Softmax 注意力模型已发布，采用结构稀疏性和瓦片跳过内核来节省长上下文 VRAM。模型权重和自定义 Triton 内核已开源。 这项工作表明免 Softmax 注意力可以扩展到数亿参数规模，有望实现更高效的长上下文处理。开源发布使社区能够实验并在此基础上构建。 该模型使用结构稀疏性和瓦片跳过内核来减少长上下文推理期间的 VRAM 使用。提供了自定义 Triton 内核以在 GPU 上高效实现。

reddit · r/MachineLearning · /u/NonGameCatharsis · 6月21日 10:46

**背景**: 标准 Transformer 注意力使用 Softmax 来归一化注意力分数，对于长序列来说计算成本高且内存密集。免 Softmax 注意力用更简单的归一化（如ℓ1 范数）替代 Softmax 以提高效率。Triton 是一种用于编写自定义 GPU 内核的语言和编译器，可实现高性能实现。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/html/2207.03341v3">Softmax - free Linear Transformers</a></li>
<li><a href="https://openai.com/index/triton/">Introducing Triton: Open-source GPU programming for neural networks | OpenAI</a></li>
<li><a href="https://github.com/triton-lang/triton">GitHub - triton-lang/triton: Development repository for the Triton language and compiler · GitHub</a></li>

</ul>
</details>

**社区讨论**: 社区讨论活跃，有关于免 Softmax 注意力相比标准注意力的实际优势的技术问题，以及关于准确性和效率权衡的辩论。

**标签**: `#attention`, `#efficiency`, `#open-source`, `#Triton`, `#long-context`

---

<a id="item-4"></a>
## [minFLUX：FLUX 扩散模型的极简 PyTorch 实现](https://www.reddit.com/r/MachineLearning/comments/1ub1db3/studying_flux_in_diffusers_library_was_hard_so_i/) ⭐️ 8.0/10

一位开发者发布了 minFLUX，这是一个 FLUX.1 和 FLUX.2 扩散模型的极简开源 PyTorch 实现，并提供了与 HuggingFace diffusers 库的逐行映射。 该项目通过剥离官方 diffusers 库的复杂性，使研究人员和学生能够更轻松地研究 FLUX 模型的内部架构，FLUX 模型是当前最先进的文本到图像生成模型之一。 minFLUX 包含 FLUX.1 和 FLUX.2 的实现，涵盖 VAE、transformer、基于流匹配的训练循环以及使用欧拉 ODE 求解器的推理循环。它还突出了 FLUX.1 和 FLUX.2 之间的架构差异，如改进的 transformer 块、调制和 FFN。

reddit · r/MachineLearning · /u/Other-Eye-8152 · 6月20日 16:50

**背景**: FLUX 模型是一系列文本到图像扩散模型，采用混合架构，结合了多模态和并行扩散 transformer 块，参数量达 120 亿。它们使用流匹配（flow matching）训练方法，通过预测速度学习将噪声转化为数据。官方的 HuggingFace diffusers 库虽然功能全面，但常因其复杂性和抽象化而受到批评，使得研究核心架构变得困难。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/html/2507.09595v1">Demystifying Flux Architecture</a></li>
<li><a href="https://medium.com/@drmarcosv/how-does-flux-work-the-new-image-generation-ai-that-rivals-midjourney-7f81f6f354da">How does Flux work? The new image generation AI that rivals Midjourney | by Marcos V. Conde | Medium</a></li>
<li><a href="https://www.ikomia.ai/blog/flux1-text-to-image-diffusion-model">FLUX.1 Text-to-Image AI: Next-Gen Diffusion Model for Visual Fidelity</a></li>

</ul>
</details>

**社区讨论**: Reddit 社区反响积极，用户对项目的教育价值以及与 diffusers 的清晰映射表示赞赏。部分用户讨论了 FLUX.1 和 FLUX.2 之间的架构差异，以及该项目帮助新手理解扩散模型的潜力。

**标签**: `#diffusion models`, `#FLUX`, `#PyTorch`, `#open-source`, `#machine learning`

---

<a id="item-5"></a>
### *（简报）* [Google IPv6 流量全球占比达 50%](https://blog.apnic.net/2026/04/28/google-hits-50-ipv6/) ⭐️ 7.0/10

Google 的 IPv6 流量全球占比已达到 50%，标志着从 IPv4 向 IPv6 过渡的一个重要里程碑。该数据基于 Google 自身的统计，追踪通过 IPv6 访问 Google 服务的用户比例。 这一里程碑表明，半数 Google 用户现在通过 IPv6 连接，反映了互联网基础设施现代化的重大进展。它也凸显了网络运营商和内容提供商支持 IPv6 的日益必要性，以避免碎片化并确保未来的可扩展性。 50% 的数据来自 Google 自身的统计，而 APNIC Labs 报告的全球 IPv6 能力为 42%，表明统计方法存在差异。不同地区的采用率差异很大，印度、越南和沙特阿拉伯等发展中国家的增长更快。

---

<a id="item-6"></a>
### *（简报）* [慢呼吸调节大脑功能与风险行为](https://www.cell.com/neuron/fulltext/S0896-6273(26)00339-9) ⭐️ 7.0/10

《神经元》期刊发表的一项研究表明，慢呼吸能够调节大脑功能并增加冒险行为，这对焦虑症和抑郁症的治疗具有启示意义。 这项研究揭示了呼吸模式与行为之间的神经机制，为存在奖赏处理异常和自主神经功能紊乱的精神疾病提供了潜在的非药物干预手段。 研究特别发现，延长呼气时间的呼吸方式能增强心脏副交感神经调节和奖赏反应性，这或许可以解释冒险行为的增加。

---

<a id="item-7"></a>
### *（简报）* [免费 YouTube 工作坊：从零开始构建大语言模型](https://www.reddit.com/r/MachineLearning/comments/1uazlnd/hi_reddit_i_posted_my_build_your_own_llm_workshop/) ⭐️ 7.0/10

一个名为“构建你自己的大语言模型”的综合性工作坊视频已上传至 YouTube，内容涵盖从机器学习基础到 Transformer 架构、PyTorch GPU 编程及 Triton 等高级主题，无需数学先修知识。 该资源降低了开发者和爱好者理解并构建大语言模型的门槛，有望加速 AI 社区的实践学习。它通过代码和 Excel 示例弥合了理论与实践之间的差距。 工作坊涵盖分词器、嵌入、注意力机制（MHA、GQA、MQA、MLA）、预训练、指令微调和强化学习（SimPO）等章节。还包括 torch.compile()和融合内核等 GPU 优化技术。

---

<a id="item-8"></a>
### *（简报）* [机器学习博士生没有顶会论文能否毕业？](https://www.reddit.com/r/MachineLearning/comments/1uazlhg/would_you_let_an_ml_phd_student_graduate_without/) ⭐️ 7.0/10

一位 Reddit 用户提出了一个假设场景：一名博士生有扎实的工作和三篇第一作者的 A 类论文，但没有在 NeurIPS、ICML、ICLR 或 CVPR 等顶级会议上发表过论文，询问导师是否应支持其毕业。 这场辩论凸显了机器学习学术界在发表指标与研究质量之间的张力，影响毕业政策与博士生福祉。其结果可能影响未来学生如何权衡会议声望与实际贡献。 该学生有三篇第一作者论文发表在 A 类会议（非顶级），论文方向连贯，但缺少 NeurIPS、ICML、ICLR 或 CVPR 的发表记录。问题在于仅凭论文质量是否足以毕业。

---

