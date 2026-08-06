---
layout: default
title: "Horizon Weekly: 2026-W28 (ZH)"
date: 2026-07-06
lang: zh
period: weekly
period_id: 2026-W28
---

> 本周 24 条 8.0 分以上要事速览,来自过去 7 天。

---

## 头条 — 必读
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

## 索引

1. [OpenAI 发布 GPT-5.6，在 ARC-AGI-3 上达到 SOTA](#weekly-item-1) ⭐️ 10.0/10
2. [Bun 用 AI 将运行时从 Zig 重写为 Rust](#weekly-item-2) ⭐️ 9.0/10
3. [智能体安全触发器无法抵御工具调用攻击](#weekly-item-3) ⭐️ 9.0/10
4. [欧盟议会通过聊天控制 1.0，允许大规模扫描私密消息](#weekly-item-4) ⭐️ 9.0/10
5. [数字游戏 vs 实体游戏：核心问题是所有权](#weekly-item-5) ⭐️ 8.0/10
6. [突尼斯达里加语（Arabizi）开源机器翻译管线发布](#weekly-item-6) ⭐️ 8.0/10
7. [Competence Gate：基于内部置信度控制工具使用的 Qwen3.5-4B 适配器](#weekly-item-7) ⭐️ 8.0/10
8. [OpenWrt One：开源硬件路由器发布](#weekly-item-8) ⭐️ 8.0/10
9. [Anthropic 发现语言模型中的全局工作空间](#weekly-item-9) ⭐️ 8.0/10
10. [腾讯发布 Hy3：295B 参数 MoE 模型，采用 Apache 2.0 许可](#weekly-item-10) ⭐️ 8.0/10
11. [LingBot-Vision：用于自监督预训练的掩码边界建模](#weekly-item-11) ⭐️ 8.0/10
12. [TRACE：开源层次化记忆系统助力 LLM 智能体在 MemoryAgentBench 上达到 82.5%](#weekly-item-12) ⭐️ 8.0/10
13. [CPU TTS 基准测试：Kokoro、Supertonic、Inflect-Nano 与 Pocket TTS 对比](#weekly-item-13) ⭐️ 8.0/10
14. [Mistral 发布 Robostral Navigate，一款最先进的机器人导航模型](#weekly-item-14) ⭐️ 8.0/10
15. [Grok 4.5：更便宜、更快，但信任问题笼罩](#weekly-item-15) ⭐️ 8.0/10
16. [微软发布 Flint，一种面向 AI 代理的可视化语言](#weekly-item-16) ⭐️ 8.0/10
17. [OpenAI 推出 GPT-Live：全双工语音模式，可委托 GPT-5.5 处理任务](#weekly-item-17) ⭐️ 8.0/10
18. [LingBot-Video：开源稀疏 MoE 视频扩散世界模型](#weekly-item-18) ⭐️ 8.0/10
19. [用 Rust 重写的 Postgres 通过全部回归测试](#weekly-item-19) ⭐️ 8.0/10
20. [美军后勤体系面临下一场大战崩溃风险](#weekly-item-20) ⭐️ 8.0/10
21. [Meta 推出付费智能体 AI 模型 Muse Spark 1.1](#weekly-item-21) ⭐️ 8.0/10
22. [苹果起诉 OpenAI，指控前员工窃取商业机密](#weekly-item-22) ⭐️ 8.0/10
23. [GPT-5.6 Sol Ultra 声称证明了圈双覆盖猜想](#weekly-item-23) ⭐️ 8.0/10
24. [VultronRetriever 模型登顶 MTEB 排行榜，效率大幅提升](#weekly-item-24) ⭐️ 8.0/10

---

<a id="weekly-item-1"></a>
- [OpenAI 发布 GPT-5.6，在 ARC-AGI-3 上达到 SOTA](https://openai.com/index/gpt-5-6/) ⭐️ 10.0/10
<a id="weekly-item-2"></a>
- [Bun 用 AI 将运行时从 Zig 重写为 Rust](https://bun.com/blog/bun-in-rust) ⭐️ 9.0/10
<a id="weekly-item-3"></a>
- [智能体安全触发器无法抵御工具调用攻击](https://www.reddit.com/r/MachineLearning/comments/1ur1fnz/agentic_safety_triggers_arent_textual_safety/) ⭐️ 9.0/10
<a id="weekly-item-4"></a>
- [欧盟议会通过聊天控制 1.0，允许大规模扫描私密消息](https://www.patrick-breyer.de/en/eu-parliament-greenlights-chat-control-1-0-breyer-our-children-lose-out/) ⭐️ 9.0/10
<a id="weekly-item-5"></a>
- [数字游戏 vs 实体游戏：核心问题是所有权](https://popcar.bearblog.dev/its-about-ownership/) ⭐️ 8.0/10
<a id="weekly-item-6"></a>
- [突尼斯达里加语（Arabizi）开源机器翻译管线发布](https://www.reddit.com/r/MachineLearning/comments/1uo92vz/i_built_an_open_fromscratch_mt_pipeline_parallel/) ⭐️ 8.0/10
<a id="weekly-item-7"></a>
- [Competence Gate：基于内部置信度控制工具使用的 Qwen3.5-4B 适配器](https://www.reddit.com/r/MachineLearning/comments/1unw5un/competence_gate_gating_tooluse_on_a_small_models/) ⭐️ 8.0/10
<a id="weekly-item-8"></a>
- [OpenWrt One：开源硬件路由器发布](https://openwrt.org/toh/openwrt/one) ⭐️ 8.0/10
<a id="weekly-item-9"></a>
- [Anthropic 发现语言模型中的全局工作空间](https://www.anthropic.com/research/global-workspace) ⭐️ 8.0/10
<a id="weekly-item-10"></a>
- [腾讯发布 Hy3：295B 参数 MoE 模型，采用 Apache 2.0 许可](https://simonwillison.net/2026/Jul/6/hy3/#atom-everything) ⭐️ 8.0/10
<a id="weekly-item-11"></a>
- [LingBot-Vision：用于自监督预训练的掩码边界建模](https://www.reddit.com/r/MachineLearning/comments/1up4cjh/lingbotvision_masked_boundary_modeling_for/) ⭐️ 8.0/10
<a id="weekly-item-12"></a>
- [TRACE：开源层次化记忆系统助力 LLM 智能体在 MemoryAgentBench 上达到 82.5%](https://www.reddit.com/r/MachineLearning/comments/1uoz5jo/trace_opensource_hierarchical_memory_for_llm/) ⭐️ 8.0/10
<a id="weekly-item-13"></a>
- [CPU TTS 基准测试：Kokoro、Supertonic、Inflect-Nano 与 Pocket TTS 对比](https://www.reddit.com/r/MachineLearning/comments/1up0azr/cpu_tts_benchmark_with_utmos_mos_scoring_kokoro/) ⭐️ 8.0/10
<a id="weekly-item-14"></a>
- [Mistral 发布 Robostral Navigate，一款最先进的机器人导航模型](https://mistral.ai/news/robostral-navigate/) ⭐️ 8.0/10
<a id="weekly-item-15"></a>
- [Grok 4.5：更便宜、更快，但信任问题笼罩](https://x.ai/news/grok-4-5) ⭐️ 8.0/10
<a id="weekly-item-16"></a>
- [微软发布 Flint，一种面向 AI 代理的可视化语言](https://microsoft.github.io/flint-chart/#/) ⭐️ 8.0/10
<a id="weekly-item-17"></a>
- [OpenAI 推出 GPT-Live：全双工语音模式，可委托 GPT-5.5 处理任务](https://openai.com/index/introducing-gpt-live/) ⭐️ 8.0/10
<a id="weekly-item-18"></a>
- [LingBot-Video：开源稀疏 MoE 视频扩散世界模型](https://www.reddit.com/r/MachineLearning/comments/1ur0bxq/lingbotvideo_sparsemoe_video_diffusion/) ⭐️ 8.0/10
<a id="weekly-item-19"></a>
- [用 Rust 重写的 Postgres 通过全部回归测试](https://github.com/malisper/pgrust) ⭐️ 8.0/10
<a id="weekly-item-20"></a>
- [美军后勤体系面临下一场大战崩溃风险](https://mwi.westpoint.edu/the-glass-backbone-why-the-armys-logistics-will-break-in-the-next-war/) ⭐️ 8.0/10
<a id="weekly-item-21"></a>
- [Meta 推出付费智能体 AI 模型 Muse Spark 1.1](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/) ⭐️ 8.0/10
<a id="weekly-item-22"></a>
- [苹果起诉 OpenAI，指控前员工窃取商业机密](https://9to5mac.com/2026/07/10/apple-sues-openai-trade-secret-theft/) ⭐️ 8.0/10
<a id="weekly-item-23"></a>
- [GPT-5.6 Sol Ultra 声称证明了圈双覆盖猜想](https://cdn.openai.com/pdf/04d1d1e4-bc75-476a-97cf-49055cd98d31/cdc_proof.pdf) ⭐️ 8.0/10
<a id="weekly-item-24"></a>
- [VultronRetriever 模型登顶 MTEB 排行榜，效率大幅提升](https://www.reddit.com/r/MachineLearning/comments/1utmxq8/vultronretriever_family_of_models_released_on/) ⭐️ 8.0/10
