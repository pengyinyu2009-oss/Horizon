---
layout: default
title: "Horizon Daily: 2026-08-11 (ZH)"
date: 2026-08-11
lang: zh
period: daily
period_id: 2026-08-11
---

> 从 24 条内容中筛选出 3 条重要资讯。

其中 **0 条 8 分以上**展开详细简报，其余 3 条仅列于索引。

---

1. [Meta 发布 30B 本地智能体模型 Muse Glimmer](#item-1) ⭐️ 7.0/10 · 相关 6/10
2. [Needle 2：14MB 智能体 LLM，可运行于手机、可穿戴设备和机器人](#item-2) ⭐️ 7.0/10 · 相关 8/10
3. [Transformer 因算术能力差而闻名，所以我手工设置了一个模型的权重（无需训练），它能以 100%的准确率进行乘法运算 (P)](#item-3) ⭐️ 7.0/10 · 相关 4/10

---

<a id="item-1"></a>
### *（简报）* [Meta 发布 30B 本地智能体模型 Muse Glimmer](https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model) ⭐️ 7.0/10 · 相关 6/10

Meta 发布了 30B 参数的稠密多模态模型 Muse Glimmer，专为在消费级硬件上运行的常驻本地智能体工作流设计，采用 Apache 2.0 协议开源。Meta 同时宣布将很快开放其更大的 Muse Spark 1.2 基础模型的权重。 这一发布标志着 Meta 战略性地进军本地化、私有化 AI 部署领域，挑战中国开源权重模型的领先地位，并为开发者提供强大的端侧自主智能体选择。专用感知编码器、超过 120K 的上下文窗口与稠密架构的组合，使其在无需持续云端开销的长时多步骤任务中颇具吸引力。 该模型具有超过 120K token 的上下文窗口，并采用稠密（非 MoE）架构，每个 token 激活全部参数以保证可预测的延迟，已上架 Ollama、LM Studio 和 Hugging Face。Meta 还发布了 NVIDIA 技术指南，使其能在多款消费级和专业级 NVIDIA GPU 上运行。

---

<a id="item-2"></a>
### *（简报）* [Needle 2：14MB 智能体 LLM，可运行于手机、可穿戴设备和机器人](https://cactuscompute.com/needle) ⭐️ 7.0/10 · 相关 8/10

Cactus Compute 发布了 Needle 2，这是一款仅 14MB 的智能体 LLM，采用 2 比特压缩的 4500 万参数，在 28MB 内存中即可运行；在树莓派 5 上达到 500 tokens/秒，在 VR 头显上达到 400-1500 tokens/秒，在低价手机上达到 300-700 tokens/秒。Needle 2 支持工具调用、结构化提取，并可在 Mac/PC 上几分钟内完成微调，基于该公司自研的 Simple Attention Networks 架构。 全球超过 210 亿台联网 IoT 设备中，Mac/PC 仅占 15 亿，真正受限硬件（低价手机、微控制器、可穿戴设备）上的边缘 AI 仍属蓝海。Needle 2 证明函数调用和结构化提取并不需要世界知识，为端侧常驻助手开辟了路径，每 token 能耗比同类小型 LLM 低 7 到 85 倍。 Needle 2 每个 token 仅消耗 70 MFLOPs，而同等规模的 Transformer 模型则需 87-164 MFLOPs；模型还会为每个响应输出学习到的置信度分数，以便在端云混合架构中按需升级（例如将复杂企业任务路由到 DeepSeek-v4-Flash）。逐响应的置信度让分层 LLM 架构成为可能——小型本地模型处理绝大多数请求，仅把不确定的查询转发给云端。

---

<a id="item-3"></a>
### *（简报）* [Transformer 因算术能力差而闻名，所以我手工设置了一个模型的权重（无需训练），它能以 100%的准确率进行乘法运算 (P)](https://www.reddit.com/r/MachineLearning/comments/1vkrnb5/transformers_are_famously_bad_at_arithmetic_so_i/) ⭐️ 7.0/10 · 相关 4/10

作者编写了编译器 Torchwright，将小学乘法算法直接编译进 Phi-3 Transformer 的权重中，无需训练即可在最多 12 位×12 位乘法上达到 100%准确率，而前沿模型在 7 位数时即崩溃至 0%。

---

