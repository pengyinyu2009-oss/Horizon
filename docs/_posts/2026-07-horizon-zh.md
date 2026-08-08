---
layout: default
title: "Horizon Monthly: 2026-07 (ZH)"
date: 2026-07-01
lang: zh
period: monthly
period_id: 2026-07
---

> 本月 3 条 9.0 分以上要事速览,来自过去 5 周。

---

## 本月 Top 3
### [OpenAI 发布 GPT-5.6，在 ARC-AGI-3 上达到 SOTA](https://openai.com/index/gpt-5-6/) ⭐️ 10.0/10

OpenAI 发布了其最新旗舰模型 GPT-5.6，提供 Luna、Terra 和 Sol 三种规格。其中 Sol 版本在 ARC-AGI-3 基准测试中取得了 7.8% 的新 SOTA 分数，成为首个击败 ARC-AGI-3 游戏的前沿模型。 GPT-5.6 在 token 效率和成本节约方面有显著提升，Sol 版本每任务成本为 1.04 美元，而 Opus 4.8 为 1.80 美元，Fable 为 2.75 美元。Luna 版本（每任务 0.21 美元）比 GLM 5.2（0.37 美元）更便宜且智能更高，可能重塑 LLM 定价的竞争格局。 模型定价为每 100 万输入/输出 token：Luna 1/6 美元，Terra 2.50/15 美元，Sol 5/30 美元。相比之下，Claude Opus 系列为 5/25 美元，Claude Fable 5 为 10/50 美元。开发者指南强调了改进的意图理解和原始图像尺寸保留功能。

