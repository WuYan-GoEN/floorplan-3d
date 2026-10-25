#!/usr/bin/env python3
"""把一个户型 JSON 内嵌进 index.html，生成可单独打开的网页（不依赖 plans/ 目录）。
用法：python3 tools/build_single.py plans/<id>.json out.html
"""
import json, re, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
plan_path, out = sys.argv[1], sys.argv[2]
plan = json.loads(pathlib.Path(plan_path).read_text(encoding='utf8'))
assert plan.get('floors'), '户型文件缺少 floors'
html = (root / 'index.html').read_text(encoding='utf8')
data = json.dumps(plan, ensure_ascii=False).replace('</', '<\\/')
html, n = re.subn(r'<script type="application/json" id="planData"[^>]*>.*?</script>',
                  lambda m: f'<script type="application/json" id="planData" data-only="1">{data}</script>', html, count=1, flags=re.S)
assert n == 1, '在 index.html 里没找到 #planData'
title = plan.get('title') or '户型'
html = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', html, count=1)
pathlib.Path(out).write_text(html, encoding='utf8')
print(f'已生成 {out}（{len(html)//1024} KB，{len(plan["floors"])} 层）')
