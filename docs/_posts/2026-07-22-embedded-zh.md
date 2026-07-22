---
layout: default
title: "Horizon Daily: 2026-07-22 (ZH)"
date: 2026-07-22
lang: zh
period: daily
period_id: 2026-07-22
---

> 从 19 条内容中筛选出 11 条重要资讯。

其中 **7 条 8 分以上**展开详细简报，其余 4 条仅列于索引。

---

1. [在 STM32F446 上实现裸机俄罗斯方块：自定义中断架构](#item-1) ⭐️ 8.0/10
2. [在 FPGA 上实现自定义 RV32I SoC 与硬件卷积加速器](#item-2) ⭐️ 8.0/10
3. [开源 IMU 守护进程让 Linux 上多个应用共享一个传感器](#item-3) ⭐️ 8.0/10
4. [适用于以太网和 CAN 的极简发布/订阅库](#item-4) ⭐️ 8.0/10
5. [开源吸尘器项目摒弃云依赖](#item-5) ⭐️ 7.0/10
6. [超小型 RP2354A 开发板配弹簧针调试夹具](#item-6) ⭐️ 7.0/10
7. [自制赛博甲板：自定义引导加载器从 MicroSD 动态刷写语言运行时](#item-7) ⭐️ 7.0/10
8. [谁在建造那座数据中心？](#item-8) ⭐️ 6.0/10
9. [发现带有假 AGP 插槽的仿冒复古主板](#item-9) ⭐️ 6.0/10
10. [在裸机 TMS570 上实现非阻塞 SD 卡写入](#item-10) ⭐️ 6.0/10
11. [STM32L476RG 因非连续 RAM 分配在 Reset_Handler 中立即触发 HardFault](#item-11) ⭐️ 6.0/10

---

<a id="item-1"></a>
## [在 STM32F446 上实现裸机俄罗斯方块：自定义中断架构](https://www.reddit.com/r/embedded/comments/1v2n8w9/wrote_a_baremetal_tetris_on_an_stm32f446_no/) ⭐️ 8.0/10

一位开发者使用裸机 C 语言在 STM32F446RE Nucleo 板上实现了俄罗斯方块，所有寄存器定义均来自参考手册，并采用 EXTI、SysTick 和 PendSV 的三级中断架构。游戏在四个级联的 MAX7219 LED 矩阵（8×32 游戏区域）上运行，支持按键输入和 UART 分数输出。 该项目展示了开发者对 ARM Cortex-M 中断优先级和裸机编程的深刻理解，提供了一个无需 RTOS 即可分离关注点的实用范例。将游戏逻辑放在最低优先级的 PendSV 中执行，是实时系统中常用的模式，值得其他嵌入式开发者借鉴。 EXTI 中断服务程序仅负责按键去抖并存储移动/旋转意图；SysTick 负责毫秒计数，并以可配置的游戏速度触发 PendSV；PendSV 运行在最低优先级，处理所有游戏逻辑，包括意图消费、重力、碰撞检测、消行和 SPI 显示更新。意图的读取和清除在关中断下进行，以防止竞态条件。

reddit · r/embedded · /u/Pleasant_Dog2892 · 7月21日 16:22

**背景**: 裸机编程是指直接为微控制器编写代码，不使用硬件抽象层（HAL）或 CMSIS 设备头文件，从而完全控制硬件。STM32F446RE 是基于 ARM Cortex-M4 的 MCU，其 NVIC 支持可配置优先级的中断嵌套。PendSV（可挂起的服务调用）是一种异常，通常用于 RTOS 中的上下文切换；将其设置为最低优先级可确保它不会阻塞时间关键的中断。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/AdnS01/stm32f446-minimal-startup">GitHub - AdnS01/ stm 32 f 446 -minimal-startup: minimal bare - metal ...</a></li>
<li><a href="https://medium.com/embedworld/arm-cortex-pendsv-the-core-mechanism-behind-rtos-task-switching-7679e68e68da">ARM Cortex PendSV : The Core Mechanism Behind RTOS... | Medium</a></li>
<li><a href="https://interrupt.memfault.com/blog/arm-cortex-m-exceptions-and-nvic">A Practical guide to ARM Cortex-M Exception Handling | Interrupt</a></li>

</ul>
</details>

**社区讨论**: Reddit 社区对该项目的中断架构和代码质量表示赞赏，许多人认为这是一次扎实的学习实践。一些评论者建议使用环形缓冲区而非单个变量来存储意图，以避免丢失输入；另一些人建议添加看门狗定时器以增强鲁棒性。总体评价积极且富有建设性。

**标签**: `#bare-metal`, `#STM32`, `#embedded systems`, `#interrupts`, `#Tetris`

---

<a id="item-2"></a>
## [在 FPGA 上实现自定义 RV32I SoC 与硬件卷积加速器](https://www.reddit.com/r/embedded/comments/1v2u4a6/built_an_rv32i_soc_from_scratch_on_an_artix7_fpga/) ⭐️ 8.0/10

一位开发者在 Artix-7 FPGA 上构建了自定义 RV32I 单周期 SoC，集成了 3x3 硬件卷积加速器用于实时边缘检测，并通过带节奏的串行协议将 Python/OpenCV 与硅片连接起来。 该项目展示了从 RISC-V 内核到加速器的完整软硬件协同设计流程，在低成本 FPGA 上实现实时图像处理。它凸显了定制硅片如何加速通常由软件完成的计算机视觉任务。 加速器使用 9 个并行乘法器和对数深度加法树，在一个周期内计算 Sobel-X 导数，并具有原生 CV_8U 钳位功能。系统运行在 50 MHz，建立时间余量为 0.51 ns，并使用带节奏的大端串行协议避免 UART 缓冲区溢出。

reddit · r/embedded · /u/Waseeemnabi · 7月21日 20:23

**背景**: RISC-V 是一种开放标准的指令集架构（ISA），允许自定义处理器设计。SoC（片上系统）将处理器核心、内存和外设集成在单个芯片上。FPGA（现场可编程门阵列）是可重新配置的硬件，能够实现自定义数字电路。硬件卷积加速器通过在硬件中执行并行乘累加运算来加速图像处理。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/DakshDRao/rv32im-core">GitHub - DakshDRao/ rv 32 im- core : This is a single cycle RV 32 I core ...</a></li>
<li><a href="https://deepwiki.com/mohamednaji7/RISC-V-Processor/2.1-single-cycle-core-design">Single - Cycle Core Design | DeepWiki</a></li>
<li><a href="https://github.com/Limbocaos/FPGA-Based-Multilayer-Hardware-Accelerator-for-Convolutional-Neural-Networks">GitHub - Limbocaos/FPGA-Based-Multilayer- Hardware - Accelerator ...</a></li>

</ul>
</details>

**标签**: `#RISC-V`, `#FPGA`, `#hardware accelerator`, `#edge detection`, `#SoC`

---

<a id="item-3"></a>
## [开源 IMU 守护进程让 Linux 上多个应用共享一个传感器](https://www.reddit.com/r/embedded/comments/1v2rngd/opensource_imu_daemon_for_linux_that_lets/) ⭐️ 8.0/10

一位开发者发布了 imud，这是一个开源的 Linux IMU 守护进程，允许多个应用程序同时访问单个 IMU 传感器，负责处理 I²C 通信、校准、传感器融合和数据分发。 该项目解决了嵌入式 Linux 开发中的一个常见痛点，无需每个应用程序编写自己的 IMU 驱动和融合管道，促进了代码复用和系统效率。 imud 使用 C11 编写，采用中断驱动采集和 IMU FIFO，实现了乘法扩展卡尔曼滤波器（MEKF），并支持硬件时间戳。它提供 NMEA 0183、高速二进制 UDP 和 AF_UNIX/TCP 流接口。

reddit · r/embedded · /u/richcreations · 7月21日 18:55

**背景**: IMU（惯性测量单元）结合了加速度计和陀螺仪，用于测量方向和运动。在嵌入式 Linux 系统中，多个应用程序通常需要方向数据，但传统上每个应用都必须实现自己的底层驱动和传感器融合，导致重复劳动和资源争用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/richcreations/imud">GitHub - richcreations/imud: IMU Daemon for Raspberry Pi · GitHub</a></li>
<li><a href="https://matthewhampsey.github.io/blog/2020/07/18/mekf">The Multiplicative Extended Kalman Filter</a></li>
<li><a href="https://www.st.com/en/mems-and-sensors/ism330dhcx.html">ISM 330 DHCX | Product - STMicroelectronics</a></li>

</ul>
</details>

**社区讨论**: 未提供 Reddit 讨论内容，但作者特别询问将 IMU 视为共享系统基础设施（如 gpsd）是否有用，还是应将功能直接嵌入到应用程序中。

**标签**: `#embedded`, `#Linux`, `#IMU`, `#open-source`, `#sensor fusion`

---

<a id="item-4"></a>
## [适用于以太网和 CAN 的极简发布/订阅库](https://www.reddit.com/r/embedded/comments/1v2jcv3/a_tiny_pubsub_library_that_works_over_ethernet/) ⭐️ 8.0/10

'cy'库的新版本为嵌入式系统提供了一个极简的发布/订阅网络栈，支持 UDP 和 CAN 传输，具备服务发现、流式传输和可调 QoS 功能。 该库为复杂的 DDS 实现提供了轻量级替代方案，使资源受限的嵌入式设备能够实现高效的去中心化通信。 传输无关的核心部分仅需一个.c 文件，UDP 和 CAN 的适配层很小。同时提供了 Python 实现（pycyphal），并且正在开发 TSN 支持。

reddit · r/embedded · /u/spym_ · 7月21日 14:02

**背景**: 发布/订阅是一种消息模式，发送者将消息发布到主题，接收者订阅感兴趣的主题。DDS（数据分发服务）是实时数据交换的标准，但对小型嵌入式系统来说通常过于庞大。CAN（控制器局域网）是汽车和工业应用中使用的稳健总线标准，而以太网在联网中很常见。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/amcolex/umsg">GitHub - amcolex/umsg: Lightweight pub - sub library written in C.</a></li>
<li><a href="https://community.rti.com/dds_papers">Papers | Data Distribution Service ( DDS ) Community RTI Connext...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Time-Sensitive_Networking">Time - Sensitive Networking - Wikipedia</a></li>

</ul>
</details>

**标签**: `#pub/sub`, `#embedded`, `#CAN`, `#Ethernet`, `#networking`

---

<a id="item-5"></a>
## [开源吸尘器项目摒弃云依赖](https://hackaday.com/2026/07/21/open-source-vacuum-avoids-cloud/) ⭐️ 7.0/10

一个全新的开源吸尘器项目发布，完全无需云服务即可运行，强调本地控制与隐私保护。 该项目代表了消费电子领域避免云依赖的日益增长趋势，让用户完全拥有并控制自己的设备，同时降低隐私风险。 该吸尘器采用开源硬件和软件，可能基于旋风分离原理设计，用户可自行维修和改装。

rss · Hackaday · 7月22日 02:00

**背景**: 许多现代智能家居设备依赖云服务运行，这可能导致订阅费用、数据隐私问题以及云服务关闭后的设备报废。开源替代方案旨在让用户实现本地控制，通常使用 Raspberry Pi 等平台进行 IoT 管理。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/unknowndomain/Open-Source-Vacuum-Cleaner">GitHub - unknowndomain/ Open - Source - Vacuum - Cleaner : This is the...</a></li>
<li><a href="https://blog.adafruit.com/2013/04/08/open-source-vacuum-cleaner-project/">Open Source Vacuum Cleaner Project « Adafruit Industries – Makers...</a></li>
<li><a href="https://www.vitaliihonchar.com/insights/fleeto-private-local-iot-control-without-cloud-infrastructure">Fleeto Private Local IoT Control Without Cloud... | Vitalii Honchar's Blog</a></li>

</ul>
</details>

**标签**: `#open source`, `#IoT`, `#privacy`, `#embedded systems`, `#consumer electronics`

---

<a id="item-6"></a>
## [超小型 RP2354A 开发板配弹簧针调试夹具](https://www.reddit.com/r/embedded/comments/1v2hs21/designing_an_ultrasmall_rp2354a_development_board/) ⭐️ 7.0/10

一位爱好者设计了 Romu，这是一款钥匙扣大小的 RP2354A 开发板，尺寸为 15.5×12 毫米，并配有独立的弹簧针夹具，用于 SWD、UART 和 USB 调试。 该设计展示了在极致小型化与实用调试之间的巧妙权衡，使嵌入式开发者能够在不牺牲开发能力的情况下，随时随地进行原型开发。 该板搭载了 2MB 闪存的 RP2354A，具备原生 USB、RGB LED 和电容触摸按钮，但为了节省空间省略了专用调试连接器，转而依赖外部弹簧针夹具。

reddit · r/embedded · /u/Glass_Hour_8206 · 7月21日 13:00

**背景**: RP2354A 是树莓派 RP2350 微控制器的变体，采用紧凑的 QFN-60 封装，内置 2MB 闪存。SWD（串行线调试）和 UART 是嵌入式设备编程和调试的标准接口。弹簧针夹具常用于生产中，无需焊接即可建立临时电气连接。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/RP2350">RP2350 - Wikipedia</a></li>
<li><a href="https://thepihut.com/products/raspberry-pi-rp2354a-microcontroller">Raspberry Pi RP 2354 A Microcontroller - The Pi Hut</a></li>
<li><a href="https://www.welectron.com/Raspberry-Pi-RP2354A-Microcontroller">Raspberry Pi RP 2354 A Microcontroller , 1,40 €</a></li>

</ul>
</details>

**标签**: `#RP2354A`, `#development board`, `#embedded systems`, `#PCB design`, `#Raspberry Pi`

---

<a id="item-7"></a>
## [自制赛博甲板：自定义引导加载器从 MicroSD 动态刷写语言运行时](https://www.reddit.com/r/embedded/comments/1v2h3qy/my_diy_cyberdeck_with_custom_bootloader/) ⭐️ 7.0/10

一个自制赛博甲板项目包含自定义引导加载器，可从 MicroSD 卡动态刷写语言运行时（如 Duktape），并配有运行俄罗斯方块的电子墨水屏。 该项目展示了嵌入式系统中运行时灵活性的新颖方法，用户无需重新刷写整个固件即可更换语言解释器。它展示了实用的引导加载器设计以及电子墨水屏在低功耗交互应用中的集成。 引导加载器从 MicroSD 卡读取语言运行时二进制文件，并将其刷写到特定内存区域，从而支持在 Duktape（一种可嵌入的 JavaScript 引擎）等运行时之间动态切换。电子墨水屏运行俄罗斯方块游戏，可能使用刷写的运行时实现。

reddit · r/embedded · /u/Unique-Teaching4279 · 7月21日 12:32

**背景**: 赛博甲板是一种自制的便携式计算机，通常受赛博朋克美学启发，用于黑客、复古计算或 DIY 项目。引导加载器是初始化硬件并加载主应用程序的低级软件。Duktape 是一种紧凑、可嵌入的 JavaScript 引擎，专为资源受限设备设计。电子墨水屏是低功耗、双稳态屏幕，无需电力即可保持内容，适合静态或慢速更新应用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://duktape.org/">Duktape</a></li>
<li><a href="https://github.com/svaarala/duktape">GitHub - svaarala/ duktape : Duktape - embeddable Javascript engine ...</a></li>
<li><a href="https://www.tindie.com/products/aeonlabs/213-magnetic-e-ink-3-colour-display/">2.13" Magnetic E - Ink 3 colour Display from AeonLabs on Tindie</a></li>

</ul>
</details>

**标签**: `#embedded systems`, `#bootloader`, `#cyberdeck`, `#e-ink`, `#DIY`

---

<a id="item-8"></a>
### *（简报）* [谁在建造那座数据中心？](https://hackaday.com/2026/07/21/whos-building-that-data-center/) ⭐️ 6.0/10

Hackaday 上的一篇文章探讨了美国各地社区与人工智能数据中心项目之间日益加剧的冲突，凸显了技术扩张与地方利益之间的紧张关系。 这很重要，因为人工智能数据中心需要大量电力和土地，常常因环境和规划问题引发当地反对，可能减缓人工智能基础设施的部署。 文章包含一张地图，显示美国本土 48 州众多数据中心开发项目，状态从提议到运营不等，表明活动范围广泛。

---

<a id="item-9"></a>
### *（简报）* [发现带有假 AGP 插槽的仿冒复古主板](https://hackaday.com/2026/07/21/counterfeit-retro-mainboards-with-fake-agp-slots-are-a-thing/) ⭐️ 6.0/10

一位名为 Computer Retro Bus 的复古计算爱好者发现了一些仿冒的 Socket 478 主板，这些主板带有假的 AGP 插槽，这些插槽没有实际功能，仅作装饰。 这凸显了复古硬件市场中日益严重的问题，仿冒组件可能误导买家，损害收藏家和爱好者之间的信任。 假的 AGP 插槽没有电气连接，纯粹是装饰性的，可能是为了让主板看起来更真实，以欺骗不知情的买家。这些仿冒主板针对 Socket 478 平台，该平台在 Pentium 4 构建中很受欢迎。

---

<a id="item-10"></a>
### *（简报）* [在裸机 TMS570 上实现非阻塞 SD 卡写入](https://www.reddit.com/r/embedded/comments/1v2g9l9/sd_card_usage_without_blocking/) ⭐️ 6.0/10

一位 TMS570 平台上的开发者寻求一种方法，在不阻塞 CPU 的情况下将诊断日志写入 SD 卡，使用 DMA 和简单调度器而非 RTOS。 这解决了一个常见的嵌入式挑战：在时序要求严格的裸机系统上实现非阻塞 I/O。解决方案可能惠及许多在资源受限设备上工作的开发者。 用户正在原始块级别使用 FatFs，但仍然遇到 CPU 阻塞问题。他们已经在 SD 卡读写中使用 DMA，但需要一种方法来卸载阻塞等待。

---

<a id="item-11"></a>
### *（简报）* [STM32L476RG 因非连续 RAM 分配在 Reset_Handler 中立即触发 HardFault](https://www.reddit.com/r/embedded/comments/1v2m4ht/stm32l476rg_hardfaults_almost_immediately_inside/) ⭐️ 6.0/10

一位开发者解决了 STM32L476RG 在 Reset_Handler 中、.data/.bss 初始化之前立即触发 HardFault 的问题。根本原因是在链接脚本中分配了 128KB RAM，但 STM32L476RG 的 RAM 并非连续——它由两个独立区域（96KB + 32KB）组成，导致栈指针指向未映射的内存。 这个调试案例揭示了裸机 STM32 开发中的一个常见陷阱：假设 RAM 是连续的，而实际上并非如此。理解内存映射对于正确配置链接脚本至关重要，尤其是在从较小项目迁移到全容量项目时。 STM32L476RG 的 128KB RAM 分为两个区域：SRAM1（96KB，地址 0x20000000）和 SRAM2（32KB，地址 0x10000000）。开发者的链接脚本定义了一个从 0x20000000 开始的 128KB 单一 RAM 区域，因此栈指针（MSP）被设置为 0x20020000，这超出了 SRAM1 的范围，进入了未映射空间，导致第一条 push 指令立即触发 HardFault。

---

