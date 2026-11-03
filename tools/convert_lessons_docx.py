#!/usr/bin/env python3
"""docx -> lesson JSON converter v2 (rich blocks).

v1 flaw fixed: inline formula images were hoisted out of their
sentences (broken text like「取 Buck：、，则 。」). v2 walks each
paragraph's runs IN ORDER, interleaving text and image refs, and
sniffs PNG dimensions: small (<=100px tall) = inline formula, large
= figure block. Meta lines (series title / push date) are dropped.
Runs on the NAS against 学习资料/电源基础课.
"""
import zipfile, re, json, html, os, struct

SRC = "/vol00/WDC WD200EDGZ-11B9PA0/学习资料/电源基础课"
OUT = "/vol00/WDC WD200EDGZ-11B9PA0/学习资料/电源基础课-converted"

PNG_SIG = b"\x89PNG\r\n\x1a\n"


def png_size(data):
    if data[:8] != PNG_SIG:
        return None
    w, h = struct.unpack(">II", data[16:24])
    return (w, h)


def para_parts(para_xml, relmap, media):
    """Ordered parts of one paragraph: text runs and image refs."""
    parts = []
    for run in re.findall(r"<w:r[ >].*?</w:r>", para_xml, re.S):
        for t in re.findall(r"<w:t[^>]*>([^<]*)</w:t>", run):
            if t:
                parts.append({"t": html.unescape(t)})
        for rid in re.findall(r'r:embed="(rId\d+)"', run):
            fname = relmap.get(rid)
            data = media.get(fname)
            if not data:
                continue
            size = png_size(data) or (0, 0)
            parts.append({"i": fname, "w": size[0], "h": size[1]})
    return parts


def convert(path, lesson_num, imgdir):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
        rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
        relmap = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="media/([^"]+)"', rels))
        media = {}
        for n in z.namelist():
            if n.startswith("word/media/"):
                media[os.path.basename(n)] = z.read(n)

    paras = re.findall(r"<w:p[ >].*?</w:p>", xml, re.S)
    blocks = []
    img_seq = 0
    img_map = {}

    def host(fname):
        nonlocal img_seq
        if fname not in img_map:
            img_seq += 1
            img_map[fname] = f"{img_seq:02d}.png"
            with open(os.path.join(imgdir, img_map[fname]), "wb") as f:
                f.write(media[fname])
        return img_map[fname]

    for para in paras:
        parts = para_parts(para, relmap, media)
        if not parts:
            continue
        joined = "".join(p.get("t", "") for p in parts).strip()
        if joined.startswith(("每日电源基础课 ·", "推送日期：")):
            continue
        rich = []
        textbuf = ""
        for p in parts:
            if "t" in p:
                textbuf += p["t"]
                continue
            hosted = host(p["i"])
            if p["h"] > 0 and p["h"] <= 100:
                textbuf += "⟦" + hosted + "⟧"
                continue
            if textbuf.strip():
                rich.append({"type": "text", "text": html.unescape(textbuf).strip()})
                textbuf = ""
            rich.append({"type": "img",
                         "src": f"img/l{lesson_num:02d}/{hosted}",
                         "w": p["w"], "h": p["h"]})
        if textbuf.strip():
            rich.append({"type": "text", "text": html.unescape(textbuf).strip()})
        rich = [b for b in rich if b["type"] == "img" or b.get("text")]
        if not rich:
            continue
        style = ""
        ms = re.search(r'<w:pStyle w:val="([^"]+)"', para)
        if ms:
            style = ms.group(1)
        if style:
            for b in rich:
                if b["type"] == "text":
                    b["style"] = style
        blocks.extend(rich)
    return blocks


def main():
    os.makedirs(OUT, exist_ok=True)
    for fname in sorted(os.listdir(SRC)):
        if not fname.endswith(".docx"):
            continue
        m = re.match(r"第(\d+)讲-(.+)\.docx", fname)
        if not m:
            continue
        lesson_num = int(m.group(1))
        title = m.group(2)
        imgdir = os.path.join(OUT, "img", f"l{lesson_num:02d}")
        os.makedirs(imgdir, exist_ok=True)
        blocks = convert(os.path.join(SRC, fname), lesson_num, imgdir)
        out = {"lesson": lesson_num, "title": title, "blocks": blocks}
        with open(os.path.join(OUT, f"lesson-{lesson_num:02d}.json"), "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        figs = sum(1 for b in blocks if b["type"] == "img")
        inline = sum(1 for b in blocks if b["type"] == "text" and "⟦" in b["text"])
        print(f"lesson {lesson_num:02d}: {len(blocks)} blocks, {figs} figures, {inline} rich-text, {title}")

if __name__ == "__main__":
    main()
