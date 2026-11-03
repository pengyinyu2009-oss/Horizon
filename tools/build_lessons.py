#!/usr/bin/env python3
"""Merge converted docx lessons (1-12) + authored md lessons (13-20)
into app/data/lessons.json for the PWA."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "app", "data")
SRC = os.path.join(HERE, "lessons-src")

SECTION_RE = re.compile(
    r"^(上讲自测答案|核心原理|公式|规律|算例|与 OBC 的联系|自测题|下一讲预告)"
)

def md_to_blocks(path):
    blocks = []
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n").strip()
        if not line:
            continue
        if line.startswith("# "):
            continue  # H1 title handled separately
        if SECTION_RE.match(line):
            # 「上讲自测答案：...」同行的形式拆成头+正文
            m = re.match(r"^(上讲自测答案)[：:]\s*(.+)", line)
            if m:
                blocks.append({"type": "text", "style": "h", "text": m.group(1)})
                blocks.append({"type": "text", "text": m.group(2)})
                continue
            if SECTION_RE.match(line) and len(line) < 15 and "：" not in line.split("：")[0][:14]:
                blocks.append({"type": "text", "style": "h", "text": line})
                continue
            # 带内容的小节（如 算例：...）整行当正文，前缀当头
            head = line.split("：")[0]
            rest = line[len(head) + 1:]
            blocks.append({"type": "text", "style": "h", "text": head})
            blocks.append({"type": "text", "text": rest})
            continue
        if line.startswith("· "):
            blocks.append({"type": "text", "text": line})
            continue
        if line.startswith("公式："):
            blocks.append({"type": "text", "formula": True, "text": line[3:]})
            continue
        blocks.append({"type": "text", "text": line})
    return blocks

def main():
    lessons = []
    for n in range(1, 21):
        jp = os.path.join(DATA, f"lesson-{n:02d}.json")
        mp = os.path.join(SRC, f"lesson-{n:02d}.md")
        if os.path.exists(jp):
            d = json.load(open(jp, encoding="utf-8"))
            src = "converted"
        elif os.path.exists(mp):
            d = {"title": None, "blocks": md_to_blocks(mp)}
            src = "authored"
        else:
            raise SystemExit(f"missing lesson {n}")
        title = d.get("title") or re.match(r"# 第 ?(\d+) 讲 · (.+)", open(mp, encoding="utf-8").read().split("\n")[0]).group(2)
        blocks = d["blocks"]
        # 行内公式标记展开为完整路径（App 渲染为行内小图）
        for b in blocks:
            if b.get("type") == "text" and "⟦" in b.get("text", ""):
                b["text"] = re.sub(r"⟦([^⟧]+)⟧", rf"⟦img/l{n:02d}/\1⟧", b["text"])
        lessons.append({
            "n": n,
            "title": title,
            "minutes": d.get("minutes", 6 if src == "converted" else 6),
            "tags": d.get("tags", []),
            "source": src,
            "blocks": blocks,
        })
    out = {
        "version": "2026.11.04.1",
        "start_date": "2026-11-04",
        "title": "每日电源基础课 · 从桌面电源到 OBC",
        "stages": [
            {"id": "s1", "title": "第 1-12 讲 · 开关电源与数字控制基础",
             "desc": "源自《电源基础课》讲义 1-12（伏秒平衡 → SiC 驱动）"},
            {"id": "s2", "title": "第 13-20 讲 · 面向 OBC 的进阶主线",
             "desc": "CLLC → DAB → 数字控制 → EMI → 磁集成 → 水冷 → 车规 → 结业路线"},
        ],
        "lessons": lessons,
    }
    dst = os.path.join(DATA, "lessons.json")
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"lessons.json: {len(lessons)} lessons, {os.path.getsize(dst)} bytes")

if __name__ == "__main__":
    main()
