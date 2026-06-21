---
layout: default
title: "Horizon Daily: 2026-06-21 (ZH)"
date: 2026-06-21
lang: zh
period: daily
period_id: 2026-06-21
---

> 从 19 条内容中筛选出 9 条重要资讯。

其中 **5 条 8 分以上**展开详细简报，其余 4 条仅列于索引。

---

1. [开发者不理解 CORS：一篇 2019 年的文章至今仍有现实意义](#item-1) ⭐️ 8.0/10
2. [Epoll 与 io_uring：Linux I/O 深度对比](#item-2) ⭐️ 8.0/10
3. [SMPTE 向全球免费开放其标准库](#item-3) ⭐️ 8.0/10
4. [发布 GPT-2 中等规模的免 Softmax 注意力模型](#item-4) ⭐️ 8.0/10
5. [minFLUX：FLUX 扩散模型的精简 PyTorch 实现](#item-5) ⭐️ 8.0/10
6. [Google IPv6 流量突破 50% 里程碑](#item-6) ⭐️ 7.0/10
7. [慢呼吸调节大脑功能与风险行为](#item-7) ⭐️ 7.0/10
8. [DOS 游戏《F-15 Strike Eagle II》逆向工程项目招募测试员](#item-8) ⭐️ 7.0/10
9. [没有顶会论文的机器学习博士生，该毕业吗？](#item-9) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [开发者不理解 CORS：一篇 2019 年的文章至今仍有现实意义](https://fosterelli.co/developers-dont-understand-cors) ⭐️ 8.0/10

Chris Foster 发表了一篇文章，以 Zoom 漏洞为例，指出许多开发者从根本上误解了 CORS。该文章在 Hacker News 上的评论区很大程度上证实了他的观点，许多评论者错误地解释了 CORS 的行为。 CORS 是一个关键的 Web 安全机制，但普遍的误解会导致类似 Zoom 漏洞的安全问题。这篇文章揭示了开发者教育中一个持续存在的缺口，至今仍在影响 Web 安全。 Zoom 漏洞涉及一个本地 Web 服务器，本应使用 CORS 头来限制访问，但却采用了一种基于图片的变通方案，导致任何网站都能访问。CORS 并不阻止请求，只是阻止浏览器读取响应——这一细微差别许多开发者都忽略了。

hackernews · toilet · 6月21日 01:35 · [社区讨论](https://news.ycombinator.com/item?id=48614844)

**背景**: CORS（跨源资源共享）是一种浏览器机制，允许受控地访问不同源上的资源。它通过添加 HTTP 头来告知浏览器是否允许跨源请求。同源策略（SOP）阻止网站读取来自其他源的数据，而 CORS 则有选择地放宽该策略。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://fosterelli.co/developers-dont-understand-cors">Developers don't understand CORS - Chris Foster</a></li>
<li><a href="https://css-tricks.com/zoom-cors-and-the-web/">Zoom, CORS, and the Web | CSS-Tricks</a></li>
<li><a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS">Cross-Origin Resource Sharing (CORS) - HTTP | MDN Code sample</a></li>

</ul>
</details>

**社区讨论**: 评论区高度两极分化：一些评论者同意作者的观点，并指出普遍存在的困惑，而另一些评论者则讽刺地展示了作者所描述的误解。少数评论者提供了有用的澄清，例如指出 CORS 并不限制请求，只限制响应读取。

**标签**: `#CORS`, `#web security`, `#developer misconceptions`, `#HTTP`, `#browser security`

---

<a id="item-2"></a>
## [Epoll 与 io_uring：Linux I/O 深度对比](https://sibexi.co/posts/epoll-vs-io_uring/) ⭐️ 8.0/10

一篇详细的技术文章对比了 Linux 中用于高性能 I/O 的 epoll 和 io_uring，涵盖了架构限制、CPU 绑定和忙轮询等优化技术，以及 eBPF 的作用。 这一对比对于构建高吞吐量服务器的系统程序员至关重要，因为选择正确的 I/O 模型会显著影响性能。文章提供了实用的见解，有助于优化反向代理和 Web 服务器等实际应用。 文章指出，io_uring 通过使用共享提交和完成队列来减少系统调用开销，但 epoll 结合忙轮询在网络 I/O 中仍能实现低延迟。文章还讨论了如何使用 eBPF 来卸载数据包处理。

hackernews · Sibexico · 6月20日 23:07 · [社区讨论](https://news.ycombinator.com/item?id=48613872)

**背景**: epoll 是 Linux 内核中用于可扩展 I/O 事件通知的系统调用，广泛用于 nginx 等高性能服务器。io_uring 是 Linux 5.1 引入的较新的异步 I/O 接口，旨在减少系统调用开销并提高存储和网络 I/O 的吞吐量。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/axboe/liburing/issues/536">Yet another comparison between io_uring and epoll on network ...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Io_uring">io_uring - Wikipedia</a></li>
<li><a href="https://man7.org/linux/man-pages/man7/io_uring.7.html">io_uring(7) - Linux manual page</a></li>

</ul>
</details>

**社区讨论**: 评论者讨论了实际优化技巧，如 CPU 绑定、使用 epoll_wait 进行忙轮询以及利用 eBPF 进行 DDoS 防护。一些人分享了在 Rust 和 C 中使用 io_uring 的经验，指出 io_uring 仍缺少 sendfile 支持。总体情绪积极，许多人认为文章很有见地。

**标签**: `#Linux`, `#I/O`, `#performance`, `#epoll`, `#io_uring`

---

<a id="item-3"></a>
## [SMPTE 向全球免费开放其标准库](https://www.smpte.org/blog/smpte-makes-its-standards-freely-accessible-openingstandards-library-to-the-global-media-technology-community) ⭐️ 8.0/10

SMPTE 宣布，其全部标准、推荐实践、工程指南和注册披露文档现已免费向全球媒体技术社区开放。 此举消除了获取关键媒体技术标准的经济障碍，促进了整个行业的创新和互操作性。它顺应了开放标准运动，并推动了 SMPTE 开发工作流程的现代化。 免费访问范围包括所有已发布的 SMPTE 标准、推荐实践、工程指南和注册披露文档 (RDD)，以及所有未来版本。该计划得到了亚马逊 AWS、苹果、迪士尼、谷歌和索尼等钻石级企业成员的支持。

hackernews · zdw · 6月20日 17:01 · [社区讨论](https://news.ycombinator.com/item?id=48610827)

**背景**: SMPTE（电影与电视工程师协会）为电影和电视行业制定技术标准。此前，获取这些标准需要购买单个文档或订阅，这对小型组织和独立开发者来说成本高昂。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.smpte.org/blog/smpte-makes-its-standards-freely-accessible-openingstandards-library-to-the-global-media-technology-community">SMPTE Makes Its Standards Freely Accessible, Opening ...</a></li>
<li><a href="https://www.smpte.org/setting-the-standards-free">Setting the Standards Free - smpte.org</a></li>
<li><a href="https://www.sportsvideo.org/2026/06/17/smpte-opens-entire-standards-library-to-public-at-no-cost/">SMPTE Opens Entire Standards Library to Public at No Cost</a></li>

</ul>
</details>

**社区讨论**: 社区成员普遍对此表示赞赏，一些人指出开放标准历来推动创新（例如 IETF）。其他人质疑为什么标准机构不默认这样做，一位评论者强调，在法国，法律规定的标准必须免费提供。

**标签**: `#standards`, `#media technology`, `#open access`, `#SMPTE`, `#innovation`

---

<a id="item-4"></a>
## [发布 GPT-2 中等规模的免 Softmax 注意力模型](https://www.reddit.com/r/MachineLearning/comments/1ubmybr/i_released_a_softmaxfree_attention_model_at_gpt2/) ⭐️ 8.0/10

一个在 GPT-2 中等规模（约 3.54 亿参数，在 115 亿 token 上训练）的免 Softmax 注意力模型已发布，附带开放权重和自定义 Triton 内核。该模型利用结构稀疏性和跳块内核来减少长上下文推理时的显存占用。 这项工作表明，免 Softmax 注意力可以扩展到数亿参数规模，同时实现实用的显存节省，有望在消费级 GPU 上支持更长的上下文窗口。它还贡献了开源的自定义 Triton 内核，可能惠及更广泛的高效 Transformer 社区。 该模型使用结构稀疏性和跳块内核来跳过注意力分数可忽略的计算块，从而减少长序列的显存使用。自定义 Triton 内核与模型权重一同开源，该方法在 GPT-2 中等规模上使用 115 亿 token 的训练数据进行了验证。

reddit · r/MachineLearning · /u/NonGameCatharsis · 6月21日 10:46

**背景**: 免 Softmax 注意力用更简单的操作（如ℓ1 范数）替代标准的 Softmax 归一化，从而降低计算开销。Triton 是一种开源 GPU 编程语言，允许编写高效的自定义内核。跳块是一种跳过处理对输出贡献不大的数据块的技术，从而节省内存和计算。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://openaccess.thecvf.com/content/WACV2024/papers/Koohpayegani_SimA_Simple_Softmax-Free_Attention_for_Vision_Transformers_WACV_2024_paper.pdf">SimA: Simple Softmax-free Attention for Vision Transformers</a></li>
<li><a href="https://github.com/deepseek-ai/TileKernels">GitHub - deepseek-ai/TileKernels: A kernel library written in ...</a></li>
<li><a href="https://openai.com/index/triton/">Introducing Triton: Open-source GPU programming for neural networks | OpenAI</a></li>

</ul>
</details>

**社区讨论**: 社区讨论内容充实，涉及关于免 Softmax 方法和跳块实现的技术问题。作者积极参与，解释了设计选择和潜在局限性。总体情绪积极，人们对将这些内核应用于其他模型表现出兴趣。

**标签**: `#attention`, `#efficiency`, `#transformers`, `#Triton`, `#open-source`

---

<a id="item-5"></a>
## [minFLUX：FLUX 扩散模型的精简 PyTorch 实现](https://www.reddit.com/r/MachineLearning/comments/1ub1db3/studying_flux_in_diffusers_library_was_hard_so_i/) ⭐️ 8.0/10

一位开发者发布了 minFLUX，这是一个开源的 FLUX 扩散模型（FLUX.1 和 FLUX.2）的极简 PyTorch 实现，它简化了复杂的 HuggingFace diffusers 库，包含训练和推理循环，并提供了与官方代码的逐行映射。 该项目通过去除不必要的抽象层，使研究现代扩散模型（如 FLUX）变得更加容易，让研究人员和学生无需与官方库的复杂性纠缠即可理解核心架构和数学原理。 minFLUX 包含 VAE 和 Transformer 模型实现，使用流匹配（flow matching）和速度 MSE 损失的训练循环，以及使用欧拉 ODE 求解器的推理循环。它还突出了 FLUX.1 和 FLUX.2 之间的架构差异，例如改进的 Transformer 块、调制和 VAE 归一化。

reddit · r/MachineLearning · /u/Other-Eye-8152 · 6月20日 16:50

**背景**: FLUX 是由 Black Forest Labs 开发的一系列开源扩散模型，能够根据文本提示生成高质量图像。官方的 HuggingFace diffusers 库提供了实现，但因其复杂性和大量抽象层而常被批评，使得研究底层算法变得困难。流匹配（flow matching）是一种训练模型预测噪声与数据之间插值速度场的技术，而欧拉 ODE 是在采样过程中求解常微分方程的一种简单数值方法。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://medium.com/@divija1091/from-prompt-to-picture-dall-e-stable-diffusion-flux-a2b96a773deb">From Prompt to Picture: DALL·E, Stable Diffusion & FLUX | Medium</a></li>
<li><a href="https://huggingface.co/black-forest-labs/FLUX.1-schnell">black-forest-labs/ FLUX .1-schnell · Hugging Face</a></li>
<li><a href="https://mlhonk.substack.com/p/25-flow-matching">25. Flow Matching - by Massimiliano Viola</a></li>

</ul>
</details>

**标签**: `#diffusion models`, `#FLUX`, `#PyTorch`, `#open source`, `#machine learning`

---

<a id="item-6"></a>
### *（简报）* [Google IPv6 流量突破 50% 里程碑](https://blog.apnic.net/2026/04/28/google-hits-50-ipv6/) ⭐️ 7.0/10

Google 的 IPv6 流量已达到 50%，标志着全球 IPv6 部署的一个重要里程碑。该消息于 2026 年 4 月在 APNIC 博客上公布。 这一里程碑表明，现在有一半的 Google 用户通过 IPv6 访问服务，反映了对新协议的支持在增长。然而，社区报告指出，许多 ISP 仍然缺乏对 IPv6 的适当支持，用户启用 IPv6 时会遇到性能问题和 CAPTCHA 验证提示。 50% 的数据基于 Google 服务的 IPv6 流量。社区评论显示，一些 ISP（如英国的 Virgin Media 和荷兰的 Odido）尽管早先做出承诺，仍未启用 IPv6。用户报告称，禁用 IPv6 通常能恢复全部带宽并消除 CAPTCHA 验证。

---

<a id="item-7"></a>
### *（简报）* [慢呼吸调节大脑功能与风险行为](https://www.cell.com/neuron/fulltext/S0896-6273(26)00339-9) ⭐️ 7.0/10

《神经元》期刊发表的一项研究表明，慢呼吸能够调节大脑功能并增加冒险行为，对焦虑和抑郁具有潜在临床应用价值。 这项研究揭示了呼吸模式与行为之间的神经机制，为焦虑症和公开演讲恐惧提供了一种非侵入性干预手段。 研究发现，延长呼气呼吸会选择性增强奖赏反应，这可能解释了冒险行为的增加。该发现对具有不同自主神经特征的疾病（如惊恐障碍和抑郁症）具有启示意义。

---

<a id="item-8"></a>
### *（简报）* [DOS 游戏《F-15 Strike Eagle II》逆向工程项目招募测试员](https://neuviemeporte.github.io/f15-se2/2026/06/20/needyou.html) ⭐️ 7.0/10

一个将经典 DOS 飞行模拟游戏《F-15 Strike Eagle II》从汇编语言逆向工程并移植到 C 语言的项目正在招募测试人员，以帮助发现转换过程中引入的漏洞。 这项工作保存了一段游戏历史，并使该游戏在现代平台上更易运行。它还展示了一种新颖的游戏保存方法：先完整逆向为汇编代码，再转换为二进制等效的 C 代码，最后进行移植。 该项目需要版本 451.03 的《F-15 Strike Eagle II》以及 DOS 环境（真实 DOS 或 DOSBox）。转换目标是生成二进制等效的 C 代码，即编译后的 C 代码应与原始汇编行为完全一致。

---

<a id="item-9"></a>
### *（简报）* [没有顶会论文的机器学习博士生，该毕业吗？](https://www.reddit.com/r/MachineLearning/comments/1uazlhg/would_you_let_an_ml_phd_student_graduate_without/) ⭐️ 7.0/10

一位 Reddit 用户提出了一个假设性问题：如果一名机器学习博士生工作扎实，但没有 NeurIPS、ICML 或 ICLR 等顶会论文，只有三篇第一作者 A 类论文，导师是否应支持其毕业。 这场辩论凸显了机器学习学术界在顶会发表论文的巨大压力，质疑这种要求是否是博士毕业的必要条件，或者扎实但不够亮眼的工作是否也应被认可。 该学生有三篇第一作者论文发表在“A 类”会议上，低于顶级（A*）水平。问题假设论文本身质量过硬，聚焦于发表声望在毕业决策中的作用。

---

