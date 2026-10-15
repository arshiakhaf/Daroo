import sys
sys.path.insert(0, "/home/user/Daroo/py_modules")
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

# Import all epic novel chapters
sys.path.insert(0, '/home/user/Daroo')
from chapters.vol1_part1 import PROLOGUE_EPIC, CHAPTER_1_EPIC, CHAPTER_2_EPIC, CHAPTER_3_EPIC
from chapters.vol1_part2 import CHAPTER_4_EPIC, CHAPTER_5_EPIC, CHAPTER_6_EPIC, CHAPTER_7_EPIC
from chapters.vol2_part1 import CHAPTER_8_EPIC, CHAPTER_9_EPIC, CHAPTER_10_EPIC, CHAPTER_11_EPIC
from chapters.vol2_part2 import CHAPTER_12_EPIC, CHAPTER_13_EPIC, CHAPTER_14_EPIC, CHAPTER_15_EPIC, CHAPTER_16_EPIC
from chapters.pharmacopeia_codex import PHARMACOPEIA_CODEX
from chapters.clinical_cases import CLINICAL_CASES
from chapters.biochemical_mechanisms import BIOCHEMICAL_MECHANISMS

FONT_REGULAR = 'VazirFull'
FONT_BOLD = 'VazirFull-Bold'
pdfmetrics.registerFont(TTFont(FONT_REGULAR, '/home/user/Daroo/fonts/VazirmatnFull-400.ttf'))
pdfmetrics.registerFont(TTFont(FONT_BOLD, '/home/user/Daroo/fonts/VazirmatnFull-700.ttf'))

PAGE_WIDTH, PAGE_HEIGHT = A4
TOP_MARGIN = 55
BOTTOM_MARGIN = 55
LEFT_MARGIN = 50
RIGHT_MARGIN = 545
PRINTABLE_WIDTH = RIGHT_MARGIN - LEFT_MARGIN

def fa(text):
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

def wrap_text(text, font_name, font_size, max_w):
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

