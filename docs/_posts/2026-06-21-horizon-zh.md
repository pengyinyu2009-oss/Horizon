---
layout: default
title: "Horizon Daily: 2026-06-21 (ZH)"
date: 2026-06-21
lang: zh
period: daily
period_id: 2026-06-21
---

> 从 15 条内容中筛选出 6 条重要资讯。

其中 **2 条 8 分以上**展开详细简报，其余 4 条仅列于索引。

---

1. [谷歌 IPv6 流量占比达到 50%里程碑](#item-1) ⭐️ 8.0/10
2. [发布 GPT-2 Medium 规模的无 Softmax 注意力模型](#item-2) ⭐️ 8.0/10
3. [你的 ATProto 身份归谁所有？提示：可能不是你](#item-3) ⭐️ 7.0/10
4. [用 APL 编写的 3D 体素游戏引擎](#item-4) ⭐️ 7.0/10
5. [对几何代数的批判性审视（2024）](#item-5) ⭐️ 7.0/10
6. [慢呼吸调节大脑功能与风险行为](#item-6) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [谷歌 IPv6 流量占比达到 50%里程碑](https://blog.apnic.net/2026/04/28/google-hits-50-ipv6/) ⭐️ 8.0/10

谷歌的全球 IPv6 流量占比已达到 50%，这是互联网协议采用的一个重要里程碑。然而，由于互联网服务提供商和服务商的限制，部署障碍依然存在。 这一里程碑表明 IPv6 的采用正在加速，这对于克服 IPv4 地址枯竭至关重要。同时，它也凸显了进展的不均衡：法国等地区已超过 85%，而其他地区因互联网服务提供商的惰性而落后。 50%这一数字是全球平均值；各地采用率差异很大，法国已超过 85%。GitHub 和 AWS 等主要平台仍缺乏完整的 IPv6 支持，迫使用户依赖 NAT64 等翻译服务。

hackernews · barqawiz · 6月21日 08:21 · [社区讨论](https://news.ycombinator.com/item?id=48616800)

**背景**: IPv6 是 IPv4 的继任者，IPv4 使用 32 位地址，目前已几乎耗尽。IPv6 使用 128 位地址，提供了极大的地址空间。由于需要双栈运行、遗留硬件以及互联网服务提供商不愿投资新基础设施，过渡一直缓慢。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.ipxo.com/blog/ipv6-adoption-challenges-2025/">Why IPv6 Adoption Still Lags - ipxo.com</a></li>
<li><a href="https://aws.amazon.com/compare/the-difference-between-ipv4-and-ipv6/">IPv4 vs IPv6 - Difference Between Internet Protocol Versions - AWS</a></li>
<li><a href="https://www.geeksforgeeks.org/computer-networks/differences-between-ipv4-and-ipv6/">Difference Between IPv4 and IPv6 - GeeksforGeeks</a></li>

</ul>
</details>

**社区讨论**: 评论者指出了实际部署中的挑战：一家英国互联网服务提供商自 2011 年承诺以来仍未启用 IPv6；GitHub 缺乏 IPv6 支持；AWS 用户为 IPv4 地址付费，而互联网服务提供商缺乏升级动力。一些人指出，采用率高的地区（如法国）可以推动其他地区跟进。

**标签**: `#IPv6`, `#networking`, `#internet infrastructure`, `#adoption`

---

<a id="item-2"></a>
## [发布 GPT-2 Medium 规模的无 Softmax 注意力模型](https://www.reddit.com/r/MachineLearning/comments/1ubmybr/i_released_a_softmaxfree_attention_model_at_gpt2/) ⭐️ 8.0/10

发布了一个 GPT-2 Medium 规模（约 3.54 亿参数，在 115 亿 token 上训练）的无 Softmax 注意力模型，采用结构稀疏性和 tile-skipping 内核以节省长上下文 VRAM。模型权重和自定义 Triton 内核已开源。 这项工作通过移除计算和内存开销大的 Softmax 操作，解决了长上下文 Transformer 中的 VRAM 瓶颈。开源发布促进了高效注意力机制的进一步研究和实际部署。 该模型利用结构稀疏性在注意力计算中跳过不相关的 tile，从而减少内存使用。自定义 Triton 内核实现了 tile-skipping，以在 GPU 上高效执行。模型规模为 GPT-2 Medium（3.54 亿参数），在 115 亿 token 上训练。

reddit · r/MachineLearning · /u/NonGameCatharsis · 6月21日 10:46

**背景**: 标准 Transformer 注意力使用 Softmax 函数归一化注意力分数，需要计算所有查询-键点积并存储完整注意力矩阵，导致内存随序列长度二次增长。无 Softmax 注意力用更简单的归一化（如 L1 范数）替代 Softmax，减少计算和内存。结构稀疏性利用许多注意力分数接近零的模式，允许选择性计算。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2206.08898">SimA: Simple Softmax-free Attention for Vision Transformers</a></li>
<li><a href="https://arxiv.org/abs/2110.11945">SOFT: Softmax-free Transformer with Linear Complexity</a></li>
<li><a href="https://openreview.net/pdf?id=c4m0BkO4OL">Towards Structured Sparsity in Transformers for Efficient Inference</a></li>

</ul>
</details>

**社区讨论**: Reddit 社区赞扬了技术贡献和开源发布，讨论聚焦于这种规模下无 Softmax 注意力的新颖性以及 tile-skipping 对长上下文任务的实际好处。一些用户质疑与标准注意力相比的质量权衡。

**标签**: `#attention`, `#efficient transformers`, `#Triton kernels`, `#long-context`, `#open source`

---

<a id="item-3"></a>
### *（简报）* [你的 ATProto 身份归谁所有？提示：可能不是你](https://kevinak.se/blog/who-actually-owns-your-atproto-identity-hint-its-probably-not-you) ⭐️ 7.0/10

一篇批判性分析指出，依赖托管个人数据服务器（PDS）的 AT Protocol（如 Bluesky）用户可能并未真正掌控自己的身份，因为托管服务商掌握着其域名和数据的密钥。 这挑战了 AT Protocol 去中心化身份的承诺，凸显了理论所有权与实际控制之间的差距，尤其对非技术用户而言。它引发了关于托管 PDS 解决方案是否削弱了协议核心价值主张的讨论。 AT Protocol 使用基于 DNS 的句柄和 DID 来标识身份，但当用户的 PDS 由第三方托管时，该提供商可能更改句柄的 DNS 记录或控制 DID，从而实际上拥有该身份。在个人服务器上自托管 PDS 或使用 Cirrus 等服务可以恢复用户控制权。

---

<a id="item-4"></a>
### *（简报）* [用 APL 编写的 3D 体素游戏引擎](https://github.com/namgyaaal/avoxelgame) ⭐️ 7.0/10

一位开发者发布了一个有缺陷但诚实的热情项目：完全用 APL 编程语言实现的 3D 体素游戏引擎，已在 GitHub 上开源。 该项目展示了 APL 在 3D 图形方面的表达能力，挑战了 APL 仅适用于数学或金融应用的传统观念。同时，它凸显了该语言在操作体素世界方面的独特符号系统。 该引擎被描述为有缺陷且不完整，但它展示了 APL 面向数组的方法来处理体素数据。该项目是一个业余爱好作品，并非生产级工具。

---

<a id="item-5"></a>
### *（简报）* [对几何代数的批判性审视（2024）](https://alexkritchevsky.com/2024/02/28/geometric-algebra.html) ⭐️ 7.0/10

Alex Kritchevsky 在 2024 年发表的一篇文章对几何代数（GA）进行了批判性审视，认为其数学基础薄弱，并吸引了边缘从业者，引发了关于其实用价值与理论价值的讨论。 这一批判挑战了将 GA 作为物理学和工程学统一数学框架的日益增长的倡导，揭示了关于严谨性和社区动态的担忧，这些担忧影响了其在主流数学和应用领域的采纳。 文章批评 GA 与微分形式等既定形式相比缺乏严谨的基础，并指出其支持者通常包括具有非传统学术背景的人。社区评论揭示了数学家质疑 GA 的新颖性与实践者发现其实用性之间的分歧。

---

<a id="item-6"></a>
### *（简报）* [慢呼吸调节大脑功能与风险行为](https://www.cell.com/neuron/fulltext/S0896-6273(26)00339-9) ⭐️ 7.0/10

一项发表在《Neuron》上的研究表明，慢呼吸，尤其是延长呼气，通过副交感神经激活调节大脑活动并增加冒险行为。 这项研究将呼吸模式与大脑功能和决策直接联系起来，为通过自下而上的生理调节来管理焦虑、恐慌症和抑郁症提供了实际应用价值。 研究发现，延长呼气能选择性地增强奖赏反应，这或许可以解释为何慢呼吸能帮助克服公开演讲等情境中的非理性恐惧。

---

