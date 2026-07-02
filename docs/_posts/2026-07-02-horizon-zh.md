---
layout: default
title: "Horizon Daily: 2026-07-02 (ZH)"
date: 2026-07-02
lang: zh
period: daily
period_id: 2026-07-02
---

> 从 22 条内容中筛选出 8 条重要资讯。

其中 **5 条 8 分以上**展开详细简报，其余 3 条仅列于索引。

---

1. [Linux 6.9 回归：LUKS 挂起时未清除内存中的加密密钥](#item-1) ⭐️ 8.0/10
2. [F-Droid：谷歌的开发者验证是特洛伊木马](#item-2) ⭐️ 8.0/10
3. [日本最高法院裁定人工智能不能列为专利发明人](#item-3) ⭐️ 8.0/10
4. [定理经济的衰落](#item-4) ⭐️ 8.0/10
5. [从微分几何视角看哈密顿神经网络](#item-5) ⭐️ 8.0/10
6. [代码审查的首要目的：发现难以维护的代码](#item-6) ⭐️ 7.0/10
7. [SentryCode：面向 AI 编程代理的开源内核级审计工具，集成蜜令令牌](#item-7) ⭐️ 7.0/10
8. [Gnosys 在标签稀缺下提升安全分类器性能](#item-8) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [Linux 6.9 回归：LUKS 挂起时未清除内存中的加密密钥](https://mathstodon.xyz/@iblech/116769502749142438) ⭐️ 8.0/10

Linux 内核 6.9 版本中的一个回归问题导致 LUKS（Linux 统一密钥设置）挂起功能不再从内存中清除磁盘加密密钥，使得密钥在挂起到 RAM 期间暴露。 这一安全回归削弱了 LUKS 加密磁盘的保护，因为拥有物理访问权限的攻击者可能从挂起笔记本电脑的 RAM 中提取加密密钥，从而危及磁盘上的所有数据。 该回归影响的是挂起到 RAM（S3 睡眠），而非休眠。此前，LUKS 挂起会从内核内存中清除主密钥；自 6.9 版本起，此步骤被跳过，导致密钥驻留在 RAM 中。

hackernews · IngoBlechschmid · 7月2日 15:25 · [社区讨论](https://news.ycombinator.com/item?id=48763035)

**背景**: LUKS 是 Linux 的磁盘加密规范，使用主密钥加密数据。当系统挂起到 RAM 时，通常会将主密钥从内存中清除，以防止冷启动攻击或物理内存提取。cryptsetup luksSuspend 命令用于临时锁定 LUKS 设备并清除密钥。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.reddit.com/r/archlinux/comments/hpd4hh/suspend_with_luks/">r/archlinux on Reddit: Suspend with LUKS</a></li>
<li><a href="https://security.stackexchange.com/questions/49074/erasing-encryption-luks-keys-before-suspend-to-ram">linux - Erasing encryption ( LUKS ) keys before suspend-to-RAM?</a></li>
<li><a href="https://wiki.archlinux.org/title/Dm-crypt/Device_encryption">dm-crypt/Device encryption - ArchWiki</a></li>

</ul>
</details>

**社区讨论**: 社区评论显示出不同的理解：一些用户指出安全漏洞是无声的，而另一些用户则认为密钥必须留在内存中才能在不重新输入密码的情况下恢复。关于实际威胁存在争议，一些人质疑从锁定的笔记本电脑中读取 RAM 的难易程度。

**标签**: `#Linux`, `#security`, `#encryption`, `#LUKS`, `#kernel`

---

<a id="item-2"></a>
## [F-Droid：谷歌的开发者验证是特洛伊木马](https://f-droid.org/2026/07/01/adv-malware.html) ⭐️ 8.0/10

F-Droid 发布文章指出，谷歌为打击侧载应用恶意软件而推出的 Android 开发者验证，实际上是一种伪装成保护的威胁。文章称该验证系统可能被用来阻止 F-Droid 等替代应用商店，损害用户自由。 此事意义重大，因为 Android 开发者验证可能集中控制应用分发，损害依赖侧载的开源和替代应用商店。它引发了关于用户自由以及 Android 作为开放平台未来的担忧。 谷歌的验证要求开发者提供身份证明并注册包名，侧载未验证应用时需等待一天并通过生物识别认证。F-Droid 认为这制造了障碍，可能被用来阻止来自未验证开发者的应用，实际上赋予谷歌对侧载软件的否决权。

hackernews · drewfax · 7月2日 03:00 · [社区讨论](https://news.ycombinator.com/item?id=48755965)

**背景**: F-Droid 是一个面向 Android 的免费开源应用商店，仅托管自由开源软件，允许用户无需谷歌账户即可安装应用。侧载是指从官方 Google Play 商店之外安装应用的过程，由于此类来源的恶意软件率更高，谷歌一直在加强其安全性。Android 开发者验证于 2026 年 3 月宣布，旨在通过要求开发者验证身份来减少侧载应用的恶意软件。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://android-developers.googleblog.com/2026/03/android-developer-verification.html">Android Developers Blog: Android developer verification: Balancing openness and choice with safety</a></li>
<li><a href="https://en.wikipedia.org/wiki/F-Droid">F-Droid</a></li>

</ul>
</details>

**社区讨论**: 评论意见不一：一些用户同意 F-Droid 的担忧，并建议改用 SailfishOS 或 GrapheneOS 等替代移动操作系统。另一些用户批评文章语气幼稚且适得其反，可能损害 F-Droid 的可信度。少数人指出 Keep Android Open 运动是更有效的方式。

**标签**: `#Android`, `#security`, `#app stores`, `#F-Droid`, `#Google`

---

<a id="item-3"></a>
## [日本最高法院裁定人工智能不能列为专利发明人](https://japannews.yomiuri.co.jp/science-nature/technology/20260306-314930/) ⭐️ 8.0/10

日本最高法院裁定，人工智能不能列为专利申请的发明人，确认根据日本专利法，只有人类才能被视为发明人。 这一裁决在日本确立了重要的法律先例，与美国等地的类似裁决保持一致，明确了人工智能发明权的边界，对人工智能创新和知识产权政策产生影响。 该案由斯蒂芬·塞勒提起，他在全球范围内进行了类似诉讼，唯一成功的案例是在南非获得专利。裁决强调人工智能缺乏法律人格和问责能力。

hackernews · mushstory · 7月2日 13:43 · [社区讨论](https://news.ycombinator.com/item?id=48761536)

**背景**: 专利法传统上要求发明人必须是自然人。随着人工智能系统能够生成发明，全球法院都在探讨人工智能能否被列为发明人。日本的裁决遵循了美国联邦巡回法院的决定，即只有人类才能成为发明人。

**社区讨论**: 评论者表达了不同观点：一些人欢迎这一裁决，认为人工智能缺乏问责能力，不应享有利益；另一些人则质疑专利在促进创新方面的有效性，引用了经济学研究。一位评论者指出，如果人工智能能发明，那么该发明应被视为显而易见的。

**标签**: `#AI`, `#patent law`, `#intellectual property`, `#Japan`, `#regulation`

---

<a id="item-4"></a>
## [定理经济的衰落](https://davidbessis.substack.com/p/the-fall-of-the-theorem-economy) ⭐️ 8.0/10

文章认为，数学中传统的定理证明经济正被人工智能和形式化所颠覆，焦点转向直觉和洞察。 这种范式转变可能从根本上改变数学的研究方式，降低严格证明的价值，提升人类直觉和 AI 辅助发现的作用。 文章引用了 Greg Egan 的小说《Diaspora》，其中设想在形式化记录所有定理且证明助手处理细节后，数学演变为“真理挖掘”。

hackernews · varjag · 7月2日 08:01 · [社区讨论](https://news.ycombinator.com/item?id=48758048)

**背景**: 定理经济指的是数学中证明新定理的传统价值。形式化涉及使用 Lean 等证明助手机械地验证证明，而 AI 可以自动生成猜想和证明。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Formalization_of_mathematics">Formalization of mathematics</a></li>
<li><a href="https://arxiv.org/pdf/2311.00007">Mathematics and the formal turn</a></li>

</ul>
</details>

**社区讨论**: 评论者指出 Greg Egan 的预见性想法，并与软件测试进行类比，认为随着形式化的发展，数学可能更依赖直觉和测试而非严格证明。

**标签**: `#mathematics`, `#AI`, `#formalization`, `#theorem proving`, `#research`

---

<a id="item-5"></a>
## [从微分几何视角看哈密顿神经网络](https://www.reddit.com/r/MachineLearning/comments/1ukzdnj/hamiltonian_neural_networks_from_a_differential/) ⭐️ 8.0/10

一篇博客文章从微分几何的角度介绍了哈密顿神经网络（HNN），强调了诺特定理和对称性在提升泛化能力方面的作用。 这一视角通过诺特定理将守恒定律与对称性联系起来，深入解释了 HNN 为何能良好泛化，这在物理信息机器学习中尚未得到充分探索。 文章包含交互式可视化，数学内容较多但力求易于理解。它侧重于 HNN 的几何结构，而不仅仅是损失函数。

reddit · r/MachineLearning · /u/FlameOfIgnis · 7月1日 21:55

**背景**: 哈密顿神经网络受哈密顿力学启发，该力学用能量守恒描述系统。诺特定理指出每个连续对称性对应一个守恒定律。微分几何提供了研究神经网络中对称性和不变量的工具。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://greydanus.github.io/2019/05/15/hamiltonian-nns/">Hamiltonian Neural Networks</a></li>
<li><a href="https://en.wikipedia.org/wiki/Noether's_theorem">Noether's theorem</a></li>
<li><a href="https://arxiv.org/abs/1906.01563">[1906.01563] Hamiltonian Neural Networks</a></li>

</ul>
</details>

**标签**: `#Hamiltonian Neural Networks`, `#Differential Geometry`, `#Physics-Informed ML`, `#Noether's Theorem`, `#Machine Learning`

---

<a id="item-6"></a>
### *（简报）* [代码审查的首要目的：发现难以维护的代码](https://mathstodon.xyz/@mjd/115096720350507897) ⭐️ 7.0/10

Mathstodon 上的一场讨论认为，代码审查的首要目的是发现难以维护的代码，这引发了关于代码审查多重目的的不同观点。 这场讨论凸显了软件工程中关于代码审查真正价值的持续辩论，影响着最佳实践和团队协作。 评论者强调，代码审查具有多种目的，包括安全检查、知识传递、团队所有权和缺陷检测，而不仅仅是可维护性。

---

<a id="item-7"></a>
### *（简报）* [SentryCode：面向 AI 编程代理的开源内核级审计工具，集成蜜令令牌](https://www.reddit.com/r/MachineLearning/comments/1ul7ap2/sentrycode_realtime_auditor_honeytokens_for_ai/) ⭐️ 7.0/10

随着 AI 编程代理日益普及，关于遥测、环境扫描和隐藏提示指纹识别的担忧也在增加。SentryCode 提供了一种新颖的开源防御方案，在内核层面应对这些隐私风险，并通过蜜令令牌实现零误报的数据泄露检测。 该工具能够检测经过隐写加密的隐蔽信道，并生成防篡改的审计日志。它完全在本地运行，提供预编译二进制文件用于演示，代码托管在 GitHub 上（https://github.com/byte271/sentrycode）。

---

<a id="item-8"></a>
### *（简报）* [Gnosys 在标签稀缺下提升安全分类器性能](https://www.reddit.com/r/MachineLearning/comments/1ul3ohk/making_optimization_work_when_labels_are_scarce_r/) ⭐️ 7.0/10

Gnosys 是一款自主模型工程师工具，在真实标签稀缺的情况下改进安全分类器，在 ToxicChat 基准测试上优于标准提示优化器 GEPA。 这解决了部署高风险 AI 分类器（如内容审核、欺诈检测）中的关键挑战——标注数据昂贵且稀疏，有望提升安全性和可靠性。 在 3000 个标签的主要运行中，Gnosys 在固定假阳性率为 5%的条件下，有害内容捕获得分为 0.777，而起始分类器为 0.731，GEPA 为 0.702。Gnosys 将少量已验证样本与大量未标注池融合，生成校准后的质量估计。

---

