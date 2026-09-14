#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Line- and item-level extraction of the two handout PDFs.

Produces, per PDF:
  source-lines/<stem>.txt   one visual line per line, page-marked (### صفحه N)
Prints a per-page item index (headings + bullet items) with stable IDs:
  CV-p12-03 / MM-p07-05 ...
This index is the checklist the story must satisfy, item by item.
"""
import os, re, sys, statistics
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "source-lines")
TOL = 2.5
PERSIAN = re.compile(r"[\u0600-\u06FF]")
BULLET = re.compile(r"^\s*(•|❖|▪|◆|\*|–|--|[-−]\s|\d+[\.\-)]|[\u0600-\u06FF]?[\)\]]|[١٢٣٤٥٦٧٨٩٠]+[\.\-]|[الفبجد]\))")
ROMAN = re.compile(r"^\s*(مقدمه|تعریف|فارماکو|فیزیولوژی|پاتوفیزیولوژی|مکانیسم|طبقه|گروه|عوارض|تداخل|درمان|انواع|نکات|خلاصه|مثال|دقت)")


def baseline_lines(page):
    d = page.get_text("dict")
    groups = []          # [y, [(x0,x1,text,rtl,size)]]
    for block in d.get("blocks", []):
        if block.get("type") != 0:
            continue
        for ln in block.get("lines", []):
            for sp in ln.get("spans", []):
                txt = sp.get("text", "")
                if not txt.strip():
                    continue
                x0, y0, x1, y1 = sp["bbox"]
                persian = len(PERSIAN.findall(txt)); latin = len(re.findall(r"[A-Za-z]", txt))
                rtl = persian >= latin
                for g in groups:
                    if abs(g[0] - y0) <= TOL:
                        g[1].append((x0, x1, txt, rtl, sp["size"]))
                        break
                else:
                    groups.append([y0, [(x0, x1, txt, rtl, sp["size"])]])
    groups.sort(key=lambda g: g[0])
    out = []
    for y, spans in groups:
        rtl = sum(1 for s in spans if s[3]) / max(1, len(spans)) >= 0.5
        ordered = sorted(spans, key=lambda s: s[0], reverse=rtl)
        text = "".join(s[2] for s in ordered).strip()
        size = max(s[4] for s in spans)
        if text:
            out.append((text, size))
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    index = []
    for fn in sorted(f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")):
        tag = "CV" if "قلب" in fn or "قلبي" in fn else "MM"
        doc = pymupdf.open(os.path.join(PDF_DIR, fn))
        chunks = ["### FILE %s" % fn]
        for i, page in enumerate(doc, 1):
            lines = baseline_lines(page)
            sizes = [s for _, s in lines]
            body = statistics.median(sizes) if sizes else 10
            chunks.append("### صفحه %d" % i)
            items = []
            for text, size in lines:
                chunks.append(text)
                is_head = size > body + 0.8
                if is_head or BULLET.match(text) or (len(text) < 70 and ROMAN.match(text)):
                    items.append(("H" if is_head else "•", text))
            for k, (kind, text) in enumerate(items, 1):
                index.append("%s-p%02d-%02d\t%s\t%s" % (tag, i, k, kind, text))
        stem = os.path.splitext(fn)[0]
        with open(os.path.join(OUT, stem + ".txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(chunks))
        print("wrote lines:", stem, "| pages:", doc.page_count)
    idx_path = os.path.join(HERE, "handout-items.tsv")
    with open(idx_path, "w", encoding="utf-8") as f:
        f.write("\n".join(index))
    print("items:", len(index), "->", idx_path)


if __name__ == "__main__":
    main()