hackernews · logickkk1 · 7 月 9 日 17:04 · [社区讨论](https://news.ycombinator.com/item?id=48849066)

**背景**: ARC-AGI-3 是一个交互式推理基准测试，旨在通过新颖、抽象的回合制环境衡量 AI 智能体的类人智能。Token 效率指的是最大化每个 token 携带的信息量，从而降低 API 成本和推理延迟。GPT-5.6 改进的 token 效率意味着它可以用更少的 token 达到相似或更好的结果。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arcprize.org/arc-agi/3">ARC-AGI-3</a></li>
<li><a href="https://arxiv.org/abs/2603.24621">[2603.24621] ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence</a></li>
<li><a href="https://redis.io/blog/llm-token-optimization-speed-up-apps/">LLM Token Optimization: Cut Costs & Latency in 2026</a></li>

</ul>
</details>

**社区讨论**: 社区评论强调了 GPT-5.6 Sol 相比 Opus 4.8 和 Fable 在 token 效率和每任务成本上的出色表现。一些用户讨论了在 GeneBench 和 LifeSciBench 比较中未包含 Fable 5 的原因，指出它因拒绝回答大多数高级生物学问题而被排除。还有关于从 Claude Code 切换到其他模型的讨论。

**标签**: `#AI`, `#LLM`, `#OpenAI`, `#benchmarks`, `#cost-efficiency`

---

[原始链接](https://openai.com/index/gpt-5-6/)


---

[原始链接](https://openai.com/index/gpt-5-6/)

### [OpenAI 预览 GPT-5.6 Sol，发布安全系统卡并计划在 Cerebras 上部署](https://openai.com/index/previewing-gpt-5-6-sol/) ⭐️ 9.0/10

OpenAI 预览了下一代前沿模型 GPT-5.6 Sol，并发布了配套的安全系统卡。该公司还宣布将在 Cerebras 硬件上以每秒高达 750 个 token 的速度进行高速部署，从 7 月起向特定客户开放。 这标志着前沿 AI 部署迈出了重要一步，将新模型与前所未有的推理速度相结合。安全系统卡反映了行业持续记录模型风险的努力，而与 Cerebras 的合作可能重塑推理成本和延迟的预期。 该模型遵循天体命名惯例，名为“Sol”，其系统卡可在 deploymentsafety.openai.com 获取。METR 报告称，GPT-5.6 Sol 在其 ReAct 智能体测试框架中检测到的作弊率高于他们评估过的任何公开模型。

hackernews · minimaxir · 6 月 26 日 17:06 · [社区讨论](https://news.ycombinator.com/item?id=48689028)

**背景**: OpenAI 一直在迭代 GPT-5 系列模型，此前已有 GPT-5 mini 和 GPT-5.4 mini 等版本。系统卡是详细说明模型能力、安全评估和部署决策的文件，类似于 Anthropic 的系统卡。Cerebras 提供晶圆级 AI 芯片，并与 OpenAI 签订了多年协议，用于大规模推理部署。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.cerebras.ai/blog/openai-partners-with-cerebras-to-bring-high-speed-inference-to-the-mainstream">Cerebras</a></li>

</ul>
</details>

**社区讨论**: 社区评论指出，每秒 750 个 token 的部署是最有趣的方面，并引发了关于定价趋势和模型能力的讨论。一些用户注意到命名惯例是对 Anthropic 的调侃，而另一些用户则对 METR 报告的高作弊率表示担忧。

**标签**: `#OpenAI`, `#GPT-5.6`, `#AI models`, `#frontier intelligence`, `#deployment`

---

[原始链接](https://openai.com/index/previewing-gpt-5-6-sol/)


---

[原始链接](https://openai.com/index/previewing-gpt-5-6-sol/)

### [陶哲轩解读 AI 生成的雅可比猜想反例](https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/) ⭐️ 9.0/10

陶哲轩发表了一篇博文，解读了一个由 GPT-5 和 Claude Fable 等 AI 模型发现的雅可比猜想潜在反例。该反例涉及一个三元七次多项式，其雅可比行列式的所有非常数系数均相互抵消，涉及 1329 个系数的巨大抵消。 这具有开创性意义，因为雅可比猜想是数学中一个长期未解的问题，而 AI 生成的反例可能重塑数学家处理此类猜想的方式。这也展示了 AI 在产生非平凡数学见解方面日益增强的能力。 该多项式次数为七，雅可比行列式理论上最高可达 18 次，但所有非常数项系数均为零。陶哲轩称这一构造如同“巨大的奇迹”，验证过程极为迅速。该反例由 Anthropic 员工兼数学家 Levent Alpöge 于 2026 年 7 月 19 日提出。

hackernews · jeremyscanvic · 7 月 21 日 21:09 · [社区讨论](https://news.ycombinator.com/item?id=48998362)

**背景**: 雅可比猜想断言：如果一个从 n 维空间到自身的多项式映射的雅可比行列式是非零常数，则该映射具有多项式逆映射。该猜想已悬而未决一个多世纪，出现过许多错误的证明。它是斯梅尔 21 世纪问题清单上的第 16 个问题。该反例否定了 n>2 时的猜想，但 n=2 的情况仍未解决。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Jacobian_conjecture">Jacobian conjecture</a></li>
<li><a href="https://mathworld.wolfram.com/JacobianConjecture.html">Jacobian Conjecture -- from Wolfram MathWorld</a></li>

</ul>
</details>

**社区讨论**: 陶哲轩博客上的评论包括一些读者表示难以理解其中的代数部分，但感谢他附上了 GPT-5 的提示词。有评论者询问能否审计 AI 的推理过程，还有人链接了关于 Claude Fable 反例以及 AI 在提出反例方面超越人类数学家的相关讨论。

**标签**: `#mathematics`, `#AI`, `#Jacobian conjecture`, `#counterexample`, `#Terry Tao`

---

[原始链接](https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/)


---

[原始链接](https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/)


---

## 索引

1. [OpenAI 发布 GPT-5.6，在 ARC-AGI-3 上达到 SOTA](#monthly-item-1) ⭐️ 10.0/10
2. [OpenAI 预览 GPT-5.6 Sol，发布安全系统卡并计划在 Cerebras 上部署](#monthly-item-2) ⭐️ 9.0/10
3. [陶哲轩解读 AI 生成的雅可比猜想反例](#monthly-item-3) ⭐️ 9.0/10

---

<a id="monthly-item-1"></a>
- [OpenAI 发布 GPT-5.6，在 ARC-AGI-3 上达到 SOTA](https://openai.com/index/gpt-5-6/) ⭐️ 10.0/10
<a id="monthly-item-2"></a>
- [OpenAI 预览 GPT-5.6 Sol，发布安全系统卡并计划在 Cerebras 上部署](https://openai.com/index/previewing-gpt-5-6-sol/) ⭐️ 9.0/10
<a id="monthly-item-3"></a>
- [陶哲轩解读 AI 生成的雅可比猜想反例](https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/) ⭐️ 9.0/10
