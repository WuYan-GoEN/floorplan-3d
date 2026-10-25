#!/usr/bin/env python3
"""检查户型 JSON：每个房间面积换算成帖数、各层合计、与物件标注的建筑面积对比。
用法：python3 tools/check_plan.py plans/<id>.json [建筑面积㎡]
（按墙中心线计算，和日本物件的「建物面積」口径一致；1帖≈1.62㎡，1格910×910≈0.828㎡）
"""
import json, sys
p = json.load(open(sys.argv[1], encoding='utf8'))
target = float(sys.argv[2]) if len(sys.argv) > 2 else None
def area(poly): return abs(sum(a[0]*b[1]-b[0]*a[1] for a, b in zip(poly, poly[1:]+poly[:1])))/2/1e6
def poly_of(r):
    if 'poly' in r: return r['poly']
    x0, y0, x1, y1 = r['rect']; return [[x0,y0],[x1,y0],[x1,y1],[x0,y1]]
total = 0
for f in p['floors']:
    s = 0
    print(f"== {f.get('name', f['id'])}")
    for r in f['rooms']:
        a = area(poly_of(r)); c = r.get('counted', True) is not False
        if c: s += a
        print(f"  {r['name']:<14}{a:7.2f} ㎡  {a/1.62:5.2f} 帖{'' if c else '  (不计入)'}")
    for v in f.get('voids', []):
        a = area(v.get('poly') or poly_of(v)); s += a; print(f"  {'楼梯井':<14}{a:7.2f} ㎡")
    print(f"  合计 {s:.2f} ㎡"); total += s
print(f"全部楼层合计 {total:.2f} ㎡" + (f"，物件标注 {target} ㎡，差 {total-target:+.2f} ㎡" if target else ''))
