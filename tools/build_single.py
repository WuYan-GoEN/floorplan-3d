#!/usr/bin/env python3
"""把户型 JSON 内嵌进 index.html，生成可单独打开的网页（不依赖 plans/ 目录）。
用法：python3 tools/build_single.py plans/a.json [plans/b.json ...] out.html
一个户型 → 只显示它；多个 → 顶栏下拉切换（第一个是默认，地址用 #<id> 记住）。
"""
import json, re, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
*srcs, out = sys.argv[1:]
assert srcs and out.endswith('.html'), __doc__
plans = [json.loads(pathlib.Path(p).read_text(encoding='utf8')) for p in srcs]
for p in plans: assert p.get('floors'), f'{p.get("id")} 缺少 floors'
html = (root / 'index.html').read_text(encoding='utf8')
if len(plans) == 1:
    attr, data = 'data-only="1"', plans[0]
else:
    attr = 'data-multi="1"'
    data = {'index': {'default': plans[0]['id'], 'plans': [{'id': p['id'], 'title': p.get('title') or p['id']} for p in plans]},
            'plans': {p['id']: p for p in plans}}
blob = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
html, n = re.subn(r'<script type="application/json" id="planData"[^>]*>.*?</script>',
                  lambda m: f'<script type="application/json" id="planData" {attr}>{blob}</script>', html, count=1, flags=re.S)
assert n == 1, '在 index.html 里没找到 #planData'
html = re.sub(r'<title>.*?</title>', f'<title>{plans[0].get("title") or "户型"}</title>', html, count=1)
pathlib.Path(out).write_text(html, encoding='utf8')
print(f'已生成 {out}（{len(html)//1024} KB，{len(plans)} 个方案）')
