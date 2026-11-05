#!/usr/bin/env python3
"""Merge lesson sources + backgrounds into app/data JSONs for the PWA.

Sources per lesson n (1..N, N unlimited — drop new files and rebuild):
  1. app/data/lesson-NN.json   — converted from NAS docx (⟦NN.png⟧ markers)
  2. tools/lessons-src/lesson-NN.md — authored markdown (standard sections)

build_lessons.py also:
  - injects background blocks (tools/backgrounds.json) before 核心原理
  - extracts 自测题 per lesson into a quiz bank
  - extracts 上讲自测答案 into an answers map (answers[n] reviews lesson n-1)
  - generates the quiz schedule: unit quiz every 5 lessons, comprehensive
    quiz every 10 lessons
Outputs: app/data/lessons.json + app/data/quizzes.json
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "app", "data")
SRC = os.path.join(HERE, "lessons-src")

SECTION_RE = re.compile(
    r"^(上讲自测答案|核心原理|公式|规律|算例|与 OBC 的联系|自测题|下一讲预告)"
)

STAGES = [
    {"id": "s1", "title": "第 1-12 讲 · 基础", "range": [1, 12],
     "desc": "伏秒平衡 → SiC 驱动（源自《电源基础课》讲义）"},
    {"id": "s2", "title": "第 13-20 讲 · OBC 进阶", "range": [13, 20],
     "desc": "CLLC → DAB → 数字控制 → EMI → 磁集成 → 水冷 → 车规 → 结业"},
    {"id": "s3", "title": "第 21-30 讲 · 实战篇", "range": [21, 30],
     "desc": "评审 → 布局 → 调试 → 测试 → 系统整合，从看懂到做出来"},
]


def md_to_blocks(path):
    blocks = []
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n").strip()
        if not line:
            continue
        if line.startswith("# "):
            continue  # H1 title handled separately
        if SECTION_RE.match(line):
            m = re.match(r"^(上讲自测答案)[：:]\s*(.+)", line)
            if m:
                blocks.append({"type": "text", "style": "h", "text": m.group(1)})
                blocks.append({"type": "text", "text": m.group(2)})
                continue
            if len(line) < 15 and "：" not in line.split("：")[0][:14]:
                blocks.append({"type": "text", "style": "h", "text": line})
                continue
            head = line.split("：")[0]
            rest = line[len(head) + 1:]
            blocks.append({"type": "text", "style": "h", "text": head})
            if rest:
                blocks.append({"type": "text", "text": rest})
            continue
        if line.startswith("公式："):
            blocks.append({"type": "text", "formula": True, "text": line[3:]})
            continue
        blocks.append({"type": "text", "text": line})
    return blocks


def is_h(b):
    return b.get("style") in ("Heading2", "h")


def section_range(blocks, start_kw, stop_kws):
    """Text/other blocks between a heading containing start_kw and the next
    heading containing any stop_kw (or end)."""
    out, inside = [], False
    for b in blocks:
        if is_h(b):
            if inside and any(k in b.get("text", "") for k in stop_kws):
                break
            inside = start_kw in b.get("text", "")
            continue
        if inside:
            out.append(b)
    return out


def inject_background(blocks, bg):
    pre = [{"type": "text", "style": "h", "text": "🧭 背景补给 · 读这讲前先懂这些"}]
    pre += [{"type": "text", "text": t} for t in bg.get("pre", [])]
    pre += [{"type": "text", "style": "h", "text": "🔤 术语速查"}]
    pre += [{"type": "text", "text": t} for t in bg.get("terms", [])]
    idx = next((i for i, b in enumerate(blocks)
                if is_h(b) and "核心原理" in b.get("text", "")), 1)
    return blocks[:idx] + pre + blocks[idx:]


def main():
    backgrounds = json.load(open(os.path.join(HERE, "backgrounds.json"),
                                 encoding="utf-8"))
    lessons, bank, answers = [], {}, {}
    n = 1
    while True:
        jp = os.path.join(DATA, f"lesson-{n:02d}.json")
        mp = os.path.join(SRC, f"lesson-{n:02d}.md")
        if os.path.exists(jp):
            d = json.load(open(jp, encoding="utf-8"))
            src = "converted"
        elif os.path.exists(mp):
            first = open(mp, encoding="utf-8").read().split("\n")[0]
            d = {"title": re.match(r"# 第 ?(\d+) 讲 · (.+)", first).group(2),
                 "blocks": md_to_blocks(mp)}
            src = "authored"
        else:
            break
        blocks = [dict(b) for b in d["blocks"]]
        # inline formula markers -> full paths
        for b in blocks:
            if b.get("type") == "text" and "⟦" in b.get("text", ""):
                b["text"] = re.sub(r"⟦([^⟧]+)⟧",
                                   rf"⟦img/l{n:02d}/\1⟧", b["text"])
        bg = backgrounds.get(str(n))
        if bg:
            blocks = inject_background(blocks, bg)
        # quiz bank: blocks under 自测题, drop the answer-note line
        qs = [b for b in section_range(
            blocks, "自测题", ["下一讲预告", "核心原理"])
            if b.get("type") == "text" and "答案" not in b.get("text", "")[:6]
            or b.get("type") == "text" and b.get("formula")]
        qs = [b for b in qs if b.get("type") == "text"]
        if qs:
            bank[n] = [b["text"] for b in qs]
        # answers: blocks under 上讲自测答案 of lesson n review lesson n-1
        ans = section_range(blocks, "上讲自测答案", ["核心原理"])
        if ans and n >= 2:
            answers[n - 1] = [b.get("text", "") for b in ans
                              if b.get("type") == "text"]
        lessons.append({
            "n": n,
            "title": d.get("title"),
            "minutes": d.get("minutes", 8 if src == "authored" else 6),
            "tags": d.get("tags", []),
            "source": src,
            "blocks": blocks,
        })
        n += 1

    if len(lessons) < 20:
        raise SystemExit(f"only {len(lessons)} lessons found, expected >= 20")

    maxn = lessons[-1]["n"]
    quizzes = []
    for m in range(5, maxn + 1, 5):
        kind = "final" if m % 10 == 0 else "unit"
        cover = list(range(1, m + 1)) if kind == "final" else list(range(m - 4, m + 1))
        label = "综合测验" if kind == "final" else "单元测验"
        quizzes.append({
            "id": f"quiz-{m}",
            "type": kind,
            "after": m,
            "title": f"{label} · 覆盖第 {cover[0]}-{cover[-1]} 讲",
            "cover": cover,
        })

    out = {
        "version": "2026.11.05.2",
        "start_date": "2026-11-04",
        "title": "每日电源基础课 · 从桌面电源到 OBC",
        "stages": STAGES,
        "lessons": lessons,
    }
    with open(os.path.join(DATA, "lessons.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    qout = {
        "version": out["version"],
        "steps": [1, 2, 4, 7, 15, 30],
        "bank": bank,
        "answers": answers,
        "quizzes": quizzes,
    }
    with open(os.path.join(DATA, "quizzes.json"), "w", encoding="utf-8") as f:
        json.dump(qout, f, ensure_ascii=False, indent=1)

    bg_count = sum(1 for l in lessons
                   if any("背景补给" in b.get("text", "") for b in l["blocks"]))
    print(f"lessons.json: {len(lessons)} lessons ({bg_count} with background)")
    print(f"quizzes.json: {len(bank)} bank lessons, "
          f"{len(answers)} answer sets, {len(quizzes)} quizzes, "
          f"max lesson {maxn}")


if __name__ == "__main__":
    main()
