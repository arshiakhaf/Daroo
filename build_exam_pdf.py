# -*- coding: utf-8 -*-
import os
import sys
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from generate_exam_solutions import questions_data

FONT_REGULAR = 'VazirFull'
FONT_BOLD = 'VazirFull-Bold'
pdfmetrics.registerFont(TTFont(FONT_REGULAR, '/home/user/Daroo/fonts/VazirmatnFull-400.ttf'))
pdfmetrics.registerFont(TTFont(FONT_BOLD, '/home/user/Daroo/fonts/VazirmatnFull-700.ttf'))

PAGE_WIDTH, PAGE_HEIGHT = A4
TOP_MARGIN = 50
BOTTOM_MARGIN = 50
LEFT_MARGIN = 45
RIGHT_MARGIN = 550
PRINTABLE_WIDTH = RIGHT_MARGIN - LEFT_MARGIN

def fa(text):
    if not text:
        return ""
    # Ensure no None or weird types
    s = str(text)
    reshaped = arabic_reshaper.reshape(s)
    return get_display(reshaped)

def wrap_text_fa(text, font_name, font_size, max_w):
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        reshaped = arabic_reshaper.reshape(test_line)
        w = pdfmetrics.stringWidth(reshaped, font_name, font_size)
        if w <= max_w:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