class EpicNovelPDFBuilder:
    def __init__(self, filename, chapter_page_map=None):
        self.filename = filename
        self.c = canvas.Canvas(filename, pagesize=A4)
        self.page_num = 0
        self.current_y = PAGE_HEIGHT - TOP_MARGIN
        self.current_chapter_title = ""
        self.chapter_page_map = chapter_page_map or {}
        self.record_page_map = {}
        self._current_is_cover = False
        self._current_is_toc = False

    def start_new_page(self, is_cover=False, is_toc=False):
        if self.page_num > 0 and not self._current_is_cover:
            self.draw_footer()
        if self.page_num > 0:
            self.c.showPage()
            
        self.page_num += 1
        self._current_is_cover = is_cover
        self._current_is_toc = is_toc
        self.current_y = PAGE_HEIGHT - TOP_MARGIN
        
        if not is_cover and not is_toc:
            self.draw_header()

    def draw_header(self):
        self.c.saveState()
        self.c.setFont(FONT_REGULAR, 8.5)
        self.c.setFillColor(colors.HexColor('#555555'))
        header_text = fa(f"اکسیر ویرانشهر: نغمه رگ و زهدان  |  {self.current_chapter_title}")
        self.c.drawRightString(RIGHT_MARGIN, PAGE_HEIGHT - 35, header_text)
        
        self.c.setStrokeColor(colors.HexColor('#cccccc'))
        self.c.setLineWidth(0.6)
        self.c.line(LEFT_MARGIN, PAGE_HEIGHT - 40, RIGHT_MARGIN, PAGE_HEIGHT - 40)
        self.c.restoreState()
        self.current_y = PAGE_HEIGHT - TOP_MARGIN - 15

    def draw_footer(self):
        if self._current_is_cover:
            return
            
        self.c.saveState()
        self.c.setFont(FONT_REGULAR, 9)
        self.c.setFillColor(colors.HexColor('#666666'))
        
        self.c.setStrokeColor(colors.HexColor('#dddddd'))
        self.c.setLineWidth(0.5)
        self.c.line(LEFT_MARGIN, BOTTOM_MARGIN + 15, RIGHT_MARGIN, BOTTOM_MARGIN + 15)
        
        page_str = fa(f"— صفحه {self.page_num} —")
        self.c.drawCentredString(PAGE_WIDTH / 2.0, BOTTOM_MARGIN, page_str)
        self.c.restoreState()

    def draw_cover(self):
        self.start_new_page(is_cover=True)
        c = self.c
        c.saveState()
        
        # Dark dramatic header background
        c.setFillColor(colors.HexColor('#120d13'))
        c.rect(0, PAGE_HEIGHT - 280, PAGE_WIDTH, 280, fill=1, stroke=0)
        
        # Golden double frame
        c.setStrokeColor(colors.HexColor('#d4af37'))
        c.setLineWidth(2.2)
        c.rect(LEFT_MARGIN - 15, BOTTOM_MARGIN - 15, PRINTABLE_WIDTH + 30, PAGE_HEIGHT - (BOTTOM_MARGIN + TOP_MARGIN) + 30)
        c.setLineWidth(0.8)
        c.rect(LEFT_MARGIN - 10, BOTTOM_MARGIN - 10, PRINTABLE_WIDTH + 20, PAGE_HEIGHT - (BOTTOM_MARGIN + TOP_MARGIN) + 20)
        
        # Title
        c.setFont(FONT_BOLD, 28)
        c.setFillColor(colors.HexColor('#f7d984'))
        c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 120, fa("اکسیر ویرانشهر"))
        
        c.setFont(FONT_BOLD, 21)
        c.setFillColor(colors.HexColor('#ffffff'))
        c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 165, fa("نغمه رگ و زهدان"))
        
        c.setFont(FONT_REGULAR, 12.5)
        c.setFillColor(colors.HexColor('#e5cca2'))
        c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 215, fa("رمان حماسی داروشناسی بالینی در قلمرو فانتزی تاریک و معمایی"))
        
        c.setFont(FONT_REGULAR, 10.5)
        c.setFillColor(colors.HexColor('#cccccc'))
        c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 245, fa("نسخه جامع و کامل — بر اساس تمامی سرفصل‌های دو جزوه قلب و مامایی"))
        
        # Core Topics Badge
        c.setFont(FONT_BOLD, 13)
        c.setFillColor(colors.HexColor('#8b1e22'))
        c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 330, fa("جامع‌ترین تلفیق ادبی و آموزشی داروشناسی بالینی:"))
        
        topics = [
            "• جلد اول: زمزمه‌های نبض و شریان (نارسایی قلب، آنژین، ضد آریتمی‌ها، دیورتیک‌ها، ضد انعقادها)",
            "• جلد دوم: اسرار زهدان و اکسیرهای تاریک (اکسی‌توسیک‌ها، ارگوت‌ها، پروستاگلاندین‌ها، پره‌اکلامپسی، توکولیتیک‌ها)",
            "• ضمیمه دانشنامه‌ای: فارماکوپیای بالینی تفصیلی ویرانشهر با جدول کامل مکانیسم‌ها، عوارض و پادزهرها"
        ]
        y_t = PAGE_HEIGHT - 360
        c.setFont(FONT_REGULAR, 10)
        c.setFillColor(colors.HexColor('#333333'))
        for tp in topics:
            c.drawCentredString(PAGE_WIDTH / 2.0, y_t, fa(tp))
            y_t -= 22
            
        # Character Gallery Card
        c.setFillColor(colors.HexColor('#f9f7f2'))
        c.setStrokeColor(colors.HexColor('#c8b88a'))
        c.roundRect(LEFT_MARGIN + 15, y_t - 145, PRINTABLE_WIDTH - 30, 130, 8, fill=1, stroke=1)
        
        c.setFont(FONT_BOLD, 11)
        c.setFillColor(colors.HexColor('#222222'))
        c.drawCentredString(PAGE_WIDTH / 2.0, y_t - 25, fa("شخصیت‌ها و بازیگران اصلی حماسه:"))
        
        chars = [
            "بهزاد فروتن (کیمیاگر مطرود) • حسام دانش (شمشیرزن مقاومت) • تهمینه (ساحره زهر و شهوت)",
            "امین شهبخش (رئیس مافیای متدین) • امیر آشوری (نجیب‌زاده زنباره) • مبین دامپرور (مست سرکش)",
            "علی پورسردار و مهدی بابایی (شمشیرزنان عاشق) • دکتر رضایی (شهردار ظالم)",
            "ندا (استاد دانشگاه و دیو جغد) • یاسر سربازی (سرباز خطاکار) • علیرضا رئیسی (شبح کیمیاگر)"
        ]
        y_c = y_t - 50
        c.setFont(FONT_REGULAR, 9)
        c.setFillColor(colors.HexColor('#444444'))
        for ch in chars:
            c.drawCentredString(PAGE_WIDTH / 2.0, y_c, fa(ch))
            y_c -= 19
            
        c.setFont(FONT_REGULAR, 10)
        c.setFillColor(colors.HexColor('#777777'))
        c.drawCentredString(PAGE_WIDTH / 2.0, BOTTOM_MARGIN + 25, fa("نگارش جامع و تدوین کتاب — پاییز ۱۴۰۵ / ۲۰۲۶"))
        
        c.restoreState()

    def draw_toc(self, all_items):
        self.current_chapter_title = "فهرست مطالب"
        self.start_new_page(is_toc=True)
        c = self.c
        
        c.setFont(FONT_BOLD, 18)
        c.setFillColor(colors.HexColor('#8b1e22'))
        c.drawRightString(RIGHT_MARGIN, self.current_y, fa("فهرست فصول و عناوین جامع رمان"))
        self.current_y -= 25
        
        c.setStrokeColor(colors.HexColor('#8b1e22'))
        c.setLineWidth(1.5)
        c.line(LEFT_MARGIN, self.current_y + 10, RIGHT_MARGIN, self.current_y + 10)
        self.current_y -= 12
        
        for item in all_items:
            if self.current_y < BOTTOM_MARGIN + 40:
                self.start_new_page(is_toc=True)
                
            title = item['title']
            subtitle = item.get('subtitle', '')
            page_target = self.chapter_page_map.get(title, "")
            page_text = f"صفحه {page_target}" if page_target else ""
            
            c.setFont(FONT_BOLD, 10)
            c.setFillColor(colors.HexColor('#1a1a1a'))
            c.drawRightString(RIGHT_MARGIN - 5, self.current_y, fa(title))
            
            if page_text:
                c.setFont(FONT_BOLD, 9.5)
                c.setFillColor(colors.HexColor('#8b1e22'))
                c.drawString(LEFT_MARGIN + 5, self.current_y, fa(page_text))
                
            self.current_y -= 14
            
            if subtitle:
                c.setFont(FONT_REGULAR, 8.5)
                c.setFillColor(colors.HexColor('#666666'))
                c.drawRightString(RIGHT_MARGIN - 20, self.current_y, fa(f"موضوع بالینی: {subtitle}"))
                self.current_y -= 18

    def add_chapter(self, chapter):
        self.current_chapter_title = chapter['title'].split(':')[0]
        self.start_new_page()
        self.record_page_map[chapter['title']] = self.page_num
        
        c = self.c
        
        # Chapter Banner
        c.setFillColor(colors.HexColor('#fcf8f2'))
        c.setStrokeColor(colors.HexColor('#d4af37'))
        c.roundRect(LEFT_MARGIN, self.current_y - 65, PRINTABLE_WIDTH, 65, 6, fill=1, stroke=1)
        
        c.setFont(FONT_BOLD, 13.5)
        c.setFillColor(colors.HexColor('#8b1e22'))
        c.drawRightString(RIGHT_MARGIN - 15, self.current_y - 23, fa(chapter['title']))
        
        c.setFont(FONT_REGULAR, 9.5)
        c.setFillColor(colors.HexColor('#555555'))
        c.drawRightString(RIGHT_MARGIN - 15, self.current_y - 46, fa(f"محور فارماکولوژی: {chapter['subtitle']}"))
        
        self.current_y -= 85
        
        for p in chapter['paragraphs']:
            self.add_paragraph(p)

    def add_paragraph(self, text):
        c = self.c
        font_name = FONT_REGULAR
        font_size = 10
        line_height = 18
        
        is_dialogue = text.startswith("ـ") or text.startswith("-")
        first_indent = 0 if is_dialogue else 15
        
        lines = wrap_text(text, font_name, font_size, PRINTABLE_WIDTH - first_indent)
        
        for i, line in enumerate(lines):
            if self.current_y < BOTTOM_MARGIN + 35:
                self.start_new_page()
            
            c.setFont(font_name, font_size)
            c.setFillColor(colors.HexColor('#1f1f1f'))
            
            r_x = RIGHT_MARGIN - (first_indent if i == 0 else 0)
            reshaped_line = arabic_reshaper.reshape(line)
            bidi_line = get_display(reshaped_line)
            c.drawRightString(r_x, self.current_y, bidi_line)
            
            self.current_y -= line_height
            
        self.current_y -= 8

    def add_biochemical_mechanism(self, mech):
        if not mech:
            return
            
        c = self.c
        if self.current_y < BOTTOM_MARGIN + 120:
            self.start_new_page()
            
        # Header banner for mechanism
        c.setFillColor(colors.HexColor('#4a235a'))
        c.roundRect(LEFT_MARGIN, self.current_y - 30, PRINTABLE_WIDTH, 30, 4, fill=1, stroke=0)
        
        c.setFont(FONT_BOLD, 10)
        c.setFillColor(colors.HexColor('#ffffff'))
        c.drawRightString(RIGHT_MARGIN - 10, self.current_y - 19, fa(f"تحلیل بیوشیمیایی و سلولی: {mech['title']}"))
        
        self.current_y -= 44
        
        paragraphs = mech['content'].split('\n\n')
        for p in paragraphs:
            lines = wrap_text(p, FONT_REGULAR, 8.5, PRINTABLE_WIDTH)
            for line in lines:
                if self.current_y < BOTTOM_MARGIN + 35:
                    self.start_new_page()
                c.setFont(FONT_REGULAR, 8.5)
                c.setFillColor(colors.HexColor('#1f1f1f'))
                c.drawRightString(RIGHT_MARGIN, self.current_y, fa(line))
                self.current_y -= 14.5
            self.current_y -= 6
        self.current_y -= 8

    def add_clinical_case(self, case):
        if not case:
            return
            
        c = self.c
        self.start_new_page()
        
        # Clinical Case Header Banner
        c.setFillColor(colors.HexColor('#2c3e50'))
        c.roundRect(LEFT_MARGIN, self.current_y - 55, PRINTABLE_WIDTH, 55, 6, fill=1, stroke=0)
        
        c.setFont(FONT_BOLD, 12.5)
        c.setFillColor(colors.HexColor('#ffffff'))
        c.drawRightString(RIGHT_MARGIN - 15, self.current_y - 22, fa(case['title']))
        
        c.setFont(FONT_REGULAR, 9)
        c.setFillColor(colors.HexColor('#d4af37'))
        c.drawRightString(RIGHT_MARGIN - 15, self.current_y - 42, fa("تحلیل موردی بالینی، تدابیر دارویی اورژانس و فرآیند پرستاری / مامایی"))
        
        self.current_y -= 75
        
        sections_data = [
            ("شرح حال و تریاژ بیمار:", case.get('patient_profile'), '#1f1f1f', '#2980b9'),
            ("علائم حیاتی در بدو ورود:", case.get('vitals'), '#8e44ad', '#8e44ad'),
            ("یافته‌های پاراکلینیک و تشخیصی:", case.get('diagnostics'), '#16a085', '#16a085'),
            ("تحلیل پاتوفیزیولوژی و فارماکودینامیک:", case.get('pathophysiology'), '#2c3e50', '#2c3e50'),
            ("تشخیص‌های پرستاری (NANDA):", case.get('nursing_diagnoses'), '#c0392b', '#c0392b'),
            ("دستورات دارویی و محاسبات دوز:", case.get('orders_and_dosing'), '#27ae60', '#27ae60'),
            ("پایش، مراقبت و مانیتورینگ بالینی:", case.get('monitoring'), '#d35400', '#d35400')
        ]
        
        for label, text, text_col, border_col in sections_data:
            if not text:
                continue
                
            if self.current_y < BOTTOM_MARGIN + 65:
                self.start_new_page()
                
            # Mini section header
            c.setFont(FONT_BOLD, 9.5)
            c.setFillColor(colors.HexColor(border_col))
            c.drawRightString(RIGHT_MARGIN, self.current_y, fa(f"■ {label}"))
            self.current_y -= 16
            
            # Text body
            raw_lines = text.split('\n')
            for r_line in raw_lines:
                lines = wrap_text(r_line, FONT_REGULAR, 8.5, PRINTABLE_WIDTH - 12)
                for line in lines:
                    if self.current_y < BOTTOM_MARGIN + 35:
                        self.start_new_page()
                    c.setFont(FONT_REGULAR, 8.5)
                    c.setFillColor(colors.HexColor(text_col))
                    c.drawRightString(RIGHT_MARGIN - 8, self.current_y, fa(line))
                    self.current_y -= 14.5
                self.current_y -= 2
            self.current_y -= 8

    def add_pharmacopeia(self, sections):
        self.current_chapter_title = "دانشنامه جامع فارماکوپیای ویرانشهر"
        self.start_new_page()
        self.record_page_map[self.current_chapter_title] = self.page_num
        
        c = self.c
        
        # Banner for Pharmacopeia
        c.setFillColor(colors.HexColor('#1b3b5a'))
        c.roundRect(LEFT_MARGIN, self.current_y - 65, PRINTABLE_WIDTH, 65, 6, fill=1, stroke=0)
        
        c.setFont(FONT_BOLD, 15)
        c.setFillColor(colors.HexColor('#ffffff'))
        c.drawRightString(RIGHT_MARGIN - 15, self.current_y - 25, fa("دانشنامه جامع فارماکوپیای ویرانشهر"))
        
        c.setFont(FONT_REGULAR, 9.5)
        c.setFillColor(colors.HexColor('#d4af37'))
        c.drawRightString(RIGHT_MARGIN - 15, self.current_y - 48, fa("مرجع بالینی تخصصی کلیه داروهای جزوات فارماکولوژی قلب و مامایی"))
        
        self.current_y -= 85
        
        intro_desc = (
            "این دانشنامه بر اساس سرفصل‌های جامع فارماکولوژی مامایی و داروشناسی بیماری‌های قلبی-عروقی "
            "پرستاری تدوین گردیده است و شامل مشخصات کامل سلولی، دوزاژ اورژانس، عوارض جانبی، تداخلات دارویی کشنده، "
            "نکات کلیدی مراقبت بالینی و پروتکل‌های اختصاصی پادزهر می‌باشد."
        )
        lines = wrap_text(intro_desc, FONT_REGULAR, 9.5, PRINTABLE_WIDTH)
        for line in lines:
            c.setFont(FONT_REGULAR, 9.5)
            c.setFillColor(colors.HexColor('#333333'))
            c.drawRightString(RIGHT_MARGIN, self.current_y, fa(line))
            self.current_y -= 16
            
        self.current_y -= 15
        
        for section in sections:
            if self.current_y < BOTTOM_MARGIN + 80:
                self.start_new_page()
                
            c.setFillColor(colors.HexColor('#8b1e22'))
            c.roundRect(LEFT_MARGIN, self.current_y - 26, PRINTABLE_WIDTH, 26, 4, fill=1, stroke=0)
            c.setFont(FONT_BOLD, 11)
            c.setFillColor(colors.HexColor('#ffffff'))
            c.drawRightString(RIGHT_MARGIN - 10, self.current_y - 18, fa(section['category']))
            self.current_y -= 38
            
            for item in section['items']:
                if self.current_y < BOTTOM_MARGIN + 85:
                    self.start_new_page()
                    
                c.setFillColor(colors.HexColor('#f0f4f8'))
                c.setStrokeColor(colors.HexColor('#1b3b5a'))
                c.roundRect(LEFT_MARGIN, self.current_y - 24, PRINTABLE_WIDTH, 24, 4, fill=1, stroke=1)
                
                c.setFont(FONT_BOLD, 10.5)
                c.setFillColor(colors.HexColor('#1b3b5a'))
                c.drawRightString(RIGHT_MARGIN - 10, self.current_y - 16, fa(item['drug']))
                
                if 'class' in item:
                    c.setFont(FONT_REGULAR, 8.5)
                    c.setFillColor(colors.HexColor('#4a5568'))
                    c.drawString(LEFT_MARGIN + 10, self.current_y - 16, fa(f"دسته: {item['class']}"))
                
                self.current_y -= 32
                
                fields = [
                    ("مکانیسم اثر سلولی:", item.get('mechanism'), '#1f1f1f'),
                    ("کاربرد و اندیکاسیون بالینی:", item.get('indication'), '#1f5f3a'),
                    ("فارماکوکینتیک و دوزاژ:", item.get('kinetics') or item.get('regimen'), '#2b4c7e'),
                    ("سمیت، عوارض و علائم مسمومیت:", item.get('toxicity'), '#9c1c1c'),
                    ("نکات مراقبت پرستاری و مامایی:", item.get('nursing_alerts'), '#52380a'),
                    ("پادزهر و پروتکل نجات:", item.get('antidote') or item.get('clinical_outcomes'), '#803c00')
                ]
                
                for label, txt, text_col in fields:
                    if not txt:
                        continue
                    full_str = f"■ {label} {txt}"
                    lines = wrap_text(full_str, FONT_REGULAR, 8.5, PRINTABLE_WIDTH - 16)
                    for line in lines:
                        if self.current_y < BOTTOM_MARGIN + 35:
                            self.start_new_page()
                        c.setFont(FONT_REGULAR, 8.5)
                        c.setFillColor(colors.HexColor(text_col))
                        c.drawRightString(RIGHT_MARGIN - 8, self.current_y, fa(line))
                        self.current_y -= 14.5
                    self.current_y -= 2
                self.current_y -= 10

    def save(self):
        if not self._current_is_cover:
            self.draw_footer()
        self.c.save()
        return self.record_page_map

