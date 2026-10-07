# 光标特效（cursor-effect）

## 什么时候需要
让元素或页面对指针位置有反应：CTA 被磁吸、卡片上的聚光、作品列表悬停出现缩略图、自定义光标。分两类：**局部响应**（只影响一个元素，离开就恢复）和**全局光标替换**（隐藏系统光标、全页拖尾）。后者一律算主导效果。
不需要的情况：任何要在触屏上用的核心交互（触屏没有悬停）；Operate 页面；能用普通 `:hover` 状态说清楚的地方。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | 局部：`reactbits:magnet`（Persuade 的主 CTA） | 零依赖，只改 `transform: translate3d`，有 `disabled` prop，可以按需关掉；离开范围就回到原位，不影响点击区域。缺点：每次 `mousemove` 都 setState 重渲染、每个实例挂一个 window 监听，不处理减弱动效。一页只给 1 个按钮用 |
| uiarc | `uiarc:floating-button-group` | 一个共享高亮按指针或键盘焦点在按钮间 morph，方向键、Home/End 都支持，源码里有减弱动效分支。属于"指针跟随"但仍是功能性状态，符合 uiarc 的克制风格 |
| 没有底座或其他 | `reactbits:magnet`；作品列表用 `obsidianui:hover-img` | hover-img 悬停标题时出现跟随鼠标的缩略图，适合作品集列表；依赖 gsap，没有减弱动效和触屏处理，接入时补 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 卡片聚光（Persuade 功能区块） | `reactbits:spotlight-card` | 零依赖，overlay 只改 radial-gradient 和 opacity，键盘聚焦时也会亮。写死了 `bg-neutral-900`、`border-neutral-800`，要换成主底座 token。第 3 级风险（光晕） |
| 作品集、Experience 页面的全局自定义光标 | `reactbits:target-cursor` | gsap；源码会检测触屏/移动端并直接不启用，卸载时恢复 `document.body.style.cursor`。算 1 个主导效果 |
| 3D 倾斜卡片 | 见 fun-3d 指南（`jakubantalik:transition:3d-tilt` 跳过触屏、减弱动效下变平） | |
| 类 macOS Dock 的距离放大 | `bencho:dock` | 有 `aria-label`、`aria-current`、`:focus-visible` 描边，图标用 lucide；需要映射 `--ink` 等 token（见 `_styles.md`），没有减弱动效 |
| 链接悬停预览 | `shadcn:hover-card` | 这其实是浮层，不是光标特效；键盘聚焦也能触发，Operate 页面可用 |

## 慎用
- `reactbits:splash-cursor`：WebGL 流体模拟，默认 `DYE_RESOLUTION=1440`；渲染循环的 `requestAnimationFrame` 在卸载时**没有取消**（源码只移除了首次 mouse/touch 监听），路由切换后会继续跑；不处理减弱动效。不推荐；Experience 页面确实要用，至少补卸载清理和 reduce 时不挂载。
- `reactbits:blob-cursor`、`reactbits:ghost-cursor`（three）、`reactbits:pixel-trail`（react-three-fiber）、`reactbits:ribbons`（ogl）：全局拖尾，都是主导效果；依赖重，没有减弱动效。只在 Experience 页面考虑一个。
- `reactbits:crosshair`：源码没有任何触屏判断，移动端会留下一个不跟手的准星。
- `reactbits:image-trail`：1400 多行，gsap，多变体；图片拖尾会遮挡内容，只用于作品集首屏。
- `reactbits:cursor-grid`、`reactbits:border-glow`、`reactbits:dot-field`、`reactbits:ferrofluid`、`reactbits:glow-cursor`：第 3 级风险（光晕，部分还有网格背景）。只在 Persuade 一处使用，并确认压在上面的文字对比度。
- `reactbits:specular-button`：ogl 着色器做按钮高光，第 3 级风险（毛玻璃）；一个按钮挂一个 WebGL 上下文不划算，用 CSS 渐变高光替代。
- `reactbits:text-cursor`、`reactbits:scrambled-text`、`reactbits:tech-text`：文字被光标打乱或拖尾，影响可读性；tech-text 还有第 3 级风险（弹跳）。
- `originkit:dot-cursor`、`originkit:multi-effect-cursor`、`originkit:liquid-mask-cursor` 等（需登录）：全局光标替换，同上。免费替代：`reactbits:target-cursor`。

## 页面模式约束
- Operate：0 个。不改系统光标、不做聚光和磁吸。允许的只有普通 hover 状态和 `uiarc:floating-button-group` 这类同时支持键盘的功能性高亮。
- Persuade：局部响应（磁吸 CTA、聚光卡片）算装饰动效，每屏最多 1 处；全局光标替换算主导效果，计入首屏 1 个的预算，通常不值得。
- Read：不用。
- Experience：最多 1 个全局光标效果，为作品服务。

## 接入要点
- **只在精确指针上启用**：用 `matchMedia('(hover: hover) and (pointer: fine)')` 判断，触屏设备不挂载（reactbits 里只有 target-cursor 自己做了判断，magnet、spotlight-card、crosshair、hover-img 都没有）。
- **减弱动效**：抽查的 reactbits 光标组件都没有处理 `prefers-reduced-motion`；reduce 时不挂载全局光标，局部效果（magnet）传 `disabled`。
- **不要隐藏系统光标而不恢复**：替换光标的组件卸载、窗口失焦、指针离开页面时都要恢复；输入框、文本区域里保留文本光标（I-beam）。
- **不影响点击区域**：磁吸只移动内层视觉，外层 wrapper 不动（magnet 就是这样实现的）；光标层 `pointer-events: none`。
- **键盘等价**：聚光、高亮类效果在键盘聚焦时也要有对应状态（spotlight-card 做了 focus，floating-button-group 做了键盘导航）。
- **性能**：`mousemove` 里用 rAF 节流、直接写 transform 或 CSS 变量，不要每次都 setState（magnet、spotlight-card 都是 setState，单个实例可以接受，列表里每张卡都挂就会卡）。
- **颜色**：聚光、光晕颜色从主底座取，强度低（opacity 0.1–0.25）。

## 候选清单
- `reactbits:magnet` — Persuade 主 CTA 的磁吸，零依赖
- `uiarc:floating-button-group` — uiarc 项目的指针/键盘共享高亮
- `obsidianui:hover-img` — 作品列表悬停缩略图，依赖 gsap
- `reactbits:spotlight-card` — 卡片聚光（第 3 级风险），需换 token
- `reactbits:target-cursor` — Experience 页面的全局光标，触屏自动关闭
- `bencho:dock` — Dock 距离放大，需 token 映射
- `shadcn:hover-card` — 链接悬停预览（浮层）
- `reactbits:splash-cursor` — 不推荐，卸载不清理
- `reactbits:blob-cursor` — 全局拖尾，仅 Experience
- `reactbits:crosshair` — 无触屏处理，慎用
- `reactbits:cursor-grid` — 光标点亮网格（第 3 级风险）
- `originkit:dot-cursor` — 需登录，免费替代 `reactbits:target-cursor`
