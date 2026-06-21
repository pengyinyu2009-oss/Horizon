---
layout: default
title: "Horizon Daily: 2026-06-21 (ZH)"
date: 2026-06-21
lang: zh
period: daily
period_id: 2026-06-21
---

> 从 19 条内容中筛选出 6 条重要资讯。

其中 **3 条 8 分以上**展开详细简报，其余 3 条仅列于索引。

---

1. [代码重复比错误抽象更廉价](#item-1) ⭐️ 8.0/10
2. [开发者不理解 CORS（2019）](#item-2) ⭐️ 8.0/10
3. [GPT-2 Medium 规模的无 Softmax 注意力模型，配备自定义 Triton 内核](#item-3) ⭐️ 8.0/10
4. [Anthropic 要求 Claude 用户进行身份验证，失败将永久锁定引发争议](#item-4) ⭐️ 7.0/10
5. [慢呼吸调节大脑功能与冒险行为](#item-5) ⭐️ 7.0/10
6. [探索在 LoRA 适配器上使用 EMA 进行自蒸馏](#item-6) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [代码重复比错误抽象更廉价](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction) ⭐️ 8.0/10

Sandi Metz 认为，代码重复往往比创建错误的抽象更廉价，这挑战了应始终避免重复的传统观点。 这一见解帮助开发者在何时抽象与何时重复之间做出更好的决策，从而减少技术债务并提高代码可维护性。 文章强调，过早的抽象可能导致代码僵化、难以修改，而重复则保持灵活性，直到正确的抽象变得清晰。

hackernews · rafaepta · 6月21日 16:08 · [社区讨论](https://news.ycombinator.com/item?id=48620090)

**背景**: 在软件工程中，抽象是将复杂性隐藏在简单接口背后的实践，而代码重复则是在多个地方复制相似的代码。这场争论的核心在于维护重复代码的成本与设计不良的抽象成本之间的权衡。

**社区讨论**: 评论者普遍认为平衡是关键，一些人指出重复在小规模下可以接受，但在大规模下会带来问题。其他人则警告不要教条地坚持任何极端。

**标签**: `#software engineering`, `#code quality`, `#abstraction`, `#technical debt`, `#best practices`

---

<a id="item-2"></a>
## [开发者不理解 CORS（2019）](https://fosterelli.co/developers-dont-understand-cors) ⭐️ 8.0/10

一篇 2019 年的文章指出许多开发者误解了 CORS，而 Hacker News 上的评论区通过激烈的辩论和更正，讽刺地证明了这一观点。 这凸显了开发者中普遍存在的 Web 安全知识缺口，可能导致不安全的应用程序。该文章及其讨论为开发者社区提供了宝贵的学习资源。 该文章的论点被评论区所证实，许多评论包含对 CORS 的误解，例如将其与服务器端访问控制混淆。讨论还揭示了关于预检请求和特定标头用途的困惑。

hackernews · toilet · 6月21日 01:35 · [社区讨论](https://news.ycombinator.com/item?id=48614844)

**背景**: CORS（跨源资源共享）是一种浏览器安全机制，控制来自一个源的网页如何请求另一个源的资源。它使用诸如 Access-Control-Allow-Origin 之类的 HTTP 标头，以受控方式放宽同源策略。许多开发者错误地认为 CORS 保护服务器，但实际上它保护用户的浏览器免受恶意脚本的攻击。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS">Cross-Origin Resource Sharing ( CORS ) - HTTP | MDN</a></li>
<li><a href="https://medium.com/codex/understanding-cors-cross-origin-resource-sharing-a-guide-for-developers-a15ff3d7b69c">Understanding CORS (Cross-Origin Resource Sharing)... | Medium</a></li>
<li><a href="https://shanechang.com/p/understanding-cors-developers-journey/">Understanding CORS : A Developer's Journey from Confusion to Clarity</a></li>

</ul>
</details>

**社区讨论**: 评论区参与度很高，用户指出文章本身和其他评论中的错误，证明了作者的观点。一些用户推荐 MDN 文档以获得正确理解，而另一些用户则对开发者中的困惑程度表示惊讶。

**标签**: `#CORS`, `#web security`, `#developer misconceptions`, `#HTTP`

---

<a id="item-3"></a>
## [GPT-2 Medium 规模的无 Softmax 注意力模型，配备自定义 Triton 内核](https://www.reddit.com/r/MachineLearning/comments/1ubmybr/i_released_a_softmaxfree_attention_model_at_gpt2/) ⭐️ 8.0/10

作者发布了一个 GPT-2 Medium 规模（约 3.54 亿参数，在 115 亿 token 上训练）的无 Softmax 注意力模型，利用结构稀疏性和 tile-skipping 内核来降低长上下文推理时的显存占用。该模型和自定义 Triton 内核均已开源。 这项工作展示了标准 Softmax 注意力的实用替代方案，有望以更低的内存成本支持更长的上下文长度。开源发布使社区能够尝试并在此基础上进一步发展。 该模型在自定义 Triton 内核中利用结构稀疏性和 tile-skipping 来跳过无关的注意力计算，从而节省显存。该方法在合理规模（3.54 亿参数，115 亿 token）上得到应用，表明其可以有效地训练和部署。

reddit · r/MachineLearning · /u/NonGameCatharsis · 6月21日 10:46

**背景**: 标准 Transformer 注意力使用 Softmax 操作来归一化注意力分数，对于长序列而言计算成本高且内存占用大。无 Softmax 注意力用更简单的归一化（如 L1 范数）替代 Softmax 以提高效率。Triton 是一种基于 Python 的语言和编译器，用于编写高性能 GPU 内核，可实现结构稀疏性和 tile-skipping 等自定义优化。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://triton-lang.org/main/index.html">Welcome to Triton's documentation!</a></li>
<li><a href="https://arxiv.org/abs/2206.08898">[2206.08898] SimA: Simple Softmax-free Attention for Vision Transformers</a></li>
<li><a href="https://www.emergentmind.com/topics/block-sparse-and-tile-approaches">Block- Sparse & Tile Approaches</a></li>

</ul>
</details>

**社区讨论**: 社区讨论内容充实，涉及无 Softmax 方法和 Triton 内核实现的技术问题。作者积极参与，解释了设计选择和潜在局限性。

**标签**: `#attention`, `#efficiency`, `#open-source`, `#Triton`, `#long-context`

---

<a id="item-4"></a>
### *（简报）* [Anthropic 要求 Claude 用户进行身份验证，失败将永久锁定引发争议](https://support.claude.com/en/articles/14328960-identity-verification-on-claude) ⭐️ 7.0/10

Anthropic 更新了隐私政策，要求 Claude 用户通过第三方服务 Persona 进行身份验证。验证失败的用户将被永久锁定，无法再次尝试使用顶级模型。 这一政策变化引发了严重的隐私和可访问性担忧，用户需要提供政府颁发的身份证件和生物识别数据。同时，它也引发了关于 AI 中立性的讨论，批评者将其比作互联网审查。 验证由 Persona 处理，该服务此前因用户反对被 Discord 弃用。Anthropic 表示，除法律要求外，身份数据不会与第三方共享。

---

<a id="item-5"></a>
### *（简报）* [慢呼吸调节大脑功能与冒险行为](https://www.cell.com/neuron/fulltext/S0896-6273(26)00339-9) ⭐️ 7.0/10

一项发表在《神经元》上的新研究揭示，慢呼吸，尤其是延长呼气，能激活副交感神经系统并增加人类的冒险行为。 这一发现挑战了放松技巧总是降低冒险行为的普遍假设，并表明慢呼吸可用于增强在公开演讲或不确定性决策等情境中的信心。 该研究特别发现，延长呼气呼吸选择性地增强了奖赏反应性，这对涉及适应不良奖赏处理的焦虑症、惊恐障碍和抑郁症等临床状况具有重要意义。

---

<a id="item-6"></a>
### *（简报）* [探索在 LoRA 适配器上使用 EMA 进行自蒸馏](https://www.reddit.com/r/MachineLearning/comments/1ubv0f5/ema_on_lora_r/) ⭐️ 7.0/10

一位 Reddit 用户询问关于在 LoRA 适配器上使用指数移动平均（EMA）作为自教师进行在线自蒸馏的论文或实证结果，并引用了 SDFT 论文（arXiv:2601.19897），该论文使用了 EMA 但采用的是全参数微调。 该问题涉及参数高效微调中的一个实际空白：将基于 EMA 的自蒸馏与 LoRA 结合，可以在保持性能的同时降低内存和计算成本，这对部署大型模型的从业者很有价值。 用户特别要求在线自蒸馏，即 EMA 适配器为可训练适配器生成软标签，而非离线方法。他们指出 SDFT 使用了 EMA，但采用的是全参数微调，而非 LoRA。

---

