---
id: magicui
name: Magic UI
url: https://magicui.design/
kind: effects
stack: React + Tailwind CSS v4 + motion（`motion/react`）；少数组件用 canvas、cobe、canvas-confetti、shiki、react-tweet
license: MIT（GitHub magicuidesign/magicui）
pro: partial（组件全部免费开源；另有付费的 Magic UI Pro 模板，不在 registry 里，未登记）
fetch: shadcn-registry
coverage: 全量：官方 registry 的 78 个组件（registry:ui）；170 个 demo 示例不单独登记（看组件文档页）；Pro 模板未登记；refresh 自动比对
catalog_checked: 2026-10-08
source_status: active
visual_style: polished marketing effects with motion and svg patterns
foundation: none
styling: tailwind-v4
motion_lib: motion
dark_mode: class
mixing_notes: 用 shadcn CLI 安装，但颜色大多不走 shadcn 变量：78 个里 32 个写死了颜色（多在 props 默认值里），只有 13 个用 bg-background 等变量，接入时把颜色换成主底座的值；只有 5 个处理了减弱动效
---
## 是什么 / 什么时候用
shadcn 生态里最常用的动效组件库之一：营销页的背景图案（点阵、网格、波纹）、文字特效（打字、渐变、模糊入场）、跑马灯、设备外框（Safari、iPhone、Android）、数字滚动、bento、dock、confetti、地球仪等。给落地页加一个有记忆点的效果，或要一个现成的设备外框、logo 跑马灯时用；产品界面的基础控件仍用主底座。

## 按需获取方法
- 目录：`curl -s https://magicui.design/r/registry.json`（250 项：78 个 registry:ui 组件、170 个 registry:example、style、lib）
- 单项：`curl -s https://magicui.design/r/{name}.json` → `files[].content` 是完整源码
- 安装：`npx shadcn@latest add https://magicui.design/r/{name}.json`
- 文档和示例：`https://magicui.design/docs/components/{name}`；示例源码是 `/r/{name}-demo.json` 这类 registry:example
- 本库：`fetch.sh magicui:{name}`

实测（2026-10-08）：`curl -s https://magicui.design/r/light-rays.json` 返回 1 个文件 `registry/magicui/light-rays.tsx`（3682 字符），依赖 `motion`。

## 使用注意
- 2026-10-08 拉取全部 78 个组件源码统计（来源级统计；指南里点名的有动画的组件已逐个登记到 `sources/_claims.tsv`，带源码 hash 和探针，搜索结果里显示为 ⚑ 缺能力）：只有 retro-grid、dia-text-reveal、icon-cloud、scroll-based-velocity、floating-3d-particles 5 个有减弱动效处理；其余循环动画（marquee、border-beam、shine-border、animated-beam、orbiting-circles、ripple 等）要自己加 `prefers-reduced-motion` 分支，并在离屏时暂停。
- canvas 类（flickering-grid、globe、glyph-matrix、particles、icon-cloud、confetti、floating-3d-particles、retro-grid）注意离屏暂停和移动端性能。
- 颜色（来源级统计；指南点名的组件里写死颜色的已登记为 hardcoded-color 结论）：2026-10-08 统计，32 个组件写死了 hex / rgb 颜色（光束、流光边框、渐变文字的默认色等），13 个用 shadcn 变量；接入时通过 props 或改源码换成主底座颜色，暗色下逐个检查。
- 动效依赖是 `motion`（不是 framer-motion）；globe 依赖 `cobe`，confetti 依赖 `canvas-confetti`，tweet-card 依赖 `react-tweet`。
- 很多效果属于 `guides/_scenes.md` 的主导效果（光束、流光边框、渐变文字），同一屏最多一个；Operate 页面不用。

## 组件清单
78 个组件，分类大致是：背景图案（dot/grid/hexagon/striped/retro/flickering/interactive grid、light-rays、ripple、warp）、文字特效（animated-gradient-text、aurora-text、hyper-text、morphing-text、sparkles-text、spinning-text、typing-animation、text-animate、text-reveal、word-rotate、line-shadow-text、highlighter 等）、按钮（shimmer、rainbow、pulsating、ripple、interactive-hover）、边框光效（border-beam、shine-border、magic-card、neon-gradient-card）、数字（number-ticker、animated-circular-progress-bar）、布局与展示（bento-grid、marquee、dock、orbiting-circles、animated-list、avatar-circles、file-tree、terminal、code-comparison）、设备外框（safari、iphone、android）、confetti、globe、cool-mode、smooth-cursor、pointer。逐条见 `sources/magicui.tsv`，或运行时 `curl -s https://magicui.design/r/registry.json`。
