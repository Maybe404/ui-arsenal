# 3D 与趣味效果（fun-3d）

## 什么时候需要
让一个物件"像实物"：产品卡片随指针倾斜、可旋转查看的 3D 模型、挂绳工牌、穹顶画廊、网页小游戏。适合产品展示、作品集、活动页、404/空状态彩蛋。
不需要的情况：信息传达用平面就能完成时；Operate 和 Read 页面；移动端为主的页面（大多数 3D 效果依赖指针，触屏上要么没反应，要么很耗电）。这一类全部算主导效果。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `reactbits:tilted-card` | 只依赖 motion，用 spring 驱动 rotateX/rotateY/scale（只动 transform），图片有 `alt`、带 figcaption；是这一类里最轻的。不处理减弱动效，也没有触屏判断，接入时补 |
| uiarc | 默认不加；需要倾斜卡片时用 `jakubantalik:transition:3d-tilt` | uiarc 风格克制，不配炫技 3D。Transitions.dev 的 3d-tilt 纯 CSS，文档写明只响应指针（跳过触屏）、减弱动效下保持平面；默认 1000px 透视、跟随 400ms、回正 1000ms |
| 没有底座或其他 | `jakubantalik:transition:3d-tilt` | 同上，零依赖；光泽层 opacity 0.32，可调低 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 真实 3D 模型（产品、商品） | `reactbits:model-viewer` | react-three-fiber + drei + three，支持 glTF/FBX、OrbitControls、环境光和接触阴影；加载时用 drei 的 `useProgress` 显示真实加载进度；`autoRotate` 默认关闭。依赖重，只在模型是页面主角时用 |
| 立体按钮（活动页、游戏化） | `obsidianui:raised-button` | 纯 CSS + cva，按颜色生成阴影，`active:scale-[0.96]`；写死了 `dark:bg-zinc-500` 和 `transition-all`，要按主底座调整 |
| 活动页的趣味物件 | `reactbits:tear-ticket` | 只依赖 motion 的撕票根交互（本次未 fetch，未验证） |
| 作品集沉浸画廊 | 见 media 指南；`reactbits:dome-gallery` 慎用 | |

## 慎用
- `reactbits:lanyard`：源码 import 了 `@react-three/fiber`、`@react-three/drei`、`@react-three/rapier`、`meshline`、`three`，还要一个 `card.glb` 模型和贴图，但 **registry 的 dependencies 是空的**，直接 `shadcn add` 装不全；物理引擎 rapier 是 WASM，体积大。只在 Experience 页面、且愿意承担依赖时用；`<Canvas>` 没有离屏暂停。
- `reactbits:model-viewer`：没有减弱动效处理（开 `autoRotate` 时要自己在 reduce 下关掉）、没有离屏暂停；要用 `dynamic(..., { ssr: false })` 懒加载，并给 Canvas 容器固定尺寸。
- `reactbits:dome-gallery`：900 多行，依赖 `@use-gesture/react`，拖拽旋转半球画廊；有部分键盘处理，不处理减弱动效。仅 Experience。
- `reactbits:ballpit`、`reactbits:hyperspeed`、`reactbits:pixel-blast`、`reactbits:laser-flow`、`reactbits:light-pillar` 等 three 背景：既是 3D 也是背景，按 background 指南的预算算，一页一个 WebGL。ballpit 有第 3 级风险（弹跳）。
- `reactbits:fluid-glass`、`reactbits:crystalized-ball`：react-three-fiber，第 3 级风险（毛玻璃，crystalized-ball 还有光晕）。玻璃折射后面的文字很难读，不要压在内容上。
- `reactbits:flying-posters`、`reactbits:infinite-spiral`：滚动驱动的 3D 图片带，会和页面滚动抢手势；仅 Experience。
- originkit 的 3D 和小游戏（`originkit:flap`、`originkit:stack-tower`、`originkit:slice-blade` 等，需登录）：小游戏适合 404/空状态彩蛋，必须能跳过、不能挡住返回首页的入口；部分是 Pro，不推荐。免费替代：`reactbits:tilted-card` / `jakubantalik:transition:3d-tilt` 做轻量的"实物感"。

## 页面模式约束
- Operate：0 个。不放 3D 物件、不放倾斜卡片。
- Persuade：首屏最多 1 个主导效果（3D 物件和 WebGL 背景二选一）；倾斜卡片属于轻量交互，功能区块里每屏最多 1 处。
- Read：不用。
- Experience：1 个，为作品服务，例如作品集的 3D 名片或模型展示；其余界面保持安静。
- 404 / 空状态彩蛋（属于所在产品的模式）：小游戏或趣味物件可以有，但主要出路（返回、重试）必须一眼可见、可用键盘到达。

## 接入要点
- **只在精确指针上启用倾斜**：`matchMedia('(hover: hover) and (pointer: fine)')`；tilted-card 没有这个判断，触屏上会在点击时抖一下。
- **减弱动效**：reduce 时倾斜卡片保持平面、模型不自动旋转、物理效果直接停在静止状态。reactbits 的 tilted-card、model-viewer、lanyard 都没处理。
- **依赖和加载**：three 系（model-viewer、lanyard、dome 以外的 three 背景）用 `dynamic(..., { ssr: false })` 懒加载，首屏先放一张静态图或海报，Canvas 准备好再替换；`dpr` 上限 1.5–2（lanyard 用了 `dpr={[1, 2]}`）。
- **离屏暂停**：react-three-fiber 的 Canvas 可以用 `frameloop="demand"` 或在离屏时卸载；不要让看不见的 3D 一直渲染。
- **可访问性**：3D 物件是装饰时 `aria-hidden`，承载信息时（产品模型）旁边给文字说明和静态图；拖拽旋转要有按钮或键盘替代。
- **颜色**：光泽、阴影、材质颜色从主底座取，raised-button 的硬编码颜色要改掉。

## 候选清单
- `reactbits:tilted-card` — 最轻的指针倾斜卡片，只依赖 motion
- `jakubantalik:transition:3d-tilt` — 纯 CSS 倾斜 + 光泽，已处理触屏和减弱动效
- `reactbits:model-viewer` — 真实 3D 模型展示，依赖 three
- `obsidianui:raised-button` — 立体按钮，需改硬编码颜色
- `reactbits:tear-ticket` — 撕票根趣味交互（本次未 fetch，未验证）
- `reactbits:lanyard` — 物理挂绳工牌，registry 漏列依赖，仅 Experience
- `reactbits:dome-gallery` — 穹顶画廊，仅 Experience
- `reactbits:fluid-glass` — 液态玻璃（第 3 级风险），仅 Experience
- `reactbits:ballpit` — 弹球池背景（第 3 级风险）
- `originkit:flap` — 需登录，404 小游戏
- `bencho:find:samfcheng-lanyard-badge` — 仅参考：挂绳工牌的交互节奏
