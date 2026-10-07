# 开关、勾选与滑块（toggle-slider）

## 什么时候需要
二元或少量互斥的选择，以及在连续范围里取一个大概的值：switch（立即生效的开关）、checkbox（提交后生效的独立勾选）、radio-group（少量互斥选项）、toggle / toggle-group（工具栏按下态、分段控件）、slider（音量、透明度、价格区间）。需要精确数字时用数字输入（见 `form-input.md`），选项多于 6 个时用 select（见 `select.md`）。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:switch`、`shadcn:checkbox`、`shadcn:radio-group`、`shadcn:toggle-group`、`shadcn:slider` | 全部基于 Base UI，依赖只有 `cn`；都有 `focus-visible` 3px ring 和 `aria-invalid` 样式；switch（18×32）、checkbox（16px）、radio（16px）用 `after:-inset-x-3 after:-inset-y-2` 把点击区扩大到约 40×34 / 40×32，slider 的 12px 滑块用 `after:-inset-2` 扩到 28px；switch 只动 `transform`（2026-10-07 拉取 base-nova 源码确认） |
| uiarc | `uiarc:switch`、`uiarc:checkbox`、`uiarc:radio-group`、`uiarc:segmented-control`、`uiarc:slider` | switch/checkbox 基于 Radix，radio-group 是原生 radio + fieldset/legend，segmented-control 是 `aria-pressed` 按钮组且只有选中项在 tab 序列里，slider 每个滑块 `role="slider"` 带 `aria-valuetext`，都有 `useReducedMotion` 分支（catalog + 源码）。**switch 的 CSS 写了 `:focus-visible { outline: none }` 且没有替代样式；slider 键盘聚焦时只弹出数值气泡、没有焦点框**，必须补焦点 |
| 没有底座或其他 | 原生 `<input type="checkbox">` / `type="radio"` / `type="range"` | 原生控件的键盘和读屏行为最完整；switch 用 `<button role="switch" aria-checked>` 或 `<input type="checkbox" role="switch">` |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 设置页里一行一个开关 | `shadcn:switch` + `shadcn:field`（`orientation="horizontal"`，参考 `shadcn:field-switch`）；uiarc 用 `uiarc:switch` | 整行 label 可点击，焦点样式在 field label 上统一处理 |
| 选项要带描述或价格（套餐、配送方式） | `uiarc:radio-cards`；shadcn 用 `shadcn:radio-group` + `shadcn:field` 的 choice card 写法（参考 `shadcn:field-radio`） | radio-cards 是 `role="radiogroup"`，选中用 ring + 圆点表示，不只靠颜色，不可用选项有可见原因（catalog） |
| 2–5 个视图切换（日/周/月、列表/网格） | `shadcn:toggle-group`（`type="single"`）；uiarc 用 `uiarc:segmented-control` | 切换的是视图而不是内容面板；切内容面板用 tabs |
| 定价页月付/年付切换 | `uiarc:billing-toggle`；shadcn 用 `shadcn:toggle-group` | 未拉 billing-toggle 源码，用前 fetch 确认键盘 |
| 亮/暗主题切换 | `uiarc:theme-switch-rise`（产品界面）；shadcn 用 `shadcn:mode-toggle` 示例 | uiarc catalog 自己建议安静的产品界面用 rise、展示页才用 eclipse；按钮带 `aria-pressed` 和"Switch to dark mode"标签 |
| 价格、日期等双端区间 | `shadcn:slider`（`defaultValue` 传两个值）；uiarc 用 `uiarc:slider` | 两个滑块各自可聚焦；uiarc 版支持刻度和格式化读数 |
| 前后对比图 | `bencho:image-compare` 或 `originkit:compare-slider`（**需登录**） | 都未拉源码；用前 fetch 确认滑块有 `role="slider"` 和键盘方向键，做不到就用 `shadcn:slider` 控制裁剪宽度自己拼 |
| Persuade/Experience 页想让开关有手感 | `reactbits:squish-switch` | `role="switch"`、`aria-checked`、`useReducedMotion` 都有，按住会拉伸；**但 `outline-none` 且没有任何焦点样式**，颜色默认 hex（`#27272a` 等），接入时必须补 `focus-visible` ring 并把颜色换成主底座变量 |

