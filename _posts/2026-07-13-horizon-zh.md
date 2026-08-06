---
layout: default
title: "Horizon Daily: 2026-07-13 (ZH)"
date: 2026-07-13
lang: zh
period: daily
period_id: 2026-07-13
---

> 从 20 条内容中筛选出 8 条重要资讯。

其中 **3 条 8 分以上**展开详细简报，其余 5 条仅列于索引。

---

1. [Chromium 148 的 Math.tanh 可被用于操作系统指纹识别](#item-1) ⭐️ 8.0/10
2. [Claude Code 与 OpenCode 的 Token 开销对比](#item-2) ⭐️ 8.0/10
3. [陶哲轩用 LLM 编码代理构建交互式应用](#item-3) ⭐️ 8.0/10
4. [微型模拟器：面向 8 位系统的引脚级模块化模拟](#item-4) ⭐️ 7.0/10
5. [迁移至 GPT-5.6：速度提升 2.2 倍，成本降低 27%](#item-5) ⭐️ 7.0/10
6. [爱尔兰数据中心用电量已占全国电力的 23%](#item-6) ⭐️ 7.0/10
7. [Simon Willison：LLM 代理绝不应成为直接责任人](#item-7) ⭐️ 7.0/10
8. [Zer0Fit：为谷歌 TabFM 和 TimesFM 零样本机器学习打造的 MCP 服务器](#item-8) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [Chromium 148 的 Math.tanh 可被用于操作系统指纹识别](https://scrapfly.dev/posts/browser-math-os-fingerprint/) ⭐️ 8.0/10

Chromium 148 中 Math.tanh 的实现暴露了不同操作系统在浮点运算上的差异，网站可通过分析单个函数调用的输出来推断底层操作系统。 这创造了一种比用户代理标头更难伪造的浏览器指纹识别新途径，可能削弱隐私保护，并在不使用 Cookie 的情况下实现更持久的追踪。 差异源于 Math.tanh 依赖底层的 C 数学库（例如 macOS 上的 Apple 数学库、Linux 上的 glibc、Windows 上的 Universal C Runtime），这些库在大约四分之一的输入上产生不同的结果，通常相差一个最低有效位（ULP）。

hackernews · joahnn_s · 7月12日 21:12 · [社区讨论](https://news.ycombinator.com/item?id=48884853)

**背景**: 浏览器指纹识别是一种通过收集设备和浏览器的独特特征来识别用户的技术。传统方法包括用户代理字符串、屏幕分辨率和已安装字体。这一新途径利用了不同操作系统在数学函数底层实现上的差异。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Browser_fingerprinting">Browser fingerprinting</a></li>
<li><a href="https://scrapfly.dev/posts/browser-math-os-fingerprint/">Your Browser Does Math Differently on Every OS, and Anti-Bot Systems Read the Bits · scrapfly.dev</a></li>

</ul>
</details>

**社区讨论**: 社区评论指出，用户代理伪造可能无法完全缓解这种指纹识别，一些人批评披露此信息的爬虫公司的动机。另一些人则主张采用正确舍入的超越函数来消除此类差异。

**标签**: `#browser fingerprinting`, `#privacy`, `#Chromium`, `#JavaScript`, `#security`

---

<a id="item-2"></a>
## [Claude Code 与 OpenCode 的 Token 开销对比](https://systima.ai/blog/claude-code-vs-opencode-token-overhead) ⭐️ 8.0/10

一项实证研究发现，Claude Code 在读取用户提示前会发送约 33,000 个 token，而 OpenCode 仅发送约 7,000 个 token，表明 Claude Code 存在显著的 token 低效问题。 这种 token 开销直接影响用户成本，尤其对重度使用 AI 编码助手的用户而言，并引发了对代理工具中系统提示膨胀和盈利策略的担忧。 该研究在编码工具与 Anthropic 端点之间添加了日志记录，以捕获所有请求和使用块。低效源于缓存策略和框架 token 使用，而不仅仅是原始提示大小。

hackernews · systima · 7月12日 18:25 · [社区讨论](https://news.ycombinator.com/item?id=48883275)

**背景**: 像 Claude Code 和 OpenCode 这样的 AI 编码代理通过将提示、代码和工具定义转换为 token，供大语言模型处理。Token 消耗直接转化为成本，因此效率成为用户的关键考量。Claude Code 是 Anthropic 的专有代理编码工具，而 OpenCode 是开源替代方案。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/anthropics/claude-code">GitHub - anthropics/claude-code: Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster by executing routine tasks, explaining complex code, and handling git workflows - all through natural language commands. · GitHub</a></li>
<li><a href="https://github.com/opencode-ai/opencode">GitHub - opencode-ai/opencode: A powerful AI coding agent. Built for the terminal. · GitHub</a></li>

</ul>
</details>

**社区讨论**: 社区评论指出，子代理会快速消耗 token，有用户报告单个任务启动了 7 个子代理。其他人怀疑 Anthropic 从 token 低效中获利，并指出工具质量和往返次数比原始提示大小更重要。

**标签**: `#AI coding agents`, `#token efficiency`, `#Claude Code`, `#OpenCode`, `#cost analysis`

---

<a id="item-3"></a>
## [陶哲轩用 LLM 编码代理构建交互式应用](https://terrytao.wordpress.com/2026/07/11/old-and-new-apps-via-modern-coding-agents/) ⭐️ 8.0/10

陶哲轩展示了利用 LLM 驱动的编码代理为其研究创建交互式可视化和应用的过程，强调了它们在非关键任务中的实用性和可接受的风险。 作为菲尔兹奖得主和著名数学家，陶哲轩的认可表明 LLM 编码代理已足够可靠，可用于严肃但非关键的软件开发任务，可能加速学术界及其他领域的软件创建。 陶哲轩指出，这些 LLM 生成的补充内容对其论文核心并非关键，因此使用 LLM 代理进行引导式交互的下行风险是可接受的。社区讨论强调了教育益处和平衡的风险评估。

hackernews · subset · 7月12日 11:09 · [社区讨论](https://news.ycombinator.com/item?id=48880170)

**背景**: LLM 编码代理是结合大型语言模型与代码执行、文件编辑等工具的 AI 系统，能够自主编写和调试软件。它们不同于简单的聊天界面，可以根据用户反馈迭代优化代码。陶哲轩是菲尔兹奖得主、加州大学洛杉矶分校教授，以其数学研究和博客闻名。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://magazine.sebastianraschka.com/p/components-of-a-coding-agent">Components of A Coding Agent - by Sebastian Raschka, PhD</a></li>
<li><a href="https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/">How coding agents work - Agentic Engineering Patterns - Simon Willison's Weblog</a></li>

</ul>
</details>

**社区讨论**: 评论者指出，LLM 提升了他们为教学创建可视化的能力，一位教授分享了他如何在几天内用 Claude 构建了一个简化的 8 位计算机。其他人幽默地将陶哲轩使用编码代理比作米其林星级厨师发现微波炉餐，同时赞赏他对风险的平衡看法。

**标签**: `#LLM`, `#coding agents`, `#software development`, `#AI tools`, `#education`

---

<a id="item-4"></a>
### *（简报）* [微型模拟器：面向 8 位系统的引脚级模块化模拟](https://floooh.github.io/tiny8bit-preview/index.html) ⭐️ 7.0/10

Andre Weissflog 的 Tiny Emulators 项目展示了一种新颖的引脚级模拟方法，通过 WebAssembly 在浏览器中完全运行，支持 KC85、Amstrad CPC 等复古计算机的模拟。 这种引脚级模块化设计提供了极高的灵活性和互操作性潜力，组件可以轻松替换或复用。尽管该项目已有八年历史，它仍能激发关于模拟及更广泛领域接口设计的讨论。 模拟器采用自包含的模块化行为，每个组件通过薄而明确定义的接口（类似于物理引脚）进行通信。该项目托管在 GitHub 上，可通过 floooh.github.io/tiny8bit 访问。

---

<a id="item-5"></a>
### *（简报）* [迁移至 GPT-5.6：速度提升 2.2 倍，成本降低 27%](https://ploy.ai/blog/migrating-a-production-ai-agent-to-gpt-5-6) ⭐️ 7.0/10

Ploy.ai 将其生产环境中的 AI 智能体从 GPT-5.4 迁移至 GPT-5.6，实现了 2.2 倍的运行速度提升和 27%的成本降低，同时保持或提升了输出质量。 这次真实世界的迁移为 GPT-5.6 在生产环境中的实际价值提供了有力证据，表明升级该模型可为 AI 智能体带来显著的性能和成本优势，超越了单纯的基准测试分数。 此次迁移涉及 Ploy 用于构建和编辑营销网站的智能体，升级仅需一行代码变更。GPT-5.6 包含三个变体：Luna、Terra 和 Sol，Ploy 将 Sol 设为默认模型。

---

<a id="item-6"></a>
### *（简报）* [爱尔兰数据中心用电量已占全国电力的 23%](https://www.theregister.com/on-prem/2026/07/11/irish-datacenters-now-guzzle-23-of-the-countrys-electricity/5270013) ⭐️ 7.0/10

根据最新报告，爱尔兰的数据中心目前消耗了该国总电力的 23%，较往年大幅增长。 如此高的能耗引发了对爱尔兰电网压力的担忧，以及科技投资带来的经济效益与环境可持续性之间的权衡。 爱尔兰数据中心的用电比例高于加利福尼亚州（后者数据中心用电约占其总电力的 4%）。该国还面临高电价问题，部分居民每千瓦时需支付 34 欧分。

---

<a id="item-7"></a>
### *（简报）* [Simon Willison：LLM 代理绝不应成为直接责任人](https://simonwillison.net/2026/Jul/12/directly-responsible-individuals/#atom-everything) ⭐️ 7.0/10

Simon Willison 认为，基于 LLM 的代理绝不应被视为直接责任人 (DRI)，因为它们无法承担责任。他借鉴了苹果和 GitLab 的 DRI 概念。 这一观点挑战了将决策权委托给 AI 代理的趋势，强调责任是组织责任中人类独有的特质。 Willison 引用了 IBM 1979 年的培训幻灯片，其中写道：“计算机永远无法承担责任，因此计算机绝不能做出管理决策。”DRI 概念起源于苹果，并在 GitLab 的手册中有记录。

---

<a id="item-8"></a>
### *（简报）* [Zer0Fit：为谷歌 TabFM 和 TimesFM 零样本机器学习打造的 MCP 服务器](https://www.reddit.com/r/MachineLearning/comments/1uue8cc/zer0fit_i_took_googles_new_tabfm_timesfm_ml/) ⭐️ 7.0/10

一名研究生创建了 Zer0Fit，这是一个封装了谷歌 TabFM 和 TimesFM 基础模型的 MCP 服务器，可通过聊天界面进行零样本预测、分类和回归。它在鸢尾花数据集上达到 94.7%的准确率，在加州房价数据集上 R²达到 0.91，无需任何训练。 这弥合了传统机器学习模型与生成式 AI 之间的鸿沟，用户无需手动训练或调参，即可通过自然语言执行复杂的机器学习任务。它让更广泛的 AI 社区能够民主化地使用最先进的零样本模型。 该服务器运行在单个 Docker 容器中，需要 16GB 显存（仅支持 CUDA），并支持动态加载/卸载模型（TTL 为 5 分钟）。它支持 CSV 输入，并与 Open WebUI、Claude Code 和 Codex CLI 集成。

---

