import io,re,sys,os
fn, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
p = [f for f in os.listdir('source') if f.endswith('.txt') and sys.argv[1] in f][0]
t = io.open('source/'+p, encoding='utf-8').read()
parts = re.split(r'### صفحه (\d+)\n', t)
it = iter(parts[1:])
for num, body in zip(it, it):
    n = int(num)
    if a <= n <= b:
        body = re.sub(r'داروشناسي?پرستار\s*ي?\s*[:]?استاد\s*دكتر\s*فروتن', '', body)
        body = re.sub(r'داروشناسی رشته\s*کارشناسی\s*مامایی\s*[:]?استاد\s*دکتر\s*فروتن', '', body)
        body = re.sub(r'[ \t]{2,}', ' ', body)
        print("\n───── page", n, "─────")
        print(body.strip())
