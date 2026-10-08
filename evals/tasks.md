# 评测任务

每个任务一节：项目（输入环境）、请求（原样发给 agent）、要看到的行为、判为失败的情况。"相关"列出这个任务检查的规则在哪里，方便失败时回去改。

---

## otp-real-verification：真实验证码，不能用演示件

- **项目**：Next.js + shadcn（base-nova），`components.json` 已有；登录页有一个普通 `<Input>` 用来填短信验证码，后端有 `POST /api/verify-code`。
- **请求**："把登录页的验证码输入换成好看一点的六格输入，要能接我们的校验接口。"
- **要看到的行为**：
  - 选 `shadcn:input-otp`（或说明为什么选 `uiarc:otp-input` 并处理底座冲突），接 `onComplete` / value 到校验接口，处理错误、重试、粘贴、`autoComplete="one-time-code"`。
  - 如果看了 `bencho:one-time-code`，指出它没有 `onComplete` 或 value 回调、只是演示（搜索结果的 ⚑ 或 fetch 列出的结论），不选它，或者写清改造量。
  - 汇报里区分"源码里看到的"和"没有实测的"（比如读屏）。
- **判为失败**：用了 bencho:one-time-code 却没说演示性质；引入 uiarc 和 shadcn 两个底座；校验失败没有错误态。
- **相关**：#3（⚑ 显示）、`guides/form-input.md`、`sources/_claims.tsv`。

## vue-antd-local：Vue + Ant Design 项目，只做局部

- **项目**：Vue 3 + Ant Design Vue，`package.json` 里没有 React；一个订单列表页，表格空的时候只显示"暂无数据"。
- **请求**："订单列表空的时候太单调了，帮我优化一下空状态。"
- **要看到的行为**：
  - 先判断技术栈不是 React，走短路径：用 Ant Design Vue 的 `Empty` 或项目已有组件，图标沿用项目在用的那套（或 Lucide 的 Vue 包），文案写清下一步操作。
  - 可以用 `find.sh --stack vue` 找纯 CSS 过渡或灵感参考，但不引入 shadcn、uiarc 或任何 React 组件。
- **判为失败**：安装 React 组件、引入 Tailwind 或 shadcn；把整页换成另一套设计。
- **相关**：#26（技术栈短路径）、#13（已有项目优先）、SKILL.md 第三节第 1 步。

## react-mui-date-range：React 但用别的组件库

- **项目**：React + MUI v6，已有 `@mui/x-date-pickers`。
- **请求**："报表页加一个日期区间筛选，带'最近 7 天、最近 30 天'预设。"
- **要看到的行为**：MUI 就是主底座，用 MUI X 的区间选择器或在它上面加预设；收藏库最多提供交互参考（比如 `uiarc:date-range-picker` 的预设和播报思路），不引入 shadcn 或 uiarc。
- **判为失败**：为这个功能装 shadcn / uiarc；图标换成另一套。
- **相关**：#13、`guides/date-time.md`、`sources/_styles.md` 混用规则 1。

## screenshot-spacing：只改间距

- **项目**：任意已有 shadcn 页面；用户附一张截图，卡片之间挤在一起。
- **请求**："这里太挤了，调一下间距。"
- **要看到的行为**：按"微调"处理：读 tokens 或相邻元素的取值，只改间距，说明依据；不查索引、不换组件、不跑整页设计流程。
- **判为失败**：换组件、加效果、改配色，或者先问一轮设计方向。
- **相关**：SKILL.md 第二节任务规模表。

## landing-new-page：新建落地页，默认不加主导效果

- **项目**：新的 Next.js 项目，还没有设计系统；产品是一个面向开发者的日志检索工具，有真实截图。
- **请求**："做一个产品落地页：首屏、三个核心功能、定价、FAQ、页脚。"
- **要看到的行为**：
  - 定一个主底座（新 React 项目从 shadcn、uiarc 里选），写设计基线；专项来源不超过 2–3 个。
  - 首屏默认不加 WebGL 背景、文字特效这类主导效果；加了的话写出"明确论点"（见 `guides/marketing-section.md`）。功能区不用三张等大"图标 + 标题 + 一段话"卡片，除非说明这几项真的平行。
  - 文案和数据不编；示例内容标明是示例。需登录的 OriginKit 区块只放在"登录后可换"。
  - 汇报包含采用和淘汰理由，以及键盘、移动端、减弱动效的检查。
- **判为失败**：默认加了主导背景且说不出论点；两个底座同页；编造的客户 logo、评价或统计数字没有标为示例。
- **相关**：#25、#13、`guides/_scenes.md` 第 2、6 节。

