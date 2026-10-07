---
id: loadingui
name: loading-ui
url: https://www.loading-ui.com/
kind: component-library
stack: React 19 + Tailwind CSS v4（shadcn 体系）；7 个组件额外依赖 motion
license: MIT（GitHub turbostarter/loading-ui）
pro: none
fetch: shadcn-registry
verified: 2026-10-07
---
## 是什么 / 什么时候用
loading-ui 是专做"加载态"的 shadcn 自定义 registry，47 个组件：环形 spinner、点状/typing 指示、文字扫光（text shimmer）、Unicode 字符动画（终端风）、骨架屏、图片分析扫描占位等。全部免费、MIT。
需要按钮内 loading、AI 回复生成中（pulse-dot / text-shimmer / typing）、列表/页面加载、CLI 风格等待时优先从这里挑，比手写 spinner 更成熟。大块内容占位只有一个简单 skeleton，复杂骨架屏仍需自己拼。

## 按需获取方法
机器可读入口全部可用、curl 直接拿（无反爬）：
- 组件索引：`https://www.loading-ui.com/r/registry.json`（shadcn registry，含每个组件的 dependencies）
- 文档索引：`https://www.loading-ui.com/llms.txt`；全文：`https://www.loading-ui.com/llms-full.txt`
- 单组件文档（MDX，含用法/props/定制说明）：`https://www.loading-ui.com/docs/components/{name}.mdx`
- 单组件源码 JSON：`https://loading-ui.com/r/{name}.json`（`files[0].content` 即 tsx 源码）
- GitHub 原始文件：`https://raw.githubusercontent.com/turbostarter/loading-ui/main/src/registry/components/loading-ui/{name}.tsx`

**方式 A：shadcn CLI（推荐）**
1. 项目需已有 React + Tailwind + `components.json`（没有就 `npx shadcn@latest init`）。
2. 在 `components.json` 的 `registries` 里加：
   ```json
   "registries": { "@loading-ui": "https://loading-ui.com/r/{name}.json" }
   ```
3. 安装：`npx shadcn@latest add @loading-ui/{name}`，文件落在 `components/loading-ui/{name}.tsx`。
   也可不配 registries 直接用 URL：`npx shadcn@latest add https://loading-ui.com/r/{name}.json`。

**方式 B：直接拉源码（无 shadcn 项目时）**
```bash
curl -sL https://loading-ui.com/r/{name}.json | python3 -c "import json,sys;print(json.load(sys.stdin)['files'][0]['content'])" > components/loading-ui/{name}.tsx
```
然后自备 `@/lib/utils` 的 `cn`（clsx + tailwind-merge），带 motion 的组件 `npm i motion`。

**实测**：`curl -sL https://loading-ui.com/r/ring.json` → 200（重定向到 www），返回 `Ring` 组件源码（SVG + 内联 `@keyframes`，`--duration` CSS 变量控制速度，1278 字节）；`/docs/components/ring.mdx` → 200 text/markdown，给出 `import { Ring } from "@/components/loading-ui/ring"; <Ring />` 及 size/颜色定制说明。

依赖：所有组件依赖 `utils`（`cn`，需 `clsx`、`tailwind-merge`）；以下 7 个另需 `motion`（`import { motion } from "motion/react"`）：spiral、bobbing-dots、pulsating-dots、text-shimmer、text-shimmer-wave、morphing-infinity、analyzing-image。

## 使用注意
- 用 `motion`（新包名，`motion/react`），不是 `framer-motion`；项目里已有 framer-motion 时要么装 motion，要么手动改 import。
- 官方站点基于 Tailwind v4 + shadcn `base-nova` 风格；组件本身只用 `size-*`、`text-*` 等基础工具类和内联 `<style>@keyframes`，v3 下大多能用（`size-*` 需要 v3.4+）。
- 颜色默认走 `currentColor`，用 `text-*` 改色、`size-*` 改尺寸；速度多数用 CSS 变量 `--duration` 或 props（如 TextShimmer 的 `duration`/`spread`/`baseColor`/`shimmerColor`）。
- 每个组件自带全局 `@keyframes loading-ui-*`，名字有前缀，不易冲突。
- 带 motion 的组件文件顶部有 `"use client"`，Next.js App Router 下可直接用；纯 CSS 组件是服务端安全的。
- Unicode 字符类（square-snake 等）依赖等宽字体渲染 `█▓▒░`，非等宽字体会抖。
- registry 中还有 `index`/`style`（registry:style，仅拉 utils）和 `utils`（registry:lib），不是可视组件，清单未列。

