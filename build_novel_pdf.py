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

# Import chapters
sys.path.insert(0, '/home/user/Daroo')
from chapters.prologue_and_ch1 import PROLOGUE, CHAPTER_1
from chapters.ch2_and_ch3 import CHAPTER_2, CHAPTER_3
from chapters.ch4_and_ch5 import CHAPTER_4, CHAPTER_5
from chapters.ch6_and_ch7 import CHAPTER_6, CHAPTER_7
from chapters.ch8_and_ch9 import CHAPTER_8, CHAPTER_9
from chapters.epilogue_and_appendix import EPILOGUE, APPENDIX_CONTENT

# Register Vazirmatn fonts
FONT_REGULAR = 'VazirFull'
FONT_BOLD = 'VazirFull-Bold'
pdfmetrics.registerFont(TTFont(FONT_REGULAR, '/home/user/fonts/VazirmatnFull-400.ttf'))
pdfmetrics.registerFont(TTFont(FONT_BOLD, '/home/user/fonts/VazirmatnFull-700.ttf'))

PAGE_WIDTH, PAGE_HEIGHT = A4
TOP_MARGIN = 55
BOTTOM_MARGIN = 55
LEFT_MARGIN = 50
RIGHT_MARGIN = 545
PRINTABLE_WIDTH = RIGHT_MARGIN - LEFT_MARGIN

def fa(text):
    """Helper to reshape and reorder Persian/Arabic text."""
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

def wrap_text(text, font_name, font_size, max_w):
    """Wrap text properly word by word for RTL drawing."""
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

