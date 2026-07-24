---
layout: default
title: "Horizon Daily: 2026-07-24 (ZH)"
date: 2026-07-24
lang: zh
period: daily
period_id: 2026-07-24
---

> 从 7 条内容中筛选出 2 条重要资讯。

其中 **1 条 8 分以上**展开详细简报，其余 1 条仅列于索引。

---

1. [在自制的 CPU 上运行《毁灭战士》](#item-1) ⭐️ 7.0/10
2. [DIY 超声波麦克风干扰器：基于 RP2040 和 MOSFET](#item-2) ⭐️ 6.0/10

---

<a id="item-1"></a>
## [在自制的 CPU 上运行《毁灭战士》](https://hackaday.com/2026/07/23/running-doom-on-a-custom-cpu-built-from-scratch/) ⭐️ 7.0/10

一位黑客成功将经典游戏《毁灭战士》移植到完全从零设计和制造的定制 CPU 上，展示了完整的底层硬件与软件集成。 这一成就突显了黑客对计算机架构和嵌入式系统的深刻理解，延续了在非常规硬件上运行《毁灭战士》的传统，激励他人探索定制硬件设计。 该定制 CPU 完全从零构建，意味着开发者设计了指令集、逻辑门和物理实现。运行《毁灭战士》需要将游戏代码适配到定制架构，并处理与外设的输入/输出。

rss · Hackaday · 7月23日 15:30

**背景**: 《毁灭战士》是 1993 年发行的第一人称射击游戏，已成为文化标志和移植到非常规硬件（从计算器到验孕棒）的基准。移植到定制 CPU 需要编写底层驱动程序，并优化游戏以在有限资源上运行。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://thepinballspot.com/diy-projects/running-doom-on-our-custom-cpu-and-going-viral/">Running Doom On Our Custom CPU And Going Viral - The Pinball Spot</a></li>
<li><a href="https://www.armaangomes.com/blogs/doom/">Running DOOM on our Custom CPU and Going Viral | Armaan Gomes</a></li>

</ul>
</details>

**标签**: `#DOOM`, `#custom CPU`, `#hardware hacking`, `#embedded systems`, `#retro gaming`

---

<a id="item-2"></a>
### *（简报）* [DIY 超声波麦克风干扰器：基于 RP2040 和 MOSFET](https://hackaday.com/2026/07/23/mic-jammer-relies-on-ultrasound/) ⭐️ 6.0/10

一个 DIY 项目展示了使用 RP2040 微控制器和 MOSFET 构建的超声波麦克风干扰器，用于干扰附近的麦克风。 该项目展示了利用常见组件实现隐私保护的便捷硬件方案，可阻止未经授权的音频录制。 该干扰器发出人耳听不到的超声波，在麦克风电路中产生非线性失真，从而有效干扰录音。它使用 RP2040 生成信号，并用 MOSFET 驱动超声波换能器。

---



---

### 📚 今日知识点
**概念**：MOSFET（金属氧化物半导体场效应晶体管）
**是什么**：MOSFET 是一种电子开关，就像家里的电灯开关，但它是用电压控制的，而不是用手。你给它一个很小的电压信号，它就能控制很大的电流通过或断开，而且反应速度极快。在嵌入式电路里，它常被用来驱动电机、喇叭、灯等需要大电流的器件，因为单片机引脚只能输出很小的电流，直接带不动这些设备。你可以把它想象成一个“电控水龙头”：单片机是轻轻拧开小阀门的人，MOSFET 就是那个被小阀门控制、能放出大水流的主阀门。
**和今天新闻的关系**：在“DIY 超声波麦克风干扰器”这条新闻里，RP2040 单片机产生的信号太弱，无法直接驱动超声波换能器（类似小喇叭），所以用 MOSFET 来放大信号，让换能器发出足够强的超声波。
**延伸关键词**：场效应管、N沟道MOSFET、P沟道MOSFET、栅极驱动、开关电路
