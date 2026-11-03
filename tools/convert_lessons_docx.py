#!/usr/bin/env python3
"""docx → lesson JSON converter for the 每日电源基础课 series.

Runs on the NAS. Reads the 12 prepared .docx lessons, extracts the
paragraph flow (text + inline images in document order), writes one
lesson-NN.json per lesson plus the images under img/lNN/.
"""
import zipfile, re, json, html, os, sys

SRC = "/vol00/WDC WD200EDGZ-11B9PA0/学习资料/电源基础课"
OUT = "/vol00/WDC WD200EDGZ-11B9PA0/学习资料/电源基础课-converted"

def convert(path, lesson_num):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
        rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
        relmap = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="media/([^"]+)"', rels))
        media = {}
        for n in z.namelist():
            if n.startswith("word/media/"):
                media[os.path.basename(n)] = z.read(n)

    paras = re.findall(r"<w:p[ >].*?</w:p>", regex_safe(xml))
    blocks = []
    img_count = 0
    for para in paras:
        for rid in re.findall(r'r:embed="(rId\d+)"', para):
            fname = relmap.get(rid)
            if fname:
                img_count += 1
                blocks.append({"type": "img",
                               "src": f"img/l{lesson_num:02d}/{img_count:02d}.png",
                               "orig": fname})
        texts = re.findall(r"<w:t[^>]*>([^<]*)</w:t>", para)
        line = html.unescape("".join(texts)).strip()
        if line:
            style = ""
            ms = re.search(r'<w:pStyle w:val="([^"]+)"', para)
            if ms:
                style = ms.group(1)
            blocks.append({"type": "text", "text": line, "style": style})
    return blocks, media, img_count

def regex_safe(xml):
    # <w:p > vs <w:p>: normalize both; keep self-closed p out
    return xml

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
        blocks, media, img_count = convert(os.path.join(SRC, fname), lesson_num)
        imgdir = os.path.join(OUT, "img", f"l{lesson_num:02d}")
        os.makedirs(imgdir, exist_ok=True)
        # 按文档流顺序落盘：blocks 里的 img 标记第 N 张就是第 N 张
        # （以流中首次引用的 orig 文件名为准，同名复写无妨）。
        seen = []
        for b in blocks:
            if b["type"] == "img" and b["orig"] not in seen:
                seen.append(b["orig"])
        for b in blocks:
            if b["type"] != "img":
                continue
            data = media.get(b["orig"])
            if data is None:
                b["missing"] = True
                continue
            with open(os.path.join(imgdir, b["src"].split("/")[-1]), "wb") as f:
                f.write(data)
        # 未被正文引用的孤儿图片不落盘，防止张冠李戴
        out = {"lesson": lesson_num, "title": title, "blocks": blocks}
        with open(os.path.join(OUT, f"lesson-{lesson_num:02d}.json"), "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        print(f"lesson {lesson_num:02d}: {len(blocks)} blocks, {img_count} imgs, {title}")

if __name__ == "__main__":
    main()
