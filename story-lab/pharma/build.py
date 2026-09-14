#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a single Persian RTL HTML page from the story parts + master tables."""
import io, os, re, html

BASE = os.path.dirname(os.path.abspath(__file__))
PARTS = [os.path.join(BASE, "story", "part%d.md" % i) for i in range(1, 12)]


def esc(t):
    return html.escape(t, quote=False)


def inline(t):
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", t)
    return t


def md_to_html(md):
    out, i = [], 0
    heads = []
    lines = md.split("\n")
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()

        if s == "[[DEBRIEF]]":
            out.append('<div class="debrief-flag">دِبریفِ آموزشی</div>')
            i += 1
            continue

        if s.startswith("### "):
            out.append("<h4>%s</h4>" % inline(s[4:]))
            i += 1
            continue
        if s.startswith("## "):
            txt = s[3:]
            anchor = "s%d" % (len(heads) + 1)
            heads.append((txt, anchor))
            h = '<h2 id="%s">%s</h2>' % (anchor, inline(txt))
            out.append(h)
            i += 1
            continue
        if s.startswith("> "):
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(lines[i].strip()[1:].strip())
                i += 1
            out.append("<blockquote>%s</blockquote>" % " ".join(inline(b) for b in block))
            continue
        if s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            if rows and re.match(r"^:?-{2,}", rows[0][0].replace(" ", "")):
                rows = rows[1:]
            if len(rows) > 1 and set("".join(rows[0])) <= set("-: "):
                rows = rows[1:]
            thead = rows[0]
            body = rows[1:]
            t = ["<div class='tw'><table><thead><tr>"]
            t += ["<th>%s</th>" % inline(c) for c in thead]
            t.append("</tr></thead><tbody>")
            for r in body:
                t.append("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r))
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue
        if s.startswith("---"):
            out.append("<hr>")
            i += 1
            continue
        if s == "":
            i += 1
            continue
        # paragraph: gather until blank
        buf = []
        while i < len(lines) and lines[i].strip() != "" and not lines[i].strip().startswith(("#", "|", ">", "---")):
            buf.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % inline(" ".join(buf)))
    return "\n".join(out), heads


parts_md = []
for p in PARTS:
    if os.path.exists(p):
        parts_md.append(io.open(p, encoding="utf-8").read().strip())
full_md = "\n\n".join(parts_md)

io.open(os.path.join(BASE, "story-full.md"), "w", encoding="utf-8").write(
    "# آمپولِ نهم\n\n*رمانِ کوتاهِ آموزشی — داروشناسیِ قلب‌وعروق و مامایی، در یک شیفتِ شب*\n\n---\n\n"
    + full_md + "\n")
body, HEADS = md_to_html(full_md)
toc_html = "".join('<li><a href="#%s">%s</a></li>' % (a, esc(t)) for t, a in HEADS)


