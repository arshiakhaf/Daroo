# هوش مصنوعی برای ساخت داستان، در چه حد پیشرفته شده است؟

گزارش همراهِ آزمایش عملی «دارو» — وضعیت واقعی، شهریور ۱۴۰۵ / سپتامبر ۲۰۲۶

---

## خلاصه در یک پاراگراف

امروز یک مدل زبانی می‌تواند در چند دقیقه داستانی کوتاه بسازد که ساختار دارد: قوسِ صحنه، کاراکترِ پیوسته،
دیالوگی که شخصیت را حمل می‌کند، و پایانی که موعظه نمی‌کند. همان مدل‌ها (یا مدل‌های خواهرشان) می‌توانند
همان داستان را تصویر کنند و بخوانند. یعنی «تولیدِ متنِ خوانا» دیگر مسئله نیست. مسئله‌ی باقی‌مانده دو چیز است:
**انسجام در مقیاس بلند** و **قضاوت درباره‌ی خوب و بد** — و دقیقاً همین دو، کاری است که هنوز انسان انجام می‌دهد.

---

## ۱) چه چیزی «حل شده» است

| توانایی | وضعیت | شاهد |
|---|---|---|
| نوشتن داستان کوتاهِ منسجم (۱ تا ۵ هزار کلمه) | عملاً حل‌شده؛ خروجیِ پیش‌فرض «خوانا و حرفه‌ای» است | همین آزمایش؛ [5](https://sureprompts.com/blog/which-ai-model-for-creative-writing-2026) |
| نگه‌داشتن لحن و صدای واحد در طول هزاران کلمه | به‌شدت بهتر شده؛ مدل پیشرو «دچار سکته‌ی لحنی» نمی‌شود | [1](https://benchlm.ai/blog/posts/best-llm-writing) |
| ظرفیت متن: کل رمان + انجیل داستان در یک نگاه | پنجره‌ها به ۱ میلیون توکن و بیشتر رسیده | [1](https://sureprompts.com/blog/which-ai-model-for-creative-writing-2026)، [8](https://www.buildmvpfast.com/articles/best-llms-2026-guide/creative-writing-ai) |
| پس‌زمینه‌سازی و مستندسازی جهان داستان (Worldbuilding) | وضعیت «قوی» تا «بهترین» | [2](https://www.promptquorum.com/power-local-llm/best-local-llm-creative-writing-2026) |
| تصویرسازیِ صحنه‌ها با کاراکترِ یکسان | با «تصویرِ مرجع» استاندارد شده؛ نه صددرصد، ولی قابلاستفاده | [13](https://www.mindstudio.ai/blog/what-is-sora-reference-system-character-consistency) |
| روایت صوتی فارسی | روان، با لحن قابل‌کنترل | همین آزمایش |

**نکته‌ی مهم:** تفکیک کارها شروع شده است. دیگر «یک مدل برای همه‌چیز» نیست:
بر اساس مقایسه‌های ۲۰۲۶، برای **بافت و صدای نثر** یک خانواده‌ی مدل بهتر است، برای **اجرای دقیقِ طرح و بیت‌شیت**
خانواده‌ی دیگری، و برای **پنجره‌ی بزرگ و بازبینیِ کلِ دست‌نوشته** خانواده‌ی سومی.
یعنی ابزار به سطح «نقش‌های تخصصی در یک تیم» رسیده، نه «یک مغز جادویی» [1](https://sureprompts.com/blog/which-ai-model-for-creative-writing-2026)، [3](https://www.inkfluenceai.com/blog/best-ai-models-for-novel-writing-2026).

---

## ۲) چه چیزی «حل نشده» است — و این مهم‌ترین بخش است

### الف) انسجام در مقیاس بلند
پژوهشی در مارس ۲۰۲۶ با نام **ConStory-Bench** (۲۰۰۰ پرامپت، داستان‌های هدفِ ۸ تا ۱۰ هزار کلمه) دقیقاً همین را سنجید.
نتیجه: **همه‌ی مدل‌های ارزیابی‌شده خطای انسجام دارند**؛ بهترین نتیجه (GPT-5-Reasoning با چگالی خطای ۰٫۱۱۳) هم به‌معنای
«بی‌خطا» نیست. پرتکرارترین خطاها هم دقیقاً همان چیزی است که یک رمان را می‌شکند:
**جزئیات و واقعیت‌های داستان** و **منطق زمانی و خط داستانی** [1](https://arxiv.org/html/2603.05890v1).

هزینه‌ی این ضعف در جاهای دیگر هم دیده می‌شود: مدل‌های اپن‌سورسی که برای حذف کلیشه‌ها ریزتنظیم شده‌اند،
در معیار «ضدکلیشه» امتیاز عالی می‌گیرند اما در «انسجام خروجی‌های بلند» به‌هم می‌ریزند
[4](https://awesomeagents.ai/leaderboards/creative-writing-llm-leaderboard/).

### ب) حافظه‌ی بیرونی، اعترافِ معماری است
همه‌ی ابزارهای جدیِ داستان‌نویسی (Sudowrite، Novelcrafter، NovelAI) مجبور شده‌اند یک لایه‌ی حافظه
بیرونِ مدل بسازند: «کدکس»، «لوربوک»، «Story Bible». این لایه‌ها را خودِ محصول می‌سازد، نه مدل
[4](https://www.creativindie.com/ai-story-generators-for-fiction-writers-in-2024-the-ultimate-guide/)، [10](https://www.firmcritics.com/review/novel-ai/).
در همین آزمایش کوچک ما هم، بدون نوشتنِ «انجیل داستان» روی کاغذ، احتمالاً بطریِ کهربایی یا «یک جرعه‌ی ته لیوان»
در صحنه‌ی پنجم قابل بازیابی نبود — بندِ ۱ فایل `story.md` را ببینید.

### ج) قضاوت ادبی
پدرِ همه‌ی مسئله‌ها: مدل نمی‌داند کدام پایان، کلیشه است. معیارهای کلاسیک مثل ROUGE و BLEU با قضاوت انسانی
همبستگی ضعیفی دارند [1](https://arxiv.org/html/2603.05890v1)، و وقتی خودِ مدل‌ها را به‌عنوان داور می‌گذاریم،
دقتشان در رتبه‌بندی نثر خلاقانه حدود **۶۳٪ تا ۷۳٪** است — بهتر از تصادف، دور از قابل‌اعتماد
[3](https://aclanthology.org/2026.eacl-long.362.pdf). به همین دلیل است که رتبه‌بندی‌های عمومی خلاقیت
(مثل EQ-Bench) را باید با شک خواند: داوری که خودش مدل است، سلیقه‌ی مدل‌ها را می‌سنجد
[2](https://eqbench.com/creative_writing_longform.html).

### د) «تُل»های سبکی
هر مدل اثر انگشتِ خودش را جا می‌گذارد: خط تیره‌ی اضافه، «در نهایت…»، جمله‌های سه‌عضویِ ردیفی،
و پایان‌های بسته‌ی اخلاقی [5](https://sureprompts.com/blog/which-ai-model-for-creative-writing-2026).
قابل رفع است — با دستورِ صریح و ویرایش انسانی — ولی خودبه‌خود رفع نمی‌شود.
در «دارو» برای همین بندِ «ممنوعیت‌ها» را قبل از نوشتن قید کردیم.

---

## ۳) متن، فقط بخشی از ماجراست: متن به چندرسانه

سطح واقعیِ پیشرفت وقتی روشن می‌شود که یک پرامپت تبدیل شود به **اثرِ چندلایه**:
متن، تصویرهای هم‌سبک با کاراکترِ یکسان، صدا، و در ادامه ویدئو.
امروز «قفلِ کاراکتر» با تصویرِ مرجع (Character Reference) در ابزارهای تصویری و ویدئویی به استاندارد بدل شده؛
چهره و ویژگی‌های شناسایی‌پذیر حفظ می‌شوند، اما جزئیات بدن و لباس هنوز متغیر می‌ماند
[13](https://www.mindstudio.ai/blog/what-is-sora-reference-system-character-consistency).
یک رمانِ مصور، یک کمیک، یا یک کتاب صوتیِ کامل، اکنون در محدوده‌ی یک نفر با یک لپ‌تاپ و چند روز کار است — چیزی که پیش از این
نیاز به استودیو داشت. و همین است که هم‌زمان هیجان‌انگیز و نگران‌کننده است.

---

## ۴) سیگنالِ واقعیِ بلوغ: صنعت چطور واکنش نشان داد

اگر می‌خواهید بدانید یک فناوری چقدر پیشرفته است، نگاه کنید رقابت و مقررات چگونه دورش شکل گرفته:

- **فوریه–آوریل ۲۰۲۶:** گروه انتشاراتی Hachette کتاب ترسناکی به نام *Shy Girl* را که قراردادش بسته شده بود،
  پس از اتهام‌های استفاده از هوش مصنوعی از انتشار در آمریکا و بریتانیا خارج کرد. علائمِ اعلام‌شده: نثرِ تکراری،
  صفت پیش از هر اسم، توصیف‌های سه‌تایی، و شباهت‌های سبکی [9](https://theconversation.com/a-popular-horror-novel-was-pulled-over-ai-concerns-heres-what-it-means-for-publishing-279714).
- **۲۰۲۶:** رمانی به نام *Daggermouth* که ابتدا خودانتشار بود و وارد فهرست پرفروش‌ها شد، با قراردادی هفت‌رقمی
  توسط انتشارات Simon & Schuster خریداری شد؛ پژوهشی دانشگاهی روی ۱۴٬۰۰۰ کتاب کیندل آن را «دارای متنِ عمدتاً
  هوش مصنوعی» تشخیص داد. نویسنده انکار می‌کند و ناشر پشت اثر ایستاده است
  [7](https://janefriedman.com/ai-and-publishing-faq-for-writers/).
- **۲۰۲۶:** یک قرارداد دوکتابیِ ۲٫۵ میلیون دلاری پس از آن لغو شد که نخستین ویراستارِ خریدار، نشانه‌های
  «کمکِ گسترده‌ی هوش مصنوعی» را در دست‌نوشته دید [7](https://janefriedman.com/ai-and-publishing-faq-for-writers/).
- **ژاپن، ژانویه ۲۰۲۶:** رمانی که جایزه‌ی بزرگِ یک مسابقه‌ی ادبی و رأی خوانندگان را برده بود، پس از تغییر
  مقرراتِ ضدِ هوش مصنوعی، انتشار کاغذی و اقتباس مانگا خود را از دست داد
  [11](https://automaton-media.com/en/news/ai-generated-isekai-novel-that-won-a-literary-contest-grand-prize-and-readers-choice-award-has-its-book-publication-and-manga-adaptation-cancelled/).
- **نوامبر ۲۰۲۵:** در نیوزیلند دو نویسنده‌ی سرشناس از بزرگ‌ترین جایزه‌ی کتاب کشور حذف شدند، چون **جلدِ** کتاب‌شان
  با هوش مصنوعی ساخته شده بود [10](https://www.theguardian.com/world/2025/nov/18/authors-dumped-from-new-zealands-top-book-prize-after-ai-used-in-cover-designs).

**تفسیر:** فناوری به سطحی رسیده که از «کنجکاوی آزمایشگاهی» گذشته و به «پرونده‌ی حقوقی، اخلاقی و تجاری» تبدیل شده.
ترسِ ناشران از این نیست که کتاب بد باشد؛ از این است که **قابلِ احرازِ مالکیت نباشد**. و این نشانه‌ی بلوغِ فناوری است،
نه ضعفش. ابزارهای تشخیص (Pangram، CopyLeaks) هم عملاً به صنعت فروخته می‌شوند
[7](https://janefriedman.com/ai-and-publishing-faq-for-writers/).

---

## ۵) نقشه‌ی سطحِ بلوغ — کجا ماشین تمام می‌شود

| کار | سطح امروز | قضاوت |
|---|---|---|
| ایده‌پردازی، طرح، عنوان، نامِ کاراکتر | تقریباً کامل | انسانی در چند ثانیه به صد ایده می‌رسد |
| داستان کوتاه ۱–۵ هزار کلمه | بسیار خوب | با ویرایش انسانی، قابل انتشار |
| فصل‌به‌فصل با بیرون‌سپاری حافظه | خوب | نیازمند «انجیل داستان» و بازبینی پیوسته |
| رمان ۸۰ هزار کلمه‌ای بدون ویرایش | ضعیف | خطای انسجام، به‌ویژه در زمان و جزئیات |
| صدای واحدِ نویسنده در کل کتاب | متوسط تا خوب | با «نمونه‌ی نثر» بهتر از «توصیفِ کلامی» جواب می‌دهد [5](https://sureprompts.com/blog/which-ai-model-for-creative-writing-2026) |
| قضاوت «این خوب است یا نه؟» | ضعیف | ۶۳–۷۳٪ دقت؛ کار انسان است [3](https://aclanthology.org/2026.eacl-long.362.pdf) |
| تصویرسازیِ پیوسته + صدا + ویدئو | خوب و در حال سریع‌شدن | «کاراکترِ قفل‌شده» استاندارد شده [13](https://www.mindstudio.ai/blog/what-is-sora-reference-system-character-consistency) |

---

## ۶) پس چطور از این توانایی استفاده کنیم؟ (گردش‌کار پیشنهادی)

۱. **انجیل داستان را خودت بنویس** (کاراکتر، ابژه‌های مرکزی، قاعده‌ی جهان، و فهرستِ ممنوعیت‌های سبکی).
۲. **طرح و بیت‌شیت** را با مدل بساز، ولی قلابِ پایانیِ هر صحنه را خودت تعیین کن.
۳. **صحنه‌به‌صحنه** بنویس، با صحنه‌های پیشین در متنِ ورودی، و بازبینیِ انسانی بین هر صحنه.
۴. **یک پاسِ انسجام** بگیر (زمان، مکان، اشیاء، اسم‌ها) — چون این همان‌جایی است که مدل می‌شکند.
۵. **تصویر** را با زنجیره‌ی مرجع بساز: یک تصویرِ مبنا، بعد همان به‌عنوان مرجعِ بقیه.
۶. **کلمه‌ی آخر با توست.** اگر جمله‌ای را حذف نکردی چون خودت دوستش داشتی، داستان هنوز مالِ توست.

---

## ۷) منابع

1. ConStory-Bench: *Lost in Stories: Consistency Bugs in Long Story Generation by LLMs*, arXiv — https://arxiv.org/html/2603.05890v1
2. EQ-Bench — Longform Creative Writing Leaderboard — https://eqbench.com/creative_writing_longform.html
3. LitBench, EACL 2026 — https://aclanthology.org/2026.eacl-long.362.pdf
4. Creative Writing LLM Leaderboard 2026 / Antislop — https://awesomeagents.ai/leaderboards/creative-writing-llm-leaderboard/
5. Which AI Model for Creative Writing and Long-Form Fiction in 2026 — https://sureprompts.com/blog/which-ai-model-for-creative-writing-2026
6. Best AI Models for Novel Writing 2026 — https://www.inkfluenceai.com/blog/best-ai-models-for-novel-writing-2026
7. Jane Friedman, *AI and Publishing: FAQ for Writers* — https://janefriedman.com/ai-and-publishing-faq-for-writers/
8. Best AI for Creative Writing 2026 (BuildMVPFast) — https://www.buildmvpfast.com/articles/best-llms-2026-guide/creative-writing-ai
9. The Conversation, *A popular horror novel was pulled over AI concerns* — https://theconversation.com/a-popular-horror-novel-was-pulled-over-ai-concerns-heres-what-it-means-for-publishing-279714
10. The Guardian, *Authors dumped from New Zealand's top book prize after AI used in cover designs* — https://www.theguardian.com/world/2025/nov/18/authors-dumped-from-new-zealands-top-book-prize-after-ai-used-in-cover-designs
11. Automaton Media, *AI-generated isekai novel… publication cancelled* — https://automaton-media.com/en/news/ai-generated-isekai-novel-that-won-a-literary-contest-grand-prize-and-readers-choice-award-has-its-book-publication-and-manga-adaptation-cancelled/
12. SCORE: Story Coherence and Retrieval Enhancement, arXiv — https://arxiv.org/html/2503.23512v1
13. Sora's Reference System & Character Consistency — https://www.mindstudio.ai/blog/what-is-sora-reference-system-character-consistency
14. CreativIndie, *AI Story Generators for Fiction Writers (the honest guide)* — https://www.creativindie.com/ai-story-generators-for-fiction-writers-in-2024-the-ultimate-guide/
15. Best Local LLMs for Creative Writing 2026 — https://www.promptquorum.com/power-local-llm/best-local-llm-creative-writing-2026

---

### پیوست: این آزمایش چطور انجام شد
- متن، انجیل داستان و پرامپت‌های تصویری: `story-lab/story.md`
- پنج تصویر: `story-lab/assets/scene-1.jpg` تا `scene-5.jpg` (تصویر ۱ مبنا؛ ۲ تا ۵ با مرجعِ تصویرِ ۱)
- پنج قطعه‌ی روایت صوتی فارسی: `story-lab/assets/scene-1.mp3` تا `scene-5.mp3`
- صفحه‌ی ارائه: `story-lab/index.html`
