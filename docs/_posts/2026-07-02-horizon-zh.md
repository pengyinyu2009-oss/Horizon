---
layout: default
title: "Horizon Daily: 2026-07-02 (ZH)"
date: 2026-07-02
lang: zh
period: daily
period_id: 2026-07-02
---

> 从 22 条内容中筛选出 9 条重要资讯。

其中 **4 条 8 分以上**展开详细简报，其余 5 条仅列于索引。

---

1. [Linux 6.9 回归：LUKS 挂起时未从内存中清除加密密钥](#item-1) ⭐️ 8.0/10
2. [F-Droid 警告谷歌开发者验证威胁安卓侧载](#item-2) ⭐️ 8.0/10
3. [定理经济的衰落](#item-3) ⭐️ 8.0/10
4. [从微分几何视角看哈密顿神经网络](#item-4) ⭐️ 8.0/10
5. [PeerTube：一个免费、去中心化、联邦制的视频平台替代品](#item-5) ⭐️ 7.0/10
6. [日本最高法院：AI 不能列为专利发明人](#item-6) ⭐️ 7.0/10
7. [代码审查的首要目的：发现难以维护的代码](#item-7) ⭐️ 7.0/10
8. [SentryCode：面向 AI 编程代理的开源内核级审计工具](#item-8) ⭐️ 7.0/10
9. [Gnosys 在标签稀缺下提升安全分类器性能](#item-9) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [Linux 6.9 回归：LUKS 挂起时未从内存中清除加密密钥](https://mathstodon.xyz/@iblech/116769502749142438) ⭐️ 8.0/10

Linux 内核 6.9 版本中的一个回归导致 LUKS（Linux 统一密钥设置）挂起机制在系统挂起时不再从内存中清除磁盘加密密钥，可能使攻击者能够访问这些密钥。 这是一个重大的安全问题，因为它削弱了加密磁盘的关键保护措施：确保在挂起期间从内存中移除加密密钥，以防止冷启动攻击或物理访问攻击。该回归影响所有依赖 LUKS 进行全盘加密的用户。 该回归在 Linux 6.9 中引入，且未被注意到，因为系统仍能正常运行——密钥仍留在内存中但未被清除。该问题已在 Mastodon 上报告，并已得到内核社区的确认。

hackernews · IngoBlechschmid · 7月2日 15:25 · [社区讨论](https://news.ycombinator.com/item?id=48763035)

**背景**: LUKS 是 Linux 的磁盘加密规范，使用主密钥加密数据。在挂起（挂起到 RAM）期间，系统将主密钥保留在内存中，以便快速恢复而无需重新输入密码。为了防止读取内存的攻击（例如冷启动攻击），内核通常会在挂起前从内存中清除密钥。此回归破坏了这一保护机制。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/systemd/systemd/issues/17887">Wipe LUKS Disk Encryption Key for Root Disk from RAM during ...</a></li>
<li><a href="https://www.sec.in.tum.de/i20/publications/fridgelock-preventing-data-theft-on-suspended-linux-with-usable-memory-encryption">FridgeLock: Preventing Data Theft on Suspended Linux with Usable...</a></li>

</ul>
</details>

**社区讨论**: 社区评论指出，由于系统仍能正常工作，该回归很容易被忽略。一些用户质疑实际风险，指出锁定的笔记本电脑仍需要物理访问才能提取内存。其他人则指出，密钥必须留在内存中才能在不重新输入密码的情况下恢复，但问题在于挂起前未将其清除。

**标签**: `#Linux`, `#security`, `#LUKS`, `#encryption`, `#kernel`

---

<a id="item-2"></a>
## [F-Droid 警告谷歌开发者验证威胁安卓侧载](https://f-droid.org/2026/07/01/adv-malware.html) ⭐️ 8.0/10

F-Droid 发布文章警告称，谷歌的安卓开发者验证系统虽然被包装成恶意软件保护，但实际上威胁到了应用的侧载安装和用户对设备的控制权。 该系统可能限制从 Play 商店之外安装应用的能力，损害安卓的开放性和用户自由。它引发了关于侧载未来和替代移动操作系统的讨论。 该验证系统要求开发者在发布应用前进行身份检查，对使用敏感权限的应用进行更深入的审查。F-Droid 认为这赋予了谷歌对哪些应用可以侧载的控制权。

hackernews · drewfax · 7月2日 03:00 · [社区讨论](https://news.ycombinator.com/item?id=48755965)

**背景**: 侧载是指从官方 Google Play 商店以外的来源（如 F-Droid）安装安卓应用。F-Droid 是一个自由开源的应用仓库，仅托管自由开源软件。谷歌新的开发者验证系统于 2025 年底推出，要求开发者验证身份，可能阻止未经验证的应用被侧载。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.androidsage.com/2025/08/26/google-blocks-sideloading-of-android-apps/">It's Over: Google Blocks Sideloading of Android Apps</a></li>
<li><a href="https://en.wikipedia.org/wiki/F-Droid">F-Droid</a></li>
<li><a href="https://en.wikipedia.org/wiki/Sideloading">Sideloading - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 评论显示了对验证系统的强烈反对，用户表达了沮丧，并建议使用 GrapheneOS 或基于 Linux 的移动操作系统等替代方案。一些人批评 F-Droid 的文章过于夸张，但总体情绪倾向于保持安卓的开放性。

**标签**: `#Android`, `#F-Droid`, `#Open Source`, `#Mobile Security`, `#Privacy`

---

<a id="item-3"></a>
## [定理经济的衰落](https://davidbessis.substack.com/p/the-fall-of-the-theorem-economy) ⭐️ 8.0/10

David Bessis 认为，数学中传统的定理证明经济正在衰落，取而代之的是计算性和直觉性的方法。 这一转变可能从根本上改变数学的实践和评价方式，将重点从严谨证明转向通过计算进行探索和验证。 文章将数学与软件测试相类比，后者通过测试和使用建立信心而非形式化证明。文章还引用了 Greg Egan 小说《Diaspora》中的“真理挖掘”概念。

hackernews · varjag · 7月2日 08:01 · [社区讨论](https://news.ycombinator.com/item?id=48758048)

**背景**: 定理证明长期以来一直是数学的核心，证明被视为真理的黄金标准。然而，证明助手和人工智能的兴起正在自动化形式化过程，而计算方法允许在没有完整证明的情况下进行探索。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Proof_assistant">Proof assistant</a></li>
<li><a href="https://en.wikipedia.org/wiki/Mathematical_economics">Mathematical economics - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 评论者指出与软件测试和 Egan 的“真理挖掘”的相似之处，认为数学可能演变为更经验性、测试驱动的学科。一些人担心由于私人 AI 资源，科学公开分享会减少。

**标签**: `#mathematics`, `#theorem proving`, `#AI`, `#philosophy of math`, `#proof assistants`

---

<a id="item-4"></a>
## [从微分几何视角看哈密顿神经网络](https://www.reddit.com/r/MachineLearning/comments/1ukzdnj/hamiltonian_neural_networks_from_a_differential/) ⭐️ 8.0/10

一篇博客文章从微分几何角度解释哈密顿神经网络（HNN），强调诺特定理将对称性与守恒定律联系起来。 这一视角提供了对 HNN 为何泛化良好的更深入理解，将物理原理与机器学习归纳偏置联系起来。 文章包含交互式可视化，数学内容较多但易于理解。作者在 HNN 和 LNN 相关领域有多年经验。

reddit · r/MachineLearning · /u/FlameOfIgnis · 7月1日 21:55

**背景**: 哈密顿神经网络是一类物理信息神经网络，学习哈密顿动力学，保持能量守恒。诺特定理指出每个连续对称性对应一个守恒定律，这是理解 HNN 归纳偏置的关键。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/1906.01563">[1906.01563] Hamiltonian Neural Networks</a></li>
<li><a href="https://en.wikipedia.org/wiki/Noether's_theorem">Noether's theorem</a></li>
<li><a href="https://greydanus.github.io/2019/05/15/hamiltonian-nns/">Hamiltonian Neural Networks</a></li>

</ul>
</details>

**社区讨论**: 鉴于高分，Reddit 讨论可能很有深度，但未提供具体评论。

**标签**: `#Hamiltonian Neural Networks`, `#differential geometry`, `#Noether's theorem`, `#physics-informed ML`, `#deep learning`

---

<a id="item-5"></a>
### *（简报）* [PeerTube：一个免费、去中心化、联邦制的视频平台替代品](https://github.com/Chocobozzz/PeerTube) ⭐️ 7.0/10

PeerTube 是一个免费开源、去中心化的视频平台，它利用 ActivityPub 联邦协议和点对点技术，将视频托管分布到各个独立的实例上。 PeerTube 提供了一个抗审查的替代方案，取代了 YouTube 等中心化平台，让内容创作者和社区对自己的视频内容和数据隐私拥有更多控制权。 任何人都可以运行 PeerTube 实例，视频通过 ActivityPub 在联邦内共享。当视频变得流行时，点对点流媒体有助于减轻服务器负载。

---

<a id="item-6"></a>
### *（简报）* [日本最高法院：AI 不能列为专利发明人](https://japannews.yomiuri.co.jp/science-nature/technology/20260306-314930/) ⭐️ 7.0/10

日本最高法院裁定，人工智能不能被列为专利申请的发明人，维持了以人为中心的专利法解释。 这一裁决为 AI 发明人身份确立了关键法律先例，强调只有人类才能拥有专利权，影响 AI 生成发明的保护与激励机制。 该裁决源于一起发明人试图将 AI 系统列为发明人的案件。法院确认《专利法》要求发明人必须是“自然人”。

---

<a id="item-7"></a>
### *（简报）* [代码审查的首要目的：发现难以维护的代码](https://mathstodon.xyz/@mjd/115096720350507897) ⭐️ 7.0/10

Mathstodon 上的一篇文章认为，代码审查的首要目的是找出难以维护的代码，而非发现错误。该帖子引发了超过 117 条评论的丰富讨论，探讨了代码审查的多重角色。 这场辩论挑战了代码审查主要用于发现错误的常见假设，强调可维护性是软件质量的关键因素。它影响团队如何优先安排审查工作，并塑造软件工程的最佳实践。 原帖声称通过代码审查发现错误通常是不可能的，这一点遭到评论者反驳，他们举出了未关闭文件描述符等例子。评论者还强调了其他目的，如知识传递、团队所有权以及针对恶意代码的安全检查。

---

<a id="item-8"></a>
### *（简报）* [SentryCode：面向 AI 编程代理的开源内核级审计工具](https://www.reddit.com/r/MachineLearning/comments/1ul7ap2/sentrycode_realtime_auditor_honeytokens_for_ai/) ⭐️ 7.0/10

SentryCode 是一款开源的内核级审计工具，通过蜜令令牌和防篡改日志来监控 AI 编程代理的数据泄露和隐蔽通道行为。 随着 AI 编程代理的普及，关于遥测和数据泄露的隐私担忧日益增加。SentryCode 提供了一种全新的、零误报的检测方法，且完全在本地运行，填补了关键的安全空白。 该工具记录文件、网络和提示活动，检测隐写加密的隐蔽通道，并支持策略执行。所有功能均在本地运行，无任何出站连接，并提供预编译二进制文件用于演示。

---

<a id="item-9"></a>
### *（简报）* [Gnosys 在标签稀缺下提升安全分类器性能](https://www.reddit.com/r/MachineLearning/comments/1ul3ohk/making_optimization_work_when_labels_are_scarce_r/) ⭐️ 7.0/10

Gnosys Labs 提出了一种自主模型工程方法，在真实标签稀缺时改进提示和分类器。在 ToxicChat 基准测试中，它优于初始分类器和 GEPA 提示优化器，在 5% 误报率下实现了高达 0.909 的有害内容捕获率。 标签稀缺是内容审核、欺诈检测等高安全性 AI 应用中的常见挑战。Gnosys 的方法将稀疏标签与未标注数据融合，构建更好的优化目标，有望在无需大量标注数据的情况下实现更可靠的分类器调优。 Gnosys 使用稀疏标签和未标注池的校准质量估计，包含逐片校准和可信度检查。在 3000 个标签的主要运行中，Gnosys 的有害内容捕获率为 0.777，而初始分类器为 0.731，GEPA 为 0.702；在 1000 个标签的先前运行中，Gnosys 达到 0.909，对比 0.788 和 0.848。

---

