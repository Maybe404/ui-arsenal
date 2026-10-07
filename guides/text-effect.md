# 文字动效（text-effect）

## 什么时候需要
让一段文字的出现、切换或数值变化本身带上含义：首屏标题入场、状态文字切换（"Saving…" → "Saved"）、数字从旧值滚到新值、AI 状态行。
不需要的情况：正文、表单标签、表格内容、导航文字；每个区块标题都做一遍"淡入上移"不算设计，只会拖慢阅读。大多数页面一处文字动效就够了。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | 标题入场：`reactbits:blur-text`；状态切换：`jakubantalik:transition:text-states-swap`；数字：`reactbits:count-up` | blur-text 只依赖 motion，按词拆分，屏幕阅读器仍能按原文读出。但它**不处理减弱动效**，初始状态是 `opacity: 0`（SSR 也输出隐藏），必须按接入要点补。text-states-swap 是纯 CSS（位移 + 模糊 + 透明度），自带减弱动效守卫。count-up 只用 motion 的 spring 写 textContent，性能好，但 SSR 输出空 span、不处理减弱动效 |
| uiarc | 标题：`uiarc:text-reveal`（首屏）/ `uiarc:in-view-title`（滚动进入）；数字：`uiarc:animated-counter`；状态：`uiarc:text-morph` | 源码看过，质量明显高于其他来源：text-reveal 是纯 CSS 动画，首帧就开始、不等 hydration，`animation-fill-mode: backwards` 保证动画结束后不留 transform/filter，另放一份 sr-only 全文，减弱动效时只剩淡入。in-view-title 对已经滚过的标题直接显示，脚本 2.4 秒没接管时 CSS 兜底显示。animated-counter 有 sr-only 完整数值、固定 locale 避免 SSR 不一致、减弱动效时直接跳到目标值 |
| 没有底座或其他 | `uiarc:text-reveal`（按 `_styles.md` 的借用条件）或 `jakubantalik:transition:texts-reveal` | text-reveal 不依赖 motion（只引用 `motionTokens` 常量和四个 CSS 变量），借用成本低；非 React 项目用 Transitions.dev 的纯 CSS 版本（texts-reveal 本次未 fetch；同系列抽查的过渡都带减弱动效守卫） |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| Persuade 首屏主标题（本页唯一的主导效果） | `uiarc:text-reveal`；shadcn 项目可用 `reactbits:split-text` | split-text 用 GSAP SplitText + ScrollTrigger，字符/单词/行都能拆，等字体加载完再拆避免抖动；依赖 gsap + @gsap/react，比 motion 重 |
| 状态文字切换（保存、同步、复制成功） | `jakubantalik:transition:text-states-swap` / `uiarc:text-morph` | 文字变化即状态变化，Operate 页面可以用；uiarc 版有 sr-only 文本和减弱动效分支 |
| AI 状态行 | 见 loading 指南：`shadcn:shimmer` / `uiarc:text-shimmer` | 扫光属于加载态，不在这里重复 |
| AI 流式输出 | `jakubantalik:transition:streaming-text` | 逐词柔和模糊浮现，有减弱动效守卫；别用打字机光标模拟流式 |
| Dashboard 数值更新（值真的变了） | `uiarc:animated-counter`；shadcn 用 `reactbits:count-up` 并补减弱动效 | 只在值变化时滚动；首屏加载不要从 0 滚上来（那是装饰，不是状态） |
| 落地页统计数字（"10,000+ teams"） | `reactbits:count-up` 或 `uiarc:animated-counter`（`animateOnView`） | 每页最多一组；数字必须真实 |
| 轮换标语（"Built for designers / developers / teams"） | `reactbits:rotating-text` | 有 sr-only 当前文本、动画层 `aria-hidden`；需补减弱动效（停在第一条）和暂停 |
| 品牌化标题的"解码"效果 | `reactbits:decrypted-text` | 有 sr-only 全文、乱码层 `aria-hidden`；只用于 Experience 或开发者向的 Persuade 页 |