class ExamSolutionsPDF:
    def __init__(self, filename):
        self.filename = filename
        self.c = canvas.Canvas(filename, pagesize=A4)
        self.page_num = 0
        self.current_y = PAGE_HEIGHT - TOP_MARGIN
        self.is_cover = False

    def start_new_page(self, is_cover=False):
        if self.page_num > 0 and not self.is_cover:
            self.draw_footer()
        if self.page_num > 0:
            self.c.showPage()
            
        self.page_num += 1
        self.is_cover = is_cover
        self.current_y = PAGE_HEIGHT - TOP_MARGIN
        
        if not is_cover:
            self.draw_header()

    def draw_header(self):
        c = self.c
        c.saveState()
        c.setFont(FONT_REGULAR, 8.5)
        c.setFillColor(colors.HexColor('#475569'))
        
        # Right title
        header_text = fa("پاسخنامه تشریحی سوالات داروشناسی — استاد فروتن")
        c.drawRightString(RIGHT_MARGIN, PAGE_HEIGHT - 32, header_text)
        
        # Left topic
        sub_text = fa("آزمون پایانی کلاسی (۴۰ سوال تستی)")
        c.drawString(LEFT_MARGIN, PAGE_HEIGHT - 32, sub_text)
        
        # Separator line
        c.setStrokeColor(colors.HexColor('#cbd5e1'))
        c.setLineWidth(0.75)
        c.line(LEFT_MARGIN, PAGE_HEIGHT - 38, RIGHT_MARGIN, PAGE_HEIGHT - 38)
        c.restoreState()
        self.current_y = PAGE_HEIGHT - TOP_MARGIN - 5

    def draw_footer(self):
        if self.is_cover:
            return
        c = self.c
        c.saveState()
        
        # Separator line
        c.setStrokeColor(colors.HexColor('#e2e8f0'))
        c.setLineWidth(0.5)
        c.line(LEFT_MARGIN, BOTTOM_MARGIN + 16, RIGHT_MARGIN, BOTTOM_MARGIN + 16)
        
        # Page number centered
        c.setFont(FONT_REGULAR, 9)
        c.setFillColor(colors.HexColor('#64748b'))
        page_str = fa(f"صفحه {self.page_num}")
        c.drawCentredString(PAGE_WIDTH / 2.0, BOTTOM_MARGIN, page_str)
        
        # Bottom left watermark note
        note_str = fa("داروشناسی کاربردی | منطبق با تدریس استاد فروتن")
        c.drawString(LEFT_MARGIN, BOTTOM_MARGIN, note_str)
        
        c.restoreState()

    def ensure_space(self, required_h):
        if self.current_y - required_h < BOTTOM_MARGIN + 25:
            self.start_new_page()

    def draw_cover(self):
        self.start_new_page(is_cover=True)
        c = self.c
        c.saveState()
        
        # Deep Indigo/Navy Top Banner
        c.setFillColor(colors.HexColor('#1e293b'))
        c.rect(0, PAGE_HEIGHT - 260, PAGE_WIDTH, 260, fill=1, stroke=0)
        
        # Gold Accent Line
        c.setFillColor(colors.HexColor('#d97706'))
        c.rect(0, PAGE_HEIGHT - 266, PAGE_WIDTH, 6, fill=1, stroke=0)
        
        # Outer Border
        c.setStrokeColor(colors.HexColor('#cbd5e1'))
        c.setLineWidth(1)
        c.rect(LEFT_MARGIN - 15, BOTTOM_MARGIN - 15, PRINTABLE_WIDTH + 30, PAGE_HEIGHT - (BOTTOM_MARGIN + TOP_MARGIN) + 30)
        
        # Inner Gold Border
        c.setStrokeColor(colors.HexColor('#f59e0b'))
        c.setLineWidth(0.5)
        c.rect(LEFT_MARGIN - 10, BOTTOM_MARGIN - 10, PRINTABLE_WIDTH + 20, PAGE_HEIGHT - (BOTTOM_MARGIN + TOP_MARGIN) + 20)
        
        # Top Banner Titles
        c.setFont(FONT_BOLD, 14)
        c.setFillColor(colors.HexColor('#fbbf24'))
        c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 75, fa("دانشگاه علوم پزشکی — گروه آموزشی داروشناسی"))
        
        c.setFont(FONT_BOLD, 22)
        c.setFillColor(colors.white)
        c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 125, fa("پاسخنامه تشریحی و تحلیلی آزمون داروشناسی"))
        
        c.setFont(FONT_BOLD, 15)
        c.setFillColor(colors.HexColor('#93c5fd'))
        c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 165, fa("تحلیل موشکافانه ۴۰ سوال آزمون پایانی کلاسی استاد فروتن"))
        
        c.setFont(FONT_REGULAR, 11)
        c.setFillColor(colors.HexColor('#e2e8f0'))
        c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 205, fa("ویژه دانشجویان مامایی، پرستاری، هوشبری و فوریت‌های پزشکی"))

        c.setFont(FONT_REGULAR, 10)
        c.setFillColor(colors.HexColor('#cbd5e1'))
        c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 235, fa("استاد دوره: جناب آقای دکتر فروتن  |  نگارش جامع و تشریحی"))

        # Main Body Features Card
        card_y = PAGE_HEIGHT - 310
        card_w = PRINTABLE_WIDTH
        card_h = 240
        c.setFillColor(colors.HexColor('#f8fafc'))
        c.setStrokeColor(colors.HexColor('#e2e8f0'))
        c.setLineWidth(1)
        c.roundRect(LEFT_MARGIN, card_y - card_h, card_w, card_h, 8, fill=1, stroke=1)
        
        c.setFont(FONT_BOLD, 13)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawRightString(RIGHT_MARGIN - 20, card_y - 30, fa("ویژگی‌های انحصاری این پاسخنامه:"))
        
        features = [
            "پوشش کامل ۱۰۰ درصدی تمام ۴۰ سوال آزمون تستی کلاسی استاد فروتن",
            "تحلیل گام‌به‌گام و فیزیوپاتولوژیک تمام گزینه‌ها به همراه علت دقیق رد گزینه‌های نادرست",
            "استخراج مرواریدهای طلایی امتحانی و کدهای حفظی سریع برای جمع‌بندی پیش از آزمون",
            "تطبیق مو‌به‌مو با سرفصل‌های دو جزوه مرجع مامایی و کارشناسی قلب و عروق استاد فروتن",
            "جدول کلید سریع تستی در ابتدای کتابچه جهت خودآزمایی و تورق سریع در ۵ دقیقه",
            "پرهیز کامل از هرگونه ابهام با تفکیک دقیق دوزها، مکانیسم‌ها، عوارض و منع مصرف‌های بالینی"
        ]
        
        feat_y = card_y - 65
        for feat in features:
            c.setFont(FONT_BOLD, 11)
            c.setFillColor(colors.HexColor('#2563eb'))
            c.drawRightString(RIGHT_MARGIN - 25, feat_y, fa("•"))
            
            c.setFont(FONT_REGULAR, 10)
            c.setFillColor(colors.HexColor('#334155'))
            c.drawRightString(RIGHT_MARGIN - 42, feat_y, fa(feat))
            feat_y -= 28

        # Bottom Info Box
        info_y = card_y - card_h - 40
        c.setFillColor(colors.HexColor('#eff6ff'))
        c.setStrokeColor(colors.HexColor('#bfdbfe'))
        c.roundRect(LEFT_MARGIN, info_y - 70, card_w, 70, 6, fill=1, stroke=1)
        
        c.setFont(FONT_BOLD, 10.5)
        c.setFillColor(colors.HexColor('#1e40af'))
        c.drawCentredString(PAGE_WIDTH / 2.0, info_y - 25, fa("راهنمای مطالعه:"))
        c.setFont(FONT_REGULAR, 9.5)
        c.setFillColor(colors.HexColor('#1e3a8a'))
        c.drawCentredString(PAGE_WIDTH / 2.0, info_y - 45, fa("ابتدا از روی جدول کلید سریع خود را بسنجید، سپس به تحلیل تشریحی و مرواریدهای طلایی مراجعه فرمایید."))

        # Footer date
        c.setFont(FONT_REGULAR, 9)
        c.setFillColor(colors.HexColor('#94a3b8'))
        c.drawCentredString(PAGE_WIDTH / 2.0, BOTTOM_MARGIN + 10, fa("نگارش و تنظیم نهایی: مهرماه ۱۴۰۵ — نسخه چاپی ویژه دانشجویان"))
        
        c.restoreState()

    def draw_quick_key_table(self):
        self.start_new_page()
        c = self.c
        c.saveState()
        
        # Section Title
        c.setFont(FONT_BOLD, 14)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawRightString(RIGHT_MARGIN, self.current_y, fa("جدول کلید سریع پاسخ‌های آزمون (در یک نگاه)"))
        
        self.current_y -= 18
        c.setFont(FONT_REGULAR, 9.5)
        c.setFillColor(colors.HexColor('#64748b'))
        c.drawRightString(RIGHT_MARGIN, self.current_y, fa("جهت خودآزمایی و مرور سریع پاسخ‌های ۴۰ سوال پیش از ورود به جلسه آزمون:"))
        
        self.current_y -= 25
        
        # We build two parallel tables side by side:
        # Col 1 (Questions 1 to 20): left half of page
        # Col 2 (Questions 21 to 40): right half of page
        table_w = (PRINTABLE_WIDTH - 20) / 2.0
        row_h = 22.5
        header_h = 26
        
        letters = ["الف", "ب", "ج", "د"]
        
        cols = [
            {"title": "بخش اول: سوالات ۱ تا ۲۰", "x": LEFT_MARGIN + table_w + 20, "items": questions_data[:20]},
            {"title": "بخش دوم: سوالات ۲۱ تا ۴۰", "x": LEFT_MARGIN, "items": questions_data[20:]}
        ]
        
        table_top_y = self.current_y
        
        for col_data in cols:
            bx = col_data["x"]
            by = table_top_y
            
            # Draw Column Header
            c.setFillColor(colors.HexColor('#1e293b'))
            c.rect(bx, by - header_h, table_w, header_h, fill=1, stroke=0)
            
            c.setFont(FONT_BOLD, 9.5)
            c.setFillColor(colors.white)
            c.drawCentredString(bx + table_w / 2.0, by - 17, fa(col_data["title"]))
            
            curr_row_y = by - header_h
            
            for idx, q in enumerate(col_data["items"]):
                # Alternating row background
                bg_color = colors.HexColor('#f8fafc') if idx % 2 == 0 else colors.white
                c.setFillColor(bg_color)
                c.setStrokeColor(colors.HexColor('#e2e8f0'))
                c.setLineWidth(0.5)
                c.rect(bx, curr_row_y - row_h, table_w, row_h, fill=1, stroke=1)
                
                # Question Number Box on right edge
                c.setFont(FONT_BOLD, 8.5)
                c.setFillColor(colors.HexColor('#334155'))
                c.drawRightString(bx + table_w - 6, curr_row_y - 15, fa(f"سوال {q['id']}"))
                
                # Correct Option Pill
                corr_opt = letters[q["correct_idx"]]
                c.setFillColor(colors.HexColor('#dcfce7'))
                c.setStrokeColor(colors.HexColor('#86efac'))
                c.roundRect(bx + table_w - 68, curr_row_y - 18, 24, 14, 3, fill=1, stroke=1)
                
                c.setFont(FONT_BOLD, 8.5)
                c.setFillColor(colors.HexColor('#166534'))
                c.drawCentredString(bx + table_w - 56, curr_row_y - 14, fa(corr_opt))
                
                # Correct Name
                name_short = q["options"][q["correct_idx"]]
                if len(name_short) > 26:
                    name_short = name_short[:24] + "..."
                c.setFont(FONT_REGULAR, 8)
                c.setFillColor(colors.HexColor('#0f172a'))
                c.drawRightString(bx + table_w - 74, curr_row_y - 15, fa(name_short))
                
                curr_row_y -= row_h
        
        c.restoreState()
        self.current_y = table_top_y - header_h - (20 * row_h) - 30

    def draw_question_item(self, q):
        c = self.c
        letters = ["الف", "ب", "ج", "د"]
        
        # Estimate heights
        header_h = 24
        
        stem_lines = wrap_text_fa(q["question"], FONT_BOLD, 10, PRINTABLE_WIDTH - 24)
        stem_h = len(stem_lines) * 16 + 14
        
        options_h = 4 * 20 + 8
        
        exp_lines = wrap_text_fa(q["explanation"], FONT_REGULAR, 9, PRINTABLE_WIDTH - 24)
        exp_h = len(exp_lines) * 14 + 20
        
        pearl_lines = wrap_text_fa(q["pearl"], FONT_REGULAR, 8.5, PRINTABLE_WIDTH - 28)
        pearl_h = len(pearl_lines) * 13 + 16
        
        total_q_h = header_h + stem_h + options_h + exp_h + pearl_h + 20
        
        self.ensure_space(total_q_h)
        
        c.saveState()
        
        # 1. Question Top Header Bar
        c.setFillColor(colors.HexColor('#0f172a'))
        c.roundRect(LEFT_MARGIN, self.current_y - header_h, PRINTABLE_WIDTH, header_h, 4, fill=1, stroke=0)
        
        c.setFont(FONT_BOLD, 10)
        c.setFillColor(colors.HexColor('#fbbf24'))
        q_num_str = fa(f"سوال شماره {q['id']}")
        c.drawRightString(RIGHT_MARGIN - 12, self.current_y - 16, q_num_str)
        
        c.setFont(FONT_REGULAR, 8.5)
        c.setFillColor(colors.HexColor('#e2e8f0'))
        topic_str = fa(f"مبحث: {q['topic']}")
        c.drawString(LEFT_MARGIN + 12, self.current_y - 16, topic_str)
        
        self.current_y -= header_h + 3
        
        # 2. Question Stem Box
        c.setFillColor(colors.HexColor('#f1f5f9'))
        c.setStrokeColor(colors.HexColor('#cbd5e1'))
        c.setLineWidth(0.6)
        c.roundRect(LEFT_MARGIN, self.current_y - stem_h, PRINTABLE_WIDTH, stem_h, 4, fill=1, stroke=1)
        
        c.setFont(FONT_BOLD, 9.5)
        c.setFillColor(colors.HexColor('#1e293b'))
        line_y = self.current_y - 16
        for sline in stem_lines:
            c.drawRightString(RIGHT_MARGIN - 12, line_y, fa(sline))
            line_y -= 16
            
        self.current_y -= stem_h + 4
        
        # 3. Four Options Box
        opt_box_h = 4 * 19 + 6
        c.setFillColor(colors.white)
        c.setStrokeColor(colors.HexColor('#e2e8f0'))
        c.setLineWidth(0.5)
        c.roundRect(LEFT_MARGIN, self.current_y - opt_box_h, PRINTABLE_WIDTH, opt_box_h, 4, fill=1, stroke=1)
        
        opt_y = self.current_y - 15
        for i, opt in enumerate(q["options"]):
            is_correct = (i == q["correct_idx"])
            if is_correct:
                # Highlight correct row
                c.setFillColor(colors.HexColor('#ecfdf5'))
                c.setStrokeColor(colors.HexColor('#a7f3d0'))
                c.setLineWidth(0.6)
                c.roundRect(LEFT_MARGIN + 4, opt_y - 4, PRINTABLE_WIDTH - 8, 18, 3, fill=1, stroke=1)
                
                # Tag
                c.setFillColor(colors.HexColor('#059669'))
                c.setFont(FONT_BOLD, 8.5)
                c.drawString(LEFT_MARGIN + 12, opt_y + 1, fa("[پاسخ صحیح]"))
                
                c.setFont(FONT_BOLD, 9)
                c.setFillColor(colors.HexColor('#065f46'))
            else:
                c.setFont(FONT_REGULAR, 8.5)
                c.setFillColor(colors.HexColor('#475569'))
                
            opt_str = fa(f"{letters[i]}) {opt}")
            c.drawRightString(RIGHT_MARGIN - 14, opt_y + 1, opt_str)
            opt_y -= 19
            
        self.current_y -= opt_box_h + 4
        
        # 4. Clinical Explanation Box
        c.setFillColor(colors.HexColor('#f8fafc'))
        c.setStrokeColor(colors.HexColor('#cbd5e1'))
        c.setLineWidth(0.6)
        c.roundRect(LEFT_MARGIN, self.current_y - exp_h, PRINTABLE_WIDTH, exp_h, 4, fill=1, stroke=1)
        
        c.setFont(FONT_BOLD, 8.5)
        c.setFillColor(colors.HexColor('#0284c7'))
        c.drawRightString(RIGHT_MARGIN - 12, self.current_y - 13, fa("استدلال بالینی و فارماکولوژیک:"))
        
        c.setFont(FONT_REGULAR, 8.5)
        c.setFillColor(colors.HexColor('#334155'))
        exp_line_y = self.current_y - 27
        for eline in exp_lines:
            c.drawRightString(RIGHT_MARGIN - 12, exp_line_y, fa(eline))
            exp_line_y -= 14
            
        self.current_y -= exp_h + 4
        
        # 5. Golden Pearl Box
        c.setFillColor(colors.HexColor('#fffbeb'))
        c.setStrokeColor(colors.HexColor('#fde68a'))
        c.setLineWidth(0.7)
        c.roundRect(LEFT_MARGIN, self.current_y - pearl_h, PRINTABLE_WIDTH, pearl_h, 4, fill=1, stroke=1)
        
        c.setFont(FONT_BOLD, 8)
        c.setFillColor(colors.HexColor('#b45309'))
        c.drawRightString(RIGHT_MARGIN - 12, self.current_y - 12, fa("نکته کلیدی و مروارید امتحانی دکتر فروتن:"))
        
        c.setFont(FONT_REGULAR, 8)
        c.setFillColor(colors.HexColor('#78350f'))
        pearl_line_y = self.current_y - 24
        for pline in pearl_lines:
            c.drawRightString(RIGHT_MARGIN - 12, pearl_line_y, fa(pline))
            pearl_line_y -= 13
            
        self.current_y -= pearl_h + 16
        
        c.restoreState()

    def draw_statistical_summary(self):
        self.start_new_page()
        c = self.c
        c.saveState()
        
        # Title
        c.setFont(FONT_BOLD, 14)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawRightString(RIGHT_MARGIN, self.current_y, fa("تحلیل آماری و دسته‌بندی بودجه‌بندی سوالات آزمون"))
        
        self.current_y -= 20
        c.setFont(FONT_REGULAR, 9.5)
        c.setFillColor(colors.HexColor('#475569'))
        c.drawRightString(RIGHT_MARGIN, self.current_y, fa("توزیع مباحث امتحانی در آزمون ۴۰ سوالی پایانی بر اساس سرفصل‌های تدریس دکتر فروتن:"))
        
        self.current_y -= 30
        
        stats = [
            {"topic": "فارماکولوژی عمومی (فارماکوکینتیک، دینامیک، گیرنده‌ها و متابولیسم)", "count": "۷ سوال", "percent": "۱۷.۵ ٪", "questions": "۵، ۶، ۱۵، ۲۱، ۲۸، ۳۸، ۴۰", "color": "#3b82f6"},
            {"topic": "قلب و عروق، نارسایی قلبی، ضد آریتمی و کنترل فشار خون", "count": "۹ سوال", "percent": "۲۲.۵ ٪", "questions": "۱، ۲، ۷، ۱۰، ۱۶، ۲۰، ۳۲، ۳۶، ۳۹", "color": "#ef4444"},
            {"topic": "سیستم اعصاب خودمختار (کولینرژیک، آدرنرژیک و آنتی‌کولینرژیک)", "count": "۸ سوال", "percent": "۲۰.۰ ٪", "questions": "۸، ۱۲، ۱۴، ۱۹، ۲۷، ۳۳، ۳۵، ۳۷", "color": "#10b981"},
            {"topic": "سیستم اعصاب مرکزی (CNS)، ضد صرع، سداتیو-هیپنوتیزم و بیهوشی", "count": "۸ سوال", "percent": "۲۰.۰ ٪", "questions": "۳، ۱۱، ۲۲، ۲۳، ۲۴، ۲۵، ۲۶، ۲۹", "color": "#8b5cf6"},
            {"topic": "کلیه، تعادل آب و الکترولیت و داروهای دیورتیک", "count": "۴ سوال", "percent": "۱۰.۰ ٪", "questions": "۹، ۱۸، ۳۴، ۳۰", "color": "#f59e0b"},
            {"topic": "داروشناسی بالینی مامایی، حاملگی و آنتی‌هیستامین‌ها", "count": "۴ سوال", "percent": "۱۰.۰ ٪", "questions": "۴، ۱۳، ۲۳، ۲۰", "color": "#ec4899"},
        ]
        
        table_y = self.current_y
        row_h = 36
        header_h = 28
        
        # Header
        # Column X coordinates:
        # Table runs from LEFT_MARGIN (45) to RIGHT_MARGIN (550). Width = 505.
        # Right column: Topic (from 535 down to 260) -> width 275
        # Col 2: Count (from 260 down to 205) -> width 55, center = 232
        # Col 3: Percent (from 205 down to 155) -> width 50, center = 180
        # Col 4: Question numbers (from 155 down to 45) -> width 110, right = 150
        c.setFillColor(colors.HexColor('#1e293b'))
        c.rect(LEFT_MARGIN, table_y - header_h, PRINTABLE_WIDTH, header_h, fill=1, stroke=0)
        
        c.setFont(FONT_BOLD, 9.5)
        c.setFillColor(colors.white)
        c.drawRightString(RIGHT_MARGIN - 15, table_y - 18, fa("فصل / سرفصل آموزشی آزمون"))
        c.drawCentredString(LEFT_MARGIN + 205, table_y - 18, fa("تعداد"))
        c.drawCentredString(LEFT_MARGIN + 150, table_y - 18, fa("درصد"))
        c.drawRightString(LEFT_MARGIN + 115, table_y - 18, fa("شماره سوالات"))
        
        curr_y = table_y - header_h
        for idx, row in enumerate(stats):
            bg = colors.HexColor('#f8fafc') if idx % 2 == 0 else colors.white
            c.setFillColor(bg)
            c.setStrokeColor(colors.HexColor('#e2e8f0'))
            c.setLineWidth(0.5)
            c.rect(LEFT_MARGIN, curr_y - row_h, PRINTABLE_WIDTH, row_h, fill=1, stroke=1)
            
            # Left color badge
            c.setFillColor(colors.HexColor(row["color"]))
            c.rect(RIGHT_MARGIN - 5, curr_y - row_h, 5, row_h, fill=1, stroke=0)
            
            # Topic (with wrap if needed)
            c.setFont(FONT_BOLD, 7.8)
            c.setFillColor(colors.HexColor('#1e293b'))
            c.drawRightString(RIGHT_MARGIN - 14, curr_y - 21, fa(row["topic"]))
            
            # Count
            c.setFont(FONT_BOLD, 8.5)
            c.setFillColor(colors.HexColor('#0f172a'))
            c.drawCentredString(LEFT_MARGIN + 205, curr_y - 21, fa(row["count"]))
            
            # Percent
            c.setFont(FONT_BOLD, 8.5)
            c.setFillColor(colors.HexColor('#2563eb'))
            c.drawCentredString(LEFT_MARGIN + 150, curr_y - 21, fa(row["percent"]))
            
            # Questions
            c.setFont(FONT_REGULAR, 7.8)
            c.setFillColor(colors.HexColor('#475569'))
            c.drawRightString(LEFT_MARGIN + 115, curr_y - 21, fa(row["questions"]))
            
            curr_y -= row_h
            
        # Total Row
        c.setFillColor(colors.HexColor('#f1f5f9'))
        c.setStrokeColor(colors.HexColor('#cbd5e1'))
        c.setLineWidth(1)
        c.rect(LEFT_MARGIN, curr_y - 30, PRINTABLE_WIDTH, 30, fill=1, stroke=1)
        
        c.setFont(FONT_BOLD, 9.5)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawRightString(RIGHT_MARGIN - 15, curr_y - 20, fa("مجموع کل سوالات آزمون پایانی:"))
        c.drawCentredString(LEFT_MARGIN + 205, curr_y - 20, fa("۴۰ سوال"))
        c.drawCentredString(LEFT_MARGIN + 150, curr_y - 20, fa("۱۰۰ ٪"))
        c.drawRightString(LEFT_MARGIN + 115, curr_y - 20, fa("تمام ۴۰ تست آزمون"))
        
        self.current_y = curr_y - 60
        
        # Study Recommendations Box
        rec_h = 130
        c.setFillColor(colors.HexColor('#eff6ff'))
        c.setStrokeColor(colors.HexColor('#93c5fd'))
        c.setLineWidth(0.8)
        c.roundRect(LEFT_MARGIN, self.current_y - rec_h, PRINTABLE_WIDTH, rec_h, 6, fill=1, stroke=1)
        
        c.setFont(FONT_BOLD, 11)
        c.setFillColor(colors.HexColor('#1e40af'))
        c.drawRightString(RIGHT_MARGIN - 16, self.current_y - 25, fa("توصیه‌های راهبردی استاد فروتن برای کسب نمره عالی (۲۰):"))
        
        recs = [
            "۱. فارماکولوژی قلب و اتونوم بیش از ۴۲٪ نمره آزمون را تشکیل می‌دهند؛ روی این دو بخش تسلط صددرصدی پیدا کنید.",
            "۲. به تفاوت‌های ظریف دارویی دقت کنید: مثلاً نیفدیپین در آریتمی AV بی‌اثر است ولی وراپامیل داروی انتخابی است.",
            "۳. موارد منع مصرف در بارداری (مانند ACEIها و هیدروکسی‌زین) و پادزهرها (مانند فلومازنیل) سوالات قطعی آزمون هستند.",
            "۴. قبل از ورود به جلسه، حتماً جدول کلید سریع ۲ صفحه‌ای این جزوه را یک بار دیگر مرور فرمایید."
        ]
        
        r_y = self.current_y - 50
        for rec in recs:
            c.setFont(FONT_REGULAR, 9)
            c.setFillColor(colors.HexColor('#1e3a8a'))
            c.drawRightString(RIGHT_MARGIN - 20, r_y, fa(rec))
            r_y -= 20
            
        c.restoreState()

    def build(self):
        print("Starting PDF generation...")
        # 1. Cover
        self.draw_cover()
        
        # 2. Quick Key Table
        self.draw_quick_key_table()
        
        # 3. All 40 Questions
        self.start_new_page()
        for q in questions_data:
            self.draw_question_item(q)
            
        # 4. Statistical Summary
        self.draw_statistical_summary()
        
        # Finalize
        self.draw_footer()
        self.c.save()
        print(f"PDF built successfully: {self.filename} (Total pages: {self.page_num})")

if __name__ == "__main__":
    builder = ExamSolutionsPDF("پاسخنامه_تشریحی_سوالات_داروشناسی_فروتن.pdf")
    builder.build()