class NovelPDFBuilder:
    def __init__(self, filename, chapter_page_map=None):
        self.filename = filename
        self.c = canvas.Canvas(filename, pagesize=A4)
        self.page_num = 0
        self.current_y = PAGE_HEIGHT - TOP_MARGIN
        self.current_chapter_title = ""
        self.chapter_page_map = chapter_page_map or {}
        self.record_page_map = {}
        
    def start_new_page(self, is_cover=False, is_toc=False):
        if self.page_num > 0 and not getattr(self, '_current_is_cover', False):
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
        
        # Decorative thin rule
        self.c.setStrokeColor(colors.HexColor('#cccccc'))
        self.c.setLineWidth(0.6)
        self.c.line(LEFT_MARGIN, PAGE_HEIGHT - 40, RIGHT_MARGIN, PAGE_HEIGHT - 40)
        self.c.restoreState()
        self.current_y = PAGE_HEIGHT - TOP_MARGIN - 15

    def draw_footer(self):
        # Do not draw footer on cover
        if getattr(self, '_current_is_cover', False):
            return
            
        self.c.saveState()
        self.c.setFont(FONT_REGULAR, 9)
        self.c.setFillColor(colors.HexColor('#666666'))
        
        # Decorative thin rule
        self.c.setStrokeColor(colors.HexColor('#dddddd'))
        self.c.setLineWidth(0.5)
        self.c.line(LEFT_MARGIN, BOTTOM_MARGIN + 15, RIGHT_MARGIN, BOTTOM_MARGIN + 15)
        
        # Page number (Cover is not counted, so TOC is page 1, story starts on page 2)
        display_page = self.page_num
        page_str = fa(f"— صفحه {display_page} —")
        self.c.drawCentredString(PAGE_WIDTH / 2.0, BOTTOM_MARGIN, page_str)
        self.c.restoreState()

    def draw_cover(self):
        self.start_new_page(is_cover=True)
        c = self.c
        c.saveState()
        
        # Dark dramatic header background
        c.setFillColor(colors.HexColor('#1a1118'))
        c.rect(0, PAGE_HEIGHT - 260, PAGE_WIDTH, 260, fill=1, stroke=0)
        
        # Golden decorative frame
        c.setStrokeColor(colors.HexColor('#d4af37'))
        c.setLineWidth(2)
        c.rect(LEFT_MARGIN - 15, BOTTOM_MARGIN - 15, PRINTABLE_WIDTH + 30, PAGE_HEIGHT - (BOTTOM_MARGIN + TOP_MARGIN) + 30)
        c.setLineWidth(0.8)
        c.rect(LEFT_MARGIN - 10, BOTTOM_MARGIN - 10, PRINTABLE_WIDTH + 20, PAGE_HEIGHT - (BOTTOM_MARGIN + TOP_MARGIN) + 20)
        
        # Title in gold
        c.setFont(FONT_BOLD, 26)
        c.setFillColor(colors.HexColor('#f5d77f'))
        title = fa("اکسیر ویرانشهر")
        c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 120, title)
        
        c.setFont(FONT_BOLD, 20)
        c.setFillColor(colors.HexColor('#ffffff'))
        sub = fa("نغمه رگ و زهدان")
        c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 160, sub)
        
        c.setFont(FONT_REGULAR, 12)
        c.setFillColor(colors.HexColor('#e0cda9'))
        tagline = fa("رمانی تاریک، معمایی و بی‌پرده در قلمرو جادوی بیوشیمی و شریان")
        c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 210, tagline)
        
        # Book Description in Center
        c.setFont(FONT_BOLD, 13)
        c.setFillColor(colors.HexColor('#8b1e22'))
        c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 320, fa("تلفیق کامل سرفصل‌های فارماکولوژی بالینی:"))
        
        c.setFont(FONT_REGULAR, 11)
        c.setFillColor(colors.HexColor('#333333'))
        topics = [
            "• دارودرمانی بیماری‌های قلبی-عروقی (دیگوکسین، ضد آریتمی‌ها، نیترات‌ها، بتابلوکرها، ضد انعقادها)",
            "• فارماکولوژی مامایی و بارداری (اکسی‌توسین، مترژین، پروستاگلاندین‌ها، سولفات منیزیم، توکولیتیک‌ها)",
            "• مکانیسم گیرنده‌ها، تداخلات دارویی مرگبار، عوارض ناخواسته و پادزهرهای نجات‌بخش"
        ]
        y_t = PAGE_HEIGHT - 350
        for tp in topics:
            c.drawCentredString(PAGE_WIDTH / 2.0, y_t, fa(tp))
            y_t -= 22
            
        # Character & World badge
        c.setFillColor(colors.HexColor('#f7f5f0'))
        c.setStrokeColor(colors.HexColor('#c8b88a'))
        c.roundRect(LEFT_MARGIN + 20, y_t - 140, PRINTABLE_WIDTH - 40, 125, 8, fill=1, stroke=1)
        
        c.setFont(FONT_BOLD, 10.5)
        c.setFillColor(colors.HexColor('#222222'))
        c.drawCentredString(PAGE_WIDTH / 2.0, y_t - 30, fa("شخصیت‌های اصلی داستان:"))
        
        c.setFont(FONT_REGULAR, 9.5)
        c.setFillColor(colors.HexColor('#444444'))
        chars = [
            "بهزاد فروتن • حسام دانش • تهمینه • امین شهبخش • امیر آشوری",
            "مبین دامپرور • معید براهویی • دکتر رضایی • ندا (دیو جغد) • یاسر سربازی",
            "علی پورسردار و مهدی بابایی • کیمیاگر اثیری علیرضا رئیسی"
        ]
        y_c = y_t - 55
        for ch in chars:
            c.drawCentredString(PAGE_WIDTH / 2.0, y_c, fa(ch))
            y_c -= 20
            
        # Release info
        c.setFont(FONT_REGULAR, 10)
        c.setFillColor(colors.HexColor('#777777'))
        c.drawCentredString(PAGE_WIDTH / 2.0, BOTTOM_MARGIN + 25, fa("پاییز ۱۴۰۵ / ۲۰۲۶ — ویرانشهر"))
        
        c.restoreState()

    def draw_toc(self, chapters):
        self.current_chapter_title = "فهرست فصول"
        self.start_new_page(is_toc=True)
        c = self.c
        
        c.setFont(FONT_BOLD, 18)
        c.setFillColor(colors.HexColor('#8b1e22'))
        c.drawRightString(RIGHT_MARGIN, self.current_y, fa("فهرست فصول و عناوین رمان"))
        self.current_y -= 30
        
        c.setStrokeColor(colors.HexColor('#8b1e22'))
        c.setLineWidth(1.5)
        c.line(LEFT_MARGIN, self.current_y + 10, RIGHT_MARGIN, self.current_y + 10)
        self.current_y -= 15
        
        for ch in chapters:
            if self.current_y < BOTTOM_MARGIN + 45:
                self.start_new_page(is_toc=True)
            
            ch_title = ch['title']
            page_target = self.chapter_page_map.get(ch_title, "")
            page_text = f"صفحه {page_target}" if page_target else ""
            
            # Draw chapter title on right
            c.setFont(FONT_BOLD, 11)
            c.setFillColor(colors.HexColor('#1a1a1a'))
            c.drawRightString(RIGHT_MARGIN - 5, self.current_y, fa(ch_title))
            
            # Draw page target on left
            if page_text:
                c.setFont(FONT_BOLD, 10.5)
                c.setFillColor(colors.HexColor('#8b1e22'))
                c.drawString(LEFT_MARGIN + 5, self.current_y, fa(page_text))
                
            self.current_y -= 16
            
            c.setFont(FONT_REGULAR, 9.5)
            c.setFillColor(colors.HexColor('#666666'))
            c.drawRightString(RIGHT_MARGIN - 20, self.current_y, fa(f"موضوع بالینی: {ch['subtitle']}"))
            self.current_y -= 22

    def add_chapter(self, chapter):
        self.current_chapter_title = chapter['title'].split(':')[0]
        self.start_new_page()
        self.record_page_map[chapter['title']] = self.page_num
        
        c = self.c
        
        # Chapter header badge
        c.setFillColor(colors.HexColor('#fcf8f2'))
        c.setStrokeColor(colors.HexColor('#d4af37'))
        c.roundRect(LEFT_MARGIN, self.current_y - 65, PRINTABLE_WIDTH, 65, 6, fill=1, stroke=1)
        
        c.setFont(FONT_BOLD, 14.5)
        c.setFillColor(colors.HexColor('#8b1e22'))
        c.drawRightString(RIGHT_MARGIN - 15, self.current_y - 25, fa(chapter['title']))
        
        c.setFont(FONT_REGULAR, 10)
        c.setFillColor(colors.HexColor('#555555'))
        c.drawRightString(RIGHT_MARGIN - 15, self.current_y - 48, fa(f"محور فارماکولوژی: {chapter['subtitle']}"))
        
        self.current_y -= 90
        
        # Paragraphs
        for p in chapter['paragraphs']:
            self.add_paragraph(p)

    def add_paragraph(self, text):
        c = self.c
        font_name = FONT_REGULAR
        font_size = 10.5
        line_height = 18.5
        
        is_dialogue = text.startswith("ـ") or text.startswith("-")
        first_indent = 0 if is_dialogue else 15
        
        # Calculate max width
        lines = wrap_text(text, font_name, font_size, PRINTABLE_WIDTH - first_indent)
        
        for i, line in enumerate(lines):
            # Check if need new page
            if self.current_y < BOTTOM_MARGIN + 35:
                self.start_new_page()
            
            c.setFont(font_name, font_size)
            c.setFillColor(colors.HexColor('#1f1f1f'))
            
            r_x = RIGHT_MARGIN - (first_indent if i == 0 else 0)
            reshaped_line = arabic_reshaper.reshape(line)
            bidi_line = get_display(reshaped_line)
            c.drawRightString(r_x, self.current_y, bidi_line)
            
            self.current_y -= line_height
            
        self.current_y -= 7 # spacing between paragraphs

    def add_appendix(self, appendix_data):
        self.current_chapter_title = "ضمیمه فارماکولوژی"
        self.start_new_page()
        self.record_page_map["ضمیمه: کتابچه جامع فارماکولوژی"] = self.page_num
        c = self.c
        
        # Title
        c.setFont(FONT_BOLD, 16)
        c.setFillColor(colors.HexColor('#8b1e22'))
        c.drawRightString(RIGHT_MARGIN, self.current_y, fa("کتابچه جامع فارماکولوژی بالینی ویرانشهر"))
        self.current_y -= 25
        
        c.setFont(FONT_REGULAR, 10.5)
        c.setFillColor(colors.HexColor('#444444'))
        intro = "این ضمیمه علمی، تمامی داروها، دسته‌بندی‌ها، مکانیسم‌های سلولی، عوارض و پادزهرهای مطرح‌شده در رمان را بر اساس دو جزوه بالینی قلب و مامایی به طور جامع خلاصه می‌کند:"
        lines = wrap_text(intro, FONT_REGULAR, 10.5, PRINTABLE_WIDTH)
        for line in lines:
            c.drawRightString(RIGHT_MARGIN, self.current_y, fa(line))
            self.current_y -= 18
            
        self.current_y -= 15
        
        for section in appendix_data:
            if self.current_y < BOTTOM_MARGIN + 60:
                self.start_new_page()
                
            # Section Header
            c.setFillColor(colors.HexColor('#8b1e22'))
            c.roundRect(LEFT_MARGIN, self.current_y - 25, PRINTABLE_WIDTH, 25, 4, fill=1, stroke=0)
            c.setFont(FONT_BOLD, 12)
            c.setFillColor(colors.HexColor('#ffffff'))
            c.drawRightString(RIGHT_MARGIN - 10, self.current_y - 18, fa(section['category']))
            self.current_y -= 40
            
            for item in section['items']:
                # Calculate needed height for this drug item card
                content_lines = []
                content_lines.extend(wrap_text(f"مکانیسم: {item['mechanism']}", FONT_REGULAR, 9, PRINTABLE_WIDTH - 20))
                content_lines.extend(wrap_text(f"اندیکاسیون: {item['indication']}", FONT_REGULAR, 9, PRINTABLE_WIDTH - 20))
                content_lines.extend(wrap_text(f"سمیت و عوارض: {item['toxicity']}", FONT_REGULAR, 9, PRINTABLE_WIDTH - 20))
                content_lines.extend(wrap_text(f"پادزهر و تدابیر: {item['antidote']}", FONT_REGULAR, 9, PRINTABLE_WIDTH - 20))
                
                card_h = 35 + len(content_lines) * 15 + 15
                
                if self.current_y - card_h < BOTTOM_MARGIN + 20:
                    self.start_new_page()
                    
                # Draw drug card box
                c.setFillColor(colors.HexColor('#faf9f6'))
                c.setStrokeColor(colors.HexColor('#d9d2c5'))
                c.roundRect(LEFT_MARGIN, self.current_y - card_h, PRINTABLE_WIDTH, card_h, 5, fill=1, stroke=1)
                
                # Drug Title Bar
                c.setFont(FONT_BOLD, 11)
                c.setFillColor(colors.HexColor('#1b3b5a'))
                c.drawRightString(RIGHT_MARGIN - 10, self.current_y - 18, fa(item['drug']))
                
                c.setFont(FONT_REGULAR, 9)
                c.setFillColor(colors.HexColor('#666666'))
                c.drawString(LEFT_MARGIN + 10, self.current_y - 18, fa(f"دسته: {item['class']}"))
                
                # Dividing line
                c.setStrokeColor(colors.HexColor('#e5dfd5'))
                c.line(LEFT_MARGIN + 8, self.current_y - 25, RIGHT_MARGIN - 8, self.current_y - 25)
                
                # Body lines
                y_text = self.current_y - 40
                
                pairs = [
                    ("مکانیسم اثر:", item['mechanism'], '#222222'),
                    ("کاربرد بالینی:", item['indication'], '#1f5f3a'),
                    ("سمیت و هشدار:", item['toxicity'], '#8b1e22'),
                    ("پادزهر و منع مصرف:", item['antidote'], '#803c00')
                ]
                
                for label, txt, col in pairs:
                    c.setFont(FONT_BOLD, 9)
                    c.setFillColor(colors.HexColor(col))
                    full_str = f"{label} {txt}"
                    lines = wrap_text(full_str, FONT_REGULAR, 9, PRINTABLE_WIDTH - 20)
                    for l in lines:
                        c.drawRightString(RIGHT_MARGIN - 10, y_text, fa(l))
                        y_text -= 15
                        
                self.current_y -= (card_h + 12)

    def save(self):
        if not getattr(self, '_current_is_cover', False):
            self.draw_footer()
        self.c.save()
        return self.record_page_map

