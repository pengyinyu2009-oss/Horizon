---
layout: default
title: "Horizon Daily: 2026-08-21 (ZH)"
date: 2026-08-21
lang: zh
period: daily
period_id: 2026-08-21
---

> 从 27 条内容中筛选出 4 条重要资讯。

其中 **0 条 8 分以上**展开详细简报，其余 4 条仅列于索引。

---

1. [AliExpress 静默 WebAudio 指纹追踪干扰蓝牙多点连接](#item-1) ⭐️ 7.0/10 · 相关 4/10
2. [恶意 Rust crate arrayref 在构建时执行恶意载荷](#item-2) ⭐️ 7.0/10 · 相关 5/10
3. [Show HN：我训练了一个 1.25 亿参数的模型，在设备上实现钢琴自动补全](#item-3) ⭐️ 7.0/10 · 相关 4/10
4. [Linux 7.2 内核发布，开源驱动支持 HDMI 2.1](#item-4) ⭐️ 7.0/10 · 相关 5/10

---

<a id="item-1"></a>
### *（简报）* [AliExpress 静默 WebAudio 指纹追踪干扰蓝牙多点连接](https://blog.laserphile.com/2026/08/aliexpress-webpage-keeping-multipoint.html) ⭐️ 7.0/10 · 相关 4/10

一项技术分析揭示，AliExpress 网页会静默播放人耳听不到的 WebAudio 信号作为浏览器指纹追踪手段，而这种后台音频活动同时会干扰已配对耳机和助听器的蓝牙多点连接功能。该发现于 2026 年 8 月在 laserphile 博客上公布，并已被多位用户独立验证。 这是一个少见的案例：追踪技术除了侵犯隐私之外，还产生了用户可感知的副作用——切实破坏了用户依赖的硬件功能。它也表明浏览器指纹追踪不仅仅是理论上的隐私问题，还会干扰现实世界中的消费电子产品，这给浏览器厂商和应用商店带来了压力，要求它们检测并阻止此类滥用行为。 该指纹追踪通过生成 OscillatorNode 信号并测量浏览器音频栈对其的处理方式，产生设备特定的值，用于跨会话追踪用户。Firefox 工程师 Tom Ritter 记录了 Firefox 已经大幅降低了这种指纹的熵，但其他浏览器可能仍然脆弱。多位评论者反馈，这种音频活动会导致车载蓝牙信息娱乐系统误将其识别为语音命令。

---

<a id="item-2"></a>
### *（简报）* [恶意 Rust crate arrayref 在构建时执行恶意载荷](https://safedep.io/arrayref-proc-macro1-rust-build-time-malware/) ⭐️ 7.0/10 · 相关 5/10

流行的 Rust crate arrayref（版本 0.3.10）所在包集合累计下载量约达 2.44 亿次，其依赖 proc-macro1 的 build.rs 脚本在编译时下载并执行了二阶段二进制载荷。Rust 官方博客和 RustSec 公告库均已发布告警，但 crates.io 并未正确 yank 该恶意版本，也未在 crate 页面发布安全公告。 由于 build.rs 脚本会在每次 cargo build 时自动执行，任何 lockfile 解析到 arrayref 0.3.10 的开发者只要编译就会被感染，无需任何额外操作。此次事件暴露了 crates.io 在安全事件响应机制上的结构性缺陷，并重新引发了关于 Rust "精简标准库"设计哲学的争论——这种设计迫使项目引入数百个间接依赖。 该下载器在通过 HTTPS 获取二阶段载荷前禁用了 TLS 证书校验，将其写入临时目录，并以一个 C2 地址作为参数执行。受感染的关联 crate 还包括 internment 和 append-only-vec；build.rs 沙箱化提案已列入 Rust 2024H2 目标清单，但至今尚未落地。

---

<a id="item-3"></a>
### *（简报）* [Show HN：我训练了一个 1.25 亿参数的模型，在设备上实现钢琴自动补全](https://simedw.com/2026/08/20/midi-autocomplete/) ⭐️ 7.0/10 · 相关 4/10

作者训练了一个拥有 1.25 亿参数的 Transformer 模型，可对 MIDI 钢琴演奏进行实时自动补全，在 iPhone 15 上完全本地运行，速度约为每秒 108 个音符。

---

<a id="item-4"></a>
### *（简报）* [Linux 7.2 内核发布，开源驱动支持 HDMI 2.1](https://www.igalia.com/2026/08/19/Linux-72-Released.html) ⭐️ 7.0/10 · 相关 5/10

Linux 7.2 内核正式发布，Igalia 的报道重点介绍了 HDMI 2.1 开源驱动支持以及其他内核改进。该版本因对显示接口和单板电脑（包括 Raspberry Pi）的潜在影响而受到社区关注。 由于 HDMI Forum 的许可证限制，HDMI 2.1 开源支持长期受阻，因此任何实质进展都会影响在 Linux 上使用 AMD 和 Intel GPU 的用户，并扩大硬件兼容性。此类规模的内核更新也会波及以 Linux 为主导的嵌入式和单板电脑生态。 根据 Phoronix 最近的报道，Intel 提交了 44 个补丁系列，在 Meteor Lake 及更新硬件上实现 HDMI 2.1 FRL 支持；而 AMD 此前一直依靠社区补丁绕过 HDMI Forum 的限制。读者应注意，各厂商间完整的 HDMI 2.1 功能对等仍在演进中，可能暂时无法匹配专有驱动的功能集。

---

