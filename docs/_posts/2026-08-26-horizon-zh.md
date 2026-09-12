---
layout: default
title: "Horizon Daily: 2026-08-26 (ZH)"
date: 2026-08-26
lang: zh
period: daily
period_id: 2026-08-26
---

> 从 22 条内容中筛选出 3 条重要资讯。

其中 **1 条 8 分以上**展开详细简报，其余 2 条仅列于索引。

---

1. [OpenAI 自研芯片 Jalapeño：性能对标 Nvidia Blackwell](#item-1) ⭐️ 8.0/10 · 相关 6/10
2. [Apple 发布 M6 和 M5 Ultra](#item-2) ⭐️ 7.0/10 · 相关 3/10
3. [Nitter 项目收到停止侵权函](#item-3) ⭐️ 7.0/10 · 相关 2/10

---

<a id="item-1"></a>
## [OpenAI 自研芯片 Jalapeño：性能对标 Nvidia Blackwell](https://newsletter.semianalysis.com/p/openai-jalapeno-better-than-nvidia) ⭐️ 8.0/10 · 相关 6/10

SemiAnalysis 发布了关于 OpenAI 首款自研 AI 推理芯片「Jalapeño」的深度拆解，该芯片由 Broadcom 联合设计，采用台积电 3nm 工艺制造，是一颗接近光罩极限尺寸（约 840mm²）的 ASIC，搭载 8 颗 HBM 堆叠和脉动阵列架构。报告从 FP4 精度、token/Joule 能效和 die size 等维度将 Jalapeño 与 Nvidia Blackwell 进行了系统对标，认为 OpenAI 的垂直整合芯片在规模化部署下具备竞争力。 Jalapeño 表明超大规模 AI 实验室已经具备打造可对标 Nvidia 旗舰加速器的推理芯片的能力，这或将重塑 AI 算力供应链，并加速从「GPU 为中心的训练」向「ASIC 优化的推理」迁移。Google（TPU）、Amazon（Trainium/Inferentia）和微软（Maia）等公司也在推进类似的垂直整合趋势，可能在未来几个产品周期内侵蚀 Nvidia 在前沿 AI 硬件上的近乎垄断地位。 Jalapeño 专为 LLM 解码吞吐量而非训练而调优，采用激进的低精度格式（NVFP4）以最大化每焦耳生成的 token 数；SemiAnalysis 指出人类语音的能效仍比目前最先进的推理芯片高出约 22 倍，并将这一差距视为未来进步的基准。需要注意的是，OpenAI 的芯片不对外部客户开放，且社区读者对 die size 数据与 Nvidia 双 die Rubin 封装之间的对比仍存在争议。

hackernews · bmulholland · 8月25日 14:06 · [社区讨论](https://news.ycombinator.com/item?id=49434378)

**背景**: AI 芯片按工作负载分为两大类：训练（算力密集、显存带宽受限，目前由 Nvidia 的 Blackwell 及下一代 Rubin 等 GPU 主导）和推理（对时延敏感，正越来越多地由定制 ASIC 承担）。Nvidia Blackwell 架构采用两颗光罩极限尺寸的 die 通过 10 TB/s 互联组成单一 GPU，基于台积电 4NP 工艺，集成了 2080 亿晶体管，长期以来是 AI 加速器的标杆。OpenAI 的 Jalapeño 是前沿模型实验室推出的首款纯推理 ASIC，与 Google TPU 和 Amazon Trainium2 一道，在推理市场对 Nvidia 的利润率发起挑战。

**对中国影响**: Jalapeño 由台积电代工并受美国出口管制约束，无法直接服务中国市场，但它会进一步倒逼华为昇腾、寒武纪、平头哥等国产 AI 芯片厂商证明自身的推理能效竞争力。SemiAnalysis 文中讨论的 FP4 与 token/Joule 评测体系，很可能会被阿里、字节、百度等中国超大规模客户在评估自家定制推理路线图时借鉴采用。

**对我有什么用**: Jalapeño 是一款 OpenAI 自用的封闭式 ASIC，并非可复刻的开源硬件项目，对于关注开源板卡和 EDA 工具的硬件开发者来说直接用途有限。不过其底层设计趋势（脉动阵列、经由 Broadcom/台积电实现的 3nm ASIC 流程、NVFP4 量化）值得关注，这些技术将在未来 1–2 年内逐步渗透到可获取的 dev kit、边缘推理加速器以及基于 RISC-V 的 AI 协处理器中。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://awesomeagents.ai/hardware/openai-jalapeno/">OpenAI Jalapeño - Custom LLM Inference ASIC | Awesome Agents</a></li>
<li><a href="https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/">The Engine Behind AI Factories | NVIDIA Blackwell Architecture</a></li>
<li><a href="https://valueaddvc.com/blog/inference-chips-vs-training-chips-why-the-next-semiconductor-race-is-different">Inference vs Training Chips 2026: 60–70% of $400B Market</a></li>

</ul>
</details>

**社区讨论**: HN 评论者将当前的推理芯片竞争类比于早期 3dfx/RIVA 时代的消费级 GPU 格局，认为推理芯片市场最终可能会向少数赢家集中。多位用户指出，模型的服役周期如今已延长到 2 年以上，值得把 LLM 权重直接固化到硅片里；也有人感叹 FP4 这种精度低得「近乎滑稽」，但实际可用。社区的主流共识是利好终端用户：硬件持续迭代意味着 token 价格将继续大幅下降。

**标签**: `#AI hardware`, `#OpenAI`, `#Nvidia`, `#custom silicon`, `#inference chips`

---

<a id="item-2"></a>
### *（简报）* [Apple 发布 M6 和 M5 Ultra](https://www.apple.com/newsroom/2026/08/apple-introduces-m6-and-m5-ultra-for-a-big-leap-in-performance-and-ai-compute/) ⭐️ 7.0/10 · 相关 3/10

Apple 发布 M6 基础款芯片和 M5 Ultra 芯片，主打性能与 AI 算力大幅提升，并据传跳过 M6 Pro/Max/Ultra，集中资源研发 AI 导向的 M7。

---

<a id="item-3"></a>
### *（简报）* [Nitter 项目收到停止侵权函](https://github.com/zedeus/nitter/issues/1442) ⭐️ 7.0/10 · 相关 2/10

广受欢迎的开源 X/Twitter 前端项目 Nitter 收到停止侵权函，所有实例预计将长期下线，引发开源社区对法律风险和平台依赖问题的广泛讨论。

---