HTML = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>آمپولِ نهم — رمانِ کوتاهِ آموزشی داروشناسی</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
:root{--amber:#c8862f;--amber2:#e0a94e;--teal:#1d4a44;--ink:#0f1512}
*{box-sizing:border-box}
body{margin:0;background:radial-gradient(1100px 600px at 85% -5%,#1d4a44 0,transparent 60%),
  radial-gradient(900px 600px at 5% 105%,#3a2a12 0,transparent 55%),#0e1311;
  color:#e9e1d2;font-family:'Vazirmatn',Tahoma,sans-serif;line-height:2.05;font-weight:300}
.wrap{max-width:880px;margin:0 auto;padding:56px 22px 90px}
.kicker{display:inline-block;font-size:.72rem;letter-spacing:.2em;color:var(--amber2);
  border:1px solid rgba(200,134,47,.4);border-radius:999px;padding:7px 16px;margin-bottom:22px}
h1{font-size:clamp(2.4rem,8vw,4.2rem);margin:0;line-height:1.15;
  background:linear-gradient(180deg,#f7e6c4,#c8862f 88%);-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{color:#a89b86;margin-top:14px}
.hero{margin:34px 0;border-radius:16px;overflow:hidden;box-shadow:0 26px 60px -30px #000}
.hero img{display:block;width:100%;height:auto}
.toc{background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:18px 26px;margin:34px 0 10px}
.toc h3{margin:0 0 10px;font-size:.95rem;color:var(--amber2);font-weight:500}
.toc ol{margin:0;padding-inline-start:20px}
.toc a{color:#ddd2be;text-decoration:none;border-bottom:1px dotted rgba(255,255,255,.2)}
.toc a:hover{color:var(--amber2)}
h2{font-size:clamp(1.4rem,4.2vw,1.95rem);font-weight:500;color:#f4e9d6;margin:74px 0 22px;
  padding-bottom:12px;border-bottom:1px solid rgba(200,134,47,.28)}
h4{font-size:1.05rem;color:var(--amber2);margin:34px 0 12px;font-weight:500}
p{font-size:1.06rem;margin:0 0 20px;color:#e6dccb}
strong{color:#f7ecd8;font-weight:500}
em{color:#e0a94e;font-style:normal}
blockquote{margin:26px 0;padding:18px 22px;border-inline-start:3px solid var(--amber);
  background:linear-gradient(180deg,rgba(200,134,47,.10),transparent);border-radius:0 12px 12px 0;color:#f2e7d3}
.debrief-flag{display:inline-block;margin:40px 0 6px;font-size:.72rem;letter-spacing:.18em;color:#0f1512;
  background:linear-gradient(180deg,var(--amber2),var(--amber));border-radius:999px;padding:5px 14px;font-weight:700}
.tw{overflow-x:auto;margin:12px 0 30px;border:1px solid rgba(255,255,255,.09);border-radius:12px}
table{border-collapse:collapse;width:100%;font-size:.92rem;background:rgba(255,255,255,.02)}
th{background:rgba(200,134,47,.14);color:#f6ecd9;font-weight:500;text-align:right;padding:11px 13px;
  border-bottom:1px solid rgba(255,255,255,.1);white-space:nowrap}
td{padding:10px 13px;border-bottom:1px solid rgba(255,255,255,.055);color:#ded4c2;vertical-align:top;line-height:1.95}
tr:last-child td{border-bottom:none}
hr{border:none;border-top:1px solid rgba(255,255,255,.08);margin:50px 0}
footer{margin-top:70px;padding-top:34px;border-top:1px solid rgba(255,255,255,.1);color:#9d9182;font-size:.86rem;line-height:2}
footer b{color:var(--amber2);font-weight:500}
</style>
</head>
<body>
<div class="wrap">
<div class="kicker">رمانِ کوتاهِ آموزشی · داروشناسیِ قلب‌وعروق + مامایی</div>
<h1>آمپولِ نهم</h1>
<div class="sub">یک شیفتِ شب در بیمارستانی که بخشِ قلب و زایشگاهش را موقتاً به هم چسبانده‌اند — از ۲۰:۰۰ تا ۰۷:۱۰.
بعد از «پایان»، جزوه‌ی کاملِ دو درس، در جدول‌های همان داستان، جلوی چشم است.</div>
<div class="hero"><img src="assets/hero-night-shift.jpg" alt="راهروی بیمارستان، نیمه‌شب"></div>
<div class="toc"><h3>ساعتِ شیفت — فهرست</h3><ol>%TOC%</ol></div>
%HERO2%
%BODY%
<footer>
<b>چطور بخوانید و یاد بگیرید:</b> متنِ اصلی را مثل یک رمان بخوانید؛ هر صحنه با یک بلوکِ «دِبریف» تمام می‌شود که
همان داروها و اعدادِ همان صحنه را به شکلِ جدولِ مرور می‌دهد؛ و بخشِ ۱۰ (آخرین برگِ دفتر) برابر است با «جزوه‌ی جامع» هر دو درس.
<br><b>یادآوریِ صادقانه:</b> دو فایلِ PDF جزوه‌ها به محیطِ ساخت نرسید؛ این متن با استانداردِ رایجِ سرفصلِ همین دو درس
(فارماکولوژی مامایی + داروشناسیِ پرستاریِ قلب‌وعروق) نوشته شده است. برای هم‌ترازکردنِ واژه‌به‌واژه با نسخه‌ی کلاس خودتان،
فایل‌ها را دوباره بفرستید.
<br><b>تصاویر:</b> تولیدشده با هوش مصنوعی.
</footer>
</div>
</body>
</html>"""

hero2 = '<div class="hero"><img src="assets/ampoule-check.jpg" alt="بررسیِ آمپول زیر نورِ لامپ"></div>'
HTML = HTML.replace("%BODY%", body).replace("%TOC%", toc_html).replace("%HERO2%", hero2)
io.open(os.path.join(BASE, "index.html"), "w", encoding="utf-8").write(HTML)
print("wrote index.html", len(HTML), "chars;", len(parts_md), "parts")
