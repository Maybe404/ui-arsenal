---
id: animateui
name: Animate UI
url: https://animate-ui.com/
kind: component-library
stack: React + Tailwind CSS v4 + motion；交互件分 Radix、Base UI、Headless UI 三种底层实现
license: MIT + Commons Clause（GitHub imskyleen/animate-ui；可用于自己的产品，禁止转售组件本身）
pro: none
fetch: shadcn-registry
coverage: 全量：官方 registry 的 73 个 components、81 个 primitives、260 个动画图标；159 个 demo、5 个 hook、style 和 lib 不单独登记；refresh 自动比对
catalog_checked: 2026-10-08
source_status: active
visual_style: shadcn-like controls with spring motion
foundation: shadcn-compatible
styling: tailwind-v4
motion_lib: motion
dark_mode: class
mixing_notes: components-* 是带样式的 shadcn 风格件，primitives-* 是无样式的动画原语；Radix 版和 shadcn（radix 风格）同构，Base UI 版对应 shadcn base 风格，同页只选一种底层；154 个组件里只有 1 个处理了减弱动效
---
## 是什么 / 什么时候用
给 shadcn 风格组件加上弹簧动画的库：对话框、tabs、手风琴、开关、复选框、下拉菜单、popover、tooltip、sheet、sidebar 等都有带动画的版本，并分 Radix / Base UI / Headless UI 三套实现；另有文字动画原语（数字滚动、打字、拆分、高亮、滚动文字）、效果原语（倾斜、磁吸、光泽、粒子、自动高度）、背景（星空、气泡、烟花、渐变、六边形）和 260 个基于 Lucide 的动画图标。已经在用 shadcn、想让基础控件的开合和切换有动画时用；也可以只借动画图标。

## 按需获取方法
- 目录：`curl -s https://animate-ui.com/r/registry.json`（580 项；名字前缀 components- / primitives- / icons- / demo- / hooks-）
- 单项：`curl -s https://animate-ui.com/r/{name}.json`
- 安装：`npx shadcn@latest add https://animate-ui.com/r/{name}.json`（或注册 `@animate-ui` 命名空间后 `npx shadcn@latest add @animate-ui/{name}`）
- 文档：`https://animate-ui.com/docs/{components|primitives}/{group}/{name}`，例如 `/docs/components/radix/dialog`；图标总览 `/docs/icons`
- 本库：`fetch.sh animateui:{name}`

实测（2026-10-08）：`curl -s https://animate-ui.com/r/components-radix-dialog.json` 返回 `registry/components/radix/dialog/index.tsx`（4442 字符），依赖 `lucide-react`，registryDependencies `@animate-ui/primitives-radix-dialog`。

## 使用注意
- components-* 依赖同名的 primitives-*（registryDependencies 用 `@animate-ui/` 命名空间），`fetch.sh` 不连带下载，用 shadcn CLI 安装最省事。
- 2026-10-08 拉取全部 154 个 components / primitives 源码（来源级统计；指南里点名的组件已逐个登记到 `sources/_claims.tsv`，搜索结果里显示为 ⚑ 缺能力）：只有 primitives-effects-click 有减弱动效处理；弹簧开合、背景动画都要自己加 `prefers-reduced-motion` 分支（`MotionConfig reducedMotion="user"` 可以一次覆盖 motion 动画）。
- 和 shadcn 同名的件（dialog、tabs、switch 等）会覆盖 `components/ui` 下的文件：已有 shadcn 时装到别的目录，或只借动画写法。
- 动画图标依赖 `icons-icon` 基础组件和 motion；图标形状来自 Lucide，项目在用别的图标集时不要混用。

## 组件清单
components 73 个（animate、backgrounds、base、buttons、community、headless、radix 七组），primitives 81 个（animate、base、buttons、effects、headless、radix、texts），icons 260 个。逐条见 `sources/animateui.tsv`。
