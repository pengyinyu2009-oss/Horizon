#!/usr/bin/env python3
"""Build the 立创复刻 data for the PWA.

episodes: assembled from tools/fuke-plan.json (explicit curriculum —
week structure, per-episode goal, section references) against the P2
细纲 markdown. Replaces the old naive heading-splitter that produced
mixed-level titles and 12x size variance between episodes.

liaojie: daily one-line introductions rotating the verified double-
board + TI/PI/GitHub/IEEE ecosystem, links taken from the 细纲.
"""
import json
import os
import re

BASE = os.path.expanduser("~/Documents/ZCodeProject/复刻路线")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "app", "data")
PLAN = os.path.join(HERE, "fuke-plan.json")
OUTLINE = os.path.join(BASE, "电源榜细纲/P2-65W_GaN反激_细纲.md")


def parse_sections(md):
    """Flat map: exact heading line -> raw markdown of that section
    (heading included, stops before the next heading of any level)."""
    sections = {}
    cur_key = None
    cur = []
    for line in md.split("\n"):
        if re.match(r"^#{1,6} ", line):
            if cur_key is not None:
                sections[cur_key] = "\n".join(cur).strip()
            cur_key = line.strip()
            cur = [line.strip()]
        elif cur_key is not None:
            cur.append(line)
    if cur_key is not None:
        sections[cur_key] = "\n".join(cur).strip()
    return sections


def assemble(sections, refs):
    parts, missing = [], []
    for ref in refs:
        body = sections.get(ref)
        if body is None:
            missing.append(ref)
        else:
            parts.append(body)
    return "\n\n".join(parts), missing


def build():
    plan = json.load(open(PLAN, encoding="utf-8"))
    sections = parse_sections(open(OUTLINE, encoding="utf-8").read())
    series = dict(plan["series"])

    episodes = []
    for ep in plan["episodes"]:
        body, missing = assemble(sections, ep["sections"])
        if missing:
            raise SystemExit(f"episode {ep['n']} missing sections: {missing}")
        if not body:
            raise SystemExit(f"episode {ep['n']} assembled an empty body")
        episodes.append({"n": ep["n"], "week": ep["week"], "kind": ep["kind"],
                         "title": ep["title"], "goal": ep["goal"], "body": body})

    appendix = []
    for ap in plan["appendix"]:
        body, missing = assemble(sections, ap["sections"])
        if missing:
            raise SystemExit(f"appendix {ap['id']} missing sections: {missing}")
        appendix.append({"id": ap["id"], "icon": ap["icon"],
                         "title": ap["title"], "body": body})

    series["episodes"] = episodes
    series["appendix"] = appendix
    series["weeks"] = sorted({e["week"] for e in episodes})
    series["week_titles"] = plan.get("week_titles", {})
    with open(os.path.join(OUT, "fujing.json"), "w", encoding="utf-8") as f:
        json.dump(series, f, ensure_ascii=False, indent=1)
    sizes = [len(e["body"]) for e in episodes]
    print(f"fujing.json: {series['project']} · {len(episodes)} 期 / "
          f"{len(series['weeks'])} 周 · 附录 {len(appendix)} 篇 · "
          f"篇幅 {min(sizes)}-{max(sizes)} 字")


