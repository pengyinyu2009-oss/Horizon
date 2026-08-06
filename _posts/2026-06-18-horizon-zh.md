---
layout: default
title: "Horizon Daily: 2026-06-18 (ZH)"
date: 2026-06-18
lang: zh
period: daily
period_id: 2026-06-18
---

> 从 26 条内容中筛选出 13 条重要资讯。

其中 **4 条 8 分以上**展开详细简报，其余 9 条仅列于索引。

---

1. [研究人员发现 1 万个 GitHub 仓库在分发木马恶意软件](#item-1) ⭐️ 9.0/10
2. [GLM-5.2：最强开源权重大语言模型发布](#item-2) ⭐️ 9.0/10
3. [医院和大学以 90%更低成本重新利用药物](#item-3) ⭐️ 8.0/10
4. [对比监督微调用于大模型因果依赖映射](#item-4) ⭐️ 8.0/10
5. [康奈尔大学 CS 6120 高级编译器课程现可免费在线学习](#item-5) ⭐️ 7.0/10
6. [W Social 因开源声明和商业模式面临质疑](#item-6) ⭐️ 7.0/10
7. [Modos 彩色显示器推动电子纸显示技术再进一步](#item-7) ⭐️ 7.0/10
8. [Ubiquiti 推出基于 ZFS 的企业级 NAS](#item-8) ⭐️ 7.0/10
9. [DeepSeek 为聊天应用添加视觉理解功能](#item-9) ⭐️ 7.0/10
10. [Git 的全局和仓库级排除文件：.gitignore 的替代方案](#item-10) ⭐️ 7.0/10
11. [对话级语音调试优于孤立基准测试，用于多轮 AI 评估](#item-11) ⭐️ 7.0/10
12. [没有高性能计算，基础 AI 研究还能做吗？](#item-12) ⭐️ 7.0/10
13. [机械可解释性中探针容量与网络容量的权衡](#item-13) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [研究人员发现 1 万个 GitHub 仓库在分发木马恶意软件](https://orchidfiles.com/github-repositories-distributing-malware/) ⭐️ 9.0/10

一名安全研究人员发现超过 1 万个 GitHub 仓库正在分发木马恶意软件，这些仓库由不同用户创建，名称各异且非派生仓库，但具有共同模式，从而实现了自动化检测。 这种大规模供应链攻击针对开发者，他们可能无意中下载并使用这些恶意仓库，从而危及自身系统及所构建的软件安全。 这些仓库并非派生仓库，且看似合法，增加了检测难度。研究人员利用脚本根据共同特征识别它们，凸显了 GitHub 上需要更好的自动化扫描机制。

hackernews · theorchid · 6月18日 11:45 · [社区讨论](https://news.ycombinator.com/item?id=48583928)

**背景**: 软件供应链攻击是指攻击者通过篡改库或工具等受信任组件，向所有用户分发恶意代码。GitHub 等开源仓库日益成为攻击目标，因为开发者常常在未彻底审查的情况下下载并集成代码。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://orchidfiles.com/github-repositories-distributing-malware/">How I found 10,000 GitHub repositories distributing Trojan malware</a></li>
<li><a href="https://en.wikipedia.org/wiki/Supply_chain_attack">Supply chain attack - Wikipedia</a></li>
<li><a href="https://www.reversinglabs.com/blog/open-source-malware-sows-havoc-on-supply-chain">Open-source repository malware sows Havoc | ReversingLabs</a></li>

</ul>
</details>

**社区讨论**: 评论者指出 GitHub 未能充分解决恶意软件问题，有人分享了自己名字被冒用至恶意项目的经历。其他人讨论称，这些攻击针对的是自动化代理而非人类，利用了依赖搜索机制。

**标签**: `#security`, `#malware`, `#supply chain`, `#GitHub`, `#open source`

---

<a id="item-2"></a>
## [GLM-5.2：最强开源权重大语言模型发布](https://simonwillison.net/2026/Jun/17/glm-52/#atom-everything) ⭐️ 9.0/10

Z.ai 发布了 GLM-5.2，这是一个拥有 7530 亿参数、100 万 token 上下文窗口的开源权重大语言模型，采用 MIT 许可证。该模型为纯文本模型，使用混合专家（MoE）架构，激活参数为 400 亿。 GLM-5.2 在 Artificial Analysis 智能指数中领先所有开源权重模型，并在 Code Arena WebDev 排行榜上位列第二，超越了许多专有模型。其采用 MIT 许可证的开源权重特性允许广泛的研究和商业使用，可能加速 AI 发展。 该模型每个任务使用 43k 输出 token，高于 MiniMax-M3（24k）和 DeepSeek V4 Pro（37k）等竞品。通过 OpenRouter 的定价为输入每百万 token 1.40 美元、输出每百万 token 4.40 美元，远低于 GPT-5.5（5/30 美元）和 Claude Opus 4.5-4.8（5/25 美元）。

rss · Simon Willison · 6月17日 23:58

**背景**: 开源权重模型公开了训练后的参数，允许修改和微调。混合专家（MoE）架构将计算分散到多个专家子网络中，每次输入仅激活部分专家，从而在保持高效推理的同时实现大规模总参数。GLM-5.2 是 Z.ai 的 GLM 系列最新版本，前代 GLM-5.1 拥有 20 万 token 上下文窗口。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/zai-org/GLM-5.2">zai-org/GLM-5.2 · Hugging Face</a></li>
<li><a href="https://artificialanalysis.ai/articles/glm-5-2-is-the-new-leading-open-weights-model-on-the-artificial-analysis-intelligence-index">GLM-5.2 is the new leading open weights model on the Artificial Analysis Intelligence Index</a></li>
<li><a href="https://docs.z.ai/guides/llm/glm-5.2">GLM-5.2 - Overview - Z.AI DEVELOPER DOCUMENT</a></li>

</ul>
</details>

**社区讨论**: 社区对 GLM-5.2 的性能和开源许可证感到非常兴奋。一些用户指出其 token 消耗较高且缺乏视觉输入，但总体评价积极，许多人称赞其 SVG 生成和编码能力。

**标签**: `#LLM`, `#open-weights`, `#AI`, `#GLM-5.2`, `#Mixture of Experts`

---

<a id="item-3"></a>
## [医院和大学以 90%更低成本重新利用药物](https://www.kcl.ac.uk/news/hospitals-and-universities-repurposing-drugs-at-90-lower-cost) ⭐️ 8.0/10

伦敦国王学院的一份报告指出，医院和大学正在以比开发新药低 90%的成本重新利用现有药物，但监管和专利障碍阻碍了广泛采用。 药物重新利用可以大幅降低医疗成本，并为制药公司缺乏激励的罕见病提供治疗方法，可能节省数十亿美元并改善患者可及性。 成本降低是通过跳过早期开发和安全性试验实现的，但重新利用的药物通常缺乏专利保护，使制造商难以收回投资。未经制造商同意的新适应症监管途径有限。

hackernews · giuliomagnifico · 6月18日 10:33 · [社区讨论](https://news.ycombinator.com/item?id=48583386)

**背景**: 药物重新利用是指为已批准或研究中的药物寻找新的治疗用途。由于药物的安全性已知，这比传统药物开发更快、更便宜。然而，专利和监管框架通常有利于新药开发，为重新利用设置了障碍。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC12048090/">Drug repurposing : Clinical practices and regulatory pathways - PMC</a></li>
<li><a href="https://link.springer.com/chapter/10.1007/978-981-95-4522-3_8">Challenges for Drug Repurposing: Special Emphasis on Regulatory and Patent Issues | Springer Nature Link</a></li>
<li><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC10627937/">Drug Repurposing of Generic Drugs: Challenges and the Potential Role for Government - PMC</a></li>

</ul>
</details>

**社区讨论**: 评论者分享了实际案例：有人指出 esketamine（Spravato）是氯胺酮的专利改良版，效果较差但利润丰厚；另有人提到 Cures Within Reach，一个资助亨廷顿病药物重新利用研究的非营利组织。一个关键担忧是缺乏未经制造商同意正式扩展药物用途的监管途径。

**标签**: `#drug repurposing`, `#healthcare`, `#pharmaceuticals`, `#regulatory`, `#cost reduction`

---

<a id="item-4"></a>
## [对比监督微调用于大模型因果依赖映射](https://www.reddit.com/r/MachineLearning/comments/1u8if6l/contrastive_targeted_sft_as_a_mechinterp_method/) ⭐️ 8.0/10

一位研究者提出使用对比目标监督微调（SFT）来定位 31B 模型中特定能力维度的电路，然后消融这些电路，构建能力间因果依赖关系图。 该方法可通过确定最优训练顺序（先训练上游节点）并诊断能力差距，实现更高效的多能力训练，推动机械可解释性超越静态电路发现。 该方法包括从同一检查点训练对比变体（某维度深 vs 浅的样本）以隔离电路，然后消融这些注意力头并测量其他维度的退化，从而推断因果依赖关系。

reddit · r/MachineLearning · /u/Substantial_Diver469 · 6月17日 18:31

**背景**: 机械可解释性旨在将神经网络逆向工程为可理解的组件，例如实现特定能力的电路。消融研究通过移除或损坏组件来理解其作用。对比方法通过比较包含和不包含某概念的输入激活来定位相关电路。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Mechanistic_interpretability">Mechanistic interpretability - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Ablation_(artificial_intelligence)">Ablation (artificial intelligence) - Wikipedia</a></li>
<li><a href="https://arxiv.org/abs/2309.05973">[2309.05973] Circuit Breaking: Removing Model Behaviors with Targeted Ablation</a></li>

</ul>
</details>

**社区讨论**: 该 Reddit 帖子暂无评论，但[D]标签表明预期会有研究级讨论。作者寻求关于电路追踪引导的迭代 SFT 以及区分直接与间接因果效应方法的反馈。

**标签**: `#mechanistic interpretability`, `#supervised fine-tuning`, `#causal inference`, `#model internals`, `#capability analysis`

---

<a id="item-5"></a>
### *（简报）* [康奈尔大学 CS 6120 高级编译器课程现可免费在线学习](https://www.cs.cornell.edu/courses/cs6120/2025fa/self-guided/) ⭐️ 7.0/10

康奈尔大学的 CS 6120 高级编译器课程现已作为免费的自定进度在线资源开放，涵盖 SSA 形式、动态编译等主题。 这提供了来自顶尖学府的免费高质量编译器教育资源，惠及全球学生和专业人士。社区讨论指出了重要的内容缺失，例如缺少类型反馈和去优化等现代技术。 该课程为自定进度，涵盖 SSA 形式和动态编译等高级主题，但社区评论指出它侧重于追踪编译（一种被认为已过时的方法），而缺少类型反馈和去优化等内容。课程基于 Adrian Sampson 教授的康奈尔 CS 6120 课程。

---

<a id="item-6"></a>
### *（简报）* [W Social 因开源声明和商业模式面临质疑](https://blog.elenarossini.com/w-social-public-institutions-and-the-theater-of-european-digital-sovereignty/) ⭐️ 7.0/10

基于 AT Protocol 的欧洲社交网络 W Social 悄然转为闭源，引发对其透明度及与欧洲数字主权目标一致性的担忧。 此举削弱了对 W Social 开源承诺的信任，并凸显了商业利益与欧洲公共部门推动数字主权之间的紧张关系。 W Social 是一家由瑞典企业家拥有的私营营利性有限责任公司，其 GitHub 仓库曾短暂隐藏后恢复。批评者指出，它获得了高调的政治支持，而像 Eurosky 这样的替代开源项目却鲜有媒体报道。

---

<a id="item-7"></a>
### *（简报）* [Modos 彩色显示器推动电子纸显示技术再进一步](https://spectrum.ieee.org/modos-e-paper-monitor) ⭐️ 7.0/10

两人初创公司 Modos 正在开发 Modos Flow，这是一款 13.3 英寸彩色电子纸显示器，原生分辨率 3200x2400，支持触摸输入，刷新率达到 60Hz。 这款显示器通过提供高分辨率和 60Hz 刷新率，可能显著推动电子纸技术发展，使其适合视频播放并减少眼睛疲劳，在特定使用场景中可能挑战传统 LCD 和 OLED 显示器。 Modos Flow 需要两个 USB-C 连接——一个用于 DisplayPort 视频，一个用于补充供电——才能达到完整的 60Hz 刷新率。这是一个开源项目，初创公司目前正在 Crowd Supply 上筹款。

---

<a id="item-8"></a>
### *（简报）* [Ubiquiti 推出基于 ZFS 的企业级 NAS](https://blog.ui.com/article/introducing-enterprise-nas) ⭐️ 7.0/10

Ubiquiti 发布了 Enterprise NAS（ENAS），这是一款 3U 机架式存储设备，配备 16 个 SATA 盘位、双 25GbE SFP28 端口，并原生支持 ZFS，售价为 3,999 美元。 这标志着 Ubiquiti 凭借基于 ZFS 的解决方案进入企业级 NAS 市场，挑战 QNAP 和 Synology 等老牌厂商。无订阅模式以及与 UniFi 管理的集成可能吸引中小企业和 MSP。 ENAS 支持热插拔 M.2 NVMe 缓存、Mini-SAS HD 扩展以实现 PB 级容量，并配备冗余电源。它包含双 25 Gbps SFP28 和 10 GbE RJ45 端口，但社区成员质疑机械硬盘能否饱和 25GbE 链路。

---

<a id="item-9"></a>
### *（简报）* [DeepSeek 为聊天应用添加视觉理解功能](https://chat.deepseek.com/) ⭐️ 7.0/10

DeepSeek 在其聊天应用中引入了视觉能力，使 AI 能够理解和描述图像，但不能生成或修改图像。 此次更新使 DeepSeek 成为多模态 AI，支持更丰富的交互，并扩展了其在文档分析、视觉问答和无障碍访问等场景中的应用。 视觉功能仅限于理解图像，不能生成或编辑图像。DeepSeek 的视觉模型（如 DeepSeek-VL 和 DeepSeek-VL2）是开放权重的，支持视觉问答和文档理解等任务。

---

<a id="item-10"></a>
### *（简报）* [Git 的全局和仓库级排除文件：.gitignore 的替代方案](https://nelson.cloud/.gitignore-isnt-the-only-way-to-ignore-files-in-git/) ⭐️ 7.0/10

文章指出，Git 提供了全局和仓库级排除文件作为 .gitignore 的替代方案，用于忽略个人或环境特定文件，而不会影响其他协作者。 此功能帮助开发者避免将 IDE、操作系统或 AI 生成的文件提交到共享仓库，减少噪音并防止意外提交个人配置。 全局排除文件通过 core.excludesFile 配置（默认 ~/.config/git/ignore），而仓库级排除文件位于 .git/info/exclude。两者都不会被提交到仓库。

---

<a id="item-11"></a>
### *（简报）* [对话级语音调试优于孤立基准测试，用于多轮 AI 评估](https://www.reddit.com/r/MachineLearning/comments/1u99fe5/voice_debugging_at_the_conversation_level_seems/) ⭐️ 7.0/10

一位 Reddit 用户根据自动对话级 QA 的实践经验提出，对话级语音调试在评估真实世界多轮对话系统时远比孤立的基准测试指标更有用。 这一观点挑战了对传统基准测试（如语音识别分数和任务完成率）的依赖，这些指标常常遗漏多轮交互中令用户沮丧的涌现性失败。它凸显了评估方法需要捕捉对话模式和交互动态的日益增长的需求。 作者指出，微小的时序错误、重复确认和不自然的轮换会累积成令人沮丧的体验，但传统基准测试无法捕捉这些。他们的团队现在专注于识别重复出现的对话模式，而非单个模型失败。

---

<a id="item-12"></a>
### *（简报）* [没有高性能计算，基础 AI 研究还能做吗？](https://www.reddit.com/r/MachineLearning/comments/1u8jyat/is_foundational_ai_research_still_something_that/) ⭐️ 7.0/10

一位 Reddit 用户提问，在没有高性能计算（HPC）资源的情况下，基础 AI 研究是否仍然可行，并指出最初的 Transformer 论文仅用了几块高端游戏 GPU 进行训练。 这个问题凸显了 AI 研究中日益增长的准入门槛：随着模型规模扩大，HPC 变得不可或缺，可能将独立研究者和小型实验室排除在基础贡献之外。 用户承认自己能够负担与原始 Transformer 论文相当的硬件（例如几块高端 GPU），但想知道如今这些资源是否足以支撑最先进的基础研究工作。

---

<a id="item-13"></a>
### *（简报）* [机械可解释性中探针容量与网络容量的权衡](https://www.reddit.com/r/MachineLearning/comments/1u8lo60/how_do_you_analyze_the_relative_strength_of/) ⭐️ 7.0/10

一位研究者提出了一个关于机械可解释性中探针容量与网络容量平衡的理论保证的细致问题，特别关注于分析模型对词元分解和位置编码的“认知”。 这个问题凸显了机械可解释性中的一个关键方法论空白：如果没有关于探针容量的清晰理论，关于模型“知道”什么的结论可能不可靠。解决这一问题可以提高电路分析和 AI 安全性研究中事实性保证的严谨性。 研究者引用了一篇旧帖，其中使用逻辑回归探针检测词元位置，并指出较小的词汇量可能夸大探针性能。他们还提供了一个真实案例：Gemini 错误地统计了“Google”中的字母数量，表明模型缺乏稳健的词元分解能力。

---