## ai-streaming-real-state：真实流式和工具调用

- **项目**：React + shadcn，用 Vercel AI SDK 的 `useChat`，后端会发 reasoning 分片和 tool-call / tool-result。
- **请求**："给聊天界面加上'正在思考'和工具调用的状态展示。"
- **要看到的行为**：状态挂在 `status` 和 message parts 上；等待阶段写"等待回复/处理中"，有 reasoning 分片才写"思考中"；工具调用每个 `tool-call` 一行、`tool-result` 到了才打勾，失败有重试；可停止；`aria-busy` 和 `role="log"`。如果借用 `beautifului:thinking-state` / `tool-chips`，说明要把 `STAGES` / `STEP_MS` 定时器换成外部状态。
- **判为失败**：用定时器推进步骤或伪造"思考了 N 秒"；拿到全文再逐字播放；把 debounce 之类合法的计时器也一起删掉而破坏功能不算失败，但要在汇报里说明。
- **相关**：#11、`guides/ai-ux.md`、`sources/_claims.tsv`（beautifului 条目）。

## uiarc-focus-current：上游已修复的问题不能再打旧补丁

- **项目**：React + uiarc（已装 arc-foundation），一个设置页用了 `uiarc:switch` 和 `uiarc:button`。
- **请求**："检查一下这个设置页的键盘可访问性，有问题就修。"
- **要看到的行为**：fetch 或 `claims.sh uiarc:arc-foundation` 看到当前焦点由 foundation 统一处理；用键盘实测；不删除 foundation 的焦点规则、不加 `html body :focus-visible { … !important }` 一类全局覆盖。文本框焦点偏弱可以作为建议提出。
- **判为失败**：照旧版说法删除"全局 outline: none"、或者叠加全局焦点覆盖。
- **相关**：#2、`sources/uiarc.md`「焦点」。

## no-suitable-component：收藏库里没有合适的

- **项目**：React + shadcn 的项目管理工具。
- **请求**："做一个看板，按泳道分组，每列有 WIP 上限，超了要提示。"
- **要看到的行为**：搜索后说明收藏库没有成熟的看板组件（低相关的拖拽、卡片件不硬凑），可以提一句 SKILL.md「来源一览」里没收录的库，由用户决定；用主底座组件 + 拖拽库自己实现，写清自己写的部分。
- **判为失败**：拿不相关的条目拼凑并声称是"推荐组件"；未经同意从没收录的来源取码。
- **相关**：#23、SKILL.md 第三节第 8 步。

## login-and-pro：需登录和 Pro 条目

- **项目**：React + shadcn 的营销站。
- **请求（交互式）**："首屏想要 OriginKit 的 hero-26 那种点阵背景，另外 uiarc 的 morph-nav 也挺好看。"
- **要看到的行为**：OriginKit 需要用户登录：一次性列出登录项、为什么值得登录、免费替代（比如 reactbits 的背景），等用户决定，不需要登录的部分先做；uiarc:morph-nav 是 Pro，不获取，只当灵感，用免费组件做近似效果并告诉用户。
- **判为失败**：尝试登录、注册或从页面抠付费源码；无人值守时停在登录项上不做免费替代。
- **相关**：SKILL.md 第五节、`fetch.sh` 退出码 3 / 4。

## pending-and-degraded：待审条目和不完整的刷新

- **项目**：本仓库本身（维护者视角）。在临时副本里把某个条目的 review 列设为 `changed:<今天>`，并模拟一次 Lucide Lab 列表取不到的 refresh（参考 `scripts/tests/test_refresh.py` 的做法）。
- **请求**："跑一下更新流程，把能应用的都应用上。"
- **要看到的行为**：diff 里看到 degraded 原因和"未核对"的条目，不把它们当下线；apply 前读懂提案；待审条目不被自动改成 active，用 `review.sh` 列出来交给人。
- **判为失败**：手工改 TSV 绕过 apply；用 `--accept-suspect` 却没有人工核对；把 degraded 提案里的条目标成下线。
- **相关**：#4、#7、#9。

## multi-file-variants：多文件和多变体

- **项目**：React + Tailwind 项目，用 JS 不用 TS。
- **请求**："用 React Bits 的 SplitText 做标题动画。"
- **要看到的行为**：取 `--variant JS-TW`（或说明为什么用别的变体），从"文件在：…"给出的目录拿文件，不混用之前取过的 TS 版本；registryDependencies 和依赖单独说明；按 `_claims.tsv` / 指南补减弱动效。
- **判为失败**：把 TS 文件复制进 JS 项目；漏装依赖却声称能用。
- **相关**：#5、#6。
