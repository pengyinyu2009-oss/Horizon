---
layout: default
title: "Horizon Daily: 2026-07-23 (ZH)"
date: 2026-07-23
lang: zh
period: daily
period_id: 2026-07-23
---

> 从 20 条内容中筛选出 10 条重要资讯。

其中 **5 条 8 分以上**展开详细简报，其余 5 条仅列于索引。

---

1. [ESP32 上实现 60 帧 NES 模拟器](#item-1) ⭐️ 8.0/10
2. [Tatum Robotics 开发用于触觉手语的柔性机械手](#item-2) ⭐️ 8.0/10
3. [动作分块：机器人吞吐量与修正时间的权衡](#item-3) ⭐️ 8.0/10
4. [工厂中的人形机器人：可靠性胜过人形外观](#item-4) ⭐️ 7.0/10
5. [LeRobot 生产就绪性遭质疑：定制化部署栈兴起](#item-5) ⭐️ 7.0/10
6. [旧电视真空管变身 DIY X 光机](#item-6) ⭐️ 6.0/10
7. [从六轴机械臂构建中理解逆运动学的关键心得](#item-7) ⭐️ 6.0/10
8. [爱好者用智能手机打造移动机器人](#item-8) ⭐️ 6.0/10
9. [HM-LD1 3D dToF LiDAR 用于无人机避障](#item-9) ⭐️ 6.0/10
10. [爱好者寻求为修复的 Puma 500 机械臂自制伺服驱动器的建议](#item-10) ⭐️ 6.0/10

---

<a id="item-1"></a>
## [ESP32 上实现 60 帧 NES 模拟器](https://hackaday.com/2026/07/22/60-fps-nes-emulator-on-esp32/) ⭐️ 8.0/10

一位开发者成功在 ESP32 微控制器上实现了以每秒 60 帧全速运行的 NES 模拟器，这对于资源受限的设备来说是一项重大成就。 这展示了在低功耗微控制器上实现极致优化的可能性，为嵌入式系统上的复古游戏开辟了道路，并激励物联网和爱好者社区进行进一步的性能调优。 该模拟器通过精心优化 CPU 模拟、内存访问和显示渲染实现了 60 帧/秒，可能利用了 ESP32 的双核处理器和硬件加速功能。

rss · Hackaday · 7月22日 08:00

**背景**: ESP32 是一款集成了 Wi-Fi 和蓝牙的流行微控制器，常用于物联网项目。模拟 NES 这样的经典游戏机通常需要比微控制器提供的更强的处理能力，因此这一成就尤为引人注目。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/ESP32">ESP32 - Wikipedia</a></li>
<li><a href="https://www.espressif.com/en/products/socs/esp32">ESP32 Wi-Fi & Bluetooth SoC | Espressif Systems</a></li>

</ul>
</details>

**标签**: `#ESP32`, `#NES emulator`, `#embedded systems`, `#retro gaming`, `#optimization`

---

<a id="item-2"></a>
## [Tatum Robotics 开发用于触觉手语的柔性机械手](https://www.reddit.com/r/robotics/comments/1v3ewzu/why_existing_robotic_hands_could_not_be_used_for/) ⭐️ 8.0/10

Tatum Robotics 专门为触觉手语开发了一款柔性、肌腱驱动的机械手，因为标准的刚性连杆机械手对聋盲用户存在夹伤风险。 这项创新使聋盲人士能够安全地从机器人接收触觉手语，为辅助技术和人机交互开辟了新的可能性。 该机械手采用肌腱驱动机制并增加了自由度，以实现美国手语所需的精确手指定位，同时通过柔性设计避免夹伤点。

reddit · r/robotics · /u/Responsible-Grass452 · 7月22日 12:36

**背景**: 触觉手语是聋盲人士使用的一种交流方式，通过触摸（通常是手把手）接收手势。带有刚性连杆的标准机械手可能产生夹伤点，当用户需要直接握住手时存在危险。肌腱驱动的手使用缆绳模拟人类肌腱，实现柔性且更安全的运动。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Tactile_sign_language">Tactile sign language</a></li>
<li><a href="https://ruka-hand-v2.github.io/">RUKA-v2: Tendon Driven Open-Source Dexterous Hand with Wrist ...</a></li>
<li><a href="https://www.mdpi.com/2313-7673/9/6/370">Design and Control of a Tendon-Driven Robotic Finger ... - MDPI</a></li>

</ul>
</details>

**标签**: `#robotics`, `#assistive technology`, `#sign language`, `#compliant mechanisms`, `#human-robot interaction`

---

<a id="item-3"></a>
## [动作分块：机器人吞吐量与修正时间的权衡](https://www.reddit.com/r/robotics/comments/1v3q44h/action_chunking_trades_throughput_for_correction/) ⭐️ 8.0/10

Reddit 上的一篇帖子指出，机器人中的动作分块虽然降低了策略运行频率，但增加了修正时间，尤其在接触附近，并引入了中断延迟这一指标来衡量安全性。 这一见解对于设计安全且响应迅速的机器人控制系统至关重要，因为它揭示了高吞吐量（每秒动作数）并不能保证安全性；对于接触密集的任务，中断延迟是更相关的指标。 帖子区分了异步推理（如 LingBot-VA 2.0）和缓冲长动作块，指出两者结合可能导致低级控制器在意外接触后执行过时的命令。长块在自由空间中可接受，但接近接触时视野必须缩小。

reddit · r/robotics · /u/SynthwaveMariner · 7月22日 19:19

**背景**: 动作分块是机器人学习中的一种技术，策略一次性预测一系列未来动作，从而减少策略运行频率。它常用于像 Action Chunking with Transformers (ACT)这样的模型中以提高效率。然而，这会使机器人执行一个可能因环境变化而过时的计划，尤其是在接触时。中断延迟衡量的是在应该触发改变的新观察之后，机器人继续执行旧计划的时间。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2304.13705">[2304.13705] Learning Fine-Grained Bimanual Manipulation with ... GitHub - tonyzhaozh/act [2604.04161] Adaptive Action Chunking at Inference-time for ... ACT (Action Chunking with Transformers) · Hugging Face Action Chunking with Transformers - ACT — Open Edge Platform ... BIDIRECTIONAL DECODING: IMPROVING ACTION CHUNKING VIA GUIDED ... Action Chunking Transformers (ACT): Complete Guide for Robot ...</a></li>
<li><a href="https://arxiv.org/abs/2604.04161">[2604.04161] Adaptive Action Chunking at Inference-time for ... ACT (Action Chunking with Transformers) · Hugging Face Action Chunking with Transformers - ACT — Open Edge Platform ... BIDIRECTIONAL DECODING: IMPROVING ACTION CHUNKING VIA GUIDED ... Action Chunking Transformers (ACT): Complete Guide for Robot ...</a></li>
<li><a href="https://robohub.org/a-practical-look-at-latency-in-robotics-the-importance-of-metrics-and-operating-systems/">A practical look at latency in robotics: The importance of metrics and operating systems - Robohub</a></li>

</ul>
</details>

**社区讨论**: Reddit 讨论可能包括关于吞吐量与安全性权衡的评论，一些用户强调中断延迟比每秒动作数更重要。可能还有关于如何根据接触距离动态调整块大小的辩论。

**标签**: `#robotics`, `#control systems`, `#action chunking`, `#safety`, `#latency`

---

<a id="item-4"></a>
## [工厂中的人形机器人：可靠性胜过人形外观](https://www.reddit.com/r/robotics/comments/1v3ige8/humanoid_robots_are_entering_factories_but/) ⭐️ 7.0/10

A3 主席 Jeff Burnstein 表示，工厂中的大多数人形机器人仍处于试点阶段，效率仅为 20%至 50%，制造商更看重可靠性、经济性和安全性，而非人形外观。 这为人形机器人行业敲响了警钟：尽管炒作不断，实际应用仍面临重大障碍，尤其是缺乏专门的安全标准。同时，这也凸显了美国与中国之间日益扩大的机器人技术差距。 安全仍是主要障碍，因为目前尚无专门的人形机器人安全标准；大多数系统目前只能在围栏后或远离工人的地方运行。Burnstein 预计人形机器人将补充而非取代现有的工业机器人、移动机器人和协作臂。

reddit · r/robotics · /u/Responsible-Grass452 · 7月22日 14:53

**背景**: 人形机器人旨在模仿人类形态和运动，以便在人类环境中工作。然而，它们在稳定性、安全性和成本方面面临挑战。推进自动化协会（A3）是一家北美贸易组织，致力于推广自动化技术。协作臂是设计用于与人类安全协作的机器人手臂。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://theresarobotforthat.com/blog/humanoid-robot-safety-standards-2026/">ISO 25785-1: Complete Humanoid Robot Safety Guide for 2026</a></li>
<li><a href="https://en.wikipedia.org/wiki/Association_for_Advancing_Automation">Association for Advancing Automation - Wikipedia</a></li>
<li><a href="https://reliablerobotics.ai/product-category/robotic-arms/collaborative-robotic-arms/">Collaborative Robotic Arms - Robotics... - Reliable Robotics</a></li>

</ul>
</details>

**标签**: `#humanoid robots`, `#factory automation`, `#robotics safety`, `#industrial robotics`, `#manufacturing`

---

<a id="item-5"></a>
## [LeRobot 生产就绪性遭质疑：定制化部署栈兴起](https://www.reddit.com/r/robotics/comments/1v35mre/is_anyone_running_lerobot_in_production_or_are/) ⭐️ 7.0/10

一位机器人从业者在 Reddit 上质疑 LeRobot 是否被用于生产环境，指出其在定制机器人集成、异步推理支持以及缺乏经典运动规划方面的局限性。像 MiMicrobotics 这样的公司在评估后发现 LeRobot 的 IPC 层在实时控制方面延迟和抖动过大，因此构建了自己的零拷贝中间件。 这一讨论凸显了开源机器人框架与实际部署需求之间的关键差距，尤其是对于构建定制硬件的公司而言。转向构建专有堆栈的趋势可能导致生态系统碎片化，并减缓共享机器人学习工具的采用。 LeRobot 的异步推理仅支持固定策略列表（ACT、SmolVLA、pi0、pi05、GR00T），不包括 MolmoAct2 等较新模型。该框架还缺乏经典运动规划（MoveIt 风格）、抓取规划、分割以及导航/SLAM 功能，迫使用户集成单独的系统。

reddit · r/robotics · /u/aryanmadhavverma · 7月22日 04:29

**背景**: LeRobot 是 Hugging Face 推出的开源框架，提供 PyTorch 中用于机器人学习的模型、数据集和工具。它提供了记录传感器数据、训练策略和执行部署的抽象层，但主要面向研究和常见机器人平台（如 SO-101、Aloha 和 Koch）。生产部署通常需要低延迟、确定性的控制循环以及对定制硬件的支持，而 LeRobot 的 IPC 和日志层可能无法满足这些需求。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/huggingface/lerobot">GitHub - huggingface/ lerobot : LeRobot : Making AI for Robotics ...</a></li>
<li><a href="https://huggingface.co/blog/async-robot-inference">Asynchronous Robot Inference : Decoupling Action Prediction and...</a></li>

</ul>
</details>

**社区讨论**: Reddit 帖子引发了富有洞察力的评论，许多人同意 LeRobot 对于定制硬件尚未达到生产就绪状态。一些用户分享了构建自己堆栈的经验，而另一些用户则指出 LeRobot 的价值在于研究和原型设计。讨论还涉及了将学习策略与经典控制相结合的混合系统的需求。

**标签**: `#LeRobot`, `#robotics deployment`, `#open-source robotics`, `#robot learning`, `#production challenges`

---

<a id="item-6"></a>
### *（简报）* [旧电视真空管变身 DIY X 光机](https://hackaday.com/2026/07/22/old-tv-vacuum-tube-turned-diy-x-ray-machine/) ⭐️ 6.0/10

有人利用从旧黑白电视中拆下的 DY86 真空管，配合 Cockcroft-Walton 倍压电路，制作了一台 DIY X 光机。该项目展示了设备的工作原理，并强调了安全注意事项。 该项目以远低于商用 X 光管（动辄数百美元）的成本，让爱好者也能接触 X 光技术。它凸显了旧电子元件再利用的潜力，以及高压 DIY 项目中安全的重要性。 DY86 管是旧电视中的整流管，并非专为产生 X 射线设计，但在高压下可产生 X 射线。Cockcroft-Walton 倍压电路将电压升至所需水平，而适当的屏蔽和距离对安全操作至关重要。

---

<a id="item-7"></a>
### *（简报）* [从六轴机械臂构建中理解逆运动学的关键心得](https://www.reddit.com/r/robotics/comments/1v3907d/what_finally_helped_me_understand_inverse/) ⭐️ 6.0/10

一位制作者分享了在从零搭建六轴桌面机械臂后，帮助其理解逆运动学的三个实用心得：在推导方程前建立几何直觉、从二自由度平面臂开始、以及使用基于雅可比矩阵的数值求解器。 逆运动学是机器人学中的基本难题，这段个人学习经历提供了易于理解的逐步建议，可帮助爱好者和学生克服常见的概念障碍。 制作者强调，最大的错误是在理解工作空间几何之前就尝试推导封闭形式的逆运动学方程。他们还指出，数值方法虽然有效，但依赖于初始猜测，且在奇异点或不可达目标附近可能遇到困难。

---

<a id="item-8"></a>
### *（简报）* [爱好者用智能手机打造移动机器人](https://www.reddit.com/r/robotics/comments/1v3i1t7/i_turned_a_smartphone_into_a_mobile_robot_heres/) ⭐️ 6.0/10

一位爱好者分享了一款移动机器人原型，该机器人以智能手机作为机载计算机，通过浏览器进行远程控制并实时传输视频，由 Arduino 控制电机和外设。 该项目通过复用智能手机的摄像头、网络和计算能力，展示了一种低成本、易获取的机器人开发方式，对爱好者和教育场景很有价值。 该机器人具备浏览器控制、实时视频、LED 照明、实验性安全模式以及正在开发中的 BLE 跟随功能。下一版本将专注于更安静的驱动系统、更好的线缆管理、充电站和模块化配件。

---

<a id="item-9"></a>
### *（简报）* [HM-LD1 3D dToF LiDAR 用于无人机避障](https://www.reddit.com/r/robotics/comments/1v3i7if/3d_dtof_lidar_hmld1_for_uav_obstacle_avoidance/) ⭐️ 6.0/10

一位 Reddit 用户分享了将 HM-LD1 3D dToF LiDAR 集成到无人机避障系统中的进展，并计划在代码准备好后开源。 该项目展示了经济型固态 dToF LiDAR 在无人机避障中的实际应用，有望让自主无人机导航变得更加普及。 HM-LD1 的测距范围为 20–2500 毫米，视场角为 60° × 45°，采用 940 nm 人眼安全 VCSEL。用户还提到无人机在松开摇杆后会轻微向后漂移，并就此向社区寻求建议。

---

<a id="item-10"></a>
### *（简报）* [爱好者寻求为修复的 Puma 500 机械臂自制伺服驱动器的建议](https://www.reddit.com/r/robotics/comments/1v3z1c2/i_got_an_old_puma_500_any_advice_for_building/) ⭐️ 6.0/10

一位爱好者已从机械上修复了一台老式 Unimate Puma 500 机械臂，现在正在寻求关于为其六个带 500 PPR 光学编码器和绝对电位计的直流有刷电机制作定制数字伺服驱动器的建议。 该项目展示了为老式工业机器人改装现代控制系统的挑战，这对于希望重复利用旧硬件的爱好者、教育工作者和小规模自动化爱好者具有参考价值。 Puma 500 使用 24V 直流有刷电机（估计 40W 和 150W），带有电磁制动器和 500 PPR 光学编码器，但编码器存在抖动问题。用户计划使用 Arduino Every 微控制器和 RS-485 通信，但担心中断处理和编码器噪声。

---



---

### 📚 今日知识点
**概念**：逆运动学（Inverse Kinematics）
**是什么**：逆运动学就是让机器人“想好每个关节该转多少度，才能让手到达指定位置”。好比你想用手去够书架上的杯子，大脑会自然算出肩膀、肘部、手腕该弯多少度——这就是逆运动学。对机器人来说，它需要先知道“手要去哪”，然后反推出每个电机该转的角度。
**和今天新闻的关系**：在“从六轴机械臂构建中理解逆运动学的关键心得”这条新闻里，制作者分享了学习逆运动学的实用方法，比如先理解几何直觉、从二维平面臂开始、用数值求解器计算。
**延伸关键词**：正运动学、雅可比矩阵、奇异点、DH参数、数值求解
