---
layout: default
title: "Horizon Daily: 2026-09-02 (ZH)"
date: 2026-09-02
lang: zh
period: daily
period_id: 2026-09-02
---

> 从 27 条内容中筛选出 3 条重要资讯。

其中 **1 条 8 分以上**展开详细简报，其余 2 条仅列于索引。

---

1. [Slotstream：48GB Mac 以约 12 tok/s 运行 104GB Qwen3.8-Flash-Next](#item-1) ⭐️ 8.0/10 · 相关 8/10
2. [Anthropic 发布 Claude Fable 5.1 与 Mythos 5.1，写作风格与缓存定价双升级](#item-2) ⭐️ 7.0/10 · 相关 4/10
3. [2026 年潜在推理领域综述：BDH-CQ、HRM/TRM 与 Coconut 的映射 (D)](#item-3) ⭐️ 7.0/10 · 相关 5/10

---

<a id="item-1"></a>
## [Slotstream：48GB Mac 以约 12 tok/s 运行 104GB Qwen3.8-Flash-Next](https://github.com/carloslfu/slotstream) ⭐️ 8.0/10 · 相关 8/10

开发者发布了开源工具 Slotstream，通过 SSD 流式加载与 MoE 专家卸载，让仅配备 16GB 统一内存的 Apple Silicon Mac 也能运行约 104GB（4-bit 量化）的 Qwen3.8-Flash-Next，并在 48GB 机器上达到约 12 tok/s 的推理速度。项目基于 Apple 的 MLX 框架、以 Swift 原生实现，提供在内存占用与速度之间自动权衡的 "auto-mode"，作者下一步计划加入基于 MTP 的推测解码。 它打破了消费级 Apple Silicon 本地运行百亿参数级开源模型的"装得下就跑得动"二元限制，让大量无需租用云端 GPU 的开发者也能体验 100B+ 模型。该方案同时也验证了一种通用思路——把不活跃的 MoE 专家按需从高速 NVMe 分页调入——这种思路很可能在今后几年影响本地 AI 工具链的设计。 Slotstream 利用了 MoE 的稀疏激活特性（类似 DeepSeek-R1 的模型每 token 仅激活约 3.5% 的专家），因此绝大多数专家权重常驻 SSD，仅在需要时被分页调入；项目以 Swift 编写以实现 macOS 原生集成、底层依托 MLX，后续还将引入 MTP 推测解码模块以进一步提升吞吐。

hackernews · carloslfu · 9月1日 16:42 · [社区讨论](https://news.ycombinator.com/item?id=49524447)

**背景**: Qwen3.8-Flash-Next 是阿里通义千问团队的混合专家（MoE）大模型，总参数约 1250 亿，但每个 token 只会激活其中一小部分专家，这就是 4-bit 量化后仍然需要约 100GB 磁盘空间的原因。MLX 是 Apple 开源的数组框架，专为 Apple Silicon 上的高效机器学习研究设计。MoE 专家卸载与 SSD 流式加载是近年来兴起的技术，把"冷"的专家权重放在高速 NVMe 上、需要时再分页调入统一内存，以一定的 I/O 延迟换取远超物理内存容量的模型运行能力。

**对中国影响**: Qwen3.8-Flash-Next 出自阿里通义千问团队，这次演示进一步印证了中国开源 MoE 模型在全球本地大模型生态中的竞争力；叠加 Apple 的 MLX 工具链，也为国内开发者提供了一条无需租用云端 GPU、就能在 Mac 上评估和部署千问模型的可行路径。

**对我有什么用**: 对于电子工程师而言，这个项目值得研究，因为它是一次对"消费级 Apple Silicon 统一内存 + 高速 NVMe"极限性能的实测，其卸载思路可以为边缘 AI 盒子或资源受限的 RISC-V SBC 提供借鉴。但如果日常工作主要是 HarmonyOS 应用开发或开源硬件原理图设计，则与本项目的直接关联度不高。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://opensource.apple.com/projects/mlx/">Apple Open Source</a></li>
<li><a href="https://www.mindstudio.ai/blog/ssd-streaming-ai-models-ram-dial">SSD Streaming for AI Models: How to Turn RAM from a Wall into a Dial | MindStudio</a></li>
<li><a href="https://arxiv.org/html/2508.06978v1">SSD Offloading for LLM Mixture-of-Experts Weights Considered Harmful in Energy Efficiency</a></li>

</ul>
</details>

**社区讨论**: 评论区整体谨慎乐观：一位用户质疑 16GB 统一内存能否在不触发散热降频的情况下维持 ~5 tok/s，另一位拥有 48GB M5 的用户希望进一步扩展上下文窗口，多人建议作者精简 README 以方便新人上手。还有用户希望在编程等具体任务中，看到 Flash-Next 相对 27B 级别模型有可量化的能力提升。

**标签**: `#local-llm`, `#Apple-Silicon`, `#MLX`, `#model-offloading`, `#SSD-streaming`

---

<a id="item-2"></a>
### *（简报）* [Anthropic 发布 Claude Fable 5.1 与 Mythos 5.1，写作风格与缓存定价双升级](https://www.anthropic.com/claude-fable-and-mythos-5-1) ⭐️ 7.0/10 · 相关 4/10

Anthropic 正式发布 Claude Fable 5.1 与 Claude Mythos 5.1，两者是同一个模型但配备了不同级别的安全防护措施。新版本在写作风格、代码精度和复杂推理方面都有明显提升，并将缓存读取价格从原来的每百万 token 1 美元大幅下调至 0.25 美元。 缓存读取价格的大幅下调（已降至 Opus 缓存读取费用的一半）显示出 LLM API 市场竞争正在加剧，并很可能为前沿模型的定价划定上限。配合 Anthropic 员工重点强调的写作风格改进，这次发布体现了厂商正在同时从质量和成本两个维度寻求差异化。 Fable 5.1 的缓存读取价格现为每百万 token 0.25 美元，而 Opus 为 0.5 美元；Fable 5.1 与 Mythos 5.1 使用同一套模型权重，区别仅在于 Mythos 设置了更严格的安全护栏。Anthropic 发布了系统卡详述安全评估，但社区批评者指出新版移除了原本用于调试 prompt 的可见思维链输出。

---

<a id="item-3"></a>
### *（简报）* [2026 年潜在推理领域综述：BDH-CQ、HRM/TRM 与 Coconut 的映射 (D)](https://www.reddit.com/r/MachineLearning/comments/1w4evwo/latent_reasoning_landscape_in_2026_mapping_bdhcq/) ⭐️ 7.0/10 · 相关 5/10

2026 年潜在推理领域综述：将推理机制从语言化的思维链转向连续隐藏状态转换的多种架构（Coconut、BDH-CQ、HRM/TRM 等）的分类与对比分析。

---