def generate_book():
    output_pdf = '/home/user/Daroo/رمان_اکسیر_ویرانشهر.pdf'
    
    all_chapters = [
        PROLOGUE,
        CHAPTER_1,
        CHAPTER_2,
        CHAPTER_3,
        CHAPTER_4,
        CHAPTER_5,
        CHAPTER_6,
        CHAPTER_7,
        CHAPTER_8,
        CHAPTER_9,
        EPILOGUE
    ]
    
    # PASS 1: Dry run to record page numbers
    print("Pass 1: calculating page mapping...")
    builder1 = NovelPDFBuilder('/tmp/pass1.pdf')
    builder1.draw_cover()
    builder1.draw_toc(all_chapters)
    for ch in all_chapters:
        builder1.add_chapter(ch)
    builder1.add_appendix(APPENDIX_CONTENT)
    page_map = builder1.save()
    print("Recorded page mapping:", page_map)
    
    # PASS 2: Build final PDF with exact page numbers in TOC
    print("Pass 2: building final beautifully bound PDF book...")
    builder2 = NovelPDFBuilder(output_pdf, chapter_page_map=page_map)
    builder2.draw_cover()
    builder2.draw_toc(all_chapters)
    for ch in all_chapters:
        builder2.add_chapter(ch)
    builder2.add_appendix(APPENDIX_CONTENT)
    builder2.save()
    
    print(f"Final novel book saved to: {output_pdf}")
    return output_pdf

if __name__ == '__main__':
    generate_book()
