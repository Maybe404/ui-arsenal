# 媒体展示（media）

## 什么时候需要
展示图片、视频、音频：轮播、固定比例容器、前后对比、画廊、图片生成占位、语音输入。核心是让媒体本身好看、加载稳定、能用键盘和触屏操作。
不需要的情况：只有 2–3 张图时用网格平铺而不是轮播（轮播里第 2 张以后的内容大多没人看）；关键信息不要只放在会自动切换的轮播里；作品展示页的画廊特效不能比作品还抢眼。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:carousel` + `shadcn:aspect-ratio` | 基于 Embla，源码有 `role="region"`、`aria-roledescription="carousel"`，每张 `role="group"`、`aria-roledescription="slide"`，左右方向键切换；aspect-ratio 防止图片加载时跳版。没有自动播放，也就没有暂停问题 |
| uiarc | `uiarc:carousel` + `uiarc:image-compare` | carousel 源码：自动播放时提供播放/暂停控件，悬停、键盘聚焦、拖拽、离屏、标签页隐藏时都暂停，减弱动效下不能自动轮播；image-compare 有键盘控制和减弱动效分支 |
| 没有底座或其他 | `shadcn:carousel`（可以单独复制源码，依赖 embla-carousel-react） | 依赖少、可访问性完整；没有 Tailwind 时把类名改成自己的样式 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 前后对比（修图、设计改版） | `uiarc:image-compare`；shadcn 项目用 `bencho:image-compare` | bencho 版只依赖 React（图标是内联 SVG），`role="slider"`、`aria-valuenow`、左右方向键各移 10%、有 `:focus-visible` 样式；引用 `--signal`、`--font-ui` 等 token 需要映射，没有减弱动效处理 |
| AI 生成图片的占位 | `librariesdev:img-fx` | 生成中显示像素马赛克着色器、完成后溶解成真图；所有卡共用一个 WebGL context、用 IntersectionObserver；`paused` prop 可停。需要 peer 依赖 three，文档示例在减弱动效时传 `paused` |
| 作品集列表悬停预览 | `obsidianui:hover-img` | 见 cursor-effect 指南 |
| 品牌 logo 或图片带 | `uiarc:logo-marquee` / `obsidianui:draggable-marquee` | 都是第 3 级风险（跑马灯）；uiarc 版有暂停按钮，obsidianui 版有键盘拖动和减弱动效判断，依赖 gsap |
| 语音输入的可视反馈 | `librariesdev:voice-glow-processing` | 第 3 级风险（光晕）；只在语音实际进行时显示（本次未 fetch，按 librariesdev.md 的说明） |
| 图片手风琴画廊（Persuade） | `bencho:image-accordion` / `reactbits:accordion-gallery` | hover 展开，触屏上要改成点击（本次未 fetch，未验证） |

## 慎用
- `reactbits:circular-gallery`：ogl WebGL 画廊，像素比上限 2、有键盘处理，但把 `wheel`、`mousedown`、`mousemove`、`touchstart/touchmove` 全部挂在 **window** 上——页面任何位置滚动或拖动都会转动画廊（滚轮事件不 `preventDefault`，页面同时也在滚）。只在它独占一屏的 Experience 页面用，或改成只监听容器。不处理减弱动效。
- `reactbits:carousel`：依赖 `react-icons`（要换成项目在用的图标库（项目还没定就用 lucide）），源码没有键盘处理。用 `shadcn:carousel` 替代。
- `reactbits:dome-gallery`、`reactbits:infinite-spiral`、`reactbits:flex-carousel`（第 3 级风险：毛玻璃）、`reactbits:morph-slider`（gsap + ogl）：展示型画廊，仅 Experience；都要补减弱动效。
- `obsidianui:art-gallery`：WebGL 桶形畸变无限照片墙，演示图走 obsidianui 的 CDN，上线前换成自己的资源。
- `obsidianui:skeumorphic-music-card`：用了 `next/image`，非 Next 项目要替换。
- `bencho:glass-bubble`：第 3 级风险（毛玻璃），纯展示。
- `librariesdev:voice-glow-usemicrophone`：这是麦克风权限和 MediaStream 管理的 hook，申请麦克风前要有用户主动操作和说明。
- originkit 的画廊和图片过渡（`originkit:flip-gallery`、`originkit:roundcarousel`、`originkit:noise-wipe` 等，需登录）：多为 WebGL，检查暂停和清理。免费替代：`shadcn:carousel` / `uiarc:carousel`。
- 自动轮播：没有暂停控件、不遵守减弱动效的自动轮播是第 1 级问题。

## 页面模式约束
- Operate：只用功能性的媒体组件：aspect-ratio、简单轮播（无自动播放）、图片对比、生成占位。不用 WebGL 画廊。
- Persuade：一个轮播或画廊可以作为区块主体；带 WebGL 的画廊算主导效果，计入预算。
- Read：文章配图用 aspect-ratio + 原生 `<img>`/`<figure>`，不轮播。
- Experience：作品是主角。画廊交互可以有表现力，但不能劫持整页滚动，作品图片要清晰、可放大。

## 接入要点
- **尺寸稳定**：所有图片、视频都给宽高比（`shadcn:aspect-ratio` 或 CSS `aspect-ratio`），避免加载时跳版；用响应式图片（`srcset`、Next.js `<Image>`）。
- **自动播放**：默认关闭。必须开时，提供可见的暂停按钮、悬停和键盘聚焦时暂停、离屏暂停、`prefers-reduced-motion` 下禁用（uiarc:carousel 是参照）。
- **键盘和读屏**：轮播左右键可切换、当前项可读出（"3 of 8"）；对比滑块用 `role="slider"` 和 `aria-valuenow`；装饰性图片 `alt=""`，内容图片写有意义的 alt。
- **触屏**：hover 展开的画廊、悬停预览在触屏上要换成点击或直接展示；拖拽手势不要和页面纵向滚动冲突（设置 `touch-action`）。
- **全局监听**：画廊只监听自己的容器，不要在 window 上监听 wheel/pointer（circular-gallery 的问题）。
- **WebGL 画廊**：懒加载、离屏暂停、像素比上限、卸载时释放纹理和 context；图片数量多时先加载缩略图。
- **演示资源**：obsidianui（art-gallery、v-prism、playground-navbar）和 bencho 的演示图都要替换成自己的资源。

## 候选清单
- `shadcn:carousel` — 默认轮播，Embla，ARIA 和键盘完整
- `shadcn:aspect-ratio` — 固定比例容器
- `uiarc:carousel` — uiarc 项目的轮播，自动播放有完整暂停逻辑
- `uiarc:image-compare` — 前后对比，键盘 + 减弱动效
- `bencho:image-compare` — shadcn 项目的前后对比，需 token 映射
- `librariesdev:img-fx` — AI 生图占位，依赖 three
- `uiarc:logo-marquee` — 能暂停的跑马灯（第 3 级风险）
- `obsidianui:draggable-marquee` — 可拖动图片跑马灯（第 3 级风险）
- `obsidianui:hover-img` — 作品列表悬停缩略图
- `librariesdev:voice-glow-processing` — 语音处理光晕（第 3 级风险，本次未 fetch）
- `reactbits:circular-gallery` — WebGL 环形画廊，全局监听，见慎用
- `reactbits:carousel` — 不推荐，无键盘，依赖 react-icons
- `reactbits:dome-gallery` — 仅 Experience
- `obsidianui:art-gallery` — 仅 Experience，需换演示图
- `originkit:flip-gallery` — 需登录，免费替代 `shadcn:carousel`
