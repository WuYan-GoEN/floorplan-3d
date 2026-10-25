#!/usr/bin/env python3
"""从间取图里找墙线（深色粗线）的像素位置，辅助换算尺寸。
用法：python3 tools/wall_lines.py 图片 x0 y0 x1 y1 [--dark 90] [--min 像素数]
  x0..y1 是某一层的裁剪框（原图像素）。
输出：竖墙（x 坐标 + 沿 y 的连续段）和横墙（y 坐标 + 沿 x 的连续段）。
连续段之间的空缺通常就是门、窗或开口。
换算：先用已知帖数的房间或外墙总长定出「910mm 对应多少像素」，
     再把像素换成 mm，最后对齐到 455mm（半格）。
"""
import sys, numpy as np
from PIL import Image
args = [a for a in sys.argv[1:] if not a.startswith('--')]
opt = {sys.argv[i][2:]: float(sys.argv[i+1]) for i in range(len(sys.argv)) if sys.argv[i].startswith('--')}
img, x0, y0, x1, y1 = args[0], *map(int, args[1:5])
dark = np.array(Image.open(img).convert('L')).astype(int) < opt.get('dark', 90)
sub = dark[y0:y1, x0:x1]
def bands(proj, base, mn):
    out, cur = [], None
    for i, v in enumerate(proj):
        if v > mn:
            if cur and i + base == cur[1] + 1: cur[1] = i + base
            else: cur = [i + base, i + base]; out.append(cur)
    return [b for b in out if b[1] - b[0] >= 3]          # 墙至少 4px 厚
def runs(mask, base, minlen=6):
    out, s = [], None
    for i, v in enumerate(list(mask) + [False]):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s >= minlen: out.append((s + base, i - 1 + base))
            s = None
    return out
mnx = opt.get('min', 0.12*(y1-y0)); mny = opt.get('min', 0.12*(x1-x0))
print('竖墙 x（中心）: 连续段 y')
for a, b in bands(sub.sum(axis=0), x0, mnx):
    cols = dark[y0:y1, a:b+1].sum(axis=1) >= (b - a)
    print(f'  x={(a+b)/2:7.1f} 厚{b-a+1}px  ', runs(cols, y0))
print('横墙 y（中心）: 连续段 x')
for a, b in bands(sub.sum(axis=1), y0, mny):
    rows = dark[a:b+1, x0:x1].sum(axis=0) >= (b - a)
    print(f'  y={(a+b)/2:7.1f} 厚{b-a+1}px  ', runs(rows, x0))