LIAOJIE = [
    ("P1 · LLC 300W (L6599)", "立创", "PFC+LLC 架构 30V/10A，UCC28180+L6599；你的 300W 桌面电源主参考。"),
    ("P3 · Zeruns STM32G4 450W 同步 Buck-Boost", "立创", "效率 94.3%、HRPWM 184ps 分辨率、数字控制环路——数字电源必读。"),
    ("P4 · FLPowerPro", "立创", "SC8701+AT32+PD 诱骗+CC 表+电子负载，7.7w 收藏的全能桌面电源。"),
    ("P5 · 山雀桌面电源", "立创", "LM25116 电流模式 Buck+RS 锁存过流+继电器切断，1750 次下载。"),
    ("P6 · SC8701+SW2305 100W", "立创", "23.4×18mm 跑满 100W 无散热，5.5k 收藏的极限小型化。"),
    ("P7 · LGS6302 Boost", "立创", "3-60V 宽输入 Boost，BOM 完整，6.2k 收藏。"),
    ("E1 · FLPowerPro 嵌入式侧", "立创", "AT32+FUSB302 状态机+TFT 多页面+FreeRTOS，PD 界面层范本。"),
    ("E2 · 数显 PD 电源", "立创", "PL5501+SW2303+STC8H+IPS，4.9k 收藏的数显 PD 方案。"),
    ("E3 · USB 可编程电源", "立创", "AT32F415+INA3221 16-bit+BLE+小程序，资料 9/10。"),
    ("E5 · Zeruns STM32G4 嵌入式侧", "立创", "HRPWM 184ps+数字环路，与 P3 同源，嵌入式视角。"),
    ("E6 · 数控稳压电源 V1.0", "立创", "STC 8A8K64S4A12+TL431，830 次下载的入门数控。"),
    ("E7 · PD 诱骗双向监测表头", "立创", "CH32V003 RISC-V+CH224K+INA219+OLED。"),
    ("TIDA-050074", "TI", "140W Boost-PFC+AHB GaN，地球上最接近你 300W 目标的官方参考（>95.5% 效率）。", "https://www.ti.com/tool/TIDA-050074"),
    ("PMP41115", "TI", "240W Buck-Boost PD3.1 EPR，97.6% 满载效率。", "https://www.ti.com/tool/PMP41115"),
    ("PMP23558", "TI", "240W GaN PFC+LLC（UCC25661+LMG3622），95.96% 峰值。", "https://www.ti.com/tool/PMP23558"),
    ("TIDA-01623", "TI", "100W 极紧凑 PFC+ACF GaN，30 W/in³。", "https://www.ti.com/tool/TIDA-01623"),
    ("TIDA-010047", "TI", "100W PFC+ACF Si 双口 USB-PD（UCC28780+TPS65987D）。", "https://www.ti.com/tool/TIDA-010047"),
    ("DER-1077", "PI", "140W PowiGaN PD3.2 EPR，>95% 效率。", "https://power.com/design-support/design-examples/der-1077/"),
    ("DER-1065", "PI", "90W 双口共享容量（INN5375F-H907+IP2738），>93.5%。", "https://power.com/design-support/design-examples/der-1065/"),
    ("LeoDJ/USB-C_PD_PSU", "GitHub", "唯一开源 240W EPR（BQ25758A+CH32X035 双控），WIP 但稀缺。", "https://github.com/LeoDJ/USB-C_PD_PSU"),
    ("Jana-Marie/Otter-Iron", "GitHub", "USB-PD 完整协议栈，519 stars。", "https://github.com/Jana-Marie/Otter-Iron"),
    ("sydundar/BenchVolt-PD", "GitHub", "工作台级 USB-PD 桌面电源，77 stars。", "https://github.com/sydundar/BenchVolt-PD"),
    ("Motoori 2025 论文", "IEEE", "Voltage-clamper + Mid-voltage AHB + SR——直接对应你的动态 AHB 母线架构。"),
    ("Cao 2023 论文", "IEEE", "135W AHB Type-C（P Cao, Y Wang, Y Sun, X Lyu, F Yu）。"),
]


def build_liaojie():
    urls = {}
    for root, _dirs, files in os.walk(BASE):
        for fn in files:
            if not fn.endswith("细纲.md"):
                continue
            try:
                md = open(os.path.join(root, fn), encoding="utf-8").read()
            except OSError:
                continue
            for mm in re.finditer(r"立创项目页\*\*：(\S+)", md):
                urls[fn] = mm.group(1)
    items = []
    for entry in LIAOJIE:
        it = {"name": entry[0], "source": entry[1], "oneliner": entry[2]}
        if len(entry) > 3:
            it["link"] = entry[3]
        prefix = entry[0].split(" · ")[0] + "-"
        for fn, u in urls.items():
            if fn.startswith(prefix):
                it["link"] = u
        items.append(it)
    with open(os.path.join(OUT, "liaojie.json"), "w", encoding="utf-8") as f:
        json.dump({"version": 1, "items": items}, f, ensure_ascii=False, indent=1)
    print(f"liaojie.json: {len(items)} entries, "
          f"{sum(1 for i in items if i.get('link'))} with links")


if __name__ == "__main__":
    build()
    build_liaojie()
