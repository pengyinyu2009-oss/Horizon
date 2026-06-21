---
layout: default
title: "Horizon Daily: 2026-06-21 (ZH)"
date: 2026-06-21
lang: zh
period: daily
period_id: 2026-06-21
---

> 从 13 条内容中筛选出 5 条重要资讯。

其中 **3 条 8 分以上**展开详细简报，其余 2 条仅列于索引。

---

1. [Epoll 与 io_uring 对比：深入解析 Linux I/O 性能](#item-1) ⭐️ 8.0/10
2. [发布 GPT-2 中等规模的免 Softmax 注意力模型](#item-2) ⭐️ 8.0/10
3. [minFLUX：FLUX 扩散模型的极简 PyTorch 实现](#item-3) ⭐️ 8.0/10
4. [Google IPv6 流量突破 50% 里程碑](#item-4) ⭐️ 7.0/10
5. [慢呼吸通过副交感神经激活增强冒险行为](#item-5) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [Epoll 与 io_uring 对比：深入解析 Linux I/O 性能](https://sibexi.co/posts/epoll-vs-io_uring/) ⭐️ 8.0/10

一篇详细的技术文章对比了 Linux 下的两种 I/O 多路复用机制——epoll 和 io_uring，分析了它们在高性能应用中的性能和架构差异。 这一对比有助于开发者为高吞吐量服务器选择合适的 I/O 模型，因为 io_uring 在现代工作负载下相比 epoll 具有潜在的性能优势。 文章指出 io_uring 通过共享环形缓冲区减少了系统调用开销，而 epoll 则更简单、更成熟。基准测试显示，在高连接数下 io_uring 可以实现更低的延迟。

hackernews · Sibexico · 6月20日 23:07 · [社区讨论](https://news.ycombinator.com/item?id=48613872)

**背景**: epoll 是 Linux 内核中用于可扩展 I/O 事件通知的系统调用，广泛应用于高性能服务器。io_uring 是一种较新的异步 I/O 接口，通过共享环形缓冲区减少系统调用次数，从而提升性能。两者都用于高效处理大量并发连接。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Io_uring">io_uring - Wikipedia</a></li>
<li><a href="https://man7.org/linux/man-pages/man7/io_uring.7.html">io_uring(7) - Linux manual page</a></li>
<li><a href="https://github.com/samcode206/io_uring-vs-epoll-tcp">GitHub - samcode206/ io _ uring - vs - epoll -tcp: IO _ URING vs epoll ...</a></li>

</ul>
</details>

**社区讨论**: 评论者讨论了 CPU 绑定和零拷贝等优化技术，并提到了 kTLS、eBPF 和 DPDK 等相关技术。一些人分享了自己的实现和基准测试结果，指出 io_uring 仍缺少 sendfile 等特性。

**标签**: `#Linux`, `#I/O`, `#epoll`, `#io_uring`, `#performance`

---

<a id="item-2"></a>
## [发布 GPT-2 中等规模的免 Softmax 注意力模型](https://www.reddit.com/r/MachineLearning/comments/1ubmybr/i_released_a_softmaxfree_attention_model_at_gpt2/) ⭐️ 8.0/10

发布了一个 GPT-2 中等规模（约 3.54 亿参数，在 115 亿 token 上训练）的免 Softmax 注意力模型，采用结构稀疏性和跳块内核以节省长上下文 VRAM。模型权重和自定义 Triton 内核已开源。 这项工作表明免 Softmax 注意力可以扩展到有意义的模型规模，可能减少长上下文推理的内存瓶颈。开源发布有助于进一步研究高效 Transformer 架构及其实际应用。 该模型使用结构稀疏模式和用 Triton 实现的跳块内核，跳过不相关的注意力块，从而减少长序列的 VRAM 使用。模型在 GPT-2 中等规模（3.54 亿参数）上使用 115 亿 token 训练，权重和自定义内核已开源。

reddit · r/MachineLearning · /u/NonGameCatharsis · 6月21日 10:46

**背景**: 标准 Transformer 注意力使用 Softmax 操作归一化注意力分数，需要计算所有查询-键交互，对长序列内存消耗大。免 Softmax 注意力用更简单的归一化（如ℓ1 范数）替代 Softmax，可实现线性复杂度近似。结构稀疏性和跳块通过忽略无关块进一步减少计算。Triton 是一种用于编写高效自定义内核的 GPU 编程语言。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/html/2207.03341v3">Softmax - free Linear Transformers</a></li>
<li><a href="https://openai.com/index/triton/">Introducing Triton: Open-source GPU programming for neural networks | OpenAI</a></li>
<li><a href="https://openaccess.thecvf.com/content/WACV2024/papers/Koohpayegani_SimA_Simple_Softmax-Free_Attention_for_Vision_Transformers_WACV_2024_paper.pdf">SimA: Simple Softmax - Free Attention for Vision Transformers</a></li>

</ul>
</details>

**标签**: `#attention`, `#efficiency`, `#open-source`, `#Triton`, `#long-context`

---

<a id="item-3"></a>
## [minFLUX：FLUX 扩散模型的极简 PyTorch 实现](https://www.reddit.com/r/MachineLearning/comments/1ub1db3/studying_flux_in_diffusers_library_was_hard_so_i/) ⭐️ 8.0/10

一位开发者发布了 minFLUX，这是 FLUX.1 和 FLUX.2 扩散模型的极简 PyTorch 实现，包含逐行映射到 HuggingFace diffusers 以及完整的训练和推理循环。 该项目通过剥离官方 diffusers 库的复杂性，使研究 FLUX 的架构和数学原理变得更加容易，有利于研究人员和学习现代扩散模型的学生。 minFLUX 包含 VAE 和 Transformer 模型、基于速度 MSE 的流匹配训练、Euler ODE 推理以及 RoPE 和时间步嵌入等共享工具。它还突出了 FLUX.1 和 FLUX.2 之间的架构差异。

reddit · r/MachineLearning · /u/Other-Eye-8152 · 6月20日 16:50

**背景**: FLUX 是 Black Forest Labs 开发的一系列文本到图像扩散模型，基于具有 120 亿参数的整流流 Transformer 块。官方的 HuggingFace diffusers 库提供了全面但复杂的实现，使学习者难以隔离核心概念。流匹配是一种生成建模框架，涵盖了扩散路径，并使用 Euler–Maruyama 等 ODE 求解器进行采样。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Flux_(text-to-image_model)">Flux (text-to-image model) - Wikipedia</a></li>
<li><a href="https://arxiv.org/abs/2210.02747">[2210.02747] Flow Matching for Generative Modeling</a></li>
<li><a href="https://en.wikipedia.org/wiki/Euler–Maruyama_method">Euler–Maruyama method - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: Reddit 社区反应积极，赞赏该项目的清晰度和教育价值。用户指出它解决了研究扩散模型时的一个常见痛点，并赞扬了与官方代码的逐行映射。

**标签**: `#diffusion models`, `#FLUX`, `#PyTorch`, `#open-source`, `#machine learning`

---

<a id="item-4"></a>
### *（简报）* [Google IPv6 流量突破 50% 里程碑](https://blog.apnic.net/2026/04/28/google-hits-50-ipv6/) ⭐️ 7.0/10

Google 的 IPv6 流量已达到总流量的 50%，标志着全球 IPv6 部署的一个重要里程碑。 这一里程碑凸显了互联网基础设施对 IPv6 的日益成熟，但 ISP 部署的持续障碍仍是全面过渡的瓶颈。 50% 的数据基于 Google 的全球流量统计。尽管取得进展，许多 ISP 仍不支持 IPv6，且 GitHub 等主要平台也未原生支持 IPv6。

---

<a id="item-5"></a>
### *（简报）* [慢呼吸通过副交感神经激活增强冒险行为](https://www.cell.com/neuron/fulltext/S0896-6273(26)00339-9) ⭐️ 7.0/10

发表在《Neuron》上的一项研究表明，慢呼吸（尤其是延长呼气）能增强副交感神经系统的活动，并增加人类的冒险行为。 这一发现挑战了慢呼吸仅能镇静身体的普遍假设，表明它还能将行为转向冒险，这对焦虑治疗和公开演讲等表现场景具有启示意义。 该研究特别指出延长呼气是增加奖赏反应的关键驱动因素，这可能与焦虑、恐慌症和抑郁症等涉及自主神经和奖赏处理异常的临床状况相关。

---