## 慎用
- `reactbits:elastic-slider`、`jakubantalik:transition:toggle`：⚠ bounce，第 3 级。弹性回弹放在 Operate 设置页里会显得轻佻，只用在 Persuade/Experience 的单个展示控件上。
- `reactbits:jelly-radio`、`reactbits:rubber-segment`、`reactbits:spring-check`、`reactbits:wake-slider`、`reactbits:slosh-gauge`：都是单点手感件，未拉源码；用前 fetch 确认 role、键盘和焦点样式（同系列的 squish-switch 就缺焦点样式），颜色从主底座取值。
- `bencho:liq-toggle`、`bencho:slosh`、`bencho:humidity`、`bencho:sleep`：液态/表盘类控件，依赖 framer-motion 或 liquid-gooey，要映射 token，未拉源码；只在它就是页面主角时用。
- `uiarc:theme-switch-eclipse`、`uiarc:theme-switch-split`：展示性的主题切换转场，Operate 页面用 rise 或普通 toggle。
- `uiarc:carousel`、`originkit:smooth-scroll-slider`：名字里有 slider，其实是轮播/图库，不是取值控件（见索引修正建议）。
- `obsidianui:switch`、`obsidianui:checkbox`、`obsidianui:slider` 等：Radix 版 shadcn 同构件，不要重复装。
- 用 switch 表示"提交后才生效"的选项：语义错误，改用 checkbox。用 checkbox 表示立即生效的设置：同理改用 switch。
- Pro 条目（`reactbits:pro-comparison-slider`、`uiarc:pricing-calculator`）：只当灵感。

## 页面模式约束
- **Operate**：只用主底座控件。动效限于状态切换本身（滑块位移、勾选描边），150–300ms，不加回弹以外的装饰；uiarc 的 switch 已经是临界阻尼（`bounce: 0`），可以直接用。
- **Persuade**：定价页的计费切换、主题切换可以有一处有手感的控件；其余保持底座样式。
- **Read**：文档里的主题切换、代码语言切换用 toggle-group 或 native-select。
- **Experience**：控件尽量隐形，必要时用 segmented-control。

## 接入要点
- **语义**：switch = 立即生效；checkbox = 随表单提交；radio = 互斥且选项可见；toggle-group single = 视图模式。每个控件都要有可见 label（或 `aria-label`），点击 label 能切换。
- **触控目标**：shadcn 的小尺寸控件靠 `after:` 伪元素扩大点击区，自己改样式时别删掉这些类；`size="sm"` 的 switch 只有 14×24，触屏页面不要用。
- **uiarc 焦点（必须做）**：删掉 `arc-foundation.css` 末尾的 `:is(*:focus, *:focus-visible, *:focus-within) { outline: none !important; }`，把 `--focus-ring` 从 `transparent` 改成可见色，再补：
  ```css
  :root, :root[data-theme="dark"] { --focus-ring: color-mix(in oklch, var(--foreground) 35%, transparent); }
  :where(button, input, [role="switch"], [role="checkbox"], [role="radio"], [role="slider"], [tabindex]):focus-visible { outline: 2px solid var(--foreground) !important; outline-offset: 2px; }
  ```
  uiarc:switch 的模块 CSS 自己写了 `.switch:focus-visible { outline: none; }`，所以这里的 `!important` 不能省。
- **token**：shadcn switch 开启色 `--primary`、关闭色 `--input`；slider 轨道 `--muted`、已选段 `--primary`、滑块边框 `--ring`、滑块底色写死 `bg-white`（暗色主题下仍是白色，需要时改成 `bg-background`）。
- **减弱动效**：shadcn 的过渡只有颜色和 transform，时长很短；uiarc 和 reactbits 的弹簧都有 `useReducedMotion` 分支。自写回弹、拉伸动画必须加减弱分支。
- **常见坑**：slider 的值要有文字读数（`aria-valuetext` 或旁边的数字），不能只靠滑块位置；区间滑块两个 thumb 都要有名字（"最低价""最高价"）；暗色主题下检查 switch 关闭态和背景的对比度（非文字元素至少 3:1）。

## 候选清单
- `shadcn:switch` — 立即生效的开关
- `shadcn:checkbox` — 随表单提交的勾选
- `shadcn:radio-group` — 少量互斥选项
- `shadcn:toggle-group` — 分段控件、工具栏按下态
- `shadcn:toggle` — 单个按下态按钮（加粗、静音）
- `shadcn:slider` — 单值或区间滑块
- `uiarc:switch` — uiarc 开关（补焦点后用）
- `uiarc:checkbox` — uiarc 勾选，支持 indeterminate
- `uiarc:radio-group` — uiarc 单选
- `uiarc:segmented-control` — 视图切换
- `uiarc:slider` — 带刻度和读数的滑块
- `uiarc:radio-cards` — 带描述/价格的单选卡片
- `uiarc:billing-toggle` — 月付/年付切换
- `uiarc:theme-switch-rise` — 安静的主题切换
- `reactbits:squish-switch` — 有手感的开关（补焦点、换颜色）
- `bencho:image-compare` — 前后对比滑块，未验证
- `originkit:compare-slider` — 需登录；对比滑块，免费替代见上
- `jakubantalik:transition:checkbox-check` — 只借勾选描边的过渡节奏
- `inspora:1-20` — 仅参考：切换到高级套餐的动效
- `collectui:category:range-slider` — 仅参考：区间滑块样式
