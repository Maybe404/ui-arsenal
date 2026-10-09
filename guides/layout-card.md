# 布局与卡片（layout-card）

## 什么时候需要
把相关内容收进一个有边界的容器（card），按需展开或收起（accordion、collapsible），在并排面板之间分配空间（resizable），限定滚动区（scroll-area），或用分隔线划分区块。不需要的情况：页面结构本身就该靠标题、间距和对齐来分层，不是每个区块都要一张卡片。

impeccable 的三条规则在这里最常被违反：
- **不要用同样大小的卡片堆出整页结构**（"图标 + 标题 + 一段话"×N）。卡片适合"可浏览的同类条目"（项目、商品、文章），不适合当版式工具。
- **卡片里不套卡片**。内层用分隔线、留白或背景色差分组。
- **不要"大数字 + 小标签"的英雄数据模板**。数字要带上下文（比较对象、时间范围、单位），见 chart 指南。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:card` + `shadcn:accordion`、`shadcn:collapsible`、`shadcn:resizable`、`shadcn:separator`、`shadcn:scroll-area` | 已拉源码：card 103 行，只依赖 `cn`，分 Header / Title / Description / Action / Content / Footer 插槽，间距走 `--card-spacing`；accordion 89 行，基于 Base UI |
| uiarc | `uiarc:card`、`uiarc:expandable-card`、`uiarc:accordion`、`uiarc:resizable-panels` | 已拉源码：card 渲染 `<article>` + h3，只有标题是按钮，内嵌操作仍可单独聚焦；`details` 打开时用 Radix Dialog 做"快速查看"；状态行走 `role="status"`。expandable-card 头部是原生 button + `aria-expanded`，收起时面板 inert。都有减弱动效分支，没有写死颜色 |
| 没有底座或其他 | 原生 `<article>` / `<section>` + `<details>`；需要展开动画时用 `jakubantalik:transition:accordion` | 已拉文档：用 `grid-template-rows: 0fr ↔ 1fr` 做高度动画，不需要 JS 测量；有减弱动效守卫；头部是 button + `aria-expanded` |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| FAQ、设置分组、帮助页 | `shadcn:accordion` / `uiarc:accordion` | uiarc 版 catalog：触发器放在标题元素里，收起后 `visibility: hidden` 退出无障碍树 |
| 单张摘要卡（订单、套餐、日志）按需展开 | `uiarc:expandable-card` | 比 accordion 轻，适合单个独立条目 |
| 编辑器、邮件、后台的左右分栏 | `shadcn:resizable` / `uiarc:resizable-panels` | uiarc 版分隔条是 `role="separator"`，带 `aria-valuenow` 和 `aria-valuetext`，折叠的面板 inert；只支持水平分栏 |
| 项目、商品等可浏览条目的网格 | `shadcn:card` / `uiarc:card` | 这是卡片该出现的地方；条目要能点进详情时用 uiarc card 的 `details` 快速查看 |
| 逐张决策（筛选、审核队列） | `uiarc:card-stack` | catalog：每个手势都有对应按钮，不强制滑动；决策和撤销有 live region 播报 |
| 落地页功能区要一处"有分量"的展示 | `reactbits:magic-bento`（⚠ glow，见慎用）或 `obsidianui:split-showcase` | 只在 Persuade 页面、作为该屏唯一的主导效果；split-showcase 已拉源码（2026-10-08），用 `useReducedMotion` 处理减弱动效，hover 时卡片弹簧位移 |

## 慎用
- `shadcn:dashboard-01` 的 `section-cards.tsx`：四张等大卡片，每张是"小标签 + 大号 `text-3xl` 数字 + 涨跌徽章"，背景 `bg-linear-to-t from-primary/5`。这个样式接近 impeccable 拒绝的英雄数据模板，但要不要改看它在页面上做什么：用户进来就要扫这几个数、每个数有对比期或目标、分组有意义（比如收入、活跃、留存），就保留卡片，只把样式统一到设计基线；只是示例数字、没有对比对象、占着首屏却不帮用户做决定，就改成一行紧凑指标（数字 + 对比期 + 迷你趋势），或者删掉。不按卡片数量或"像模板"来决定。
- `reactbits:magic-bento`（⚠ glow）：已拉源码，860 行，依赖 gsap，粒子 + 聚光 + 倾斜，约 28 处写死颜色，源码里没有 `prefers-reduced-motion` 处理，也没有任何 ARIA。只用于 Persuade 页面一处，接入时自己补减弱动效（关闭粒子和倾斜），颜色改为主底座变量。
- `reactbits:spotlight-card`（⚠ glow）：已拉源码，73 行，跟随光标的渐变光斑，无减弱动效处理；触屏没有效果。Operate 页面不用。
- `reactbits:border-glow`、`reactbits:chroma-grid`、`reactbits:cursor-grid`（均 ⚠ glow）、`reactbits:bounce-cards`（⚠ bounce）、`reactbits:tilted-card`、`reactbits:reflective-card`（会申请摄像头权限，reactbits.md）：表现型卡片，未逐个拉源码；只在 Persuade / Experience 页面，且同一屏不叠两个。
- `jakubantalik:transition:card-resize`：已拉文档，直接过渡 `width` / `height`，会触发布局。按 `_scenes.md`「动效规范」的条件，单个小元素（一张卡的紧凑 ↔ 展开）可以用；不要用在会推动整列布局的容器上，网格里多张卡同时变化时换 transform 方案或先实测。
- `bencho:tilt`、`bencho:mb-holo`、`bencho:scratch-card`：交互玩具，需要 token 映射（bencho.md），只在 Experience 页面考虑。
- `librariesdev:border-beam-md`（⚠ glow）：作者规则是等待不足 2 秒不加效果，适合"正在运行"的 AI 卡片，不是常驻装饰。
- `originkit:neon-border`、`originkit:pulsating-border`（⚠ glow，需登录）：同上，且需用户自己登录取码；免费替代是 `librariesdev:border-beam-md`。

## 页面模式约束
- Operate：用主底座的 card、accordion、resizable；卡片只用于条目列表和独立的功能块，不做外观特效；展开收起 150–300 ms。
- Persuade：功能区可以有一处 bento 或展示型卡片作为该屏主导效果；其余区块用排版和留白分层，不要整页卡片。
- Read：几乎不用卡片；正文里的提示用 callout（见 feedback 的 alert），折叠内容用 `<details>` 或 accordion。
- Experience：作品卡可以有悬停反馈，作品本身是主角，卡片边框、阴影要退后。

## 接入要点
- **语义**：可浏览条目用 `<article>` + 标题元素；整卡可点击时只让标题链接扩展点击区域（伪元素覆盖），不要把整张卡包成 `<a>` 再在里面放按钮。
- **分组不靠嵌套卡片**：shadcn Card 内部用 `Separator` 或 `CardFooter` 分区；uiarc 用 `--border`、`--surface` 区分层级。
- **减弱动效**：shadcn accordion 的展开动画来自 tw-animate-css，该库不处理 `prefers-reduced-motion`；加 `motion-reduce:animate-none`。uiarc、Transitions.dev 已自带。
- **uiarc 焦点**：装了 `uiarc:arc-foundation` 时，键盘焦点由它统一画描边（文本框靠边框变色，菜单项和选项靠高亮），不用再补，也不要删它的焦点规则或加全局 `!important` 覆盖；旧版的全局 `outline: none !important` 已经移除。接入后用键盘走一遍；只借单个组件、不装 foundation 时要自己补。细节和核对版本见 `sources/uiarc.md`「焦点」。
- **对比度**：卡片背景和页面背景的色差很小时，靠 1px 边框区分；卡片上的次要文字（`--muted-foreground` / `--text-secondary`）在卡片底色上也要 ≥ 4.5:1。
- **移动端**：网格卡片在窄屏变单列；resizable 在窄屏通常改为 tabs 或上下堆叠，拖拽分隔条在触屏上不好用。
- **性能**：带 canvas、gsap 粒子的卡片在列表里重复渲染时成本会叠加；列表里只用纯 CSS 卡片。

## 候选清单
- `shadcn:card` — shadcn 卡片，条目和功能块
- `shadcn:accordion` / `shadcn:collapsible` — 折叠内容
- `shadcn:resizable` — 可拖拽分栏
- `shadcn:separator` / `shadcn:scroll-area` — 分隔与滚动区
- `uiarc:card` — uiarc 卡片，带快速查看
- `uiarc:expandable-card` — 单张卡片按需展开
- `uiarc:accordion` / `uiarc:resizable-panels` — uiarc 底座对应件
- `jakubantalik:transition:accordion` — 无底座时的展开动画
- `uiarc:card-stack` — 逐张决策
- `reactbits:magic-bento` — 落地页一处 bento 展示，慎用
- `obsidianui:split-showcase` — 落地页分栏展示
- `jakubantalik:transition:card-resize` — 单个小元素尺寸过渡，慎用
- `reactbits:spotlight-card` / `reactbits:border-glow` / `reactbits:tilted-card` — 表现型卡片，仅 Persuade / Experience
- `librariesdev:border-beam-md` — AI 运行中状态的边框光束
- `shadcn:dashboard-01` — 后台整页 block，指标卡部分需改造
- `magicui:bento-grid` — bento 布局
- `magicui:magic-card`、`magicui:border-beam`、`magicui:shine-border` — 卡片光效（主导效果）
