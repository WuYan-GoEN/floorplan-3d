# 户型数据格式（plans/*.json）

打开 `index.html?plan=<id>` 加载 `plans/<id>.json`；不带参数时加载 `plans/index.json` 里的 `default`。
单位 mm，x 向右、y 向下（图纸上方 y 小）。多层共用同一坐标系（上下层对齐）。

```jsonc
{
  "id": "3gou-4ldk",                 // 与文件名一致
  "title": "3号棟 4LDK",
  "subtitle": "土地150.04㎡ · 建物97.29㎡",
  "north": 22,                        // 正北方向：从图纸正上方顺时针的角度，用于日照
  "floors": [ { ...楼层... } ]
}
```

## 楼层（推荐 `format: "center"`）

| 字段 | 说明 |
|---|---|
| `id` / `name` | `"1F"` 等，显示在顶栏切换按钮上 |
| `walls` | `[x0,y0,x1,y1,类型,厚度?]` 墙**中心线**，只能水平或竖直。类型：`e` 外墙(150) `n` 内墙(110) `b` 承重(150) `low` 矮墙/栏杆(60, 高1m) |
| `openings` | 门窗，`at` 写在所在墙的中心线上，加载时自动在墙上开洞 |
| `rooms` | `{id,name,rect:[x0,y0,x1,y1] 或 poly:[[x,y]..],mat,at?,counted?,label?,bay?}` 按墙中心线围合 |
| `stairs` | `{steps:[多边形...],rise:207,base:0,show3d,label,labelAt,arrow}` 每级踏步一个多边形，3D 按序号逐级升高 |
| `voids` | 楼梯井等不铺地板的区域 `{rect}` 或 `{poly}` |
| `dims` | 尺寸链 `[是否水平, 标注线位置, 起点, [分段...]]`，省略时自动标总长总宽 |
| `entry` | 入户箭头 `{from:[x,y],to:[x,y],label:[x,y]}` |
| `furniture` | `[类型,名称,cx,cy,宽,深,旋转,颜色?]`，类型见家具库 |

openings：

```jsonc
{"type":"window","at":[0,1000,0,1600],"sill":1100,"head":1900}   // 窗台高 / 窗顶高 mm
{"type":"door","at":[x0,y0,x1,y1],"hinge":"start|end","swing":[0,1],"name":"浴室门","entry":false}
{"type":"slide","at":[...],"head":2000,"glass":false}             // 推拉门 / 衣柜门
{"type":"open","at":[...],"head":2100}                            // 无门洞口
```

- `hinge`：铰链在 `at` 的起点还是终点；`swing`：门扇开向哪一侧（单位向量）。
- 地面材料 `mat`：wood 橡木 / walnut 胡桃木 / tile800 / tile600 / antislip 防滑砖 / marble / terrazzo / carpet / tatami 榻榻米 / pale 浅色木地板 / ryukyu 琉球榻榻米（无边方块）。
- `counted:false` 不计入使用面积（门廊、阳台）；`bay:true` 是飘窗（3D 抬高 45cm）。

旧写法 `format: "rect"`（墙和门窗直接写矩形）仍然支持，见 `plans/demo.json`。

## 工具

```bash
python3 tools/wall_lines.py 间取图.png x0 y0 x1 y1   # 找墙线像素位置
python3 tools/check_plan.py plans/<id>.json 97.29     # 面积 / 帖数核对
python3 tools/build_single.py plans/<id>.json out.html  # 生成单文件网页
```