## 慎用
- `reactbits:text-type`：第 3 级风险（打字机光标）。源码里 SSR 输出空字符串，文字在 JS 跑起来前完全不可见（第 1 级：内容默认不可见）；光标闪烁的 GSAP tween 在卸载时没有 kill；循环删除重打会让屏幕阅读器反复读到半截文字；不处理减弱动效。只在 Experience 或开发者工具落地页的次要位置用，并且：首屏渲染完整文本、`aria-label` 放完整句子、动画层 `aria-hidden`、reduce 时直接显示全文、`loop={false}`。
- `reactbits:shiny-text`：第 3 级风险（渐变文字）。默认 `color="#b5b5b5"`，放在白底上对比度约 2:1，直接用就是第 1 级问题；`useAnimationFrame` 一直跑，离屏也不停；不处理减弱动效。要用必须把底色改成满足 4.5:1（大字 3:1）的颜色、只放在一处徽标或短标签上，减弱动效时传 `disabled`。
- `reactbits:gradient-text`：第 3 级风险（渐变文字）。外层写死了 `cursor-pointer`、`backdrop-blur`、`mx-auto`，`showBorder` 的内底是写死的 `bg-black`；rAF 常驻；默认紫粉配色。Persuade 首屏一处可以接受，但颜色要从主底座取、文字对比度在渐变最浅处也要达标、去掉 `cursor-pointer`。
- `reactbits:scroll-velocity`、`reactbits:text-loop`、`reactbits:curved-loop`：第 3 级风险（跑马灯）。没有暂停控件，也不处理减弱动效。要用就加暂停按钮（参考 `uiarc:logo-marquee` 的做法），减弱动效时停住，内容不能只在跑马灯里出现。
- `reactbits:falling-text`：依赖 matter-js，第 3 级风险（弹跳），仅 Experience。
- `reactbits:blur-text` 默认参数：`y: ±50px`、三段关键帧、线性缓动，位移偏大，看起来像模板。改成 8–12px 位移、`cubic-bezier(0.16, 1, 0.3, 1)`，只用在一个标题上；长段落逐词模糊对性能不友好。
- `obsidianui:flip-text`：registry 只给了 tsx，**没有附带 `.flip-char` 的 keyframes 样式**，直接装上不会动；默认 `loop` 无限翻转，没有减弱动效。不推荐。
- `reactbits:glitch-text`、`reactbits:fuzzy-text`：抖动和 RGB 分离会影响可读性，只用在 404 这类装饰性标题，不用于需要读懂的信息。
- `originkit:type-sequence`（需登录，打字机）、`originkit:vector-wordmark`（需登录，渐变文字）：同上述风险。免费替代分别是 `jakubantalik:transition:text-states-swap` 和 `uiarc:text-reveal`。

## 页面模式约束
- Operate：0 个主导效果。只允许表达状态的文字变化：状态文字切换、数值真实变化时的滚动、AI 状态行。不做标题入场、不做渐变字。
- Persuade：首屏标题动效算作那 1 个主导效果；如果首屏已经有 WebGL 背景，标题就只做简单淡入或不动。整页文字动效最多 2 处，而且不在同一屏。
- Read：不用。更新日志的版本号、文档标题都保持静态。
- Experience：可以有一个标志性的文字效果，为作品服务；其余文字保持静态。

## 接入要点
- **内容默认可见**：SSR 输出必须包含完整文字。用 motion 的组件（blur-text、count-up）在减弱动效或未进入视口时，要确保 JS 失败也能看到文字（例如 count-up 先渲染最终值，进入视口后再从 from 滚过去）；uiarc 的 text-reveal / in-view-title 已经处理。
- **减弱动效**：reactbits 抽查的 9 个文字组件里，只有 rotating-text 和 decrypted-text 处理了屏幕阅读器，**没有一个处理 `prefers-reduced-motion`**。用 `useReducedMotion()` 包一层：reduce 时直接渲染纯文本。
- **屏幕阅读器**：拆成单字/单词的组件，要么像 uiarc、rotating-text、decrypted-text 那样放一份 sr-only 全文并给动画层 `aria-hidden`，要么在父元素上设 `aria-label`。不要让读屏逐字母读。
- **只动 transform、opacity、filter**：逐字符 `filter: blur()` 在长文本上很贵，只用于短标题。
- **数字**：用 `Intl.NumberFormat` 并固定 locale（count-up 写死了 `en-US`，中文站要改）；`tabular-nums` 防止数字宽度抖动。
- **颜色**：渐变/扫光的颜色从主底座 token 取（shadcn 的 `--foreground`、`--muted-foreground`、`--primary`），每个色标处都检查对比度。
- **依赖**：motion（blur-text、count-up、shiny-text、gradient-text、rotating-text、decrypted-text、scroll-velocity）和 gsap（split-text、text-type）不要为了一个文字效果两个都装。

## 候选清单
- `uiarc:text-reveal` — 首屏标题入场，纯 CSS，可访问性和兜底都做了
- `uiarc:in-view-title` — 滚动进入的区块标题，五种变体
- `uiarc:animated-counter` — 数值变化的里程表滚动
- `uiarc:text-morph` — 状态文字逐字母变形
- `reactbits:blur-text` — shadcn 项目的标题入场，需补减弱动效和可见性
- `reactbits:split-text` — GSAP 拆字入场，适合重视排版的 Persuade 首屏
- `reactbits:count-up` — 统计数字滚动，需补减弱动效
- `jakubantalik:transition:text-states-swap` — 状态文字切换，纯 CSS
- `jakubantalik:transition:texts-reveal` — 两行文字错峰入场，纯 CSS（本次未 fetch，未验证）
- `jakubantalik:transition:streaming-text` — AI 流式输出逐词浮现
- `jakubantalik:transition:spinning-counter` — 纯 CSS 数字滚轮（本次未 fetch，未验证）
- `reactbits:rotating-text` — 轮换标语，有 sr-only
- `reactbits:decrypted-text` — 解码效果，有 sr-only
- `reactbits:text-type` — 打字机，见慎用
- `reactbits:shiny-text` — 金属扫光，见慎用
- `reactbits:gradient-text` — 流动渐变字，见慎用
- `reactbits:scroll-velocity` — 滚动跑马灯，见慎用
- `obsidianui:flip-text` — 不推荐，registry 缺样式
