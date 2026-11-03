#!/usr/bin/env python3
"""Build 立创复刻 data: 精讲连载 (P2 细纲 → daily episodes) + 了解 roster.

精讲 = the user's replication roadmap P2-65W GaN 反激 细纲 (阶段1 首个
精讲项目), split by its H2/H3 sections into daily episodes — one month
of deep-dive that ends with a real replication. 了解 = daily one-liner
introductions rotating through the verified 双榜 (P1-P7/E1-E7) and the
v6 ecosystem (TI/PI/GitHub/IEEE), links taken from the 细纲/候选库.
"""
import json
import os
import re

BASE = os.path.expanduser("~/Documents/ZCodeProject/复刻路线")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "app", "data")

EPS_INFIX = "电源榜细纲/P2-65W_GaN反激_细纲.md"


def read(p):
    return open(p, encoding="utf-8").read()


def split_episodes(md):
    """Split 细纲 markdown into daily episodes by H2/H3 boundaries."""
    lines = md.split("\n")
    # 头部引言块（# 标题 + > 引用）= 第 1 期 项目档案
    eps = []
    i = 0
    # find first "## " line
    while i < len(lines) and not lines[i].startswith("## "):
        i += 1
    intro = "\n".join(lines[:i]).strip()
    eps.append({"n": 1, "title": "第 1 期 · 项目档案与复刻目标", "body": intro})

    cur_h2 = None
    cur = []          # current episode lines
    cur_title = None

    def flush():
        nonlocal cur, cur_title
        if cur_title and cur:
            eps.append({"n": len(eps) + 1, "title": cur_title, "body": "\n".join(cur).strip()})
        cur = []
        cur_title = None

    while i < len(lines):
        ln = boundaries = lines[i]
        i += 1
        if ln.startswith("## "):
            flush()
            cur_title = ln[3:].strip()
            cur = [ln]
            continue
        if ln.startswith("### "):
            flush()
            cur_title = ln[4:].strip()
            cur = [ln]
            continue
        if cur_title is not None:
            cur.append(ln)
    flush()
    # 合并过小节（<80 字符 body 且非首期）到上一期
    merged = []
    for e in eps:
        if merged and len(e["body"]) < 80 and not e["body"].startswith("# "):
            merged[-1]["body"] += "\n\n" + e["body"]
            merged[-1]["title"] = merged[-1]["title"].split("·")[0].strip() + " · " + e["title"]
        else:
            merged.append(e)
    for n, e in enumerate(merged, start=1):
        e["n"] = n
    return merged, intro


def parse_meta(md):
    meta = {"project": "P2 · 65W GaN 反激充电器", "source": "立创开源硬件平台"}
    mm = re.search(r"立创项目页\*\*：(\S+)", md)
    if mm:
        meta["url"] = mm.group(1)
    mm = re.search(r"\| 项目名 \| ([^|]+)\|", md)
    if mm:
        meta["project"] = mm.group(1).strip()
    mm = re.search(r"\| 作者 \| ([^|]+)\|", md)
    if mm:
        meta["author"] = mm.group(1).strip()
    mm = re.search(r"\| 开源协议 \| \*\*([^*]+)\*\*", md)
    if mm:
        meta["license"] = mm.group(1).strip()
    return meta


def build_episodes():
    md = read(os.path.join(BASE, EPS_INFIX))
    eps, intro = split_episodes(md)
    meta = parse_meta(md)
    series = {
        "id": "p2-gan-65w",
        "project": meta.get("project", "P2 · 65W GaN 反激充电器"),
        "author": meta.get("author", ""),
        "license": meta.get("license", ""),
        "url": meta.get("url", ""),
        "source": "立创开源硬件平台",
        "stage": "阶段 1 · 复刻路线第一弹",
        "pitch": "65W GaN 反激：单管反激 + GaN 高频化 + PD 协议，一个项目吃透反激、GaN 驱动、PD 握手三条主线，成品即日常可用充电器。",
        "start_date": "2026-11-04",
        "cadence": "每日一期，讲透为止；跟着做，成品可真实复刻。",
        "episodes": eps,
    }
    with open(os.path.join(OUT, "fujing.json"), "w", encoding="utf-8") as f:
        json.dump(series, f, ensure_ascii=False, indent=1)
    print(f"fujing.json: {series['project']} {len(eps)} 期, url={meta.get('url','')[:60]}")


