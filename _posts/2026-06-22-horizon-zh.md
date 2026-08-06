---
layout: default
title: "Horizon Daily: 2026-06-22 (ZH)"
date: 2026-06-22
lang: zh
period: daily
period_id: 2026-06-22
---

> 从 25 条内容中筛选出 8 条重要资讯。

其中 **5 条 8 分以上**展开详细简报，其余 3 条仅列于索引。

---

1. [我过去的工作是否只因欺诈而存在？](#item-1) ⭐️ 8.0/10
2. [宁可重复代码，也不要错误的抽象（2016）](#item-2) ⭐️ 8.0/10
3. [Cloudflare 推出面向 AI 代理和开发者的临时账户功能](#item-3) ⭐️ 8.0/10
4. [矩阵循环单元更新：稳定性修复与局限性](#item-4) ⭐️ 8.0/10
5. [发布 GPT-2 Medium 规模的无 Softmax 注意力模型，开放权重](#item-5) ⭐️ 8.0/10
6. [Anthropic 对 Claude 的身份验证引发 AI 访问争议](#item-6) ⭐️ 7.0/10
7. [可销售软件的最小可行单元](#item-7) ⭐️ 7.0/10
8. [sqlite-utils 4.0rc1 新增迁移和嵌套事务功能](#item-8) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [我过去的工作是否只因欺诈而存在？](https://david.newgas.net/did-my-old-job-only-exist-because-of-fraud/) ⭐️ 8.0/10

一篇个人文章和社区讨论探讨了欺诈性计费和管理实践如何人为地膨胀 IT 岗位和成本，尤其是在政府和公司项目中。 这揭示了 IT 承包中的系统性欺诈，浪费纳税人和股东的资金，并对许多技术岗位的合法性提出了存在性问题。 作者回忆了个人经历，其中承包商通过外包公司以虚高费率被重新雇用，经理欺诈性地计费以耗尽预算。社区评论证实了在政府和公司环境中的类似模式。

hackernews · advisedwang · 6月21日 21:40 · [社区讨论](https://news.ycombinator.com/item?id=48622867)

**背景**: IT 领域的欺诈性计费包括幽灵计费、升级编码和重复计费等做法，即对未提供或夸大的服务进行计费。这些做法可能人为地维持本应被裁撤的岗位，导致低效和浪费。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://lawslearned.com/fraudulent-billing/">Understanding Fraudulent Billing: Legal Implications and ...</a></li>
<li><a href="https://lawslearned.com/fraudulent-billing-practices/">Understanding Fraudulent Billing Practices and Their Impact</a></li>

</ul>
</details>

**社区讨论**: 评论者分享了类似经历：一位英国银行的初级工程师看到承包商通过外包被重新雇用并加价；一位政府承包商发现他的经理欺诈性地编辑了他的工时表；其他人指出，帝国建设和欺诈往往是工作环境有毒的信号。

**标签**: `#fraud`, `#software engineering`, `#corporate culture`, `#government contracting`, `#IT management`

---

<a id="item-2"></a>
## [宁可重复代码，也不要错误的抽象（2016）](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction) ⭐️ 8.0/10

Sandi Metz 在 2016 年的文章中提出，过早或错误的抽象比代码重复更糟糕，开发者应等到看到足够多的重复后再引入抽象。 这篇文章已成为软件工程领域的经典参考文献，影响了开发者对重构和设计的思考方式。它挑战了“重复总是坏事”的常见教条，强调了错误抽象的成本。 该文章发表于 2016 年，在 Hacker News 上获得了 430 分和 297 条评论，社区参与度很高。它主张仅在抽象正确时才进行谨慎的重构，并警告不要过早优化。

hackernews · rafaepta · 6月21日 16:08 · [社区讨论](https://news.ycombinator.com/item?id=48620090)

**背景**: 在软件工程中，抽象是一种通过隐藏实现细节来降低复杂性的技术。然而，创建错误的抽象可能导致代码更难修改和理解。代码重复虽然常被视为坏味道，但有时是更安全的中间状态。

**社区讨论**: 评论者们就重复与抽象之间的权衡展开了辩论。一些人强调“单一真相来源”原则，认为违反该原则的重复应该被重构。另一些人指出函数式编程减少了重复问题，并且很难在看到足够多的重复之前判断一个抽象是否正确。

**标签**: `#software engineering`, `#code quality`, `#abstraction`, `#refactoring`, `#best practices`

---

<a id="item-3"></a>
## [Cloudflare 推出面向 AI 代理和开发者的临时账户功能](https://simonwillison.net/2026/Jun/21/temporary-cloudflare-accounts/#atom-everything) ⭐️ 8.0/10

Cloudflare 推出了临时、短暂的账户功能，开发者无需注册完整账户即可通过命令 'npx wrangler deploy --temporary' 部署 Workers 项目。部署后的项目可存活 60 分钟，并可通过认领来延长其生命周期。 该功能大幅降低了测试和原型开发无服务器应用的门槛，尤其适合需要快速部署和测试代码的 AI 代理。同时，它也帮助开发者免去账户管理负担，实现快速实验。 临时部署通过 Wrangler CLI 的 '--temporary' 标志创建，项目会被分配一个随机名称（如 'Educated Celery'）。认领页面包含倒计时器，显示项目过期前的剩余时间。

rss · Simon Willison · 6月21日 22:01

**背景**: Cloudflare Workers 是一个无服务器计算平台，允许开发者在 Cloudflare 的全球边缘网络上运行代码。Wrangler 是用于构建、测试和部署 Workers 项目的官方 CLI 工具。临时部署是一种在设定时间后自动过期的临时环境，常用于测试和 CI/CD 流水线。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://developers.cloudflare.com/workers/">Overview · Cloudflare Workers docs</a></li>
<li><a href="https://developers.cloudflare.com/workers/wrangler/">Wrangler · Cloudflare Workers docs</a></li>

</ul>
</details>

**标签**: `#Cloudflare`, `#serverless`, `#deployment`, `#AI agents`, `#developer tools`

---

<a id="item-4"></a>
## [矩阵循环单元更新：稳定性修复与局限性](https://www.reddit.com/r/MachineLearning/comments/1ubz5o8/an_update_on_matrix_recurrent_units_an_attention/) ⭐️ 8.0/10

作者重新审视了矩阵循环单元（MRU），这是一种线性时间的注意力替代方案，并通过改进输入状态矩阵的构建方法（包括使用矩阵指数/凯莱映射的斜对称矩阵、LDU 分解和 QR 分解）来解决训练不稳定性问题。 MRU 旨在用线性复杂度替代 Transformer 中的注意力机制，有望支持更长的序列和更低的内存占用。然而，实验表明 MRU 在 TinyStories 等较大数据集上表现不如 Transformer，凸显了线性时间架构在扩展性方面的挑战。 表现最佳的输入状态构建方法是 LDU 分解，并对 D 使用激活函数以确保行列式为 1。正交矩阵方法（凯莱映射、矩阵指数）表现不佳，表明剪切变换对学习至关重要。标量因子方法导致结果更差，表明模型在玩具数据集上存在“作弊”行为。

reddit · r/MachineLearning · /u/mikayahlevi · 6月21日 19:39

**背景**: 矩阵循环单元（MRU）是一种循环神经网络，它使用矩阵乘法而非向量运算来处理序列。它利用基于结合操作的并行扫描算法，在 GPU 等现代硬件上实现线性时间复杂度，这与 Transformer 中标准注意力机制的二次复杂度形成对比。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Recurrent_neural_network">Recurrent neural network - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Prefix_sum">Prefix sum - Wikipedia</a></li>
<li><a href="https://developer.nvidia.com/gpugems/gpugems3/part-vi-gpu-computing/chapter-39-parallel-prefix-sum-scan-cuda">Chapter 39. Parallel Prefix Sum (Scan) with CUDA | NVIDIA ...</a></li>

</ul>
</details>

**社区讨论**: 最初的 Reddit 帖子收到了关于矩阵状态边界和较大数据集训练不稳定的评论。作者的更新直接通过新的构建方法解决了这些问题，但鉴于 TinyStories 上的结果，社区可能仍对 MRU 的实际性能持怀疑态度。

**标签**: `#machine learning`, `#sequence modeling`, `#attention alternative`, `#recurrent neural networks`, `#linear-time architecture`

---

<a id="item-5"></a>
## [发布 GPT-2 Medium 规模的无 Softmax 注意力模型，开放权重](https://www.reddit.com/r/MachineLearning/comments/1ubmybr/i_released_a_softmaxfree_attention_model_at_gpt2/) ⭐️ 8.0/10

一个 GPT-2 Medium 规模（约 3.54 亿参数，在 115 亿 tokens 上训练）的无 Softmax 注意力模型已发布，采用结构稀疏性和 tile-skipping 内核以节省长上下文 VRAM。模型权重和自定义 Triton 内核均已开源。 这项工作通过消除 softmax 操作并引入高效稀疏模式，解决了长上下文 transformer 中的 VRAM 瓶颈。它可能使消费级 GPU 支持更长的序列，并激发对注意力替代方案的进一步研究。 该模型使用结构稀疏性跳过不相关的注意力块，并结合自定义 Triton 内核实现 tile-skipping 以减少内存使用。发布内容包括预训练权重和推理代码，但训练细节和完整基准测试尚未提供。

reddit · r/MachineLearning · /u/NonGameCatharsis · 6月21日 10:46

**背景**: 标准 transformer 注意力使用 softmax 函数归一化注意力分数，这需要计算所有查询-键点积并存储完整的注意力矩阵，导致内存随序列长度二次增长。无 softmax 注意力方法（如 SimA）用更简单的归一化（如ℓ1 范数）替代 softmax 以减少计算。transformer 中的结构稀疏性涉及以结构化模式剪枝权重或激活以提高效率。Tile-skipping 内核跳过预测为贡献可忽略的 tile（数据块）的处理，节省内存和计算。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://openaccess.thecvf.com/content/WACV2024/papers/Koohpayegani_SimA_Simple_Softmax-Free_Attention_for_Vision_Transformers_WACV_2024_paper.pdf">SimA: Simple Softmax-free Attention for Vision Transformers</a></li>
<li><a href="https://www.sciencedirect.com/science/article/pii/S092523122400239X">Sparsity in transformers: A systematic literature review</a></li>
<li><a href="https://github.com/deepseek-ai/TileKernels">GitHub - deepseek-ai/TileKernels: A kernel library written in tilelang · GitHub</a></li>

</ul>
</details>

**标签**: `#attention`, `#efficient transformers`, `#Triton kernels`, `#long-context`, `#open-source`

---

<a id="item-6"></a>
### *（简报）* [Anthropic 对 Claude 的身份验证引发 AI 访问争议](https://support.claude.com/en/articles/14328960-identity-verification-on-claude) ⭐️ 7.0/10

Anthropic 更新了支持页面，要求对某些 Claude 功能进行身份验证，用户需提交政府颁发的身份证件和由第三方 Persona Identities 处理的实时自拍。尽管该政策并非新规，但在美国限制外国访问先进 AI 模型的背景下重新引发关注。 这一验证要求，加上美国政府下令对外国用户禁用顶级模型，可能导致全球 AI 市场分裂，并推动国际用户转向非美国替代方案。这引发了对尖端 AI 公平获取以及 AI 治理地缘政治影响的担忧。 验证过程由 Persona 处理，该公司可能使用用户数据改进其防欺诈模型。OpenAI 也有类似政策，验证失败可能导致用户永久无法使用顶级模型。更新后的隐私政策将于 2026 年 7 月 8 日生效。

---

<a id="item-7"></a>
### *（简报）* [可销售软件的最小可行单元](https://brandur.org/minimum-viable-unit) ⭐️ 7.0/10

Brandur Leach 提出了“可销售软件的最小可行单元”这一概念——即当构建替代品的成本低于或等于购买成本时的临界点，即使 AI 降低了开发成本也是如此。 这一分析挑战了“AI 让构建软件几乎免费”的假设，指出构建可销售软件的真实成本仍然不为零，且往往高于预期，从而影响开发者和企业的“构建 vs 购买”决策。 文章定义了一个“可行区域”，在此区域内购买软件在经济上是合理的，并指出即使有了强大的 LLM，构建、维护和支持软件的工作量仍然很大。该概念通过使用 Linear 替代 Jira 等例子加以说明。

---

<a id="item-8"></a>
### *（简报）* [sqlite-utils 4.0rc1 新增迁移和嵌套事务功能](https://simonwillison.net/2026/Jun/21/sqlite-utils-40rc1/#atom-everything) ⭐️ 7.0/10

sqlite-utils 4.0rc1 是 4.0 版本的第一个候选发布版，新增了内置的数据库迁移功能以及通过保存点实现的嵌套事务支持。迁移系统移植自成熟的 sqlite-migrate 包，允许用户通过 Python 函数或命令行工具定义和应用数据库模式变更。 这一重大更新简化了使用 SQLite 的 Python 开发者的数据库模式管理，无需再依赖外部迁移工具。嵌套事务功能支持更安全、更模块化的数据库操作，对复杂工作流尤其有价值。 迁移通过 @migrations() 装饰的 Python 函数定义，并可通过 'sqlite-utils migrate' 命令行应用。该系统不支持反向迁移，错误应通过添加新的正向迁移来修复。嵌套事务使用 SQLite 保存点，允许在事务内部分回滚。

---

