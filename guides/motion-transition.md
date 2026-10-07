# 过渡与入场动效（motion-transition）

## 什么时候需要
状态变化时让用户看清"什么变了、从哪来、到哪去"：弹层开合、面板展开收起、手风琴、toast 进出、tabs 指示器滑动、步骤页前进后退、滚动进入时的揭示。好的过渡表达连续性和因果，而不是装饰。
不需要的情况：每个区块都加同一种"淡入上移"；数据表格的每一行入场；任何会让用户等动画结束才能操作的地方。主底座组件（shadcn 的 dialog、popover、accordion，uiarc 的全部组件）自带过渡时，直接用自带的，不要再叠一层。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | 先用组件自带的 `data-state` 过渡；自定义过渡的参数取 `jakubantalik:transition:*`（Transitions.dev） | shadcn 组件通过 `tw-animate-css` 自带开合动画，和底座一致。需要自己写的过渡（自定义面板、状态切换），Transitions.dev 给了调好的时长和曲线，纯 CSS、`t-*` 类名前缀，每段都带 `prefers-reduced-motion` 守卫 |
| uiarc | uiarc 组件自带的过渡 + `components/arc/lib/motion-tokens.ts` 里的 `snappy/smooth/morph` | uiarc 每个动效都有减弱动效分支（看过的 skeleton、text-shimmer、text-reveal、in-view-title、animated-counter、carousel、image-compare、swipe-actions、confirm-morph 都有）。自写过渡时复用它的 token，不要再引入第二套参数 |
| 没有底座或其他 | `jakubantalik:transition:*` | 纯 CSS，没有动效库依赖；React 版首次 import 时注入 `<style>`，SSR 安全 |

Transitions.dev 已核对的默认参数（都用 `cubic-bezier(0.22, 1, 0.36, 1)`，进入慢、退出快）：

| 过渡 | 进入 / 退出 | 其他 |
|---|---|---|
| `modal-open-close` | 250ms / 150ms | scale 0.96 ↔ 1 + opacity |
| `toast-open-close` | 350ms / 250ms | 位移 16px、模糊 2px、scale 0.97 |
| `panel-reveal` | 400ms / 350ms | 位移 100px、模糊 2px |
| `accordion` | 250ms / 250ms | `grid-template-rows: 0fr ↔ 1fr`，不用 JS 量高度 |
| `page-side-by-side` | 250ms | 横向 8px、模糊 3px |
| `tabs-sliding` | 250ms | 指示器由 JS 写入 width 和 transform |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 弹层、抽屉、toast | 主底座自带；自定义时 `jakubantalik:transition:modal-open-close` / `toast-open-close` / `panel-reveal` | 时长落在 `_scenes.md` 的 150–400ms 区间，开慢关快 |
| 折叠区、FAQ、设置分组 | `jakubantalik:transition:accordion` | grid-rows 方案没有测量高度的 JS，任意内容高度都能平滑展开 |
| 分步表单、向导 | `jakubantalik:transition:page-side-by-side` | 短位移 + 模糊，方向表达前进/后退 |
| 区块标题滚动进入（Persuade） | `uiarc:in-view-title` | 已滚过的标题直接显示，脚本没加载时 2.4 秒后 CSS 兜底显示，减弱动效时直接显示 |
| 通用滚动入场包装（Persuade） | `reactbits:animated-content`，按接入要点补 | gsap + ScrollTrigger，方向、距离、缓动可调；但默认会把内容设成 `opacity: 0` 直到触发 |
| 可滚动容器边缘提示 | `shadcn:scroll-fade` | CSS scroll-driven 遮罩，没有 JS，Operate 页面可用 |
| 品牌 logo 墙 | `uiarc:logo-marquee` | 第 3 级风险（跑马灯），但它做全了：暂停/播放按钮、悬停暂停、减弱动效下停住并隐藏复制的那份列表 |
| 平滑滚动（Persuade 长页） | `obsidianui:smooth-scroll` | 基于 Lenis，动态 import；`prefers-reduced-motion` 时不启用，设置变化时会重新判断 |
| 动效参数审查 | `jakubantalik:transitions-polish-skill` / `uiarc:arc-skill` | 按时长、距离、缩放、模糊、缓动 token 检查已有代码（未本次 fetch） |