LIAOJIE = [
    ("P1 · LLC 300W (L6599)", "立创", "PFC+LLC 架构 30V/10A，UCC28180+L6599；你的 300W 桌面电源主参考。", None),
    ("P3 · Zeruns STM32G4 450W 同步 Buck-Boost", "立创", "效率 94.3%、HRPWM 184ps 分辨率、数字控制环路——数字电源必读。", None),
    ("P4 · FLPowerPro", "立创", "SC8701+AT32+PD 诱骗+CC 表+电子负载，7.7w 收藏的全能桌面电源。", None),
    ("P5 · 山雀桌面电源", "立创", "LM25116 电流模式 Buck+RS 锁存过流+继电器切断，1750 次下载。", None),
    ("P6 · SC8701+SW2305 100W", "立创", "23.4×18mm 跑满 100W 无散热，5.5k 收藏的极限小型化。", None),
    ("P7 · LGS6302 Boost", "立创", "3-60V 宽输入 Boost，BOM 完整，6.2k 收藏。", None),
    ("E1 · FLPowerPro 嵌入式侧", "立创", "AT32+FUSB302 状态机+TFT 多页面+FreeRTOS，PD 界面层范本。", None),
    ("E2 · 数显 PD 电源", "立创", "PL5501+SW2303+STC8H+IPS，4.9k 收藏的数显 PD 方案。", None),
    ("E3 · USB 可编程电源", "立创", "AT32F415+INA3221 16-bit+BLE+小程序，资料 9/10。", None),
    ("E5 · Zeruns STM32G4 嵌入式侧", "立创", "HRPWM 184ps+数字环路，与 P3 同源，嵌入式视角。", None),
    ("E6 · 数控稳压电源 V1.0", "立创", "STC 8A8K64S4A12+TL431，830 次下载的入门数控。", None),
    ("E7 · PD 诱骗双向监测表头", "立创", "CH32V003 RISC-V+CH224K+INA219+OLED。", None),
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
    ("Motoori 2025 论文", "IEEE", "Voltage-clamper + Mid-voltage AHB + SR——直接对应你的动态 AHB 母线架构。", None),
    ("Cao 2023 论文", "IEEE", "135W AHB Type-C（P Cao, Y Wang, Y Sun, X Lyu, F Yu）。", None),
]


def build_liaojie():
    # 立创项目真实 URL：从 11 份细纲的「立创项目页」行抓取
    urls = {}
    for root, dirs, files in os.walk(BASE):
        for fn in files:
            if not fn.endswith("细纲.md"):
                continue
            p = os.path.join(root, fn)
            try:
                md = read(p)
            except OSError:
                continue
            for mm in re.finditer(r"立创项目页\*\*：(\S+)", md):
                urls[fn] = mm.group(1)
    items = []
    for name, source, oneliner, link in LIAOJIE:
        it = {"name": name, "source": source, "oneliner": oneliner}
        key = name.split(" · ")[0] + "-"
        for fn, u in urls.items():
            if fn.startswith(key):
                it["link"] = u
        if link:
            it["link"] = link
        items.append(it)
    with open(os.path.join(OUT, "liaojie.json"), "w", encoding="utf-8") as f:
        json.dump({"version": 1, "items": items}, f, ensure_ascii=False, indent=1)
    print(f"liaojie.json: {len(items)} entries, {sum(1 for i in items if i.get('link'))} with links")


if __name__ == "__main__":
    build_episodes()
    build_liaojie()
