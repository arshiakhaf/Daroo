# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, "/home/user/Daroo/py_modules")
import os
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import page_data_part1, page_data_part2, page_data_part3

FONT_REG = 'VazirFull'
FONT_BOLD = 'VazirFull-Bold'
pdfmetrics.registerFont(TTFont(FONT_REG, '/home/user/Daroo/fonts/VazirmatnFull-400.ttf'))
pdfmetrics.registerFont(TTFont(FONT_BOLD, '/home/user/Daroo/fonts/VazirmatnFull-700.ttf'))

PAGE_W, PAGE_H = A4
LEFT_M = 38
RIGHT_M = PAGE_W - 38
PRINT_W = RIGHT_M - LEFT_M

def fa(text):
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

def wrap_text_fa(text, font_name, font_size, max_w):
    words = text.split()
    lines = []
    curr = []
    for w in words:
        test_line = " ".join(curr + [w])
        reshaped = arabic_reshaper.reshape(test_line)
        width = pdfmetrics.stringWidth(reshaped, font_name, font_size)
        if width <= max_w:
            curr.append(w)
        else:
            if curr:
                lines.append(" ".join(curr))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))
    return lines

class Master20PagePDF:
    def __init__(self, filename):
        self.c = canvas.Canvas(filename, pagesize=A4)
        self.filename = filename

    def draw_header(self, page_num, section_text):
        c = self.c
        c.saveState()
        # Top banner line
        c.setFillColor(colors.HexColor('#0f172a'))
        c.rect(LEFT_M, PAGE_H - 35, PRINT_W, 2, fill=1, stroke=0)
        
        # Right: section text
        c.setFont(FONT_BOLD, 8)
        c.setFillColor(colors.HexColor('#0284c7'))
        c.drawRightString(RIGHT_M, PAGE_H - 28, fa(section_text))
        
        # Left: book title
        c.setFont(FONT_REG, 8)
        c.setFillColor(colors.HexColor('#64748b'))
        c.drawString(LEFT_M, PAGE_H - 28, fa("درسنامه راهبردی داروشناسی — استاد فروتن"))
        c.restoreState()

    def draw_footer(self, page_num):
        c = self.c
        c.saveState()
        # Separator
        c.setStrokeColor(colors.HexColor('#cbd5e1'))
        c.setLineWidth(0.75)
        c.line(LEFT_M, 38, RIGHT_M, 38)
        
        # Center: page number
        c.setFont(FONT_BOLD, 8.5)
        c.setFillColor(colors.HexColor('#334155'))
        c.drawCentredString(PAGE_W / 2.0, 24, fa(f"صفحه {page_num} از ۲۰"))
        
        # Right: subnote
        c.setFont(FONT_REG, 7.5)
        c.setFillColor(colors.HexColor('#94a3b8'))
        c.drawRightString(RIGHT_M, 24, fa("مرور جامع و تفکیکی دو جزوه: مامایی و قلب و عروق"))
        
        # Left: key note
        c.drawString(LEFT_M, 24, fa("منطبق بر آزمون ۴۰ سوالی پایانی"))
        c.restoreState()

    def render_page_1(self):
        c = self.c
        p = page_data_part1.page1_data
        
        # Background dark blue card at top
        c.setFillColor(colors.HexColor('#0f172a'))
        c.roundRect(LEFT_M, PAGE_H - 200, PRINT_W, 160, 8, fill=1, stroke=0)
        
        # Gold accent stripe
        c.setFillColor(colors.HexColor('#d97706'))
        c.roundRect(LEFT_M + 15, PAGE_H - 55, PRINT_W - 30, 4, 2, fill=1, stroke=0)
        
        # Title
        c.setFont(FONT_BOLD, 17)
        c.setFillColor(colors.white)
        c.drawCentredString(PAGE_W / 2.0, PAGE_H - 85, fa(p["title"]))
        
        # Subtitle
        c.setFont(FONT_BOLD, 11)
        c.setFillColor(colors.HexColor('#38bdf8'))
        c.drawCentredString(PAGE_W / 2.0, PAGE_H - 110, fa(p["subtitle"]))
        
        # Focus note
        c.setFont(FONT_REG, 9)
        c.setFillColor(colors.HexColor('#cbd5e1'))
        c.drawCentredString(PAGE_W / 2.0, PAGE_H - 135, fa(p["exam_focus"]))
        
        # Target audience
        c.setFont(FONT_REG, 8.5)
        c.setFillColor(colors.HexColor('#94a3b8'))
        c.drawCentredString(PAGE_W / 2.0, PAGE_H - 165, fa(p["target_audience"]))
        
        # Box 1: Structure & Roadmap
        cur_y = PAGE_H - 220
        c.setFillColor(colors.HexColor('#f8fafc'))
        c.setStrokeColor(colors.HexColor('#cbd5e1'))
        c.roundRect(LEFT_M, cur_y - 200, PRINT_W, 200, 6, fill=1, stroke=1)
        
        c.setFillColor(colors.HexColor('#0284c7'))
        c.roundRect(LEFT_M + 12, cur_y - 28, PRINT_W - 24, 24, 4, fill=1, stroke=0)
        c.setFont(FONT_BOLD, 10.5)
        c.setFillColor(colors.white)
        c.drawRightString(RIGHT_M - 20, cur_y - 22, fa("ساختار و تفکیک مباحث جزوه ۲۰ صفحه‌ای"))
        
        item_y = cur_y - 50
        for title, desc in p["structure"]:
            c.setFont(FONT_BOLD, 9.5)
            c.setFillColor(colors.HexColor('#0f172a'))
            c.drawRightString(RIGHT_M - 20, item_y, fa(title))
            item_y -= 14
            lines = wrap_text_fa(desc, FONT_REG, 8.5, PRINT_W - 40)
            c.setFont(FONT_REG, 8.5)
            c.setFillColor(colors.HexColor('#334155'))
            for l in lines:
                c.drawRightString(RIGHT_M - 20, item_y, fa(l))
                item_y -= 13
            item_y -= 8
            
        # Box 2: 5 Golden Secrets of Dr. Foroutan
        cur_y = cur_y - 215
        c.setFillColor(colors.HexColor('#fffbeb'))
        c.setStrokeColor(colors.HexColor('#fde68a'))
        c.roundRect(LEFT_M, cur_y - 290, PRINT_W, 290, 6, fill=1, stroke=1)
        
        c.setFillColor(colors.HexColor('#b45309'))
        c.roundRect(LEFT_M + 12, cur_y - 28, PRINT_W - 24, 24, 4, fill=1, stroke=0)
        c.setFont(FONT_BOLD, 10.5)
        c.setFillColor(colors.white)
        c.drawRightString(RIGHT_M - 20, cur_y - 22, fa("۵ راز طلایی و شیوه‌نامه طراح آزمون (دکتر فروتن)"))
        
        sec_y = cur_y - 50
        for sec in p["exam_secrets"]:
            lines = wrap_text_fa(sec, FONT_REG, 8.5, PRINT_W - 40)
            c.setFont(FONT_REG, 8.5)
            c.setFillColor(colors.HexColor('#78350f'))
            for i, l in enumerate(lines):
                if i == 0:
                    c.setFont(FONT_BOLD, 8.5)
                else:
                    c.setFont(FONT_REG, 8.5)
                c.drawRightString(RIGHT_M - 20, sec_y, fa(l))
                sec_y -= 13
            sec_y -= 6

        self.draw_footer(1)
        c.showPage()

    def render_lesson_page(self, page_num, data):
        c = self.c
        self.draw_header(page_num, data["header"])
        
        # Page Title Banner
        c.setFillColor(colors.HexColor('#f1f5f9'))
        c.setStrokeColor(colors.HexColor('#cbd5e1'))
        c.roundRect(LEFT_M, PAGE_H - 72, PRINT_W, 30, 4, fill=1, stroke=1)
        
        # Pill indicator
        c.setFillColor(colors.HexColor('#0284c7'))
        c.rect(RIGHT_M - 6, PAGE_H - 72, 6, 30, fill=1, stroke=0)
        
        c.setFont(FONT_BOLD, 11)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawRightString(RIGHT_M - 15, PAGE_H - 62, fa(data["title"]))
        
        cur_y = PAGE_H - 85
        cards = data["cards"]
        card_count = len(cards)
        
        # Compute dynamic card height or spacing
        # Total usable height for cards = cur_y - 50 (footer) = ~700 pt
        avail_h = cur_y - 48
        # We will render each card neatly
        for idx, card in enumerate(cards):
            content_text = card["content"]
            lines = []
            for raw_line in content_text.split("\n"):
                if raw_line.strip():
                    wrapped = wrap_text_fa(raw_line.strip(), FONT_REG, 8.5, PRINT_W - 28)
                    lines.extend(wrapped)
                else:
                    lines.append("")
            
            # Height required: header (22) + padding (12) + lines * 13
            box_h = 24 + len(lines) * 13.2 + 8
            
            # Card background
            c.setFillColor(colors.HexColor('#f8fafc'))
            c.setStrokeColor(colors.HexColor('#e2e8f0'))
            c.roundRect(LEFT_M, cur_y - box_h, PRINT_W, box_h, 5, fill=1, stroke=1)
            
            # Header pill
            c.setFillColor(colors.HexColor(card["color"]))
            c.roundRect(LEFT_M + 6, cur_y - 20, PRINT_W - 12, 18, 3, fill=1, stroke=0)
            
            c.setFont(FONT_BOLD, 9)
            c.setFillColor(colors.white)
            c.drawRightString(RIGHT_M - 14, cur_y - 15, fa(card["tag"]))
            
            # Body text
            text_y = cur_y - 34
            c.setFont(FONT_REG, 8.5)
            c.setFillColor(colors.HexColor('#1e293b'))
            for l in lines:
                if l.startswith("•"):
                    c.setFont(FONT_BOLD, 8.5)
                    c.setFillColor(colors.HexColor('#0f172a'))
                else:
                    c.setFont(FONT_REG, 8.5)
                    c.setFillColor(colors.HexColor('#334155'))
                c.drawRightString(RIGHT_M - 14, text_y, fa(l))
                text_y -= 13.2
            
            cur_y -= (box_h + 8)

        self.draw_footer(page_num)
        c.showPage()

    def render_page_16(self):
        c = self.c
        data = page_data_part3.page16_data
        self.draw_header(16, data["header"])
        
        # Title banner
        c.setFillColor(colors.HexColor('#f1f5f9'))
        c.setStrokeColor(colors.HexColor('#cbd5e1'))
        c.roundRect(LEFT_M, PAGE_H - 72, PRINT_W, 30, 4, fill=1, stroke=1)
        c.setFillColor(colors.HexColor('#d97706'))
        c.rect(RIGHT_M - 6, PAGE_H - 72, 6, 30, fill=1, stroke=0)
        c.setFont(FONT_BOLD, 11)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawRightString(RIGHT_M - 15, PAGE_H - 62, fa(data["title"]))
        
        cur_y = PAGE_H - 85
        for card in data["analysis_cards"]:
            content_text = card["content"]
            lines = []
            for raw_line in content_text.split("\n"):
                if raw_line.strip():
                    wrapped = wrap_text_fa(raw_line.strip(), FONT_REG, 8.5, PRINT_W - 28)
                    lines.extend(wrapped)
            box_h = 24 + len(lines) * 14 + 10
            
            c.setFillColor(colors.HexColor('#f8fafc'))
            c.setStrokeColor(colors.HexColor('#e2e8f0'))
            c.roundRect(LEFT_M, cur_y - box_h, PRINT_W, box_h, 5, fill=1, stroke=1)
            
            c.setFillColor(colors.HexColor(card["color"]))
            c.roundRect(LEFT_M + 6, cur_y - 20, PRINT_W - 12, 18, 3, fill=1, stroke=0)
            
            c.setFont(FONT_BOLD, 9.5)
            c.setFillColor(colors.white)
            c.drawRightString(RIGHT_M - 14, cur_y - 15, fa(card["tag"]))
            
            text_y = cur_y - 36
            for l in lines:
                if l.startswith("•") or (len(l) > 2 and l[0] in "۱۲۳۴۵۶۷" and l[1] == "."):
                    c.setFont(FONT_BOLD, 8.5)
                    c.setFillColor(colors.HexColor('#0f172a'))
                else:
                    c.setFont(FONT_REG, 8.5)
                    c.setFillColor(colors.HexColor('#334155'))
                c.drawRightString(RIGHT_M - 14, text_y, fa(l))
                text_y -= 14
            
            cur_y -= (box_h + 10)

        self.draw_footer(16)
        c.showPage()

    def render_simulation_page(self, page_num, data):
        c = self.c
        self.draw_header(page_num, data["header"])
        
        # Title banner
        c.setFillColor(colors.HexColor('#f8fafc'))
        c.setStrokeColor(colors.HexColor('#cbd5e1'))
        c.roundRect(LEFT_M, PAGE_H - 68, PRINT_W, 26, 4, fill=1, stroke=1)
        c.setFillColor(colors.HexColor('#059669'))
        c.rect(RIGHT_M - 6, PAGE_H - 68, 6, 26, fill=1, stroke=0)
        c.setFont(FONT_BOLD, 10)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawRightString(RIGHT_M - 15, PAGE_H - 59, fa(data["title"]))
        
        cur_y = PAGE_H - 76
        
        questions = data["questions"]
        # Render 10 questions per page
        for q_text, opts, ans, exp in questions:
            # Box height budget: question (12) + options (11) + answer (11) = ~48 pt
            q_lines = wrap_text_fa(q_text, FONT_BOLD, 8, PRINT_W - 16)
            exp_lines = wrap_text_fa("استدلال: " + exp, FONT_REG, 7.5, PRINT_W - 90)
            
            q_box_h = 8 + len(q_lines) * 11 + 24 + len(exp_lines) * 10.5 + 4
            
            # Subtle card
            c.setFillColor(colors.HexColor('#ffffff'))
            c.setStrokeColor(colors.HexColor('#e2e8f0'))
            c.roundRect(LEFT_M, cur_y - q_box_h, PRINT_W, q_box_h, 4, fill=1, stroke=1)
            
            # Left accent dot
            c.setFillColor(colors.HexColor('#059669'))
            c.circle(LEFT_M + 8, cur_y - 10, 2.5, fill=1, stroke=0)
            
            # Question line
            c.setFont(FONT_BOLD, 8)
            c.setFillColor(colors.HexColor('#0f172a'))
            text_y = cur_y - 11
            for ql in q_lines:
                c.drawRightString(RIGHT_M - 10, text_y, fa(ql))
                text_y -= 11
            
            # Options in 2x2 symmetric grid (2 rows x 2 columns)
            c.setFont(FONT_REG, 7.5)
            c.setFillColor(colors.HexColor('#334155'))
            opt_y = text_y - 2
            if len(opts) == 4:
                # Row 1: Opt 0 (Right) and Opt 1 (Left)
                c.drawRightString(RIGHT_M - 14, opt_y, fa(opts[0]))
                c.drawRightString(RIGHT_M - 265, opt_y, fa(opts[1]))
                opt_y -= 11
                # Row 2: Opt 2 (Right) and Opt 3 (Left)
                c.drawRightString(RIGHT_M - 14, opt_y, fa(opts[2]))
                c.drawRightString(RIGHT_M - 265, opt_y, fa(opts[3]))
                opt_y -= 11
            text_y = opt_y - 2
            
            # Answer badge & explanation
            # Badge
            c.setFillColor(colors.HexColor('#ecfdf5'))
            c.setStrokeColor(colors.HexColor('#a7f3d0'))
            c.roundRect(RIGHT_M - 70, text_y - 9, 62, 13, 3, fill=1, stroke=1)
            c.setFont(FONT_BOLD, 7.5)
            c.setFillColor(colors.HexColor('#047857'))
            c.drawCentredString(RIGHT_M - 39, text_y - 6, fa(f"کلید: گزینه {ans}"))
            
            # Explanation
            c.setFont(FONT_REG, 7.5)
            c.setFillColor(colors.HexColor('#475569'))
            ey = text_y - 5
            for el in exp_lines:
                c.drawRightString(RIGHT_M - 76, ey, fa(el))
                ey -= 10
            
            cur_y -= (q_box_h + 4)
            
        if "gold_summary" in data:
            # Draw summary card on remaining space
            remain_h = cur_y - 45
            if remain_h > 35:
                c.setFillColor(colors.HexColor('#eff6ff'))
                c.setStrokeColor(colors.HexColor('#bfdbfe'))
                c.roundRect(LEFT_M, cur_y - remain_h, PRINT_W, remain_h, 4, fill=1, stroke=1)
                
                c.setFont(FONT_BOLD, 8)
                c.setFillColor(colors.HexColor('#1d4ed8'))
                sy = cur_y - 12
                c.drawRightString(RIGHT_M - 10, sy, fa(data["gold_summary"][0]))
                sy -= 11
                c.setFont(FONT_REG, 7)
                c.setFillColor(colors.HexColor('#1e40af'))
                for g_line in data["gold_summary"][1:]:
                    if sy > 48:
                        c.drawRightString(RIGHT_M - 10, sy, fa(g_line))
                        sy -= 9.5

        self.draw_footer(page_num)
        c.showPage()

    def build_all(self):
        print("Rendering Page 1 (Cover & Roadmap)...")
        self.render_page_1()
        
        # Pages 2 to 9: Part 1
        part1_pages = [
            page_data_part1.page2_data,
            page_data_part1.page3_data,
            page_data_part1.page4_data,
            page_data_part1.page5_data,
            page_data_part1.page6_data,
            page_data_part1.page7_data,
            page_data_part1.page8_data,
            page_data_part1.page9_data,
        ]
        for idx, pdata in enumerate(part1_pages):
            pnum = idx + 2
            print(f"Rendering Page {pnum} (Part 1 - Cardio)...")
            self.render_lesson_page(pnum, pdata)
            
        # Pages 10 to 15: Part 2
        part2_pages = [
            page_data_part2.page10_data,
            page_data_part2.page11_data,
            page_data_part2.page12_data,
            page_data_part2.page13_data,
            page_data_part2.page14_data,
            page_data_part2.page15_data,
        ]
        for idx, pdata in enumerate(part2_pages):
            pnum = idx + 10
            print(f"Rendering Page {pnum} (Part 2 - Midwifery)...")
            self.render_lesson_page(pnum, pdata)
            
        # Page 16: Analysis
        print("Rendering Page 16 (Exam Analysis & Secrets)...")
        self.render_page_16()
        
        # Pages 17 to 20: 40 Simulation Questions
        sim_pages = [
            page_data_part3.page17_data,
            page_data_part3.page18_data,
            page_data_part3.page19_data,
            page_data_part3.page20_data,
        ]
        for idx, pdata in enumerate(sim_pages):
            pnum = idx + 17
            print(f"Rendering Page {pnum} (Simulation Questions)...")
            self.render_simulation_page(pnum, pdata)
            
        self.c.save()
        print(f"Master 20-Page PDF saved successfully: {self.filename}")

if __name__ == '__main__':
    pdf_out = "خلاصه_جامع_۲۰_صفحه_ای_داروشناسی_دو_جزوه.pdf"
    builder = Master20PagePDF(pdf_out)
    builder.build_all()
