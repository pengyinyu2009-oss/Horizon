---
layout: default
title: "Horizon Daily: 2026-09-11 (ZH)"
date: 2026-09-11
lang: zh
period: daily
period_id: 2026-09-11
---

> 从 19 条内容中筛选出 6 条重要资讯。

其中 **2 条 8 分以上**展开详细简报，其余 4 条仅列于索引。

---

1. [OpenAI 发布 Navier-Stokes 成果，附 Lean 4 形式化证明](#item-1) ⭐️ 8.0/10 · 相关 3/10
2. [微软正式将 Rust 列为 tier-1 级别语言](#item-2) ⭐️ 8.0/10 · 相关 5/10
3. [Shopify 从 React Native 回归 Swift 与 Kotlin 原生开发](#item-3) ⭐️ 7.0/10 · 相关 2/10
4. [Forgejo <=16.0.3 存在严重远程代码执行漏洞](#item-4) ⭐️ 7.0/10 · 相关 4/10
5. [WeWorm：首个通过微信通话传播的零点击蠕虫，由 AI 在约两周内构建完成](#item-5) ⭐️ 7.0/10 · 相关 3/10
6. [我尝试让真实的果蝇连接组学习打 Pong，结果失败了——而审计失败原因竟然比它成功更有趣 (p)](#item-6) ⭐️ 7.0/10 · 相关 3/10

---

<a id="item-1"></a>
## [OpenAI 发布 Navier-Stokes 成果，附 Lean 4 形式化证明](https://www.johndcook.com/blog/2026/09/09/formal-method-revolution/) ⭐️ 8.0/10 · 相关 3/10

OpenAI 发布了与 Navier-Stokes 相关的成果，其中包含一段由 AI 生成、并通过机器验证的 Lean 4 形式化数学证明。据社区披露，验证阶段消耗约 230 GB 内存、耗时约 15 小时，而由 AI 智能体集群生成对应 Lean 代码大约耗时 11 天。 这是 AI 不仅能给出合理的数学推理、还能产出可被机器检查的形式化成果的里程碑，大幅降低了机械化数学的成本门槛。它预示着数学研究、软件验证与 AI 辅助工程之间的协作方式可能发生结构性转变。 社区估算 AI 一侧的计算成本约为 4000 万美元，而等效人力工作约需 1.32 亿美元（≈88 万专家小时），因此加速比更接近三个数量级而非四个。Lean 4 本身是验证阶段的瓶颈，其刻意做小、便于审计的内核限制了其优化空间。

hackernews · ibobev · 9月10日 21:22 · [社区讨论](https://news.ycombinator.com/item?id=49650326)

**背景**: Lean 4 既是一门函数式编程语言，也是一个交互式定理证明器，可用于编写机器可检查的数学命题与软件正确性的形式化证明。形式化证明是由良构公式构成的有限序列，严格依据公理与推理规则推导，从而消除非形式化论证中的歧义。自动定理证明（ATP）将符号搜索与近年出现的深度学习智能体相结合，既可以自动发现证明，也可以为人类证明者推荐可用的策略。

**对中国影响**: 中国形式化方法社区（中科院、北航以及华为内部的形式化验证团队）已在定理证明器方向投入大量资源，在困难 PDE 上 AI 与人类的基准对比很可能推动国内加码 AI 辅助验证工具链。同时，这也给国内前沿数学与 AI 团队带来竞争压力，需要拿出可对标的形式化证明能力。

**对我有什么用**: 对硬件/嵌入式工程师而言，直接关联不算紧密，但其底层理念——AI 生成的代码本身经过机器验证——正是让 AI 辅助 HDL 或固件代码值得信任所需要的。Lean 中开创的策略建议范式正在被推广为面向软件的 AI 编程副驾，未来也有望延伸到硬件验证流程。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Formal_proof">Formal proof - Wikipedia</a></li>
<li><a href="https://leandojo.org/">AI-Driven Formal Theorem Proving in the Lean Ecosystem</a></li>
<li><a href="https://www.mathlumen.com/articles/formal-proofs-lean-mathematics">The Formal Proof Revolution: How Lean Is Rebuilding... | MathLumen</a></li>
<li><a href="https://en.wikipedia.org/wiki/Automated_theorem_proving">Automated theorem proving - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 评论者分化为两派：一派为这一成就感到震撼，另一派则不满讨论偏离数学结果本身，滑向成本数字与 Lean 性能。反复出现的话题包括：在不损害可审计内核的前提下 Lean 还能否加速，以及当 AI 解出人类无法独立验证的难题时该如何应对。

**标签**: `#AI`, `#Formal Verification`, `#Lean 4`, `#Mathematics`, `#OpenAI`

---

<a id="item-2"></a>
## [微软正式将 Rust 列为 tier-1 级别语言](https://rustfoundation.org/media/guest-post-rust-is-tier-1-language-at-microsoft/) ⭐️ 8.0/10 · 相关 5/10

微软已正式将 Rust 提升为公司内部的 tier-1 生产语言，与 C++ 和 C# 处于同一等级。与此同时，微软披露了一项长期工程计划，目标是借助自动化工具把大约十亿行 C/C++ 老代码迁移到 Rust，预计每位工程师每月可完成一百万行的转换量。 这一决定是里程碑式的认可，标志着 Rust 已从新兴语言成长为成熟的系统级编程语言，并将加速整个行业向内存安全软件的转型。随着所有主流操作系统厂商都把 Rust 列为新建项目的首选，Rust 周边安全工具和开发生态也将快速壮大。 Rust 并没有取代微软内部的 C++，C++ 凭借数十年的代码积累依然占据主导地位，但 Rust 现在获得了编译器、安全审查和发布流程的一等支持。据 Azure CTO Mark Russinovich 透露，微软历史上有约 70% 的 CVE 与内存安全相关，这也是推动迁移的最主要动机；与此同时，DARPA 正在资助另一项专门研究 C 到 Rust 自动翻译的项目。

hackernews · mmastrac · 9月10日 13:39 · [社区讨论](https://news.ycombinator.com/item?id=49643546)

**背景**: 在微软的内部语言分级体系中，tier-1 意味着该语言可以享受完整的生产级工具链、调试器、性能优化和安全审查支持，而更低等级的语言往往只有社区级别的维护。内存安全漏洞（如缓冲区溢出、释放后使用、重复释放）困扰 C 和 C++ 已经数十年，至今仍是操作系统和浏览器中绝大多数严重漏洞的根源。Rust 通过编译期的所有权和借用检查机制，在不增加运行时开销的前提下从源头消除了一整类内存错误。

**对中国影响**: 随着内存安全逐渐成为行业基准，华为、阿里、腾讯等中国云厂商和操作系统厂商很可能会加快自家采用 Rust 的节奏，国内市场对熟悉系统编程的 Rust 工程师的需求也会随之上升。不过 DARPA 资助的 C 到 Rust 自动转换工具来自美国政府项目，可能受到出口管制影响，这会促使国内开发者去支持或自行构建开源替代方案。

**对我有什么用**: 对从事嵌入式和硬件开发的工程师来说，这一变化意味着 Rust 工具链（包括基于 LLVM 的交叉编译、RISC-V 支持以及各类 HAL crate）将获得持续的一流投入，值得作为固件和裸机项目的长期技术选型。建议现在就在 RISC-V 开发板或小型 MCU 上试用 Rust 进行实践，赶在生态进一步成熟前积累经验。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://rustfoundation.org/media/guest-post-rust-is-tier-1-language-at-microsoft/">Guest Post: Rust Is Tier - 1 Language at Microsoft</a></li>
<li><a href="https://kobzol.github.io/rust/2026/06/15/how-memory-safety-cves-differ-between-rust-and-c-cpp.html">How memory safety CVEs differ between Rust and C/C++ | Kobzol’s blog</a></li>
<li><a href="https://www.sciencedirect.com/science/article/pii/S1877050923016757">Rust's Memory Safety Model: An Evaluation of Its Effectiveness in Preventing Common Vulnerabilities - ScienceDirect</a></li>

</ul>
</details>

**社区讨论**: Hacker News 上的讨论普遍对这一消息表示欢迎，认为它印证了 Rust 已经从新生语言成长为可以与 C++、C# 同台竞争的成熟方案，有人指出在工具链成熟度上 Rust 已经领先 Zig、Odin 等更新的替代品。多位评论者从战略角度分析，指出微软拥有大量历史 CVE 的产品线最能从强制内存安全中获益；也有用户提到 DARPA 资助的 C 到 Rust 自动翻译研究是整个迁移计划的关键使能技术。少数质疑者则担心十亿行遗留代码的迁移在成本和行为兼容性方面是否真的可行。

**标签**: `#Rust`, `#Microsoft`, `#systems-programming`, `#memory-safety`, `#embedded`

---

<a id="item-3"></a>
### *（简报）* [Shopify 从 React Native 回归 Swift 与 Kotlin 原生开发](https://shopify.engineering/back-to-native) ⭐️ 7.0/10 · 相关 2/10

Shopify 宣布其移动应用将从 React Native 撤出，回到使用 Swift 和 Kotlin 的纯原生开发路径。这一决定重新审视了 2020 年时押注 React Native 的核心假设：在 LLM 能够直接生成各平台原生代码的今天，原本用一份代码让前端开发者兼顾移动端的主要理由已经不再成立。 Shopify 是目前公开承认从跨平台移动框架撤退的最大体量公司之一，而它给出的触发因素——LLM 改变了原生代码生成的成本结构——将被其他技术负责人反复参照。这一事件还重新定义了过去十年的「原生 vs 跨平台」之争：既然 AI 能够快速写出 Swift 与 Kotlin，过去认为原生开发人手太贵的论据就被大幅削弱了。 社区反馈显示迁移速度可能比预期更快：一位工程师（atonse）描述自己用 Codex 加上 Maestro 做 UI 测试，把一个 15–20 个屏幕的 React Native 应用在一夜之间转成了可运行的 iOS 与 Android 原生工程。但也有反例（netshade）指出，他主导的中等规模迁移在 2026 年 1 月之前就完成了大部分工作，期间并没有用 LLM 辅助，因此 AI 更多的是加快了收尾打磨，而非决定性推动了迁移本身。

---

<a id="item-4"></a>
### *（简报）* [Forgejo <=16.0.3 存在严重远程代码执行漏洞](https://codeberg.org/forgejo/forgejo/src/branch/forgejo/release-notes-published/16.0.4.md) ⭐️ 7.0/10 · 相关 4/10

Forgejo 16.0.3 及更早版本在模板仓库初始化流程中存在一个严重的远程代码执行（RCE）漏洞。当用户从模板生成新仓库时，变量模板展开操作会干扰 Git 仓库的初始化过程，攻击者可借此执行任意代码。建议所有受影响的用户立即升级到 16.0.4 版本。 Forgejo 是一个被广泛部署的自托管 Git 平台，在希望替代 GitHub 等中心化服务的开源社区和组织中尤为流行。其核心模板仓库功能出现严重 RCE 漏洞，意味着任何未打补丁的实例都可能被低权限甚至未授权用户完全控制，进而危及源代码、CI 凭证以及部署密钥的安全。 该漏洞源于 Forgejo 基于 Go 模板的变量展开机制（用于替换 .forgejo/template 所列文件中的占位符）与紧随其后执行的 Git 仓库初始化步骤之间的交互冲突。16.0.4 版本中的补丁确保模板展开不再干扰仓库初始化流程；上游项目 Gitea 已确认不受此漏洞影响。

---

<a id="item-5"></a>
### *（简报）* [WeWorm：首个通过微信通话传播的零点击蠕虫，由 AI 在约两周内构建完成](https://simonwillison.net/2026/Sep/10/calif-research/) ⭐️ 7.0/10 · 相关 3/10

Calif Research 公开演示了 WeWorm——一款概念验证级别的零点击蠕虫，能够通过微信语音通话在 iOS 和 Android 之间跨平台传播，受害者无需接听电话即被攻陷。研究团队表示，借助 AI 协助，他们在约两天内找到了微信 VoIP 协议栈中的内存破坏漏洞并写出首个远程代码执行利用代码，再用约一周时间完成了完整的蠕虫构建。 微信拥有超过十亿账户，在中国及全球华人社群的日常生活中深度嵌入，因此即便是概念验证级别的跨平台零点击、账号级别入侵，其潜在影响范围仍然极其巨大。更值得警惕的是时间维度的压缩——AI 协助下大约两周就能完成的工作，传统团队往往需要数月——这本身就是一个标志性事件：AI 已经能够承担漏洞利用开发中的大部分常规工作，人类只需要在目标选择和安全测试判断上把关。 攻击者只需要是受害者的微信好友，然后拨打语音通话即可；账号接管在手机响铃的几秒钟内完成，被劫持的账号又会去呼叫更多好友，从而形成蠕虫式传播链。漏洞位于微信应用层的 VoIP 协议栈中，而非 iOS 或 Android 系统代码中，因此同一段利用代码能在两个平台上通用；其概念验证演示用 Pixel 10a → iPhone 17e → 第二台 Pixel 10a 完成了两跳的跨平台感染链。

---

<a id="item-6"></a>
### *（简报）* [我尝试让真实的果蝇连接组学习打 Pong，结果失败了——而审计失败原因竟然比它成功更有趣 (p)](https://www.reddit.com/r/MachineLearning/comments/1wc67ci/i_tried_to_make_a_real_fly_connectome_learn_to/) ⭐️ 7.0/10 · 相关 3/10

作者尝试用真实果蝇连接组学习 Pong 失败后，通过逐突触审计发现了正则表达式 bug 和神经元选择无连通路径等问题，展现了严谨的实验分析方法。

---

