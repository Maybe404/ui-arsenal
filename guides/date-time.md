# 日期与时间（date-time）

## 什么时候需要
让用户选一个日期、一个日期区间或一个时间点，或者在页面上常驻一个月历。只是展示日期时直接用格式化文字（`Intl.DateTimeFormat`），不需要组件；出生日期这类离今天很远、用户心里早有答案的日期，用文本输入或年/月/日下拉比翻月历快。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:calendar` + `shadcn:popover` 组成日期选择（写法见 `shadcn:date-picker` 文档页）；时间用 `shadcn:input` `type="time"` | Calendar 封装 react-day-picker，网格、键盘方向键、`aria-selected`、禁用日期、RTL 都由 react-day-picker 负责；按钮复用 `buttonVariants`，颜色全是底座变量；依赖 `react-day-picker` 和 `date-fns`（2026-10-07 拉取 base-nova 源码确认）。官方文档的 Time Picker 示例就是 `type="time"` 原生输入，没有独立的时间组件 |
| uiarc | `uiarc:date-picker`（单日）、`uiarc:date-range-picker`（区间 + 预设）、`uiarc:time-picker`（时间） | 不依赖日期库，只依赖 motion + lucide；日期弹层 `role="dialog"`，打开时焦点移到当前日，关闭时还给触发器，Tab 移出自动关闭；日历是 `role="grid"`，roving tabindex，月份切换用 live region 播报；时间选择是 `role="listbox"`，打开时滚动到当前值、只滚动自身（catalog + 源码）。**焦点框被 arc-foundation 全局去掉**，必须补 |
| 没有底座或其他 | 原生 `<input type="date">` / `type="time"` / `type="datetime-local"` | 移动端会弹系统选择器，键盘和读屏由浏览器负责；缺点是桌面样式不可控、区间要用两个输入 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 报表筛选：区间 + "最近 7 天"等预设 | `uiarc:date-range-picker`；shadcn 参考 `shadcn:date-picker-with-range` + `shadcn:date-picker-with-presets` 组合 | uiarc 版播报起点和区间长度，离开的月份设 `inert`（catalog） |
| 预订页：月历要一直可见 | `shadcn:calendar`（不放进 popover）；uiarc 用 `uiarc:calendar` | 常驻月历比弹层更直观；用 `disabled` / `minDate` 屏蔽不可选日期 |
| 出生日期 | shadcn 文档的 Date of Birth 示例（`captionLayout="dropdown"`），或三个 `shadcn:native-select` | 年月下拉跳转，不用翻几十年 |
| 允许直接输入日期文本 | shadcn 文档的 Input 示例（输入框 + 日历按钮），或 Natural Language Picker 示例 | 键盘用户和熟练用户更快；自然语言解析依赖额外的库（文档示例，未拉源码） |
| 日期 + 时间 | `shadcn:calendar` + `shadcn:input type="time"`；uiarc 用 `uiarc:date-picker` + `uiarc:time-picker` | 两个控件各自负责一件事，比一个巨型 datetime 组件好用 |
| 手机上为主的表单 | 原生 `type="date"` / `type="time"` | 系统滚轮比自定义弹层顺手 |
| 非阿拉伯历法 | `shadcn:calendar-hijri` 示例 | react-day-picker 支持其他历法 |

## 慎用
- `shadcn:date-picker` 的 fetch 结果：`fetch.sh shadcn:date-picker` 拉到的是 new-york-v4（Radix）的 `date-picker-demo`，用了 `PopoverTrigger asChild` 和 `initialFocus`；新项目默认 Base UI，照抄会类型报错。以文档页 https://ui.shadcn.com/docs/components/base/date-picker.md 的 base 写法为准。
- `bencho:time-scrubber`：拖动刻度尺选时间，带甩动惯性和吸附，手感好但未拉源码；拖拽类控件必须另有键盘路径（方向键）和数值读出，确认后才用在 Persuade/Experience 展示位，表单里用 time-picker。
- `bencho:sleep`：环形区间表盘，适合睡眠、营业时段这类"一天中的区间"可视化；未拉源码，要映射 token，键盘未验证。
- `uiarc:timeline`：时间线展示组件，不是选择器。
- `shadcn:chart-*-interactive`、`uiarc:brush-chart`：图表里的时间范围交互，归图表任务，不当日期选择器用。
- `obsidianui:calendar`：Radix 版 shadcn 同构件，不要重复装。
- Pro 条目（`uiarc:time-dial`、`uiarc:date-reel`、`uiarc:availability-picker`、`uiarc:week-calendar`、`uiarc:booking-pill`、`reactbits:category:pro-app-ui/scheduling`）：只当灵感；预约类需求用 `shadcn:calendar` + 时段按钮组（`shadcn:toggle-group`）自己拼。

## 页面模式约束
- **Operate**：只用主底座的日历和弹层；月份切换动画 ≤ 300ms，不加装饰。筛选栏里的日期区间用紧凑触发器 + 弹层。
- **Persuade**：预约/报名页可以常驻月历，选中日期的反馈可以稍有表现，但不要给日期格子加光晕。
- **Read**：基本不需要日期选择器；更新日志按日期分组展示即可。
- **Experience**：用不到。

## 接入要点
- **时区和存储**：存 ISO 字符串（日期 `YYYY-MM-DD`，时间 `HH:mm`，时间点存 UTC），显示时再按用户时区和 locale 格式化。uiarc time-picker 显示 12 小时制、存 24 小时 `HH:mm`（catalog）。
- **locale**：shadcn Calendar 支持 react-day-picker 的 `locale`（date-fns locale），中文界面传 `zhCN`，并设置每周第一天；uiarc 按 locale 格式化显示值。
- **键盘**：日历网格内方向键移动、PageUp/PageDown 换月、Enter 选中、Esc 关闭并把焦点还给触发器。接入后实测一遍。
- **uiarc 焦点**：装了 `uiarc:arc-foundation` 时，键盘焦点由它统一画描边（文本框靠边框变色，菜单项和选项靠高亮），不用再补，也不要删它的焦点规则或加全局 `!important` 覆盖；旧版的全局 `outline: none !important` 已经移除。接入后用键盘走一遍；只借单个组件、不装 foundation 时要自己补。细节和核对版本见 `sources/uiarc.md`「焦点」。
  日历格子很密，在日历容器上设 `--focus-outline-offset: -2px`，描边画在格子内侧。
- **token**：shadcn Calendar 的格子尺寸是 `--cell-size`（默认 `--spacing(7)` = 28px）、圆角 `--cell-radius`；触屏页面把 `--cell-size` 调到 36–44px。今天和区间中段用 `--muted`，选中日期和区间两端用 `--primary`，键盘焦点用 `--ring`。
- **减弱动效**：react-day-picker 本身没有动画；popover 的进出动画见 `select.md` 的说明。uiarc 有 `useReducedMotion` 分支。
- **常见坑**：日期区间要明确"结束日是否包含"；`disabled` 日期要有原因（tooltip 或说明文字）；表单提交时日期选择器的值要进隐藏 input 或受控状态，Popover 触发器本身不带 `name`。

## 候选清单
- `shadcn:calendar` — 月历，单日/多日/区间
- `shadcn:date-picker` — 文档指南：popover + calendar 的各种组合（以 base 写法为准）
- `shadcn:date-picker-with-range` — 区间示例
- `shadcn:date-picker-with-presets` — 预设示例
- `shadcn:input` — `type="time"` 作时间输入
- `uiarc:date-picker` — uiarc 单日选择
- `uiarc:date-range-picker` — uiarc 区间 + 预设
- `uiarc:time-picker` — uiarc 时间列表
- `uiarc:calendar` — uiarc 常驻月历
- `shadcn:calendar-hijri` — 伊斯兰历示例
- `bencho:time-scrubber` — 拖动刻度选时间，仅展示位，未验证键盘
- `bencho:sleep` — 环形时段表盘，未验证
- `inspora:1-30` — 仅参考：区间选择器
- `inspora:a-calendar-booking-page` — 仅参考：预约页布局
- `collectui:category:date-picker` — 仅参考：日期选择样式
