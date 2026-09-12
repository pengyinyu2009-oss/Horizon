---
layout: default
title: "Horizon Daily: 2026-08-15 (ZH)"
date: 2026-08-15
lang: zh
period: daily
period_id: 2026-08-15
---

> 从 25 条内容中筛选出 2 条重要资讯。

其中 **0 条 8 分以上**展开详细简报，其余 2 条仅列于索引。

---

1. [阿里发布 Qwen 3.8 27B 开源权重多模态模型](#item-1) ⭐️ 7.0/10 · 相关 7/10
2. [我将 Doom 的渲染器编译成了一个 210 亿参数的 transformer——全程无需任何训练](#item-2) ⭐️ 7.0/10 · 相关 3/10

---

<a id="item-1"></a>
### *（简报）* [阿里发布 Qwen 3.8 27B 开源权重多模态模型](https://huggingface.co/Qwen/Qwen3.8-27B-FP8) ⭐️ 7.0/10 · 相关 7/10

阿里 Qwen 团队正式发布 Qwen 3.8 27B，这是一款拥有 270 亿参数、支持文本/图像/视频输入的开源权重多模态模型，专为本地部署而设计，FP8 量化版本已在 HuggingFace 上架。在阿里自研的 CoWorkBench 长周期生产力基准上，该模型取得 70.7 分，超过 Opus 4.6 Max（68.2）和 Qwen 3.6 27B（61.0），并在多项公开基准上击败了 Muse Glimmer 30B。 此次发布延续了阿里向开源权重方向转型的战略，巩固了 Qwen 作为主流实验室中最多产的开源模型发布者的地位；同时证明 27B 级别的本地模型在智能体办公场景下已能媲美甚至超越更大的闭源系统。再叠加 RTX 5090 上约 138 tok/s 的推理速度以及接近 Gemma 4 的推理能力，本地运行有竞争力的 AI 的门槛被显著拉低。 HuggingFace 上的版本是 FP8 量化版，相比 BF16 权重显存占用减半，使 27B 模型可在单张高端消费级显卡上流畅运行。多 Token 预测（MTP）通过每步预测多个 token 来加速推理，但社区测试者指出，3.8 新版采用笔记式的思维链风格可能会在一定程度上削弱 MTP 预测质量，且在同等上下文长度下其显存效率仍不及 Gemma 4 或 Glimmer。

---

<a id="item-2"></a>
### *（简报）* [我将 Doom 的渲染器编译成了一个 210 亿参数的 transformer——全程无需任何训练](https://www.reddit.com/r/MachineLearning/comments/1voazhm/i_compiled_dooms_renderer_into_a_21bparameter/) ⭐️ 7.0/10 · 相关 3/10

作者编写了一个编译器，将 Doom 的渲染算法编译成 210 亿参数的 transformer 权重，无需任何训练即可加载运行，并成功输出 E1M1 关卡的画面。

---

