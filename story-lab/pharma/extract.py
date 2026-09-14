#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract Persian text from the two handout PDFs.

PyMuPDF splits Persian words across 'spans' on the same visual baseline.
RTL text must be re-ordered by descending x within each baseline group.
"""
import os
import re
import sys
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "source")

TOL = 2.5          # baseline grouping tolerance (points)
PERSIAN = re.compile(r"[\u0600-\u06FF]")


def line_text(spans, rtl=True):
    spans = sorted(spans, key=lambda s: s[0], reverse=rtl)
    return "".join(s[2] for s in spans)


def page_lines(page):
    d = page.get_text("dict")
    groups = []          # (y, [ (x0, x1, text) ])
    for block in d.get("blocks", []):
        if block.get("type") != 0:
            continue
        for ln in block.get("lines", []):
            for sp in ln.get("spans", []):
                txt = sp.get("text", "")
                if not txt.strip():
                    continue
                x0, y0, x1, y1 = sp["bbox"]
                persian = len(PERSIAN.findall(txt))
                latin = len(re.findall(r"[A-Za-z]", txt))
                rtl = persian >= latin
                for g in groups:
                    if abs(g[0] - y0) <= TOL:
                        g[1].append((x0, x1, txt, rtl))
                        break
                else:
                    groups.append([y0, [(x0, x1, txt, rtl)]])
    groups.sort(key=lambda g: g[0])
    out = []
    for y, spans in groups:
        rtl_ratio = sum(1 for s in spans if s[3]) / max(1, len(spans))
        out.append(line_text(spans, rtl=rtl_ratio >= 0.5).strip())
    return out


def clean(lines):
    """Join wrapped lines; keep paragraph-ish flow."""
    buf = []
    for ln in lines:
        if not ln:
            if buf and buf[-1] != "":
                buf.append("")
            continue
        if buf and buf[-1] and not buf[-1].endswith((".", ":", "؟", "!", "»", ")", "؛")):
            prev = buf.pop()
            joiner = "" if prev.endswith("\u200c") else " "
            buf.append(prev + joiner + ln)
        else:
            buf.append(ln)
    txt = "\n".join(buf)
    txt = re.sub(r"[ \t]{2,}", " ", txt)
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    return txt.strip()


def main():
    os.makedirs(OUT, exist_ok=True)
    for fn in sorted(f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")):
        doc = pymupdf.open(os.path.join(PDF_DIR, fn))
        chunks = []
        for i, page in enumerate(doc, 1):
            chunks.append("### صفحه %d\n%s" % (i, clean(page_lines(page))))
        stem = os.path.splitext(fn)[0]
        path = os.path.join(OUT, stem + ".txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(chunks))
        print("wrote", path, "| pages:", doc.page_count, "| chars:", sum(len(c) for c in chunks))


if __name__ == "__main__":
    main()
