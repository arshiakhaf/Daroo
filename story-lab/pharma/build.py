#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""«هلالِ سفید» — ساختِ یک صفحهٔ HTMLِ راست‌به‌چپ از فصل‌های story/part*.md

اجرا:  python3 build.py
خروجی: index.html  +  story-full.md
"""
import io
import os
import re
import html

BASE = os.path.dirname(os.path.abspath(__file__))
STORY = os.path.join(BASE, "story")


def part_number(path):
    m = re.search(r"part(\d+)\.md$", path)
    return int(m.group(1)) if m else 0


PARTS = sorted(
    (os.path.join(STORY, f) for f in os.listdir(STORY) if re.match(r"part\d+\.md$", f)),
    key=part_number,
)

TITLE = "هلالِ سفید"
SUBTITLE = "رمانِ آموزشی — داروشناسیِ قلب‌وعروق و مامایی، از بندرِ جبل‌علی تا دادگاهِ روتردام"


def esc(t):
    return html.escape(t, quote=False)


def inline(t):
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", t)
    return t


def md_to_html(md):
    out, i, heads = [], 0, []
    lines = md.split("\n")
    while i < len(lines):
        s = lines[i].strip()

        if s.startswith("### "):
            out.append("<h4>%s</h4>" % inline(s[4:]))
            i += 1
            continue
        if s.startswith("## "):
            txt = s[3:]
            anchor = "s%d" % (len(heads) + 1)
            heads.append((txt, anchor))
            out.append('<h2 id="%s">%s</h2>' % (anchor, inline(txt)))
            i += 1
            continue
        if s.startswith("# "):
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
            if len(rows) > 1 and set("".join(rows[1])) <= set("-: "):
                rows = [rows[0]] + rows[2:]
            thead, body = rows[0], rows[1:]
            t = ["<div class='tw'><table><thead><tr>"]
            t += ["<th>%s</th>" % inline(c) for c in thead]
            t.append("</tr></thead><tbody>")
            for r in body:
                t.append("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r))
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue
        if len(s) >= 3 and set(s) <= {"*"}:
            out.append('<div class="scene-break">✳ ✳ ✳</div>')
            i += 1
            continue
        if s.startswith("---"):
            out.append("<hr>")
            i += 1
            continue
        if s == "":
            i += 1
            continue
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
    "# %s\n\n*%s*\n\n---\n\n%s\n" % (TITLE, SUBTITLE, full_md))

body, HEADS = md_to_html(full_md)
toc_html = "".join('<li><a href="#%s">%s</a></li>' % (a, esc(t)) for t, a in HEADS)

HTML = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>هلالِ سفید — رمانِ آموزشی داروشناسی</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
:root{--brass:#c9a24a;--brass2:#e6c877;--deep:#12333c;--ink:#0d1a1f;--foam:#9fd3c7}
*{box-sizing:border-box}
body{margin:0;background:radial-gradient(1200px 620px at 88% -8%,#12333c 0,transparent 62%),
  radial-gradient(900px 600px at 2% 104%,#2a1f0d 0,transparent 58%),#0a1418;
  color:#e7e0d2;font-family:'Vazirmatn',Tahoma,sans-serif;line-height:2.05;font-weight:300}
.wrap{max-width:880px;margin:0 auto;padding:56px 22px 90px}
.kicker{display:inline-block;font-size:.72rem;letter-spacing:.2em;color:var(--brass2);
  border:1px solid rgba(201,162,74,.4);border-radius:999px;padding:7px 16px;margin-bottom:22px}
h1{font-size:clamp(2.4rem,8vw,4.2rem);margin:0;line-height:1.15;
  background:linear-gradient(180deg,#f8eed6,#c9a24a 88%);-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{color:#a9a08c;margin-top:14px;max-width:640px}
.hero{margin:34px 0;border-radius:16px;overflow:hidden;box-shadow:0 26px 60px -30px #000}
.hero img{display:block;width:100%;height:auto}
.toc{background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:18px 26px;margin:34px 0 10px}
.toc h3{margin:0 0 10px;font-size:.95rem;color:var(--brass2);font-weight:500}
.toc ol{margin:0;padding-inline-start:20px}
.toc a{color:#ded4be;text-decoration:none;border-bottom:1px dotted rgba(255,255,255,.2)}
.toc a:hover{color:var(--brass2)}
h2{font-size:clamp(1.4rem,4.2vw,1.95rem);font-weight:500;color:#f5ecdb;margin:74px 0 22px;
  padding-bottom:12px;border-bottom:1px solid rgba(201,162,74,.28)}
h4{font-size:1.05rem;color:var(--brass2);margin:34px 0 12px;font-weight:500}
p{font-size:1.06rem;margin:0 0 20px;color:#e5dccb}
strong{color:#f8efdc;font-weight:500}
em{color:#e6c877;font-style:normal}
blockquote{margin:26px 0;padding:18px 22px;border-inline-start:3px solid var(--brass);
  background:linear-gradient(180deg,rgba(201,162,74,.10),transparent);border-radius:0 12px 12px 0;color:#f2e8d4}
.scene-break{text-align:center;color:var(--brass);letter-spacing:.4em;margin:40px 0;font-size:.9rem}
.debrief-flag{display:inline-block;margin:40px 0 6px;font-size:.72rem;letter-spacing:.18em;color:#0b1418;
  background:linear-gradient(180deg,var(--brass2),var(--brass));border-radius:999px;padding:5px 14px;font-weight:700}
.tw{overflow-x:auto;margin:12px 0 30px;border:1px solid rgba(255,255,255,.09);border-radius:12px}
table{border-collapse:collapse;width:100%;font-size:.92rem;background:rgba(255,255,255,.02)}
th{background:rgba(201,162,74,.14);color:#f7eeda;font-weight:500;text-align:right;padding:11px 13px;
  border-bottom:1px solid rgba(255,255,255,.1)}
td{padding:10px 13px;border-bottom:1px solid rgba(255,255,255,.055);color:#ded4c2;vertical-align:top;line-height:1.95}
tr:last-child td{border-bottom:none}
hr{border:none;border-top:1px solid rgba(255,255,255,.08);margin:50px 0}
footer{margin-top:70px;padding-top:34px;border-top:1px solid rgba(255,255,255,.1);color:#9d9484;font-size:.86rem;line-height:2}
footer b{color:var(--brass2);font-weight:500}
</style>
</head>
<body>
<div class="wrap">
<div class="kicker">رمانِ آموزشی · داروشناسیِ قلب‌وعروق + مامایی</div>
<h1>هلالِ سفید</h1>
<div class="sub">%SUB%</div>
<div class="hero"><img src="assets/hero-night-shift.jpg" alt="عرشهٔ کشتی در شب"></div>
<div class="toc"><h3>فهرست</h3><ol>%TOC%</ol></div>
%BODY%
<footer>
<b>قاعدهٔ این کتاب:</b> هر جمله‌ای که به دارو مربوط است، از دو جزوهٔ دکتر فروتن گرفته شده؛ نه یک قلم بیشتر، نه یک قلم کمتر.
فصلِ «ضمیمه» رونوشتِ صفحه‌به‌صفحهٔ خودِ جزوه‌هاست تا بشود هر جا شک کرد، مقابله کرد.
<br><b>«سه بار بگو»:</b> هر نکتهٔ مهم در داستان سه بار می‌آید — یک بار وقتی به آن نیاز می‌افتد، یک بار وقتی کسی درباره‌اش حرف می‌زند،
و یک بار در «دفترچهٔ مینا» پایِ همان فصل.
<br><b>تصاویر:</b> تولیدشده با هوش مصنوعی.
</footer>
</div>
</body>
</html>"""

HTML = HTML.replace("%SUB%", SUBTITLE).replace("%TOC%", toc_html).replace("%BODY%", body)
io.open(os.path.join(BASE, "index.html"), "w", encoding="utf-8").write(HTML)
print("wrote index.html %d chars; %d parts" % (len(HTML), len(parts_md)))
