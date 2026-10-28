---
layout: default
title: "Horizon Weekly: 2026-W37 (ZH)"
date: 2026-09-07
lang: zh
period: weekly
period_id: 2026-W37
---

> 本周 4 条 8.0 分以上要事速览,来自过去 7 天。

---

## 头条 — 必读
### [OpenAI 宣称攻克千禧年数学难题 Navier–Stokes 方程](https://www.reddit.com/r/MachineLearning/comments/1wavdi7/openal_says_it_has_cracked_one_of_maths/) ⭐️ 9.0/10 · 相关 3/10

OpenAI 宣布其一款尚未发布的内部模型驱动的智能体在约 88 小时内给出了 Navier–Stokes 方程光滑解存在性问题的证明，该问题是克雷数学研究所悬赏 100 万美元的七大千禧年难题之一。证明随后通过 GPT-6 Astra 用 Lean 形式化语言进行了 17 小时的额外验证，仅在这一个问题上智能体就交换了 270 万条消息，消耗约 1300 亿输出 token。 如果该证明通过同行评审，这将是千禧年难题首次被攻克，对数学和 AI 驱动的科学发现而言都是历史性里程碑。它同时也表明前沿 AI 智能体已经能够在重大挑战性问题上与学术研究团队一较高下，甚至可能后来居上，由此带来的研究归属、竞争伦理以及 AI 辅助数学的诚信问题都亟待回答。 OpenAI 表示，攻关工作始于 2026 年 9 月 1 日，彼时他们听说有两个千禧年难题已被解决；其智能体在所有尝试的问题上一共发送了 490 万条消息，消耗约 3000 亿输出 token，按 GPT-6 Astra 公开 API 价格估算成本约为 1500 万美元。该声明笼罩在纽约大学教授 Tristan Buckmaster 的指控之下：他与 Anthropic 员工 Levent Alpöge 合作近一年的相关工作据称在 OpenAI 启动自家智能体之前就已泄露，且 OpenAI 模型可能基于他们的 Codex 会话进行过训练或访问过其内容；OpenAI 给出的折中方案是邀请 Buckmaster 作为唯一作者撰写论文，但因 Alpöge 受雇于 Anthropic 而将其排除在外。

reddit · r/MachineLearning · /u/Shizuka_Kuze · 9 月 8 日 17:42

**背景**: Navier–Stokes 方程是一组描述流体运动的偏微分方程，虽然在工程与物理中应用广泛，但其在三维情形下的解是否始终光滑（或如 OpenAI 所声称会出现奇点）至今缺少严格证明，这一问题已悬而未决数十年。千禧年难题由克雷数学研究所于 2000 年设立，共有七道著名数学难题，每题悬赏 100 万美元，截至目前只有庞加莱猜想被官方认定为已被解决。

**对中国影响**: 中国的前沿 AI 实验室与数学界如今面临追赶此处展示的智能体式研究能力的压力，尤其考虑到 OpenAI 的系统据称可能基于竞争对手的会话数据进行训练，这背后存在明显的竞争含义。此次围绕研究归属的争议，也为国内机构倡导建立 AI 辅助数学发表与数据使用透明度方面的国际规范，提供了一个清晰的契机。

**对我有什么用**: 对于电子工程师或硬件开发者而言，这条新闻本身并不直接可操作，但它预示着一个新时代——AI 智能体能够自主驱动长达数天的多步骤技术研究与验证流程，而这种模式很可能会率先出现在 EDA、芯片设计验证以及嵌入式固件的形式化方法领域。如果你大量使用 AI 编程智能体，这条新闻值得留意：它表明“智能体工时 × token 预算”将成为一种常规的工程计量单位，成本模型也更接近高性能计算，而非交互式对话。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Millennium_Prize_Problems">Millennium Prize Problems - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Clay_Mathematics_Institute">Clay Mathematics Institute - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 社区反应明显分裂：peri-cl 转引了陶哲轩的警告，称只要听说有人在攻克某道难题，就可能触发一场大规模 AI 竞赛，在原始研究尚未成熟前就将其“压平”，这可能让研究者不愿再公开分享有前景的方向。pavel_lishin 等人则聚焦于 Buckmaster 声明中所涉及的严重抄袭嫌疑；arctic-true 指出，在这场风波之下，OpenAI 一款训练不到两周的内部模型在数学能力上似乎是公开版 Astra 的两倍多——即便仅限于数学领域，这也是惊人的能力跃升。hdivider 则提醒说，自然科学并不总是纯计算问题，AI 在形式化数学上的成功未必能直接迁移到物理或实验领域。

**标签**: `#OpenAI`, `#mathematics`, `#Navier-Stokes`, `#millennium-problem`, `#AI-breakthrough`

---

[原始链接](https://www.reddit.com/r/MachineLearning/comments/1wavdi7/openal_says_it_has_cracked_one_of_maths/)


---

## 索引

1. [OpenAI 宣称攻克千禧年数学难题 Navier–Stokes 方程](#weekly-item-1) ⭐️ 9.0/10 · 相关 3/10
2. [AlphaGenome Atlas：高分辨率人类 DNA 突变预测图谱](#weekly-item-2) ⭐️ 8.0/10 · 相关 3/10
3. [OpenAI 发布 Navier-Stokes 成果，附 Lean 4 形式化证明](#weekly-item-3) ⭐️ 8.0/10 · 相关 3/10
4. [微软正式将 Rust 列为 tier-1 级别语言](#weekly-item-4) ⭐️ 8.0/10 · 相关 5/10

---

<a id="weekly-item-1"></a>
- [OpenAI 宣称攻克千禧年数学难题 Navier–Stokes 方程](https://www.reddit.com/r/MachineLearning/comments/1wavdi7/openal_says_it_has_cracked_one_of_maths/) ⭐️ 9.0/10 · 相关 3/10
<a id="weekly-item-2"></a>
- [AlphaGenome Atlas：高分辨率人类 DNA 突变预测图谱](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/alphagenome-atlas/) ⭐️ 8.0/10 · 相关 3/10
<a id="weekly-item-3"></a>
- [OpenAI 发布 Navier-Stokes 成果，附 Lean 4 形式化证明](https://www.johndcook.com/blog/2026/09/09/formal-method-revolution/) ⭐️ 8.0/10 · 相关 3/10
<a id="weekly-item-4"></a>
- [微软正式将 Rust 列为 tier-1 级别语言](https://rustfoundation.org/media/guest-post-rust-is-tier-1-language-at-microsoft/) ⭐️ 8.0/10 · 相关 5/10
