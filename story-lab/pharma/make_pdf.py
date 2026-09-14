#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ساختِ PDF داستانِ «آمپولِ نهم» از فایل‌های story/part*.md

اجرا:
    python3 make_pdf.py            # همهٔ ۱۶ بخش
    python3 make_pdf.py 3          # فقط بخش‌های ۱ تا ۳ (برای آزمایش)
"""
import io
import os
import re
import sys

from fpdf import FPDF, FontFace

BASE = os.path.dirname(os.path.abspath(__file__))
STORY_DIR = os.path.join(BASE, "story")
FONT_DIR = os.path.join(BASE, "assets", "fonts")
ASSET_DIR = os.path.join(BASE, "assets")
OUT_NAME = sys.argv[2] if len(sys.argv) > 2 else "آمپول-نهم.pdf"
OUT_PATH = os.path.join(BASE, OUT_NAME)

INK = (18, 22, 20)
DIM = (110, 104, 92)
ACCENT = (29, 74, 68)      # teal
AMBER = (176, 112, 32)     # amber
RULE = (206, 198, 182)
HEAD_BG = (238, 233, 222)
ZEBRA = (248, 246, 241)

BODY_SIZE = 10.5
BODY_LH = 6.0
TABLE_SIZE = 8.6
TABLE_LH = 4.6


def digits(t):
    return t


class Book(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(20, 18, 20)
        self.set_auto_page_break(True, margin=20)
        self.add_font("Vazir", "", os.path.join(FONT_DIR, "Vazirmatn-Regular.ttf"))
        self.add_font("Vazir", "B", os.path.join(FONT_DIR, "Vazirmatn-Bold.ttf"))
        # فونتِ کمکی برای نویسه‌هایی که وزیرمتن ندارد (α، β، زیرنویس‌ها، فلش‌ها)
        self.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
        self.set_fallback_fonts(["DejaVu"])
        self.set_text_shaping(True, direction="rtl", script="arab", language="fas")
        self.running = ""
        self.set_title("آمپولِ نهم — داستانِ آموزشی داروشناسی")
        self.set_author("بر پایهٔ جزوه‌های دکتر فروتن")

    def header(self):
        if self.page_no() <= 2:
            return
        self.set_font("Vazir", "", 7.5)
        self.set_text_color(*DIM)
        self.set_x(self.l_margin)
        self.cell(self.epw, 5, self.running, align="R")
        self.set_draw_color(*RULE)
        y = self.get_y() + 1
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.set_y(y + 4)
        self.set_text_color(*INK)

    def footer(self):
        if self.page_no() <= 1:
            return
        self.set_y(-14)
        self.set_font("Vazir", "", 7.5)
        self.set_text_color(*DIM)
        self.set_x(self.l_margin)
        self.cell(self.epw, 6, str(self.page_no()), align="C")
        self.set_text_color(*INK)

    # ---------- building blocks ----------
    def para(self, text, size=BODY_SIZE, lh=BODY_LH, align="R", color=INK, style="",
             indent=0):
        self.set_font("Vazir", style, size)
        self.set_text_color(*color)
        self.set_x(self.l_margin)
        self.multi_cell(self.epw - indent, lh, text, align=align, markdown=True,
                        new_x="LMARGIN", new_y="NEXT")
        self.ln(lh * 0.35)

    def chapter(self, text):
        self.running = text
        self.add_page()
        self.set_font("Vazir", "B", 17)
        self.set_text_color(*ACCENT)
        self.set_x(self.l_margin)
        self.multi_cell(self.epw, 9, text, align="R", markdown=True,
                        new_x="LMARGIN", new_y="NEXT")
        y = self.get_y() + 1.5
        self.set_draw_color(*AMBER)
        self.set_line_width(0.7)
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.set_line_width(0.2)
        self.ln(6)

    def subhead(self, text):
        self.ln(1.5)
        self.set_font("Vazir", "B", 12.5)
        self.set_text_color(*AMBER)
        self.set_x(self.l_margin)
        self.multi_cell(self.epw, 7, text, align="R", markdown=True,
                        new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*INK)
        self.ln(1.5)

    def quote(self, text):
        self.set_font("Vazir", "", BODY_SIZE - 0.5)
        self.set_text_color(70, 66, 58)
        w = self.epw - 9
        x_bar = self.l_margin + w + 3          # میله در لبهٔ راستِ بلوک
        y = self.get_y()
        self.set_x(self.l_margin)
        self.multi_cell(w, BODY_LH - 0.4, text, align="R", markdown=True,
                        new_x="LMARGIN", new_y="NEXT", padding=(0, 4, 0, 2))
        self.set_draw_color(*AMBER)
        self.set_line_width(0.5)
        self.line(x_bar, y, x_bar, self.get_y() - 2)
        self.set_line_width(0.2)
        self.set_text_color(*INK)
        self.ln(1)

    def hr(self):
        self.ln(2)
        self.set_draw_color(*RULE)
        y = self.get_y()
        self.line(self.l_margin + self.epw * 0.3, y, self.l_margin + self.epw * 0.7, y)
        self.ln(3)

    def h3(self, text):
        self.ln(1)
        self.set_font("Vazir", "B", 11.5)
        self.set_text_color(*ACCENT)
        self.set_x(self.l_margin)
        self.multi_cell(self.epw, 6.5, text, align="R", markdown=True,
                        new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*INK)
        self.ln(1.5)

    def body_bold(self, text):
        self.set_font("Vazir", "B", BODY_SIZE)
        self.set_text_color(*INK)
        self.set_x(self.l_margin)
        self.multi_cell(self.epw, BODY_LH, text, align="R",
                        new_x="LMARGIN", new_y="NEXT")
        self.ln(BODY_LH * 0.4)

    def bullet(self, text):
        self.set_font("Vazir", "", BODY_SIZE)
        self.set_text_color(*INK)
        self.set_x(self.l_margin)
        self.multi_cell(self.epw - 4, BODY_LH, "\u2022 " + text, align="R", markdown=True,
                        new_x="LMARGIN", new_y="NEXT", padding=(0, 0, 0, 3))
        self.ln(BODY_LH * 0.25)

    def render_table(self, rows):
        if not rows:
            return
        header = rows[0]
        body = rows[1:]
        ncol = len(header)
        # عرض نسبی ستون‌ها بر پایهٔ بلندیِ متن
        weights = []
        for c in range(ncol):
            longest = max([len(r[c]) for r in rows if c < len(r)] or [10])
            weights.append(min(max(longest, 8), 90) ** 0.8)
        total = sum(weights)
        usable = self.epw
        widths = [max(14.0, usable * w / total) for w in weights]
        scale = usable / sum(widths)
        widths = [w * scale for w in widths]
        widths = list(reversed(widths))  # چیدمانِ راست‌به‌چپ

        style = FontFace(family="Vazir", emphasis="BOLD", size_pt=TABLE_SIZE,
                         color=(255, 255, 255))
        self.set_font("Vazir", "", TABLE_SIZE)
        self.set_text_color(*INK)
        with self.table(col_widths=tuple(widths), text_align="RIGHT",
                        line_height=TABLE_LH, padding=(1.4, 1.8, 1.4, 1.8),
                        headings_style=style, cell_fill_color=HEAD_BG,
                        cell_fill_mode="ROWS", borders_layout="SINGLE_TOP_LINE",
                        first_row_as_headings=True, v_align="TOP",
                        repeat_headings=1) as t:
            for i, r in enumerate(rows):
                row = t.row()
                cells = [c for c in r] + [""] * (ncol - len(r))
                for cell in reversed(cells[:ncol]):
                    row.cell(cell.replace("**", ""))
        self.ln(2.5)


def is_table_sep(line):
    return bool(re.match(r"^\s*\|[\s:|\-]+\|\s*$", line))


def table_cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def read_blocks(path):
    lines = io.open(path, encoding="utf-8").read().split("\n")
    blocks = []
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        s = line.strip()
        if not s:
            i += 1
            continue
        if s == "[[DEBRIEF]]":
            blocks.append(("debrief", ""))
            i += 1
            continue
        if s.startswith("## "):
            blocks.append(("chapter", s[3:].strip()))
            i += 1
            continue
        if set(s) <= set("*") and len(s) >= 3:
            blocks.append(("hr", ""))
            i += 1
            continue
        if s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                if not is_table_sep(lines[i]):
                    rows.append(table_cells(lines[i]))
                i += 1
            blocks.append(("table", rows))
            continue
        if s.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            blocks.append(("quote", " ".join(buf)))
            continue
        if s.startswith("### "):
            blocks.append(("h3", s.lstrip("#").strip()))
            i += 1
            continue
        if re.match(r"^\*\*[^*]+\*\*$", s):
            body = s.strip("*").strip()
            blocks.append(("subhead" if len(body) <= 120 else "boldline", body))
            i += 1
            continue
        if re.match(r"^(\d+[.)]|[\u06F0-\u06F9]+[.)]|[\u0660-\u0669]+[.)])\s", s):
            blocks.append(("lead", s))
            i += 1
            continue
        if s.startswith("- "):
            blocks.append(("bullet", s[2:].strip()))
            i += 1
            continue
        buf = [s]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if (not nxt or nxt.startswith("|") or nxt.startswith("> ")
                    or nxt.startswith("## ") or nxt.startswith("### ")
                    or nxt == "[[DEBRIEF]]"
                    or re.match(r"^\*\*[^*]+\*\*$", nxt)
                    or (set(nxt) <= set("*") and len(nxt) >= 3)):
                break
            buf.append(nxt)
            i += 1
        blocks.append(("para", " ".join(buf)))
    return blocks


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    pdf = Book()

    # صفحهٔ عنوان
    pdf.add_page()
    hero = os.path.join(ASSET_DIR, "hero-night-shift.jpg")
    if os.path.exists(hero):
        try:
            pdf.image(hero, x=pdf.l_margin, y=18, w=pdf.epw)
            pdf.set_y(18 + pdf.epw * 0.62 + 8)
        except Exception:
            pdf.set_y(40)
    else:
        pdf.set_y(60)
    pdf.set_font("Vazir", "B", 30)
    pdf.set_text_color(*ACCENT)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(pdf.epw, 14, "آمپولِ نهم", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Vazir", "", 12.5)
    pdf.set_text_color(*AMBER)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(pdf.epw, 8, "داستانی برای یادگرفتنِ داروشناسی — از دو جزوهٔ دکتر فروتن",
                   align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Vazir", "", 10)
    pdf.set_text_color(*DIM)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(pdf.epw, 6.5,
                   "شانزده صحنه در یک شبِ شیفت · هر شماره یا جمله‌ای که به دارو مربوط است، عیناً از متنِ "
                   "دو جزوه گرفته شده است. ضمیمهٔ پایانی، رونوشتِ صفحه‌به‌صفحهٔ هر دو جزوه است تا بشود "
                   "هربار مقابله کرد.",
                   align="C", new_x="LMARGIN", new_y="NEXT")

    # فهرست
    pdf.add_page()
    pdf.running = "فهرست"
    pdf.subhead("فهرست")
    for n in range(1, limit + 1):
        p = os.path.join(STORY_DIR, f"part{n}.md")
        blocks = read_blocks(p)
        ch = next((b[1] for b in blocks if b[0] == "chapter"), None)
        if ch is None:
            chat = [b[1] for b in blocks if b[0] == "para"]
            ch = chat[0][:80] if chat else f"بخشِ {n}"
        pdf.set_font("Vazir", "", 10.5)
        pdf.set_text_color(*INK)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(pdf.epw, 7, ch, align="R", markdown=True,
                       new_x="LMARGIN", new_y="NEXT")

    for n in range(1, limit + 1):
        path = os.path.join(STORY_DIR, f"part{n}.md")
        blocks = read_blocks(path)
        started = False
        for kind, payload in blocks:
            if kind == "table" and not started:
                pass
            if kind == "chapter":
                pdf.chapter(payload)
                started = True
            elif kind == "subhead":
                pdf.subhead(payload)
            elif kind == "h3":
                pdf.h3(payload)
            elif kind == "boldline":
                pdf.body_bold(payload)
            elif kind == "para":
                if not started:
                    pdf.chapter(f"بخشِ {n}")
                    started = True
                pdf.para(payload)
            elif kind == "debrief":
                pdf.running = "دِبریفِ همان صحنه — مرورِ نکته‌های جزوه"
                pdf.add_page()
                pdf.subhead("دِبریفِ همین صحنه — هر نکته، عیناً از جزوه")
            elif kind == "quote":
                if not started:
                    pdf.chapter(f"بخشِ {n}")
                    started = True
                pdf.quote(payload)
            elif kind == "table":
                if not started:
                    pdf.chapter(f"بخشِ {n}")
                    started = True
                pdf.render_table(payload)
            elif kind == "lead":
                if not started:
                    pdf.chapter(f"بخشِ {n}")
                    started = True
                pdf.para(payload, indent=5, align="R")
            elif kind == "bullet":
                if not started:
                    pdf.chapter(f"بخشِ {n}")
                    started = True
                pdf.bullet(payload)
            elif kind == "hr":
                pdf.hr()

    pdf.output(OUT_PATH)
    print(f"wrote {OUT_PATH} ({os.path.getsize(OUT_PATH)} bytes, {pdf.page_no()} pages)")


if __name__ == "__main__":
    main()