## 组件清单
| id | 名称 | 分类 | 一句话用途 | 获取（具体命令或URL） | 备注 |
|---|---|---|---|---|---|
| ring | Ring | 环形 spinner | 圆环缺口旋转的经典 spinner，按钮内联、页面切换通用加载 | `npx shadcn@latest add @loading-ui/ring` / https://loading-ui.com/r/ring.json | free |
| spokes | Spokes | 环形 spinner | 辐条式分段 spinner（iOS 菊花样式），轻量不定进度 | `npx shadcn@latest add @loading-ui/spokes` / https://loading-ui.com/r/spokes.json | free |
| classic | Classic | 环形 spinner | 最常见的经典 spinner，表单与通用场景 | `npx shadcn@latest add @loading-ui/classic` / https://loading-ui.com/r/classic.json | free |
| dots-ring | Dots ring | 环形 spinner | 圆点排成一圈依次闪烁的环形加载，随父容器缩放 | `npx shadcn@latest add @loading-ui/dots-ring` / https://loading-ui.com/r/dots-ring.json | free |
| spiral | Spiral | 环形 spinner | 螺旋路径运动的忙碌态动画（motion） | `npx shadcn@latest add @loading-ui/spiral` / https://loading-ui.com/r/spiral.json | 依赖 motion；free |
| swirling | Swirling | 环形 spinner | 流体漩涡效果的高动感加载 | `npx shadcn@latest add @loading-ui/swirling` / https://loading-ui.com/r/swirling.json | free |
| arc | Arc | 环形 spinner | 弧线旋转的不定进度条 | `npx shadcn@latest add @loading-ui/arc` / https://loading-ui.com/r/arc.json | free |
| dual-arc | Dual arc | 环形 spinner | 双弧线对称旋转的不定进度 | `npx shadcn@latest add @loading-ui/dual-arc` / https://loading-ui.com/r/dual-arc.json | free |
| fade-arc | Fade arc | 环形 spinner | 带渐变拖尾淡出的弧形 spinner | `npx shadcn@latest add @loading-ui/fade-arc` / https://loading-ui.com/r/fade-arc.json | free |
| concentric-ring | Concentric ring | 环形 spinner | 多层同心环嵌套旋转，技术感加载 | `npx shadcn@latest add @loading-ui/concentric-ring` / https://loading-ui.com/r/concentric-ring.json | free |
| orbit-ring | Orbit ring | 环形 spinner | 元素沿圆环轨道运行的动态加载 | `npx shadcn@latest add @loading-ui/orbit-ring` / https://loading-ui.com/r/orbit-ring.json | free |
| satellite-ring | Satellite ring | 环形 spinner | 卫星点沿环边缘绕行，适合同步/传播状态 | `npx shadcn@latest add @loading-ui/satellite-ring` / https://loading-ui.com/r/satellite-ring.json | free |
| clock-ring | Clock ring | 环形 spinner | 时钟指针式圆环，适合排程、同步、限时等待 | `npx shadcn@latest add @loading-ui/clock-ring` / https://loading-ui.com/r/clock-ring.json | free |
| quarter-ring | Quarter ring | 环形 spinner | 四分之一弧的紧凑 spinner，空间小时用 | `npx shadcn@latest add @loading-ui/quarter-ring` / https://loading-ui.com/r/quarter-ring.json | free |
| dash-ring | Dash ring | 环形 spinner | SVG 虚线描边长度变化的环，适合流式/不定进度 | `npx shadcn@latest add @loading-ui/dash-ring` / https://loading-ui.com/r/dash-ring.json | free |
| comet-spinner | Comet spinner | 环形 spinner | 带亮头和拖尾的彗星旋转，高吞吐/充满活力 | `npx shadcn@latest add @loading-ui/comet-spinner` / https://loading-ui.com/r/comet-spinner.json | free |
| pulse | Pulse | 脉冲/涟漪 | 柔和缩放的呼吸圆环，待机/平静等待 | `npx shadcn@latest add @loading-ui/pulse` / https://loading-ui.com/r/pulse.json | free |
| ripple | Ripple | 脉冲/涟漪 | 同心圆向外扩散涟漪，雷达感不定进度 | `npx shadcn@latest add @loading-ui/ripple` / https://loading-ui.com/r/ripple.json | free |
| pulse-dot | Pulse dot | 点状 | 单个呼吸脉冲圆点，聊天/AI 助手生成回复时的提示（类 ChatGPT） | `npx shadcn@latest add @loading-ui/pulse-dot` / https://loading-ui.com/r/pulse-dot.json | free |
| dots | Dots | 点状 | 三点依次闪烁，输入中/typing 指示、编辑器旁 | `npx shadcn@latest add @loading-ui/dots` / https://loading-ui.com/r/dots.json | free |
| bobbing-dots | Bobbing dots | 点状 | 上下弹跳同相位的圆点（motion），活泼加载 | `npx shadcn@latest add @loading-ui/bobbing-dots` / https://loading-ui.com/r/bobbing-dots.json | 依赖 motion；free |
| bouncing-dots | Bouncing dots | 点状 | 弹性缩放+透明度的圆点，队列/导入等内联反馈 | `npx shadcn@latest add @loading-ui/bouncing-dots` / https://loading-ui.com/r/bouncing-dots.json | free |
| typing | Typing | 点状 | 竖向波浪起伏的圆点，像按键输入，聊天/搜索/协同编辑 | `npx shadcn@latest add @loading-ui/typing` / https://loading-ui.com/r/typing.json | free |
| twin-orbit | Twin orbit | 点状 | 两个标记绕圆心对称旋转 | `npx shadcn@latest add @loading-ui/twin-orbit` / https://loading-ui.com/r/twin-orbit.json | free |
| pulsating-dots | Pulsating dots | 点状 | 缩放+透明度律动的圆点（motion） | `npx shadcn@latest add @loading-ui/pulsating-dots` / https://loading-ui.com/r/pulsating-dots.json | 依赖 motion；free |
| triple-dot-spinner | Triple dot spinner | 点状 | 三点排成小圆旋转，按钮与列表行内用 | `npx shadcn@latest add @loading-ui/triple-dot-spinner` / https://loading-ui.com/r/triple-dot-spinner.json | free |
| text-shimmer | Text shimmer | 文字 | 文字上的扫光闪烁（shimmer）效果，AI 思考中 Thinking 文案（motion） | `npx shadcn@latest add @loading-ui/text-shimmer` / https://loading-ui.com/r/text-shimmer.json | 依赖 motion；free |
| text-blink | Text blink | 文字 | 文字闪烁的加载文案 | `npx shadcn@latest add @loading-ui/text-blink` / https://loading-ui.com/r/text-blink.json | free |
| text-dots | Text dots | 文字 | 状态文字后跟动态省略号 ... | `npx shadcn@latest add @loading-ui/text-dots` / https://loading-ui.com/r/text-dots.json | free |
| text-shimmer-wave | Text shimmer wave | 文字 | 沿文字逐字波浪式扫光（motion） | `npx shadcn@latest add @loading-ui/text-shimmer-wave` / https://loading-ui.com/r/text-shimmer-wave.json | 依赖 motion；free |
| morphing-infinity | Morphing infinity | 无限/路径 | 圆形与无穷符号间变形的 SVG 动画（motion） | `npx shadcn@latest add @loading-ui/morphing-infinity` / https://loading-ui.com/r/morphing-infinity.json | 依赖 motion；free |
| infinity | Infinity | 无限/路径 | 沿无穷符号路径运动，长时间/持续加载 | `npx shadcn@latest add @loading-ui/infinity` / https://loading-ui.com/r/infinity.json | free |
| accordion-loader | Accordion Loader | Unicode 字符 | Unicode 方块字符在字符轨道上双向伸缩，终端/等宽风格 | `npx shadcn@latest add @loading-ui/accordion-loader` / https://loading-ui.com/r/accordion-loader.json | free |
| symmetric-wave | Symmetric Wave | Unicode 字符 | 十格轨道上镜像向内外脉动的字符波浪 | `npx shadcn@latest add @loading-ui/symmetric-wave` / https://loading-ui.com/r/symmetric-wave.json | free |
| square-grid | Square Grid | Unicode 字符 | 方块拖尾沿正方形外缘环绕的字符动画 | `npx shadcn@latest add @loading-ui/square-grid` / https://loading-ui.com/r/square-grid.json | free |
| square-accordion | Square Accordion | Unicode 字符 | 方形轨道上在拐角停顿、尾巴收拢的字符动画 | `npx shadcn@latest add @loading-ui/square-accordion` / https://loading-ui.com/r/square-accordion.json | free |
| conveyor-loop | Conveyor Loop | Unicode 字符 | 方块字符单向循环滚动的传送带 | `npx shadcn@latest add @loading-ui/conveyor-loop` / https://loading-ui.com/r/conveyor-loop.json | free |
| square-snake | Square Snake | Unicode 字符 | 四个字形组成的小蛇沿正方形路径移动（无轨道） | `npx shadcn@latest add @loading-ui/square-snake` / https://loading-ui.com/r/square-snake.json | free |
| infinity-square-snake | Infinity Square Snake | Unicode 字符 | 字符小蛇沿两个相连方环的无穷路径移动 | `npx shadcn@latest add @loading-ui/infinity-square-snake` / https://loading-ui.com/r/infinity-square-snake.json | free |
| infinity-track | Infinity Track | Unicode 字符 | 等宽字符单元+错峰方块遮罩的无穷轨迹 | `npx shadcn@latest add @loading-ui/infinity-track` / https://loading-ui.com/r/infinity-track.json | free |
| diamond | Diamond | Unicode 字符 | 8-bit 像素菱形，阶梯透明度，复古风等待 | `npx shadcn@latest add @loading-ui/diamond` / https://loading-ui.com/r/diamond.json | free |
| wave | Wave | 条形/其他 | 条形波浪，适合音频、同步、进度相关加载 | `npx shadcn@latest add @loading-ui/wave` / https://loading-ui.com/r/wave.json | free |
| bars | Bars | 条形/其他 | 条形活动指示器（音频播放器式），列表/密集布局 | `npx shadcn@latest add @loading-ui/bars` / https://loading-ui.com/r/bars.json | free |
| analyzing-image | Analyzing image | 场景占位 | 图片分析/计算机视觉风格的扫描占位动画（motion） | `npx shadcn@latest add @loading-ui/analyzing-image` / https://loading-ui.com/r/analyzing-image.json | 依赖 motion；free |
| skeleton | Skeleton | 场景占位 | 骨架屏占位块（skeleton），内容加载中 | `npx shadcn@latest add @loading-ui/skeleton` / https://loading-ui.com/r/skeleton.json | free |
| terminal | Terminal | 场景占位 | 终端/CLI 风格加载，面向开发者 | `npx shadcn@latest add @loading-ui/terminal` / https://loading-ui.com/r/terminal.json | free |
| wandering-eyes | Wandering eyes | 场景占位 | 一对四处张望的眼睛，俏皮品牌化加载 | `npx shadcn@latest add @loading-ui/wandering-eyes` / https://loading-ui.com/r/wandering-eyes.json | free |

## 未解决
无。（全部 47 个组件免费，无 Pro/付费项；首页的 "premium" 字样只是 text-shimmer 的描述文案，页面里的 RankGrow 是赞助商广告。）