def build_epic_novel():
    output_pdf = '/home/user/Daroo/رمان_اکسیر_ویرانشهر.pdf'
    
    all_story_items = [
        PROLOGUE_EPIC,
        CHAPTER_1_EPIC,
        CHAPTER_2_EPIC,
        CHAPTER_3_EPIC,
        CHAPTER_4_EPIC,
        CHAPTER_5_EPIC,
        CHAPTER_6_EPIC,
        CHAPTER_7_EPIC,
        CHAPTER_8_EPIC,
        CHAPTER_9_EPIC,
        CHAPTER_10_EPIC,
        CHAPTER_11_EPIC,
        CHAPTER_12_EPIC,
        CHAPTER_13_EPIC,
        CHAPTER_14_EPIC,
        CHAPTER_15_EPIC,
        CHAPTER_16_EPIC
    ]
    
    # PASS 1: Dry run to record page numbers
    print("Pass 1: calculating page mapping for expanded novel...")
    b1 = EpicNovelPDFBuilder('/tmp/epic_pass1.pdf')
    b1.draw_cover()
    b1.draw_toc(all_story_items + [{'title': 'دانشنامه جامع فارماکوپیای ویرانشهر', 'subtitle': 'جدول تفصیلی تمام داروها و پادزهرها'}])
    for idx, ch in enumerate(all_story_items):
        b1.add_chapter(ch)
        if idx < len(BIOCHEMICAL_MECHANISMS):
            b1.add_biochemical_mechanism(BIOCHEMICAL_MECHANISMS[idx])
        if idx < len(CLINICAL_CASES):
            b1.add_clinical_case(CLINICAL_CASES[idx])
    b1.add_pharmacopeia(PHARMACOPEIA_CODEX)
    page_map = b1.save()
    print("Recorded page mapping:", page_map)
    
    # PASS 2: Final PDF with exact page numbers
    print("Pass 2: compiling final epic PDF book...")
    b2 = EpicNovelPDFBuilder(output_pdf, chapter_page_map=page_map)
    b2.draw_cover()
    b2.draw_toc(all_story_items + [{'title': 'دانشنامه جامع فارماکوپیای ویرانشهر', 'subtitle': 'جدول تفصیلی تمام داروها و پادزهرها'}])
    for idx, ch in enumerate(all_story_items):
        b2.add_chapter(ch)
        if idx < len(BIOCHEMICAL_MECHANISMS):
            b2.add_biochemical_mechanism(BIOCHEMICAL_MECHANISMS[idx])
        if idx < len(CLINICAL_CASES):
            b2.add_clinical_case(CLINICAL_CASES[idx])
    b2.add_pharmacopeia(PHARMACOPEIA_CODEX)
    b2.save()
    
    print(f"Final expanded epic novel saved to: {output_pdf}")
    return output_pdf

if __name__ == '__main__':
    build_epic_novel()
