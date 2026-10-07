# 加载态（loading）

## 什么时候需要
告诉用户"系统正在处理，这块内容或这个操作还没结束"。先按位置分四种：**按钮内联**（提交、保存）、**局部区块**（列表、卡片、表格行）、**整页**（首次进入路由）、**AI 生成过程**（思考、调用工具、生成图片）。
不需要的情况：等待不足约 300ms 时不显示任何加载态（会闪一下）；能拿到真实进度时用进度条，不用无限转圈；结果已经回来但为空时用空状态，不是加载态。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:skeleton`（区块）+ `shadcn:spinner`（按钮内联）+ `shadcn:shimmer`（AI 状态行） | 都在 shadcn 自己的 token 上（`bg-muted`、currentColor），零额外依赖。spinner 自带 `role="status"`、`aria-label="Loading"`；shimmer 是 `shadcn` 包里的纯 CSS 工具类，文档写明减弱动效下自动停、`shimmer-none` 可关。skeleton 和 spinner 用的是 Tailwind 的 `animate-pulse`、`animate-spin`，**不处理减弱动效**，接入时要补（见接入要点） |
| uiarc | `uiarc:skeleton` + `uiarc:text-shimmer`；按钮用 `uiarc:button` 的 loading 状态 | 源码看过，是这一类里做得最完整的：skeleton 有 `role="status"`、`aria-busy`，脉冲只跑 11 次（约 20 秒）后停，`prefers-reduced-motion` 下关掉；传 children 时从占位交叉淡入真实内容。text-shimmer 离屏和标签页隐藏时暂停，`active=false` 时扫光滑出、文字落成实色 |
| 没有底座或其他 | `loadingui:ring`（内联）/ `loadingui:dots`（AI 回复中）+ `jakubantalik:transition:skeleton-loader-and-reveal`（区块） | loadingui 全部 currentColor、keyframes 带前缀，放进任何底座都继承文字色；但抽查的 6 个组件都没写减弱动效，`ring` 还没有 `role`/`aria-label`，要自己补。Transitions.dev 的骨架屏是纯 CSS，自带减弱动效守卫 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 按钮内联（提交、保存） | `shadcn:spinner-button` 的写法：`<Button disabled><Spinner />Saving…</Button>` | 保留文字标签，宽度基本不跳；disabled 防重复提交。uiarc 项目直接用 `uiarc:button` 的 `loading`，它会把标签变形并用弹簧过渡宽度 |
| Operate 页面的列表、表格、卡片首次加载 | `shadcn:skeleton` / `uiarc:skeleton` | 骨架屏占住真实布局的位置，加载完不跳版。Operate 页面优先骨架屏，不用居中大转圈 |
| 骨架屏到真实内容的切换 | `uiarc:skeleton`（传 children + `loading`）或 `jakubantalik:transition:skeleton-loader-and-reveal` | 两者都做了交叉淡入。Transitions.dev 版默认只脉冲 1 次（`--pulse-count: 1`）、揭示 400ms、2px 交叉模糊 |
| 能拿到真实百分比（上传、导出、批量任务） | `shadcn:progress`（uiarc 项目用 `uiarc:progress`） | 确定进度比转圈诚实；值必须来自真实进度，不能用定时器假装 |
| AI 回复生成中（聊天气泡） | `loadingui:typing` 或 `loadingui:dots` | 都有 `role="status"` 和 sr-only "Loading"，纯 CSS；需补减弱动效 |
| AI 思考/工具调用状态行（"Searching the web…"） | `shadcn:shimmer` / `uiarc:text-shimmer`；行首图标可加 `librariesdev:thinking-orbs`（size 20） | 文字本身说明在做什么。thinking-orbs 已处理减弱动效（降为静帧）、离屏和隐藏标签页暂停、`role="img"` 加按状态的 aria-label |
| AI 长等待（超过 3 秒）的工作区域 | `librariesdev:border-beam-line`，`active` 绑真实 loading 标志 | 作者规则：不足 2 秒不加效果，2 秒以上用 thinking orbs，超过 3 秒再给工作中的元素加光束；同一元素不叠两个效果 |
| AI 生成图片的占位 | `librariesdev:img-fx` | 生成中像素马赛克、完成后溶解成真图；多张卡共用一个 WebGL context，用 IntersectionObserver。需要 peer 依赖 three |
| 整页首次加载（路由级） | 页面骨架（shell + 各区块 skeleton），不用全屏遮罩 | 让导航、标题先出来，内容区占位；整页 preloader 只适合 Experience 类作品页 |

## 慎用
- `loadingui:text-shimmer`：`motion.create(Component)` 写在组件函数体里，每次父组件重渲染都会生成新的组件类型，导致整段重新挂载；底色是 `currentColor` 55% 透明度，正文对比度会被拉低。用 `shadcn:shimmer` 或 `uiarc:text-shimmer` 替代。
- loadingui 全系列（抽查 ring、skeleton、pulse-dot、typing、dots、text-shimmer）：都没有 `prefers-reduced-motion` 处理；`ring` 没有可访问名称。可以用，但按接入要点补齐。
- `loadingui:pulse-dot`：第 3 级风险（脉冲圆点）。只在表示"实时、正在进行"的状态时用（录音中、在线、流式输出中），不当装饰；减弱动效下停止缩放，保留静态圆点。
- `loadingui:bobbing-dots`：第 3 级风险（弹跳）。Operate 页面换成 `loadingui:dots`（只变透明度）。
- `librariesdev:border-beam-line`：官方文档写明 Rotate 类（`md`、`sm`、`line`）**不处理减弱动效**，要自己在 reduce 时把 `active` 设为 false；默认 `theme="dark"`，浅色页面要显式传 `theme="light"`。第 3 级风险（光晕），只给"正在为你工作"的那一个元素用。
- `beautifului:shimmer`：组件只引用 `shimmer-text` keyframes 和 `--ink`、`--ink-3`，要带上 beautifului 的 foundation 才能工作，shadcn 页面按 `_styles.md` 映射；组件里没有减弱动效（foundation 里有没有未验证）。
- `originkit:hairline-loader`、`originkit:tiles-loader`、`originkit:masthead-reveal` 等全屏 preloader（需登录）：只适合 Experience 作品页；带百分比的必须接真实加载进度，不能做成定时器假进度（第 1 级：状态虚假）。免费替代：页面骨架 + `shadcn:progress`。
- 居中的大号 spinner 盖住整个内容区：Operate 页面不用。它既不告诉用户在等什么，也挡住了已经加载好的部分。

## 页面模式约束
- Operate：0 个主导效果。只用骨架屏、按钮内联 spinner、进度条、状态行 shimmer；不用光束、光球大尺寸、全屏遮罩。同一屏同时转圈的地方不超过一处，多个区块并行加载时各自用骨架屏。
- Persuade：加载态本身不当卖点；表单提交、演示按钮按 Operate 处理。
- Read：文章区用骨架屏或直接等首屏渲染，不加 shimmer 装饰。
- Experience：允许一个整页 preloader，但要有真实进度或在 1–2 秒内结束，并且减弱动效时直接显示内容。
- AI 界面（属于 Operate）：状态行 shimmer + 小尺寸 thinking orb 可以并存（位置不同、含义不同）；同一元素或相邻元素不叠两个效果。

## 接入要点
- **减弱动效**：shadcn 的 skeleton、spinner 加 `motion-reduce:animate-none`；spinner 停转后靠文字标签说明状态（按钮里本来就有 "Saving…"）。loadingui 组件在全局 CSS 加 `@media (prefers-reduced-motion: reduce) { [class*="loading-ui"], [data-slot="skeleton"] { animation: none } }` 一类规则，或在组件上加 `motion-reduce:[animation:none]`（它们的 animation 写在 inline style 里，需用 `!important` 或改源码）。
- **可访问性**：加载区域的容器设 `aria-busy="true"`，完成后去掉；骨架块本身 `aria-hidden`，另放一个 `role="status"` 的 sr-only 文字（uiarc:skeleton 已经这样做）。完成时如需播报结果，用自己的 live region，shimmer 和 orb 都不是 live region。
- **不要假进度**：进度条的值、"Step 2 of 4"、"Reading 4 files" 都必须来自真实状态。动画不能暗示一个其实还没成功的操作已经完成。
- **延迟显示**：请求通常在 300ms 内返回时，延迟 200–300ms 再显示加载态；一旦显示，至少保持约 500ms，避免闪烁。
- **布局稳定**：骨架屏尺寸贴近真实内容；按钮 loading 时保持宽度（uiarc:button 用弹簧过渡宽度，shadcn 写法靠保留文字）。
- **shadcn:progress**：Indicator 带 `transition-all`。值高频更新（每帧）时去掉过渡，避免一直追不上；`shadcn:shimmer` 依赖相对颜色语法和 `color-mix()`，要支持旧浏览器时按文档用 `supports-*` 条件启用，否则文字可能透明。
- **thinking-orbs**：只调过 64 和 20 两档，用 CSS 放大会糊；Copy prompt 里的 `dark: boolean` 不存在，用 `theme`。站点手动切明暗时显式传 `theme`。
- **Transitions.dev 骨架屏**：骨架层和内容层都是 `position: absolute; inset: 0`，外层要有明确高度；内容层在 `.is-revealed` 之前是 `opacity: 0`，必须保证数据到达时一定会加类（失败路径也要切到错误态）。
- **motion 依赖**：loadingui 的 7 个组件、uiarc 全部动效组件用 `motion`（`motion/react`）。项目里已有 framer-motion 时统一成一个。

## 候选清单
- `shadcn:skeleton` — shadcn 项目的区块占位，补减弱动效即可
- `shadcn:spinner` — 按钮、输入框内联转圈，有 role 和 aria-label
- `shadcn:shimmer` — AI 状态行文字扫光，纯 CSS，自动遵守减弱动效
- `uiarc:skeleton` — uiarc 项目的占位，有限次脉冲、交叉淡入真实内容
- `uiarc:text-shimmer` — uiarc 项目的状态行扫光，离屏暂停、完成态落成实色
- `uiarc:button` — 自带 loading 状态的按钮
- `loadingui:ring` — 无底座时的内联转圈，需补 aria 和减弱动效
- `loadingui:dots` — 三点闪烁，只动透明度，适合 Operate
- `loadingui:typing` — 聊天"正在输入"
- `jakubantalik:transition:skeleton-loader-and-reveal` — 非 React 或想要纯 CSS 时的骨架屏加揭示
- `shadcn:spinner-button` — 按钮内联 loading 的标准写法（示例）
- `shadcn:progress` — 真实进度
- `librariesdev:thinking-orbs` — AI 思考，2 秒以上的等待
- `librariesdev:border-beam-line` — AI 超过 3 秒的工作区域，需自己补减弱动效
- `librariesdev:img-fx` — AI 生图占位，依赖 three
- `loadingui:pulse-dot` — 实时/进行中的状态点（第 3 级风险）
- `loadingui:text-shimmer` — 不推荐，见慎用
- `loadingui:bobbing-dots` — 不推荐用在 Operate，见慎用
- `originkit:hairline-loader` — 需登录，整页 preloader，仅 Experience
