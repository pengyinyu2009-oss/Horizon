---
layout: default
title: "Horizon Daily: 2026-08-31 (ZH)"
date: 2026-08-31
lang: zh
period: daily
period_id: 2026-08-31
---

> 从 15 条内容中筛选出 3 条重要资讯。

其中 **0 条 8 分以上**展开详细简报，其余 3 条仅列于索引。

---

1. [通过复制到虚拟机错误报告反向通道在 QubesOS 中实现任意代码执行](#item-1) ⭐️ 7.0/10 · 相关 3/10
2. [Simon Willison 深度拆解 ChatGPT Work 的两大独立产品形态](#item-2) ⭐️ 7.0/10 · 相关 5/10
3. [AI 智能体在多智能体环境中自主发现新数学结果](#item-3) ⭐️ 7.0/10 · 相关 4/10

---

<a id="item-1"></a>
### *（简报）* [通过复制到虚拟机错误报告反向通道在 QubesOS 中实现任意代码执行](https://www.qubes-os.org/news/2026/08/29/qsb-118/) ⭐️ 7.0/10 · 相关 3/10

QubesOS 披露严重安全漏洞 QSB-118，攻击者可通过 Dom0 中 qvm-copy-to-vm 的错误报告回传通道实现任意代码执行。

---

<a id="item-2"></a>
### *（简报）* [Simon Willison 深度拆解 ChatGPT Work 的两大独立产品形态](https://simonwillison.net/2026/Aug/30/understanding-chatgpt-work/) ⭐️ 7.0/10 · 相关 5/10

Simon Willison 发表了对 OpenAI 旗下 ChatGPT Work 的深度分析文章，指出该产品实际上由两个独立产品组成：Work Cloud（通过 chatgpt.com 网页和移动端 App 使用）以及 Work Local（通过原名 Codex 的桌面客户端使用）。他归纳出 Work 相对于普通 Chat 的七项关键差异，包括可选 Luna、Terra、Sol 等模型、具备联网能力的代码执行环境、无头 Chrome 浏览器、跨会话持久化共享文件系统、发布 ChatGPT Sites 站点的能力、子智能体会话调度以及定时任务自动化。 ChatGPT Work 标志着 OpenAI 希望将 ChatGPT 从“问答工具”升级为能够端到端交付成果的生产力中枢。通过将产品拆分为云端智能体与本地类 Codex 智能体两条线，OpenAI 正在押注于能够自主读取文件、运行代码、浏览网页，并交付成稿 PPT、电子表格、分析报告等成品文档的自动化 AI 工作流。 Work Cloud 仅对付费用户（每月 20 美元及以上档位）开放，并且调用的是 Codex 额度而不是普通 Chat 额度，这可能正解释了不同模型在不同入口的可用性差异。模型方面提供 GPT-5.6 的 Sol、Luna、Terra 三档，每档都覆盖 Light 到 Ultra 的推理强度，外加 GPT-5.5；其中 5.6 Pro 仅出现在 Chat 入口，Work 没有对应版本。Simon 还指出 Ultra 推理档位会激进地委派给子智能体，这解释了它较高的算力消耗。

---

<a id="item-3"></a>
### *（简报）* [AI 智能体在多智能体环境中自主发现新数学结果](https://www.reddit.com/r/MachineLearning/comments/1w2fl67/r_autonomous_mathematical_discovery_in_an/) ⭐️ 7.0/10 · 相关 4/10

研究者在名为"Station"的开放世界多智能体环境中部署了来自不同模型家族的 AI 代理，整个系统没有中心协调器。在 AlphaEvolve 目录中的 12 个构造问题及 2 个案例研究上，代理们在 5 个问题上取得了相对于已有文献的新颖结果，包括有限域 Kakeya 集的新无穷族、11 维中精确的 604 点 kissing 配置，以及对 Erdős 最小重叠问题的实质性改进下界。 这项工作表明，去中心化、异构的 AI 代理能够自主完成可发表的数学研究——不仅产出数值答案，还能撰写人类数学家可以继续推进的定理与分析。它让 AI 从被动工具转变为主动科研协作者，对未来科研工作流的组织方式具有深远影响。 与 DeepMind 的 AlphaEvolve 等固定进化管线不同，Station 不使用任何脚本式协调器：代理自主选择研究方向、相互协作，并共同建设共享文献。研究团队已在 GitHub（dualverse-ai/station）开源了全部代理对话、证明与验证代码，以保证完全透明。

---