## 慎用
- `reactbits:animated-content`：挂载时 `gsap.set(el, { opacity: 0 })`，ScrollTrigger 不触发（元素在页底、rootMargin 不合适）内容就一直看不见（第 1 级：内容默认不可见）；源码里残留站点专用的 `document.getElementById('snap-main-container')`；`disappearAfter` 会让内容自己再消失；不处理减弱动效。用之前：reduce 时不设初始状态，`initialOpacity` 不要设 0（或加超时兜底），不用 `disappearAfter`。
- `reactbits:fade-content`：同为 gsap 入场包装，同类问题（本次只看了依赖，未逐行验证）。
- `jakubantalik:transition:toggle`：曲线 `cubic-bezier(0.34, 1.35, 0.64, 1)` 加 1px 过冲，第 3 级风险（弹跳）。幅度很小，在 Persuade 或偏活泼的产品里可以用；Operate 页面直接用主底座的 switch。
- `jakubantalik:transition:tabs-sliding`：指示器的 width 由 JS 写入并过渡（会触发布局），只在一个小元素上，可以接受；`:root` 里写死了 `--tabs-bar-bg: #f1f1f1` 等颜色，要换成主底座 token。
- `jakubantalik` 的 `_root.css` 公共块：和 uiarc 同页时 `--duration-fast`（250ms，uiarc 是 160ms）、`--ease-in-out` 同名不同值，只复制每个过渡自己的变量（`_styles.md` 已写明）。
- `reactbits:logo-loop`：处理了减弱动效和悬停暂停，但没有暂停按钮（第 3 级风险：跑马灯）；需要符合"能暂停"时补一个按钮，或用 `uiarc:logo-marquee`。
- `obsidianui:draggable-marquee`：第 3 级风险（跑马灯）；有键盘支持和减弱动效判断，依赖 gsap。
- `reactbits:scroll-stack`（lenis）、`reactbits:gradual-blur`、`reactbits:scroll-expand`：滚动劫持或滚动驱动的大幅变化，只在 Persuade/Experience 一处使用，Operate 不用。
- `reactbits:pixel-swap`、`reactbits:pixel-transition`、`reactbits:meta-balls`、`reactbits:ripple-distortion`：装饰性转场，表达不了状态含义，不进 Operate。

## 页面模式约束
- Operate：动效强度 1–3。只用于表达状态：弹层开合、展开收起、toast、tabs 指示器、步骤切换。不做滚动入场、不做平滑滚动、不做跑马灯。
- Persuade：滚动入场每屏最多 1 处，并且要有含义（揭示一个论点、一组对比），不是每个区块都淡入上移。允许一个 logo 跑马灯（能暂停）。
- Read：只保留目录展开、代码块复制反馈这类状态过渡；不做滚动入场和平滑滚动。
- Experience：转场可以更有表现力（500–800ms 的一处主导入场），但仍要遵守减弱动效。

## 接入要点
- **时长与曲线**：按 `_scenes.md`：100–150ms 即时反馈，150–300ms 常规状态，300–500ms 布局和弹层，500–800ms 整页唯一的主导入场；退出比进入快；默认 `cubic-bezier(0.16, 1, 0.3, 1)` 或 Transitions.dev 的 `cubic-bezier(0.22, 1, 0.36, 1)`。
- **减弱动效**：Transitions.dev 的每段 CSS 结尾都有 `@media (prefers-reduced-motion: reduce)` 守卫，复制时必须保留；reduce 时保留透明度变化，去掉位移、缩放和模糊。shadcn 用的 `tw-animate-css` 是否自动遵守减弱动效本次未验证，建议在全局补 `motion-reduce:` 或媒体查询。
- **内容默认可见**：滚动入场的初始隐藏状态必须有兜底（超时显示、或 CSS 兜底），JS 失败时内容照样能看到。
- **只动 transform、opacity**：高度变化用 grid-rows 或主底座组件的实现，不要逐帧改 height/width/margin；模糊只用 2–3px 的小值。
- **一套参数**：同一项目只保留一套时长/缓动 token（shadcn 项目可以把 Transitions.dev 的变量收进全局，uiarc 项目用它自己的 motion-tokens），不要几家混用。
- **动效库统一**：motion 和 framer-motion 只留一个；gsap 只在确实需要 ScrollTrigger、SplitText 的组件里引入。

## 候选清单
- `jakubantalik:transition:modal-open-close` — 弹层开合参数
- `jakubantalik:transition:accordion` — grid-rows 展开收起
- `jakubantalik:transition:toast-open-close` — toast 进出
- `jakubantalik:transition:panel-reveal` — 容器内面板滑出
- `jakubantalik:transition:page-side-by-side` — 分步页面切换
- `jakubantalik:transition:tabs-sliding` — tabs 指示器，需换颜色 token
- `uiarc:in-view-title` — 滚动进入的标题，带兜底
- `shadcn:scroll-fade` — 滚动容器边缘渐隐，纯 CSS
- `uiarc:logo-marquee` — 能暂停的 logo 跑马灯
- `obsidianui:smooth-scroll` — Lenis 平滑滚动，遵守减弱动效
- `reactbits:animated-content` — 通用滚动入场，需补兜底
- `reactbits:logo-loop` — logo 循环，缺暂停按钮
- `jakubantalik:transition:toggle` — 轻微过冲的开关（第 3 级风险）
- `jakubantalik:transitions-data-json` — 43 个过渡的机器可读清单，查参数用（本次未 fetch）
- `jakubantalik:article-motion-examples` — 仅参考：时长、缩放、位移的正反例
