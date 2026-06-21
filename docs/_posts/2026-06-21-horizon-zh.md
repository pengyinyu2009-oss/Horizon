---
layout: default
title: "Horizon Daily: 2026-06-21 (ZH)"
date: 2026-06-21
lang: zh
period: daily
period_id: 2026-06-21
---

> 从 19 条内容中筛选出 7 条重要资讯。

其中 **4 条 8 分以上**展开详细简报，其余 3 条仅列于索引。

---

1. [宁可重复代码，也不要错误的抽象（2016）](#item-1) ⭐️ 8.0/10
2. [Peter Norvig 的经典教程：用 Python 写 Lisp 解释器](#item-2) ⭐️ 8.0/10
3. [开发者不理解 CORS（2019）](#item-3) ⭐️ 8.0/10
4. [发布 GPT-2 中等规模的免 Softmax 注意力模型](#item-4) ⭐️ 8.0/10
5. [Anthropic 要求 Claude 用户进行身份验证](#item-5) ⭐️ 7.0/10
6. [用 APL 编写的 3D 体素游戏引擎](#item-6) ⭐️ 7.0/10
7. [矩阵循环单元更新：稳定性修复与性能分析](#item-7) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [宁可重复代码，也不要错误的抽象（2016）](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction) ⭐️ 8.0/10

Sandi Metz 在 2016 年的博文中指出，过早的抽象比代码重复更糟糕，主张在出现清晰正确的抽象之前先容忍重复。 这篇文章挑战了软件工程中“代码重复总是坏事”的常见教条，提供了更细致的视角，有助于做出更好的设计决策和编写可维护的代码。 文章强调，错误抽象的成本（复杂性、间接性）通常超过重复的成本，而重复可以作为发现正确抽象的垫脚石。

hackernews · rafaepta · 6月21日 16:08 · [社区讨论](https://news.ycombinator.com/item?id=48620090)

**背景**: 在软件工程中，抽象是一种通过隐藏实现细节来降低复杂性的技术。然而，在完全理解问题之前过早创建抽象，可能导致代码僵化且难以修改。重复虽然常被视为代码坏味道，但在正确抽象尚不明确时，可以是一种务实的选择。

**社区讨论**: 社区讨论涉及单一真相来源、函数式编程减少重复以及过度工程化常量的危险。评论者普遍赞同文章的前提，但补充了关于何时可以接受重复的细微差别。

**标签**: `#software engineering`, `#abstraction`, `#code duplication`, `#refactoring`, `#best practices`

---

<a id="item-2"></a>
## [Peter Norvig 的经典教程：用 Python 写 Lisp 解释器](https://norvig.com/lispy.html) ⭐️ 8.0/10

Peter Norvig 于 2010 年发布的教程《如何用 Python 写一个 Lisp 解释器》在 Hacker News 上再次引发讨论，凸显了其作为解释器入门教程的持久价值。 该教程被广泛认为是学习编程语言和解释器工作原理的最佳入门资源之一，影响了无数开发者。 该教程用大约 100 行 Python 3 代码实现了一个名为 Lispy（lis.py）的类 Scheme Lisp 解释器，涵盖了解析、求值和环境等核心概念。

hackernews · tosh · 6月21日 15:36 · [社区讨论](https://news.ycombinator.com/item?id=48619831)

**背景**: Lisp 是一族编程语言，以其独特的全括号前缀表示法著称，最早于 20 世纪 50 年代末定义。解释器是直接执行代码而不需要预先编译的程序，是计算机科学中的基本概念。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://norvig.com/lispy.html">(How to Write a (Lisp) Interpreter (in Python))</a></li>
<li><a href="https://en.wikipedia.org/wiki/Lisp_(programming_language)">Lisp (programming language) - Wikipedia</a></li>
<li><a href="https://github.com/fluentpython/lispy">GitHub - fluentpython/lispy: Learning with Peter Norvig's lis.py interpreter · GitHub</a></li>

</ul>
</details>

**社区讨论**: 社区成员称赞该教程是编写编程语言的绝佳起点，有人指出它与《Crafting Interpreters》相辅相成。还有人分享了个人实现 Lisp 的经历。

**标签**: `#Lisp`, `#Python`, `#interpreters`, `#tutorial`, `#programming languages`

---

<a id="item-3"></a>
## [开发者不理解 CORS（2019）](https://fosterelli.co/developers-dont-understand-cors) ⭐️ 8.0/10

一篇 2019 年来自 fosterelli.co 的文章指出开发者对 CORS 普遍存在误解，而随后 Hacker News 上的讨论揭示了更深层的误解，许多评论者错误地认为 CORS 提供了服务器端的访问控制。 CORS 是一个关键的 Web 安全机制，但普遍的误解会导致配置错误，从而增加 CSRF 等安全风险。这篇文章及其讨论凸显了加强开发者对 Web 安全基础知识教育的必要性。 文章本身可能对 CORS 的描述有误，一位评论者指出 CORS 实际上并不限制哪些源可以发送请求，它只控制浏览器是否暴露响应。讨论还凸显了 CORS 和 CSRF 之间的混淆，许多开发者不理解威胁模型。

hackernews · toilet · 6月21日 01:35 · [社区讨论](https://news.ycombinator.com/item?id=48614844)

**背景**: CORS（跨源资源共享）是一种浏览器机制，允许对位于给定域之外的资源进行受控访问。它通过 HTTP 头告诉浏览器是否允许网页访问来自不同源的资源。一个常见的误解是 CORS 提供了针对跨源攻击（如 CSRF）的安全性，但实际上，CORS 是对同源策略的放宽，并不防止请求伪造，它只控制响应的共享。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://portswigger.net/web-security/cors/access-control-allow-origin">CORS and the Access-Control-Allow-Origin response header</a></li>
<li><a href="https://medium.com/@info_89273/understanding-cors-why-browsers-block-your-requests-f7c668251a37">Understanding CORS : Why Browsers Block Your Requests? | Medium</a></li>

</ul>
</details>

**社区讨论**: Hacker News 上的评论对文章和彼此都提出了严厉批评。一些评论者认为文章本身误解了 CORS，而另一些人则指出讨论证明了作者关于普遍混淆的观点。少数人建议阅读 MDN 文档以正确理解 CORS 和同源策略。

**标签**: `#CORS`, `#web security`, `#developer misconceptions`, `#HTTP`, `#browser security`

---

<a id="item-4"></a>
## [发布 GPT-2 中等规模的免 Softmax 注意力模型](https://www.reddit.com/r/MachineLearning/comments/1ubmybr/i_released_a_softmaxfree_attention_model_at_gpt2/) ⭐️ 8.0/10

发布了一个 GPT-2 中等规模（约 3.54 亿参数，在 115 亿 token 上训练）的免 Softmax 注意力模型，采用结构稀疏性和瓦片跳过内核以节省长上下文 VRAM。该模型包含开放权重和自定义 Triton 内核。 这项工作表明免 Softmax 注意力可以扩展到中等规模的语言模型，可能减少长上下文任务的内存使用。开源发布有助于进一步研究高效 LLM 推理的实际应用。 该模型使用结构稀疏性和瓦片跳过内核来避免计算零瓦片，从而为长序列节省 VRAM。提供了自定义 Triton 内核以实现高效实现。

reddit · r/MachineLearning · /u/NonGameCatharsis · 6月21日 10:46

**背景**: 免 Softmax 注意力用更简单的操作（如ℓ1 范数）替代标准 softmax 归一化，降低计算成本。Triton 是一种用于编写高效神经网络内核的开源 GPU 编程语言。结构稀疏性利用稀疏矩阵中的模式跳过不必要的计算。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://openai.com/index/triton/">Introducing Triton: Open-source GPU programming for neural networks | OpenAI</a></li>
<li><a href="https://arxiv.org/abs/2206.08898">[2206.08898] SimA: Simple Softmax-free Attention for Vision Transformers</a></li>
<li><a href="https://github.com/triton-lang/triton">GitHub - triton-lang/triton: Development repository for the Triton language and compiler · GitHub</a></li>

</ul>
</details>

**社区讨论**: Reddit 讨论包括关于免 Softmax 方法的技术问题和作者的回复，显示出对该方法有效性及潜在改进的兴趣。

**标签**: `#attention`, `#LLM`, `#Triton`, `#open-source`, `#efficiency`

---

<a id="item-5"></a>
### *（简报）* [Anthropic 要求 Claude 用户进行身份验证](https://support.claude.com/en/articles/14328960-identity-verification-on-claude) ⭐️ 7.0/10

Anthropic 宣布用户必须使用政府颁发的身份证件进行身份验证才能访问 Claude，理由是为了合规和安全。 这一政策变化引发了重大的隐私担忧，并可能限制非美国用户的访问，从而可能重塑 AI 服务的竞争格局。 验证过程由第三方提供商处理，验证失败可能导致永久无法使用顶级模型，这与 OpenAI 的政策类似。

---

<a id="item-6"></a>
### *（简报）* [用 APL 编写的 3D 体素游戏引擎](https://github.com/namgyaaal/avoxelgame) ⭐️ 7.0/10

一位开发者发布了一个用 APL 完全编写的 3D 体素游戏引擎，虽然存在一些错误但引人入胜，该项目已在 GitHub 上开源。它展示了 APL 的数组导向符号在体素世界建模中的应用。 该项目极具创新性，因为 APL 很少被用于游戏引擎，这展示了该语言的表达力和简洁性。它引发了人们对使用数组导向语言进行实时 3D 图形开发时所面临的挑战和性能权衡的好奇。 该引擎被描述为存在错误，是一个兴趣项目，其 README 文件诚实地说明了其局限性。社区成员询问了与用 C++或 Rust 编写的引擎的性能对比。

---

<a id="item-7"></a>
### *（简报）* [矩阵循环单元更新：稳定性修复与性能分析](https://www.reddit.com/r/MachineLearning/comments/1ubz5o8/an_update_on_matrix_recurrent_units_an_attention/) ⭐️ 7.0/10

矩阵循环单元的作者更新了架构，通过引入新的输入状态矩阵构建方法（包括斜对称、LDU 和 QR 分解）来解决训练不稳定性问题，并在 shakespeare-char 和 TinyStories 数据集上进行了评估。 这项工作探索了一种线性时间复杂度的注意力替代方案，对于高效序列建模（尤其是长序列）至关重要。稳定性改进和性能比较为循环架构的发展提供了宝贵见解。 MRU 使用并行关联扫描实现高效计算。作者发现强制输入状态正交（通过 Cayley 映射或矩阵指数）会损害性能，表明剪切变换很重要。在 TinyStories 上，MRU 的表现不如 Transformer 基线。

---

