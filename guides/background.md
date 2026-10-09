# 背景特效（background）

## 什么时候需要
给 Persuade 首屏或 Experience 页面一个有氛围的底：着色器渐变、光线、粒子、点阵网格。它是"主导效果"，会抢注意力。
不需要的情况：后台、表单、设置、文档、文章页——这些页面的背景就是主底座的 `--background` / `--muted`，最多一个静态的柔和渐变或纹理。能用静态 CSS（`radial-gradient`、一张压缩好的图片）达到的效果，就不要上 WebGL。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | 默认不加；Persuade 首屏有明确论点、需要主导背景时（条件见 `marketing-section.md`）用 `reactbits:grainient` | grainient 是这次看过的 reactbits 背景里工程最完整的：只依赖 ogl；IntersectionObserver 离屏暂停、`visibilitychange` 标签页隐藏暂停；像素比上限 2；ResizeObserver 跟随容器；WebGL 只建一次，改 props 只更新 uniform；有 `lightMode` 和 `color1/2/3` props，能接 shadcn 的主题色。缺点：不处理减弱动效、卸载时没有 `loseContext`，接入时补 |
| uiarc | 默认不加 | uiarc 的风格规范明确不要装饰性渐变和光晕。确实需要时按 `_styles.md`：用 `reactbits:grainient`，低饱和、取 uiarc 的 `--accent` / `--foreground` 色值，只放在 hero、不和 uiarc 控件相邻 |
| 没有底座或其他 | `reactbits:grainient`；想要光束感用 `reactbits:light-rays` | light-rays 同样只依赖 ogl，进入视口才初始化 WebGL、像素比上限 2、卸载时 `loseContext`；单色 `raysColor`，好映射到品牌色 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 登录/注册页（属于 Operate） | `shadcn:login-03` 的灰底写法 / `uiarc:login-centered` | 静态 `bg-muted`，不加动态背景 |
| 想要网格、点阵感的 Persuade 区块 | `reactbits:shape-grid` | Canvas 2D、无依赖，离屏和标签页隐藏时暂停；没做高 DPI 缩放，所以开销小但线条在 Retina 上略软。第 3 级风险（网格背景），见下方条件 |
| 暗色 hero，要低调流动 | `reactbits:dark-veil` | ogl，像素比有上限；但没有离屏暂停，要自己加（或只在首屏挂载） |
| 液态金属质感 | `obsidianui:liquid-metal` | 基于 `@paper-design/shaders-react`，`useReducedMotion` 时速度设为 0；同时依赖 motion |
| 胶片颗粒质感 | 静态噪点（SVG `feTurbulence` 或一张平铺 PNG） | 不需要动；`reactbits:noise` 的实现太贵，见慎用 |
| Experience 页面的沉浸背景 | `reactbits:grainient` / `reactbits:light-rays`，或需登录的 originkit 背景 | 一页一个；作品本身仍是主角 |

## 慎用
- `reactbits:aurora`：功能没问题（`colorStops`、`lightMode` 都能控），但 rAF 一直跑，离屏和隐藏标签页都不停；没有显式设置像素比；每帧都对每个色标 `new Color()`，产生持续的垃圾回收；只监听 window resize，容器尺寸变了不跟。清理做得对（cancelAnimationFrame + loseContext）。要用就自己加 IntersectionObserver 暂停，并把颜色解析移出渲染循环。
- `reactbits:noise`：每 2 帧在 CPU 上生成一张 1024×1024 的随机 ImageData 并 `putImageData`，持续占用主线程；尺寸写死 `100vw/100vh`；不暂停。用静态噪点纹理替代。
- `reactbits:silk`、`reactbits:beams`、`reactbits:color-bends`、`reactbits:hyperspeed`、`reactbits:pixel-blast` 等 three / react-three-fiber 背景：依赖重（three 本体数百 KB），silk 的 `<Canvas frameloop="always">` 一直渲染、不暂停。只在 Experience 页面、并且用 `dynamic(..., { ssr: false })` 懒加载时考虑。
- `reactbits:dot-grid`：依赖 gsap 和 InertiaPlugin，默认色 `#5227FF`；第 3 级风险（网格背景）。`reactbits:dot-field` 同时有光晕和网格两项第 3 级风险。
- `reactbits:ballpit`：three + gsap，第 3 级风险（弹跳），彩色小球会盖过内容，仅 Experience。
- `reactbits:grid-scan`：依赖 face-api.js 并申请摄像头，不要用在常规页面。
- `reactbits:aero-shards`、`reactbits:shape-waves`：WebGPU（vgpu），很多浏览器不支持，必须准备降级的静态背景。
- 带 ⚠ glow 的背景（`reactbits:lightfall`、`reactbits:topography`、`reactbits:web-threads`、`reactbits:gradient-blinds`、`reactbits:sliced-waves`、`reactbits:ferrofluid`）：第 3 级风险（彩色光晕）。只在 Persuade/Experience 首屏用，文字压在上面时要加不透明或半透明底板保证对比度。
- `obsidianui:v-prism`：three + postprocessing，第 3 级风险（毛玻璃），绑定 `next-themes`，演示图走 obsidianui 的 CDN。
- originkit 的约 170 个背景（全部需登录）：多为 three/WebGL 全屏，同样要检查暂停、像素比和清理。免费替代优先 `reactbits:grainient` / `reactbits:light-rays`。

