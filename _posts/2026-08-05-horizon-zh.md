---
layout: default
title: "Horizon Daily: 2026-08-05 (ZH)"
date: 2026-08-05
lang: zh
period: daily
period_id: 2026-08-05
---

> 从 25 条内容中筛选出 10 条重要资讯。

其中 **3 条 8 分以上**展开详细简报，其余 7 条仅列于索引。

---

1. [在单个 AMD MI300X 上运行 DeepSeek V4 Flash](#item-1) ⭐️ 8.0/10 · 相关 8/10
2. [Oxide Computer 完成 4.45 亿美元 D 轮融资](#item-2) ⭐️ 8.0/10 · 相关 4/10
3. [探索性建模：预训练的第三轴](#item-3) ⭐️ 8.0/10 · 相关 3/10
4. [Mistral 发布 Shieldstral：3B 开源多模态审核模型](#item-4) ⭐️ 7.0/10 · 相关 7/10
5. [生成多样化肤色的简单算法与颜色空间](#item-5) ⭐️ 7.0/10 · 相关 8/10
6. [Waymo 在达拉斯全面开放无人驾驶出租车服务](#item-6) ⭐️ 7.0/10 · 相关 4/10
7. [联邦快递邮件实践助长钓鱼风险](#item-7) ⭐️ 7.0/10 · 相关 4/10
8. [MiniMax-H3 全模态模型移植到 MLX，可在 Apple Silicon 上运行](#item-8) ⭐️ 7.0/10 · 相关 8/10
9. [LLM 同行评审：无休止的混杂变量与模糊批评](#item-9) ⭐️ 7.0/10 · 相关 4/10
10. [三行奖励塑形修复了 Atari Breakout 上 123 次失败的 PPO 实验](#item-10) ⭐️ 7.0/10 · 相关 6/10

---

<a id="item-1"></a>
## [在单个 AMD MI300X 上运行 DeepSeek V4 Flash](https://github.com/ryanzhou/deepseek-v4-flash-mi300x) ⭐️ 8.0/10 · 相关 8/10

一个 GitHub 项目展示了如何在单个 AMD MI300X 加速器上运行 DeepSeek V4 Flash（一个 284B 参数的混合专家模型），在将上下文窗口从完整的 1M 缩减到 256k 的情况下，实现了每秒超过 150 个 token 的推理速度。 这降低了运行先进开源权重模型所需的硬件门槛，使开发者和研究人员能够在单个 GPU 而非多 GPU 集群上部署 DeepSeek V4 Flash。这也凸显了 AMD MI300X 在 AI 推理工作负载中日益增强的实用性。 MI300X 是一款 OAM 模块，配备 192GB HBM3 内存，通常以 8 卡整机形式销售，价格约 25 万欧元。该项目利用原生 MXFP4 量化，并通过缩减上下文长度（256k 对比 1M）来适配模型，同时保留完整的推理权重并实现高吞吐量。

hackernews · zhoutong · 8月4日 10:00 · [社区讨论](https://news.ycombinator.com/item?id=49166386)

**背景**: DeepSeek V4 Flash 是一个面向效率优化的混合专家模型，总参数 284B，激活参数 13B，支持 1M token 的上下文窗口。AMD Instinct MI300X 加速器专为生成式 AI 和 HPC 设计，采用通用基板承载 8 个 OAM 模块，共 1.5TB HBM3 内存。运行如此大的模型通常需要多块 GPU，但通过量化和缩减上下文长度，可以在单 GPU 上部署。

**对中国影响**: 该项目可能鼓励中国开发者和企业利用 AMD MI300X 进行高性价比的 AI 推理，在出口管制背景下减少对 NVIDIA GPU 的依赖。这也契合中国推动本土 AI 基础设施和开源模型采用的方向。

**对我有什么用**: 对于电子工程师和硬件开发者而言，这个项目是单 GPU 部署大型 MoE 模型的有价值参考，提供了关于量化、内存管理和 AMD 硬件性能调优的见解。您可以在 MI300X 上复刻该配置，或将此方法适配到您使用的其他加速器上。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash">deepseek -ai/ DeepSeek - V 4 - Flash · Hugging Face</a></li>
<li><a href="https://openrouter.ai/deepseek/deepseek-v4-flash">DeepSeek V 4 Flash - API Pricing & Benchmarks | OpenRouter</a></li>
<li><a href="https://instinct.docs.amd.com/projects/system-acceptance/en/latest/gpus/mi300x.html">AMD Instinct MI300X — AMD Instinct Customer Acceptance Guide</a></li>

</ul>
</details>

**社区讨论**: 社区评论指出，MI300X 并非单卡销售，而是以 8 卡整机形式出售，并建议使用 MI350P PCIe 卡作为替代方案（拥有 144GB 内存）。有人提到先前的工作（如 DwarfStar）可以在更少内存下运行该模型，也有人称赞将上下文缩减到 256k 以换取速度和权重保真度的实用权衡。

**标签**: `#DeepSeek`, `#AMD MI300X`, `#AI推理`, `#模型部署`, `#硬件优化`

---

<a id="item-2"></a>
## [Oxide Computer 完成 4.45 亿美元 D 轮融资](https://www.sec.gov/Archives/edgar/data/1795071/000179507126000002/xslFormDX01/primary_doc.xml) ⭐️ 8.0/10 · 相关 4/10

根据美国证券交易委员会（SEC）的 Form D 文件，Oxide Computer 完成了 4.45 亿美元的 D 轮融资。此前该公司已分别完成 4400 万美元的 A 轮、1 亿美元的 B 轮和 2 亿美元的 C 轮融资。 这笔巨额融资凸显了市场对 Oxide 机架级云计算机方案的信心日益增强，该方案对传统服务器架构构成了挑战。这可能加速本地云基础设施的采用，并影响更广泛的硬件初创生态。 Oxide 设计了一款软硬件协同设计的全集成机架级系统，采用硬件信任根和嵌入式服务处理器，取代了传统的 BMC。其客户包括爱达荷国家实验室和一家全球金融服务公司。

hackernews · depr · 8月4日 20:13 · [社区讨论](https://news.ycombinator.com/item?id=49174407)

**背景**: Oxide Computer 是一家专注于为本地云计算构建新型服务器的初创公司，旨在让客户在自己的数据中心内获得超大规模云基础设施的优势。该公司的做法是软硬件协同设计，这在业内并不常见。本轮融资反映了市场对面向云和 AI 工作负载的专用硬件投资日益增长的趋势。

**对中国影响**: 这笔融资可能表明全球对本地云硬件的兴趣日益浓厚，这可能会影响中国的云服务提供商和硬件初创公司。中国企业可能会探索类似的机架级设计或合作，但地缘政治因素可能影响技术转让和市场准入。

**对我有什么用**: 对于电子工程师和硬件开发者而言，这一消息展示了机架级硬件设计的典型案例，包括集成服务处理器和信任根，这可能激发可复刻的项目或为设计决策提供参考。该公司公开分享技术细节的做法，为嵌入式系统和软硬件协同设计提供了学习机会。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://oxide.computer/blog/oxide-unveils-the-worlds-first-commercial-cloud-computer">Oxide Unveils the World's First Commercial Cloud Computer</a></li>
<li><a href="https://docs.oxide.computer/guides/introduction">Introduction / Guides / Oxide</a></li>
<li><a href="https://newsletter.pragmaticengineer.com/p/oxide">Startups on hard mode: Oxide. Part 1: Hardware</a></li>

</ul>
</details>

**社区讨论**: 社区成员对 Oxide 的进展表示兴奋，有人注意到其融资轮次接连不断。然而，一位工程副总裁表示，他们提交了销售咨询但从未收到回复，尽管他们每年在 AWS 上花费 90 万美元。另一位评论者质疑 Oxide 是否真的出货硬件，而其他人则称赞团队的专业能力。

**标签**: `#融资`, `#硬件`, `#Oxide Computer`, `#服务器`, `#创业`

---

<a id="item-3"></a>
## [探索性建模：预训练的第三轴](https://www.reddit.com/r/MachineLearning/comments/1vf6r6f/explorative_modeling_unlocking_a_third/) ⭐️ 8.0/10 · 相关 3/10

论文《探索性建模：解锁预训练的第三轴与端到端生成》提出了一种名为探索性建模（XMs）的新范式，它作为现有生成模型在参数和数据之外的第三个预训练轴，并支持端到端生成。 这项研究可能对 AI 领域产生重要影响，为扩展生成模型提供了新的维度，有望带来更强大、更高效的模型。它挑战了传统上仅将参数和数据作为扩展轴的观点。 论文声称增加探索性为现有生成模型增加了第三个预训练轴，该方法适用于现有生成模型。然而，Reddit 帖子缺乏具体技术细节，完整论文可在项目页面和 Hugging Face 上获取。

reddit · r/MachineLearning · /u/Benlus · 8月4日 10:42

**背景**: 像 GPT 和 DALL-E 这样的生成模型通常通过增加参数和数据来扩展。预训练是模型从大型数据集中学习通用表示的阶段。这篇论文提出将探索性作为额外的轴，有望在不单纯依赖更多数据或参数的情况下提升模型能力。

**对中国影响**: 中国的 AI 产业可以通过采用探索性作为新的扩展轴而受益，可能带来更高效、资源消耗更少的模型。这与中国的 AI 创新推动相符，并可能影响国内的研究与开发。

**对我有什么用**: 作为电子工程师和硬件开发者，这项研究与您关注的 AI 模型和开发工具链相关。虽然它可能不会直接影响硬件设计，但了解新的预训练范式可以为您的 AI 相关项目和自动化工具提供参考。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://explorative-modeling.github.io/">Explorative Modeling : Unlocking a Third Pretraining Axis and...</a></li>
<li><a href="https://digg.com/tech/mrt8e84i">Paper Frames Exploration as Third Pretraining Axis · Digg</a></li>
<li><a href="https://paperswithcode.co/paper/2607.27372">Explorative Modeling : Unlocking a Third Pretraining Axis and...</a></li>

</ul>
</details>

**标签**: `#AI`, `#pretraining`, `#research`, `#machine-learning`

---

<a id="item-4"></a>
### *（简报）* [Mistral 发布 Shieldstral：3B 开源多模态审核模型](https://mistral.ai/news/shieldstral/) ⭐️ 7.0/10 · 相关 7/10

Mistral AI 发布了 Shieldstral，一个 3B 参数的开源多模态安全分类器，其性能优于体积高达 7 倍的模型。它将内容审核构建为策略自适应问答任务，支持文本和图像输入。 它为开发者提供了一种高性价比、可定制的内容审核方案，尤其是对构建社交平台或图片分享服务的开发者而言。它通过提供小型、高效的开源权重替代方案，挑战了大型专有审核 API 的主导地位。 Shieldstral 已在 Hugging Face 上发布（mistralai/Shieldstral-1.0-3B）。它支持提示词审核、回复审核、提示词-回复对分类、拒答检测和安全过滤。该模型具有策略自适应性，可在无需完全重新训练的情况下针对不同审核策略进行调整。

---

<a id="item-5"></a>
### *（简报）* [生成多样化肤色的简单算法与颜色空间](https://toneyalexander.github.io/inclusive-color-space/) ⭐️ 7.0/10 · 相关 8/10

作者提出了一种新的颜色空间和简单算法，用于为数字艺术和游戏开发生成合理且多样化的肤色。他们提供了交互式取色器、程序化生成演示以及底层数学的详细解释。 这项工作解决了数字艺术家和游戏开发者在选择逼真肤色时的常见痛点。通过提供数据驱动、包容性的颜色空间，它可以改善数字媒体中的代表性，并激发其他领域的类似方法。 该颜色空间基于肤色数据集，通过函数拟合创建二维参数化，以捕捉自然变化。实现包括 JavaScript 演示和 Python 程序化生成算法，并设有“未来工作”部分承认其局限性。

---

<a id="item-6"></a>
### *（简报）* [Waymo 在达拉斯全面开放无人驾驶出租车服务](https://waymo.com/blog/shorts/dallas-open-to-all/) ⭐️ 7.0/10 · 相关 4/10

Waymo 宣布其自动驾驶出租车服务现已在德克萨斯州达拉斯全面向公众开放，将其商业化运营扩展到一个重要的新市场。 此次扩张标志着自动驾驶汽车商业化的重要一步，将无人驾驶出租车带入一个广阔且高度依赖汽车的大都市区，并可能影响公众接受度和监管方式。 服务区域覆盖达拉斯部分地区，Waymo 一直在美国各地逐步扩展业务，包括最近在迈阿密和旧金山的推出。达拉斯的推出尤其引人注目，因为该地区人口密度低且公共交通有限。

---

<a id="item-7"></a>
### *（简报）* [联邦快递邮件实践助长钓鱼风险](https://www.troyhunt.com/thanks-fedex-this-is-why-we-keep-getting-phished/) ⭐️ 7.0/10 · 相关 4/10

Troy Hunt 的文章指出，联邦快递自身的邮件实践，如使用个人邮箱发送和短链接域名，助长了钓鱼风险。文章以联邦快递为例，说明了邮件域名验证和用户意识方面的更广泛问题。 这很重要，因为即使是像联邦快递这样的知名公司也会无意中让用户接受有风险的邮件行为，从而使钓鱼攻击更加有效。这凸显了组织采用更严格的邮件认证标准和用户保持警惕的必要性。 文章提到了具体例子，如联邦快递从个人地址发送邮件和使用掩盖实际域名的短链接。社区评论还提到了类似问题，如 Google 的 c.gle 域名和 .xyz 等新通用顶级域名的激增，这些使钓鱼检测变得更加复杂。

---

<a id="item-8"></a>
### *（简报）* [MiniMax-H3 全模态模型移植到 MLX，可在 Apple Silicon 上运行](https://simonwillison.net/2026/Aug/4/minimax-h3-mlx/#atom-everything) ⭐️ 7.0/10 · 相关 8/10

PipeNetwork 发布了一个 Python 包，将全模态生成模型 MiniMax-H3 移植到 MLX，使其能在 Apple Silicon 上运行。Simon Willison 在 M5 Max MacBook Pro 上成功运行，并根据文本提示生成了带音频的 15 秒视频片段。 这一移植使 Apple Silicon 用户能够本地运行先进的 omni-modal 模型，生成带音频的视频。它展示了 MLX 移植生态的壮大，可能加速端侧 AI 开发，减少对云端 API 的依赖。 该模型需要下载约 115 GB 的模型文件，在 M5 Max 上生成视频耗时不到 45 分钟。由于未提供提示词指导，生成的音频被描述为“类似语音的垃圾”，凸显了遵循提示词指南的重要性。

---

<a id="item-9"></a>
### *（简报）* [LLM 同行评审：无休止的混杂变量与模糊批评](https://www.reddit.com/r/MachineLearning/comments/1vf4zjz/the_downsides_of_llmgenerated_peer_reviews_d/) ⭐️ 7.0/10 · 相关 4/10

一篇 Reddit 帖子指出了 LLM 辅助同行评审中反复出现的两个缺陷：无休止地寻找未控制的变量而不考虑其实际重要性，以及过于抽象的批评，未能指出具体的先前方法。 这很重要，因为如果 LLM 生成的评审意见未经判断就被直接采用，会让作者疲于回应琐碎问题，从而损害科学同行评审的质量。这凸显了在 AI 辅助评审中人工监督的必要性。 作者指出，LLM 常常高估共享高级术语的方法之间的相似性，推荐仅表面相关的比较。核心问题在于 LLM 会生成无限多的看似合理的批评，却不评估其相关性、严重性或证据负担。

---

<a id="item-10"></a>
### *（简报）* [三行奖励塑形修复了 Atari Breakout 上 123 次失败的 PPO 实验](https://www.reddit.com/r/MachineLearning/comments/1vfa9im/reactive_play_achieved_experimenting_with_atari/) ⭐️ 7.0/10 · 相关 6/10

在 Atari Breakout 上进行了 124 次 PPO 实验后，作者发现添加一个小的接近奖励——在球下落时奖励球拍与球的水平接近——成功让智能体采用反应式追球策略，而不是记忆化的动作序列。该行为在评估时无需奖励即可迁移，智能体还能处理自定义砖块配置。 这项工作挑战了强化学习智能体中防止记忆化需要环境工程改造的常见假设。它表明简单的奖励塑形可以从根本上改变优化景观，为提升强化学习的泛化能力提供了一种实用且成本低廉的解决方案。 奖励塑形在球下落期间每帧增加 0.05 的奖励，而每个砖块的奖励为 1.0-7.0，且仅在训练时应用。作者还创建了一个“Split-Watcher”工具，用于在两种不同砖块布局的 Breakout 实例中可视化智能体的行为，所有代码和文档已在 GitHub 上开源。

---

