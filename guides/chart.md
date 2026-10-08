# 图表（chart）

## 什么时候需要
数据的形状本身就是信息：趋势、比较、占比、分布、相对目标的进度。不需要的情况：只有一两个数（直接写数字和对比，如"本月 1,234，比上月 +12%"）；读者要查具体值（用表格）；数据点少于 4 个的时间序列（写成一句话或小表格）。

先选图表类型（见文末「图表类型怎么选」），再选组件。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:chart` + 对应的 `shadcn:chart-*` 示例（如 `shadcn:chart-bar-default`、`shadcn:chart-line-default`、`shadcn:chart-area-interactive`） | 已拉源码：chart 373 行，封装 Recharts 3.8.0 的 `ChartContainer` / `ChartTooltip` / `ChartLegend`；颜色走 `ChartConfig` → `--chart-1`…`--chart-5`，按 `.dark` 分明暗。已核对 Recharts 3.8.0 源码：`accessibilityLayer` 默认开启（键盘可移动 tooltip），`isAnimationActive` 默认 `'auto'`，会读 `prefers-reduced-motion` 关掉动画 |
| uiarc | `uiarc:line-chart`、`uiarc:bar-chart`、`uiarc:donut-chart`、`uiarc:sparkline` | 已拉源码：只依赖 motion，有减弱动效分支，没有写死颜色（第一条系列用 `--accent`，其余用中性色阶）。catalog：图是 `role="img"` 并带摘要，`role="slider"` 的游标可用键盘逐点读值，另有视觉隐藏的数据表，切换范围时礼貌播报。可访问性是索引里最完整的一组 |
| 没有底座或其他 | 无独立推荐；直接用 Recharts 3，照 `shadcn:chart` 的写法组织颜色和 tooltip | 索引里没有独立的图表库来源；`reactbits:radar` 是 WebGL 雷达扫描背景，不是图表 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 时间范围可切换（7 天 / 30 天 / 90 天） | `shadcn:chart-area-interactive` / `uiarc:line-chart` | uiarc 版切换时路径形变而不是重画，图例开关是 `aria-pressed` 按钮 |
| 表格行或指标旁的小趋势 | `uiarc:sparkline` | 紧凑，可用指针或键盘拖读；shadcn 底座下用 Recharts `LineChart` 去掉坐标轴自己做 |
| 单个值对比上限或目标（配额、用量） | `uiarc:usage-meter`，其次 `uiarc:gauge` | 进度条式比仪表盘省空间、更易读；两者都有减弱动效分支，无写死颜色 |
| 一年的每日活动 | `uiarc:activity-heatmap` | GitHub 贡献图样式，已拉源码，ARIA 标记较多（17 处） |
| 一年以上的密集时间序列，要缩放 | `uiarc:brush-chart` | catalog：窗口和两个手柄都是带日期的 slider，事件标记配文字 |
| 占比里有很小的份额 | `uiarc:waffle-chart` | 10×10 单元格，每格 1%，小份额也看得见；比饼图更适合精确感知 |
| 两个时间点之间的升降和排名变化 | `uiarc:slope-chart` | 排名变化用箭头 + 数字，不只靠颜色；超过约 10 项会拥挤 |
| 话题或渠道的份额随时间变化，重在讲故事 | `uiarc:streamgraph` | 只用于叙事型看板；要读准确值时换折线或堆叠柱 |

## 慎用
- `uiarc:metric-card`：已拉源码，"标签 + 滚动计数大数字 + 上下文一行"，计数器 `animateOnView`。这接近 impeccable 拒绝的英雄数据模板；只在数字确实是页面主角、且上下文那行写清对比对象时用；几张并排时先确认每张都有对比对象和含义，凑数的合并成一行紧凑指标。catalog 也写明它不播报更新，实时变化要自己包 live region。
- `shadcn:dashboard-01` 的指标卡（`section-cards.tsx`）：同上，见 layout-card 指南。
- `shadcn:chart-radar-*`（14 个变体）：雷达图只适合 5–8 个维度、最多 2–3 组数据的画像对比；读者要精确比较时换分组柱状图。变体多不代表常用。
- `shadcn:chart-pie-*`：分类超过 5 个、或份额差小于 5 个百分点时看不出差别，换横向柱状图或 `uiarc:waffle-chart`。
- `shadcn:chart-area-gradient`：渐变填充本身没问题，但别再叠发光描边；多系列面积图用堆叠或改折线，避免互相遮挡。
- `uiarc:donut-chart`（只在不装 arc-foundation、单独借用时）：组件自身不画焦点（catalog 写明 "No focus rings are drawn"），要自己补。装了 foundation 时由它的全局描边显示焦点：无图例时环是 `tabIndex=0` 的 `role="group"`，方向键预览扇区；有图例时每行是按钮（2026-10-08 核对源码）。
- `originkit:gabriel-graph`、`originkit:star-burst-graph`（需登录）：装饰性图形，不是数据图表，不要用来展示真实数据。
- `reactbits:radar`：WebGL 雷达扫描背景，标在 chart 任务下但不是图表，按 background 指南处理。
- 参考类 `designspells:054-*`、`designspells:149-*`（Shopify / Vercel 实时大屏）：活动页的展示型可视化，只借鉴节奏，不当成后台图表的样板。

## 页面模式约束
- Operate：图表服务于读数。入场动画用库默认的短动画或关掉；不做"数字滚动 + 图表生长"的组合入场；颜色从主底座 token 来，一个看板里同一指标始终同一个颜色。
- Persuade：营销页里的图表通常是论据（增长、对比），可以有一次入场动画（不超过 500–800 ms，整页一处），数值必须真实，坐标轴不截断来夸大差异。
- Read：报告和文章里的图表要有标题、单位、数据来源和一句结论；静态即可。
- Experience：数据艺术类可视化可以有表现力，但要提供文字版或数据表。

## 接入要点
- **shadcn 焦点不可见**：`ChartContainer` 的 className 里有 `[&_.recharts-surface]:outline-hidden`、`[&_.recharts-layer]:outline-hidden`、`[&_.recharts-sector]:outline-hidden`。Recharts 的 `accessibilityLayer` 让图表可以 Tab 聚焦，但焦点框被这些类去掉了。在容器上补：`has-[:focus-visible]:ring-2 has-[:focus-visible]:ring-ring/50`，或给 `.recharts-surface:focus-visible` 写 outline。
- **shadcn 图表示例在新 style 里**：chart-* 示例只在 `new-york-v4` registry，新 style 项目要用完整 URL 安装（shadcn.md）。示例都包了一层 Card，放进已有卡片时去掉外层 Card，避免卡片套卡片。
- **颜色**：用 `--chart-1`…`--chart-5`（shadcn）或 `--accent` + 中性色阶（uiarc），不要在组件里写十六进制；明暗各配一份。系列多于 5 个时先考虑合并成"其他"或拆图，而不是加颜色。
- **不只靠颜色**：多系列折线加线型（实线、虚线）或直接在线尾标注名称；涨跌用正负号和箭头，不只用红绿。
- **数据表兜底**：uiarc 图表自带视觉隐藏的数据表；shadcn 图表没有，重要图表在旁边给一个"查看数据"切换到 `shadcn:table`，或至少写一句文字摘要。
- **uiarc 焦点**：装了 `uiarc:arc-foundation` 时，键盘焦点由它统一画描边（文本框靠边框变色，菜单项和选项靠高亮），不用再补，也不要删它的焦点规则或加全局 `!important` 覆盖；旧版的全局 `outline: none !important` 已经移除。接入后用键盘走一遍；只借单个组件、不装 foundation 时要自己补。细节和核对版本见 `sources/uiarc.md`「焦点」。
- **加载**：Operate 页面用和图表同尺寸的骨架块（`shadcn:skeleton` / `uiarc:skeleton`），不要在图表区域中央转圈；uiarc line-chart 有 `loading` 属性并会播报 "Loading"。
- **性能**：SVG 图表几千个点以内没问题；更多时先在服务端聚合或降采样。`ResponsiveContainer` 放在没有确定高度的父元素里会塌成 0，给容器定高或 `aspect-*`。

## 图表类型怎么选

部分内容改编自 ui-ux-pro-max（MIT 许可，Copyright (c) 2024 Next Level Builder）的 `charts.csv`，经人工筛选和改写；原表的十六进制配色和库推荐没有采用，颜色一律用主底座的图表 token。

### 按数据关系选

| 想表达什么 | 首选 | 什么时候别用 | 数据量提示 | 本索引里能直接用的 |
|---|---|---|---|---|
| 随时间的趋势、增减速度 | 折线图；单系列强调总量时用面积图 | 少于 4 个点（直接写数字）；没有时间维度；同图超过 5–6 条线（拆成小多图或只高亮一条） | 千点以内 SVG 即可；更多先降采样或按时间段聚合 | `shadcn:chart-line-*`、`shadcn:chart-area-*`、`uiarc:line-chart` |
| 分类之间比大小、排名 | 柱状图；分类名长或分类多时用横向柱状图 | 有时间维度（用折线）；要表达占比（用堆叠柱或 waffle） | 约 15 个分类以内最好读；20–50 个用横向柱；再多改成可排序表格 | `shadcn:chart-bar-*`、`uiarc:bar-chart` |
| 部分占整体 | 少量分类时用环形图或饼图；否则用 100% 堆叠柱或 waffle | 分类超过 5 个；份额差小于约 5 个百分点；读者需要精确值 | 最多 5–6 块，其余并为"其他" | `shadcn:chart-pie-*`、`uiarc:donut-chart`、`uiarc:waffle-chart` |
| 两个连续变量的关系、聚类、离群点 | 散点图；第三个变量用点大小时是气泡图 | 变量是分类型（用分组柱）；点太少看不出模式；移动端为主的页面 | 几百点以内 SVG；上千点用 canvas 并降低点的不透明度；再多先做六边形分箱或聚合 | 索引里没有现成件，用 Recharts `ScatterChart` |
| 二维网格上的强度（如星期 × 小时） | 热力图 | 格子很少（用柱状图）；读者要读准确值（格子里直接写数或换表格） | 日历热力图一年 365 格 | `uiarc:activity-heatmap` |
| 有先后顺序的阶段转化 | 漏斗图；每两阶段之间标转化率，突出最大流失 | 阶段不是顺序关系；数值不单调递减（用柱状图）；少于 3 个阶段 | 3–8 个阶段；再多把次要步骤合并 | 索引里没有现成件，用横向柱状图按阶段排列也可以 |
| 单个指标对比目标 | 进度条或子弹图（bullet chart） | 没有目标或基准时就只是一个数字 | 多个指标并排时用子弹图网格，比一排仪表盘省空间 | `uiarc:usage-meter`、`uiarc:gauge` |
| 预测和不确定性 | 实线画历史、虚线画预测、半透明带画置信区间 | 没有历史基线；预测置信度太低 | — | Recharts `Area` + `Line` 组合 |
| 时间序列里的异常 | 折线 + 异常点标记（形状和文字注释，不只换颜色） | 实时滚动却没有暂停控制 | — | `uiarc:brush-chart`（带事件标记） |
| 层级结构里的大小关系 | 矩形树图（treemap） | 层级超过 3 层；要精确比较兄弟节点 | 节点多时先过滤到前 N 个 | 索引里没有现成件；把可折叠的树形表格作为主视图 |
| 多个来源到多个去向的流量 | 桑基图 | 流向成环（用网络图）；来源去向对太少 | 小流量合并成"其他" | 索引里没有现成件 |
| 正负分项如何累加成总数（如利润拆解） | 瀑布图 | 分项不可加；超过约 12 根柱 | 次要分项合并 | 用 Recharts 堆叠柱模拟 |
| 多个对象在同一组属性上的画像 | 雷达图 | 维度超过 8 个；要精确比较（用分组柱）；读者不熟悉雷达图 | 每图 2–3 组数据、5–8 个维度 | `shadcn:chart-radar-*` |
| 分布、中位数、离群点 | 箱线图；样本多时可用小提琴图 | 每组样本太少；读者不熟悉统计图（改用直方图或文字） | — | 索引里没有现成件 |
| 金融 OHLC 价格 | K 线图 | 非交易场景；没有 OHLC 数据（用折线） | 同屏可见的 K 线控制在几百根以内 | 索引里没有现成件 |
| 实时监控（每秒更新） | 滚动折线或面积图，配当前值文字 | 更新频率低于每分钟一次（用定时刷新的普通折线） | 只保留最近一段窗口，旧数据降采样 | 用 Recharts 或 canvas 自己做，必须有暂停按钮 |

### 通用规则
- **不只靠颜色区分**：多系列用线型、点形状或直接标注名称；涨跌、好坏用符号和文字，红黄绿只做辅助。色盲用户和黑白打印都要能读。
- **给出文字和数据兜底**：重要图表配一句结论摘要，并能切换到数据表；键盘聚焦时能读到和悬停相同的数值。
- **饼图不是天然不可访问**，问题在于只靠颜色、没有标签。要用就直接在扇区上标百分比，并提供表格或堆叠柱视图。
- **3D 图表**：普通业务看板不用；只有 Z 轴确实承载 2D 表达不了的信息（科学、工程场景）才考虑，并且必须有 2D 投影和数据表。
- **实时更新**：必须能暂停；更新不抢焦点；遵守减弱动效设置。
- **排序**：分类没有天然顺序时按数值排序；有天然顺序（月份、年龄段、等级）时保持原顺序。
- **配色方向**：单向的量用同一色相的深浅（顺序色阶）；有正负或以某个基准为中心时才用两端发散色阶；分类数据用主底座的 `--chart-*` 系列色，不要给单系列柱状图每根柱子换颜色。
- **涨跌颜色有地区差异**：中国大陆习惯红涨绿跌，欧美多为绿涨红跌；面向哪个市场就按哪个市场的习惯，并始终配正负号。

## 候选清单
- `shadcn:chart` — Recharts 3 封装，shadcn 底座默认
- `shadcn:chart-bar-default` / `shadcn:chart-line-default` / `shadcn:chart-area-interactive` — 最常用的起点示例
- `uiarc:line-chart` / `uiarc:bar-chart` / `uiarc:donut-chart` — uiarc 底座默认，可访问性最完整
- `uiarc:sparkline` — 行内小趋势
- `uiarc:usage-meter` / `uiarc:gauge` — 单值对比上限
- `uiarc:activity-heatmap` — 年度活动热力图
- `uiarc:brush-chart` — 长时间序列缩放
- `uiarc:waffle-chart` — 小份额也可见的占比图
- `uiarc:slope-chart` — 两期对比和排名变化
- `uiarc:streamgraph` — 叙事型份额变化
- `shadcn:chart-pie-*` / `shadcn:chart-radar-*` — 按上表条件使用
- `uiarc:metric-card` — 单个数字 + 上下文，慎用
- `shadcn:dashboard-01` — 后台整页示例，指标卡部分需改造
- `originkit:gabriel-graph` / `originkit:star-burst-graph` — 需登录，装饰图形，不用于真实数据