## 页面模式约束
- Operate：0 个。背景就是 `--background` / `--muted`，不放任何动态背景，也不放装饰性网格。
- Persuade：首屏最多 1 个主导背景；如果首屏还有大型文字动效或 3D 物件，就只能留一个。整页最多 2 个主导效果、不在同一屏，WebGL 背景一页只放一个。
- Read：不用。
- Experience：1 个，为作品服务，作品图片/视频不能被背景抢走注意力。

## 接入要点
- **项目还没有品牌色时**（shadcn 默认的 neutral 主题，`--primary` 接近黑色）：不要自己编一套渐变色。先问用户要品牌色，或者从 getdesign 的 DESIGN.md 里借一个方向（见 `guides/design-system.md`）；用户决定前，只用中性色的低对比度版本，或者先不加背景。
- **减弱动效**：抽查的 11 个 reactbits 背景都没有处理 `prefers-reduced-motion`（只有 obsidianui:liquid-metal 处理了）。reduce 时渲染一帧后停止循环，或直接换成同色的静态 CSS 渐变。
- **暂停与清理**：没有 IntersectionObserver 的组件（aurora、dark-veil、soft-aurora、particles、silk、noise、waves、dot-grid），自己在外层加：离屏时卸载或停 rAF，`visibilitychange` 时停。卸载时确认 `cancelAnimationFrame` 和 `WEBGL_lose_context`（grainient、dark-veil 没有 loseContext）。
- **尺寸和像素比**：容器给固定高度（如 `h-[70svh]`），不要让 canvas 铺满整个可滚动文档；像素比上限 1.5–2；移动端可以降到 1 或直接用静态图。
- **颜色**：从主底座取（`getComputedStyle(document.documentElement).getPropertyValue('--primary')`，shadcn 的 oklch 需要转成 hex 再传）；切换明暗时同步改 `lightMode` / 颜色 props。
- **对比度**：压在背景上的标题和按钮，在背景最亮/最暗的帧都要满足 4.5:1（大字 3:1）。做不到就加底板或降低背景强度。
- **SSR**：Next.js 里用 `dynamic(() => import(...), { ssr: false })`，并给容器一个和背景同色的 CSS 底色，避免 WebGL 起来前闪白。
- **网格背景（第 3 级风险）**：网格线透明度低（接近 `--border`），不和卡片边框抢；不放在表单和数据表后面；光标交互型（dot-grid、dot-field）在触屏上没有意义，移动端换静态版本。

## 候选清单
- `reactbits:grainient` — Persuade 首屏的默认选择，暂停和像素比都处理了
- `reactbits:light-rays` — 光束氛围，懒初始化、有清理
- `reactbits:shape-grid` — Canvas 2D 网格，轻、会暂停（第 3 级风险）
- `reactbits:dark-veil` — 暗色低调流动，需自己加暂停
- `obsidianui:liquid-metal` — 液态金属着色器，处理了减弱动效
- `shadcn:login-03` — Operate 类页面的静态灰底
- `uiarc:login-centered` — uiarc 项目的登录页背景
- `reactbits:aurora` — 可用，但要补暂停、移出每帧分配
- `reactbits:soft-aurora` — 同 aurora 类，未见离屏暂停
- `reactbits:silk` — three 依赖，仅 Experience
- `reactbits:noise` — 不推荐，CPU 开销大
- `reactbits:dot-grid` — 光标交互点阵，依赖 gsap（第 3 级风险）
- `reactbits:ballpit` — 仅 Experience（第 3 级风险）
- `jakubantalik:site:backgrounds` — 仅参考：渐变与 Dots/Grid/Waves/Noise 静态背景的取值思路
