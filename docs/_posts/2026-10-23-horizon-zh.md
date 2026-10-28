---
layout: default
title: "Horizon Daily: 2026-10-23 (ZH)"
date: 2026-10-23
lang: zh
period: daily
period_id: 2026-10-23
---

> 从 26 条内容中筛选出 9 条重要资讯。

其中 **4 条 8 分以上**展开详细简报，其余 4 条仅列于索引。另有 **1 条🎯猜你感兴趣**（按画像主观分入选）。

---

1. [OpenShell——面向自主 AI 代理集群的安全私有运行时](#item-1) ⭐️ 8.0/10 · 相关 8/10
2. [越狱 Nintendo Switch 2](#item-2) ⭐️ 8.0/10 · 相关 6/10
3. [eMudhra 将退出全球 SSL/TLS 证书业务](#item-3) ⭐️ 8.0/10 · 相关 3/10
4. [向 Agentic AI Foundation 捐赠 Agent Skills](#item-4) ⭐️ 8.0/10 · 相关 7/10
5. [Quad9（DNS 解析器）将退出法国](#item-5) ⭐️ 7.0/10 · 相关 2/10
6. [hackiOS 在安卓设备上启动 iOS 16.5](#item-6) ⭐️ 7.0/10 · 相关 8/10
7. [Carbon-X 是一款联合 DNA 与文本数据训练的 148 亿参数开放模型 (R)](#item-7) ⭐️ 7.0/10 · 相关 6/10
8. [我构建了 Open-XTTS-Trainer：现在只需一键即可添加新的语言文字系统，并训练 XTTS v2 的全部三个组件 (P)](#item-8) ⭐️ 7.0/10 · 相关 9/10
9. 🎯 [我们将可控制的小型 TTS 压缩至 11.84 MB：WER 保持不变，UTMOS 仅下降约 0.1 (p)](#item-9) ⭐️ 6.0/10 · 相关 8/10

---

<a id="item-1"></a>
## [OpenShell——面向自主 AI 代理集群的安全私有运行时](https://github.com/NVIDIA/OpenShell) ⭐️ 8.0/10 · 相关 8/10

OpenShell 是 NVIDIA 推出的开源 AI Agent 运行时，旨在通过隔离、访问控制和网络限制，安全地管理大规模自主 AI 代理。

hackernews · niemandhier · 10月22日 17:44 · [社区讨论](https://news.ycombinator.com/item?id=50198675)

**标签**: `#AI Agents`, `#Runtime Security`, `#Sandboxing`, `#NVIDIA`, `#Open Source`

---

<a id="item-2"></a>
## [越狱 Nintendo Switch 2](https://pepsipu.com/blog/2026-10-switch2-jailbreak-ns2jb/) ⭐️ 8.0/10 · 相关 6/10

文章展示了 Nintendo Switch 2 的越狱成果，探讨其对文件解密、硬件控制以及 AI 辅助逆向研究的影响。

hackernews · ledoge · 10月22日 08:01 · [社区讨论](https://news.ycombinator.com/item?id=50192536)

**标签**: `#Nintendo Switch 2`, `#Jailbreaking`, `#Reverse Engineering`, `#Console Security`, `#Hardware Automation`

---

<a id="item-3"></a>
## [eMudhra 将退出全球 SSL/TLS 证书业务](https://emudhra.com/en/press-release/emudhra-to-exit-global-ssl-tls-certificate-business) ⭐️ 8.0/10 · 相关 3/10

eMudhra 宣布退出全球 SSL/TLS 证书业务。此前，与其证书基础设施相关的事件曾引发浏览器厂商和安全社区的强烈质疑。

hackernews · bo0tzz · 10月22日 13:33 · [社区讨论](https://news.ycombinator.com/item?id=50195110)

**标签**: `#PKI`, `#TLS/SSL`, `#数字证书`, `#CA`, `#网络安全`

---

<a id="item-4"></a>
## [向 Agentic AI Foundation 捐赠 Agent Skills](https://simonwillison.net/2026/Oct/22/donating-agent-skills/) ⭐️ 8.0/10 · 相关 7/10

Anthropic 将 Agent Skills 开放标准捐赠给 Linux Foundation 旗下的 Agentic AI Foundation，旨在推动其成为厂商中立、由社区驱动的 AI 智能体互操作标准。

rss · Simon Willison · 10月22日 18:09

**标签**: `#Agent Skills`, `#Agentic AI Foundation`, `#Linux Foundation`, `#AI standards`, `#developer tools`

---

<a id="item-5"></a>
### *（简报）* [Quad9（DNS 解析器）将退出法国](https://quad9.net/news/blog/au-revoir-france/) ⭐️ 7.0/10 · 相关 2/10

Quad9 因法国法院要求其对侵权内容实施 DNS 解析封锁，计划在 11 月 24 日后停止向法国用户提供服务。

---

<a id="item-6"></a>
### *（简报）* [hackiOS 在安卓设备上启动 iOS 16.5](https://github.com/oosexgang/hackios-xnu-kernel) ⭐️ 7.0/10 · 相关 8/10

开源研究项目 hackiOS 宣称，其经过修改的 XNU 内核和启动组件已能在 QEMU、POCO X5 Pro 5G 以及部分其他小米设备上运行苹果 iOS 16.5 固件。它仍是概念验证项目，并非完整且可普遍安装的 ROM。 该项目展示了通过修改内核、加载器、固件和驱动，让苹果操作系统栈适应外部硬件所需的大量底层工作。对嵌入式和操作系统工程师而言，它提供了跨硬件内核移植的实用研究案例，但目前还不能替代日常手机系统。 仓库包含 XNU 补丁、EFI 加载器、UEFI 移植、Wi-Fi 相关代码、QEMU 脚本、预编译的内核、加载器和 UEFI 组件，以及通用脚本。社区评论指出，每次会话只会运行预设的秒数，随后内核便返回加载器并输出日志；缺少完整 ROM 和经常回退到加载器仍是主要限制。

---

<a id="item-7"></a>
### *（简报）* [Carbon-X 是一款联合 DNA 与文本数据训练的 148 亿参数开放模型 (R)](https://www.reddit.com/r/MachineLearning/comments/1xchayq/carbonx_is_an_open_148b_model_trained_jointly_on/) ⭐️ 7.0/10 · 相关 6/10

Carbon-X 是一款可本地运行的 148 亿参数开放模型。在五项 DNA 基准测试中，其表现接近所比较的闭源模型，但实际增益仍需进一步独立验证。

---

<a id="item-8"></a>
### *（简报）* [我构建了 Open-XTTS-Trainer：现在只需一键即可添加新的语言文字系统，并训练 XTTS v2 的全部三个组件 (P)](https://www.reddit.com/r/MachineLearning/comments/1xcurgj/i_built_openxttstrainer_now_you_can_add_new/) ⭐️ 7.0/10 · 相关 9/10

Open-XTTS-Trainer 提供模块化的 XTTS v2 全组件训练方案，支持扩展新的语言文字系统，并通过 Colab 简化上手流程。

---

## 🎯 猜你感兴趣

以下 1 条未进客观分前 10，但与你的兴趣画像高度相关。

---

<a id="item-9"></a>
## [我们将可控制的小型 TTS 压缩至 11.84 MB：WER 保持不变，UTMOS 仅下降约 0.1 (p)](https://www.reddit.com/r/MachineLearning/comments/1xcum4s/we_shrank_our_steerable_small_tts_to_1184_mb_wer/) ⭐️ 6.0/10 · 相关 8/10

SteerTTS 推出 11.84 MB 的边缘端版本，在保持原版词错误率（WER）和可控性的同时，仅使自然度评分轻微下降。

reddit · r/MachineLearning · /u/Working_Hat5120 · 10月22日 20:57

**入选理由**: 与读者关注的边缘 AI、模型压缩和开发工具链高度相关；11.84 MB 的完整运行时及量化、蒸馏方案对资源受限的嵌入式设备部署具有较强实操价值。

**标签**: `#Edge AI`, `#Text-to-Speech`, `#Model Quantization`, `#Mamba`, `#Speech Synthesis`

---

