# AI 界面（ai-ux）

## 什么时候需要
需要展示模型或 agent 的运行过程时用：聊天消息列表、流式回答、思考过程、工具调用、执行前的审批或追问、对话输入框。如果只是"提交一个请求，等结果"，一个 shadcn `spinner` 加一句状态文字就够了，不需要整套 AI 组件。

这类组件有一条硬规则：**每个动的东西都必须对应一个真实的后端状态。** 思考动画、计时器、步骤勾选、"Thought for N seconds"、流式逐字显现，都只能由真实事件驱动（SSE / AI SDK 的 `status`、`reasoning` 分片、`tool-call` / `tool-result`、`finish` / `error`）。用定时器假装在思考、假装出步骤、把已经拿到的全文再按打字速度放一遍，都属于 `_scenes.md` 第 1 级的"状态虚假"，必须修。

| UI 元素 | 必须绑定的真实状态 | 不允许 |
|---|---|---|
| 思考中文字 / 光球 / 流光 | 已发出请求、还没有收到第一个 token 或 reasoning 分片 | 收到结果后仍在播；固定时长后自动"完成" |
| "思考了 N 秒" | 第一个 reasoning 分片到 reasoning 结束的真实时间差，或服务端返回的耗时 | 组件内部计时器自己停在某个数 |
| 步骤列表、工具调用行 | 每个 `tool-call` 事件新增一行；`tool-result` 到达才打勾；出错显示失败和重试 | 预先写好的步骤按时间轴依次点亮 |
| 流式文字 | 按收到的增量追加；网络停了文字就停 | 拿到全文后用 `setInterval` 逐字放出来 |
| 审批 / 追问 | 后端真的在等待用户输入（agent 已暂停） | 演示用的"自动批准" |
| 生成中占位（图片、文件） | 有排队、生成中、完成、失败四态，失败可重试 | 进度条匀速走到 99% |

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:message-scroller` + `shadcn:message` + `shadcn:bubble` | 官方聊天件，2026 新增。message-scroller 基于 `@shadcn/react` 的 headless 实现：只在读者停在底部时跟随新内容，滚轮、触摸、键盘一动就释放；列表默认 `role="log"`、`aria-relevant="additions"`，流式时可设 `aria-busy`；用 `content-visibility:auto` 处理长对话。message / bubble 只是带 `data-slot` 的布局件，颜色全走 `--primary`、`--muted`、`--secondary`，零映射成本（源码已看） |
| shadcn | `shadcn:shimmer`（工具类） | 思考中文字。`init` 后自带，基于 currentColor，官方文档写明减弱动效时自动停；只要在"等待首个 token"期间加上 `shimmer` 类，收到内容就移除 |
| shadcn | `shadcn:questionnaire` | 审批、追问、多选确认。底层是真实 `<input type=radio/checkbox>`，焦点环、`min-h-11` 触控目标都在；比 beautifului 的审批卡更好接真实状态（源码已看） |
| uiarc | `uiarc:chat-thread` + `uiarc:text-shimmer` | chat-thread 免费，列表 `role="log" aria-live="polite"`，消息有 `sending / sent / delivered / read / failed` 状态和重试，自带输入框（Enter 发送、粘贴附件）。text-shimmer 是看过的流光里实现最好的：`active` 受控，结束时光带滑出、文字变实，减弱动效、离屏、标签页隐藏都会停，设 `aria-busy`。AI 专用的 `ai-chat`、`agent-run`、`ai-composer` 都是 Pro，不推荐 |
| 没有底座或其他 | `reactbits:thought-line` + `reactbits:status-mark` | 思考过程标题行和工具调用状态图标，都是受控 props（`working`、`elapsed`、`status`、`progress`），有 `useReducedMotion`、`sr-only role="status"`。依赖 motion 和 hugeicons，接入时把图标换成 lucide |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 想要更"AI 产品感"的思考轨迹（步骤、搜索、代码四种变体） | `beautifului:thinking-state` | 视觉和信息结构都好，结束后折叠成"Thought for Ns"。但**内部用 `STAGES` 定时器自己推进**，没有 `working` / `status` prop，`Thought for 4 seconds` 也是写死的，必须改成受控（把 `useSequence` 换成外部传入的阶段和耗时）才能上线 |
| 工具调用、代码编辑的紧凑展示 | `beautifului:tool-chips` | 可展开看 diff，按钮有 `aria-expanded`、`aria-label`；同样内置 `STEP_MS` 演示时间线，要改成按 `tool-call` 事件渲染 |
| 带 @ 引用、/ 命令、模型选择的输入框 | `beautifului:prompt-bar` 或 `reactbits:prompt-bar` | 功能全。beautifului 版处理了输入法组合（`isComposing`），但 @ 和 / 菜单项是 `div role="button"`，没有 listbox / combobox 语义，要补；还依赖 `glimm` 做切换模型时的彩虹扫光（第 3 级，Operate 页面去掉）。reactbits 版依赖 hugeicons，要换 lucide。只要普通输入框时用 shadcn `input-group` + `textarea` |
| agent 正在做什么的小图标（搜索、写作、连接、规划） | `librariesdev:thinking-orbs` | 2D canvas，零依赖，九种状态各对应一种真实活动；作者规则：等待不足 2 秒不显示、长列表里一次只显示一个；减弱动效降为静帧，离屏暂停。`state` 必须跟着后端当前步骤切换，不要固定一个状态循环 |
| 多个并行任务的状态行 | `beautifului:task-rows` 或 `reactbits:lattice-loader` | task-rows 有运行中 / 失败 / 完成和子项；lattice-loader 有 `status`、`elapsed`、`role="status"`。前者同样是定时器演示，要改受控 |
| 回答里的 markdown | `shadcn:typeset` | prose 替代，按 `--font-heading`、`--font-mono` 取值；流式追加内容时不会因为样式重算闪烁 |
| 附件 | `shadcn:attachment` | `idle / uploading / processing / error / done` 五态，正好对应真实上传流程 |
| 语音输入 | `librariesdev:voice-glow` | 随麦克风音量变化，带 `useMicrophone`；彩色光晕是第 3 级风险，只在语音模式打开时出现 |
| 生图占位 | `reactbits:refine-frame` | 排队、生成、精修、完成各阶段尺寸不变，没有布局抖动；`librariesdev:img-fx` 视觉更强但要 three，只在生图是主功能时用 |

## 慎用
- `beautifului:stream-text`、`beautifului:streaming-text`：拿到**完整字符串**后用 `setInterval` / `setTimeout` 逐字放出来，是演示用的假流式。更严重的是 stream-text 在 `text` 变化时 `setCount(0)`，真流式下每来一个 token 都会从头重播。要用它的模糊边缘视觉，必须改成"已显示长度 = 已收到长度"。另外它带打字机光标（`typewriter` 风险）。
- `beautifului:loading-state`：有一个 Surfer 变体会从 Vercel Blob 拉 mp4（地铁跑酷视频），生产环境别用这个变体；计时器是组件内部 `setInterval` 从挂载算起，不等于真实耗时，要显示耗时请传入后端时间。
- `beautifului:*` 整体：foundation.css 不能整份导入 shadcn 项目（见 `_styles.md` 的 shadcn + beautifului），所有组件都有冰淇淋店演示数据；Central Icons、iconoir 要换成 lucide。
- `loadingui:text-shimmer`：效果可以，但没有处理减弱动效（motion 默认不读系统设置，除非外层包 `MotionConfig reducedMotion="user"`），而且每次渲染 `motion.create(Component)` 会重建组件。shadcn 项目直接用 `shimmer` 工具类。
- `loadingui:pulse-dot`、`loadingui:typing`、`loadingui:dots`：类 ChatGPT 的"正在输入"，可以用，但只在"已发请求、未收到首个 token"这段时间出现，收到第一段内容就撤掉，不要和流式文字同时显示。
- `shadcn:helpers-ai-sdk`、`shadcn:helpers-tanstack-ai`：假会话 transport，只用于原型和 Storybook，**上线前必须换成真实 transport**，否则就是假状态。
- `librariesdev:border-beam`：沿输入框边缘的彩虹光束（`glow`），在 Operate 页面会持续抢注意力。只在"正在等待模型响应"时短暂出现，空闲时去掉。
- `uiarc:chat-thread` 放进 AI 聊天：它是人与人的 IM 线程，`aria-live="polite"` 会在每次增量时播报，流式 AI 回复会造成屏幕阅读器刷屏。流式期间设 `aria-busy` 或只在完成后插入整条消息。
- `reactbits:category:pro-app-ui/*`、`uiarc:ai-chat`、`uiarc:agent-run`、`uiarc:ai-composer`：Pro，不推荐。用上面的免费组合实现。

## 页面模式约束
- Operate（AI 产品主界面、agent 控制台）：主导效果 0 个。允许的动效只有状态表达：思考中流光 / orb、工具调用的运行与完成、消息进入、展开收起。动效强度 1–3，流光和 orb 只在等待期间存在。光晕、彩色边框光束、彩虹扫光默认不用。
- Persuade（AI 产品落地页里演示对话）：可以用 `originkit:live-chat`（需登录）或自己用 shadcn message 拼一段演示对话，作为首屏唯一主导效果。演示必须标明是示意，不能伪装成实时数据。
- Read（文档里的 AI 问答）：只用 typeset 排版和静态状态文字，不加思考动画。
- Experience：可以用 `librariesdev:thinking-orbs` 64px 版做主角，但仍要绑定真实状态。

## 接入要点
- **状态机先行**：先把 `idle → submitted → streaming(reasoning / text / tool) → awaiting-approval → done / error / aborted` 写清楚，再把每个视觉元素挂到状态上。用 AI SDK 时直接读 `useChat` 的 `status` 和 message parts，不要另起计时器。
- **可停止**：流式期间发送按钮变成停止按钮（有 `aria-label="Stop"`），停止后保留已收到的部分并标记为中断。
- **出错**：每条 AI 消息都要有失败态和重试；工具调用失败显示在那一行，不只是 toast。
- **可访问性**：消息列表用 `role="log"`；流式期间 `aria-busy="true"`，完成后再让屏幕阅读器读整条；思考状态用一个 `role="status"` 的短文字（"正在搜索网页"），动画本身 `aria-hidden`；canvas orb 有文字标签时 `aria-hidden`，没有时给 `aria-label`。
- **键盘与输入法**：Enter 发送、Shift+Enter 换行，判断 `event.nativeEvent.isComposing`，中文输入法选词时的 Enter 不能发送。@ / 斜杠菜单用 combobox + listbox 语义，或直接用 `shadcn:command`。
- **减弱动效**：流光、orb、流式模糊边缘都要在 `prefers-reduced-motion` 下停；文字直接显示。
- **滚动**：只有读者在底部时才自动跟随（message-scroller 的 `autoScroll`），用户往上翻就不要拉回去，给一个"回到最新"按钮。
- **混用**：beautifului 进 shadcn 项目只复制 `@theme inline` 映射和用到的 keyframes，`--accent` 映射到 `--primary`；动效库统一用 `motion/react`；图标统一 lucide。
- **最常见的坑**：把演示组件原样上线，结果动画按自己的时间轴跑，和后端真实进度对不上。每接一个组件，先搜源码里的 `setTimeout` / `setInterval` / `STAGES` / `STEP_MS`，确认已全部替换成外部状态。

## 候选清单
- `shadcn:message-scroller` — 聊天滚动容器，跟随与释放、`role="log"`，默认首选
- `shadcn:message` — 消息行布局（头像、header、footer、左右对齐）
- `shadcn:bubble` — 气泡，七种变体，颜色全走 shadcn token
- `shadcn:shimmer` — 思考中文字流光工具类，自动处理减弱动效
- `shadcn:questionnaire` — 审批、追问、多选确认
- `shadcn:attachment` — 附件与上传五态
- `shadcn:typeset` — 回答里的 markdown 排版
- `shadcn:marker` — 对话中的系统提示、分隔行
- `uiarc:chat-thread` — uiarc 底座的聊天线程（IM 取向）
- `uiarc:text-shimmer` — 受控流光，结束时平滑变实
- `reactbits:thought-line` — 受控的思考标题行，带耗时
- `reactbits:status-mark` — 工具调用 / 任务状态图标
- `reactbits:lattice-loader` — 带计时和完成标记的 agent 状态行
- `librariesdev:thinking-orbs` — 按活动类型区分的思考指示器
- `beautifului:thinking-state` — 四变体思考轨迹（需改受控）
- `beautifului:tool-chips` — 工具调用与 diff chip（需改受控）
- `beautifului:prompt-bar` — 功能全的 AI 输入框（需补菜单语义）
- `beautifului:approval-card` — 多题审批卡，比 questionnaire 更有产品感
- `beautifului:task-rows` — 多任务状态行（需改受控）
- `reactbits:prompt-bar` — 另一个 AI 输入框，hugeicons 需替换
- `reactbits:refine-frame` — 生图占位，无布局抖动
- `librariesdev:voice-glow` — 语音输入光晕（`glow`）
- `loadingui:typing` — "正在输入"三点
- `originkit:live-chat` — 落地页演示对话（需登录；免费替代：shadcn message + bubble 手动编排）
- `shadcn:helpers-ai-sdk` — 仅原型用的假会话
- 仅参考：`collectui:category:ai-agents`、`collectui:category:chat-layout`、`inspora:1-37`（审批卡）、`inspora:agent-plan`、`designspells:179-loading-animations-when-performing-a-pro-search-on-perplexity`、`bencho:find:kevin-agent-pill`
