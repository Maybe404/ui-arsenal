---
id: beautifului
name: Beautiful UI
url: https://www.beautifului.dev/
kind: component-library
stack: React（"use client"，Next.js 友好）+ Tailwind CSS v4，shadcn registry；绝大多数组件零 npm 依赖
license: MIT（站点 /license，Copyright 2026 Shane Levine）
pro: none
fetch: shadcn-registry
verified: 2026-10-07
---
## 是什么 / 什么时候用
专做"AI-native 界面"的小而精组件库：agent 思考轨迹、加载态、流式回答带引用、工具调用 chip、任务状态行、人机协同审批卡、推荐卡、RAG 上下文卡、AI 改表 diff、选中文本改写、Prompt 输入框、聊天面板等，共 21 个展示组件。
做 AI 聊天 / agent 产品前端（尤其 thinking state、tool call、human-in-the-loop、streaming）时优先来这里挑；通用后台组件不是它的方向。
单页站点，所有组件都在首页 `#<id>` 锚点下（如用户收藏的 `#thinking-state`），每节有 Copy code / View code 两个按钮。没有"复制提示词"功能。

## 按需获取方法
机器可读入口：
- 目录：`curl -s https://www.beautifului.dev/r/registry.json`（27 个 item，只有 name/type/title，不含源码）
- 单项：`curl -s https://www.beautifului.dev/r/{name}.json` → `files[].content` 完整源码，`files[].path`（如 `components/primitives/ThinkingState.tsx`），`registryDependencies` 为其他 beautifului 条目的完整 URL，shadcn CLI 会递归安装
- 无 sitemap / llms.txt / robots.txt（均 404），无公开 GitHub 仓库链接

安装：
```bash
npx shadcn@latest add https://www.beautifului.dev/r/{name}.json
# foundation 会被自动拉进来（写到 app/beautifui/foundation.css），之后在 globals.css 里：
#   @import "./beautifui/foundation.css";
npm i shadow-plugin   # foundation.css 里 @import "shadow-plugin/unprefixed"，但 registry 没把它列为依赖
```
手动安装：先拉 `/r/foundation.json` 写 css，再拉 `/r/{name}.json`，按 `registryDependencies` 递归拉 atoms（button / glide-menu / entity-chip / value-pill / shimmer / stream-text，路径 `components/atoms/*` 或 `components/primitives/GlideMenu.tsx`），import 别名是 `@/components/...`。

页面 UI 方式：在 `https://www.beautifului.dev/#{name}` 每节演示区有 "Copy code"（直接复制该组件 tsx 源码）和 "View code"（弹窗显示文件路径、依赖说明如"Self-contained — needs only the foundation tokens."/"Requires · also copy Button"、`npx shadcn add` 命令和源码）。

Agent Screen 不在 registry（`/r/agent-screen.json` 404，但 View code 弹窗仍显示该命令），源码嵌在首页 RSC payload，可 curl 提取：
```bash
curl -sL https://www.beautifului.dev/ | python3 -c '
import re,json,sys
s=sys.stdin.read()
chunks=[json.loads(m)[1] for m in re.findall(r"self\.__next_f\.push\((\[1,.*?\])\)</script>",s)]
print(next(c for c in chunks if c.startswith("\"use client\"") and "AGENT SCREEN" in c))' > AgentScreen.tsx
```
（把 "AGENT SCREEN" 换成其他组件文件头注释的大写标题，如 "THINKING —"，即可提取任意组件，作为 registry 失效时的后备。）

实测（2026-10-07）：
- `curl -s https://www.beautifului.dev/r/thinking-state.json` → 1 个文件 `components/primitives/ThinkingState.tsx`（11358 字符），只 import react，registryDependencies 仅 foundation
- 浏览器内点 `#thinking-state` 的 Copy code，剪贴板内容 11358 字符，与 registry 内容一致
- `npx shadcn@latest view https://www.beautifului.dev/r/thinking-state.json` 正常返回
- Agent Screen：Copy code 得到 14775 字符源码；上面的 RSC 提取脚本得到同样 14775 字符

## 使用注意
- Tailwind v4 专用：foundation.css 以 `@import "tailwindcss"` 开头，用 `@theme`、`@custom-variant dark (&:where(.dark, .dark *))`（class 方式暗色）。Tailwind v3 项目不能直接用。
- 组件使用的是 foundation 定义的语义 token 类（`text-ink`、`bg-canvas`、`shadow-hairline`、`rounded-window` 等），不装 foundation 样式会全部失效；和 shadcn/ui 的 token 命名不同，可能与已有主题并存但需注意 `:root` 变量覆盖。
- 漏列依赖：`shadow-plugin`（foundation 用）需手动装。
- 外部依赖：prompt-bar → `glimm`；insight-cards → `liveline`；selection-actions → `iconoir-react`；sidebar-nav → `@central-icons-react/round-outlined-radius-2-stroke-2`。最后这个 npm 上能装，但 license 字段是 "SEE LICENSE IN LICENSE.md"，Central Icons 是商业图标集，商用前确认授权或换成 lucide 等。
- records-table、sidebar-nav 额外带 css 文件（`app/beautifui/*.css`），需在 globals.css 补 `@import`。
- 组件以演示数据（冰淇淋店场景）硬编码，接入真实数据要改 props/常量；多数组件内置了自动播放的演示时间线（如 Thinking 的 STAGES），产品里要改成受控。
- 首页底部的 "Notify me" 是邮件订阅表单，与获取代码无关。

## 组件清单
首页 21 个展示组件（20 个在 registry + Agent Screen）+ 1 个 foundation 样式 + 6 个共享 atoms = 28 条。全部免费，无 Pro。

| id | 名称 | 分类 | 一句话用途 | 获取（具体命令或URL） | 备注 |
|---|---|---|---|---|---|
| foundation | Beautiful UI foundation | style | 设计 token（:root/.dark）、@theme 映射、primitive-* 间距工具类、共享 keyframes；所有组件的必备前置样式 design tokens theme | `npx shadcn@latest add https://www.beautifului.dev/r/foundation.json` | 所有组件 registryDependencies 都含它；需 npm i shadow-plugin（未列入 dependencies） |
| button | Button | atom | 共享按钮原子组件（cva 变体），被审批卡/推荐卡/差异表等引用 button | `npx shadcn@latest add https://www.beautifului.dev/r/button.json` | 依赖 class-variance-authority |
| glide-menu | GlideMenu | atom | 共享下拉/滑动高亮菜单原子组件，被审批卡、表格、搜索、侧栏等引用 menu dropdown | `npx shadcn@latest add https://www.beautifului.dev/r/glide-menu.json` |  |
| entity-chip | EntityChip | atom | 共享实体标签 chip 原子组件（推荐卡使用）entity tag chip | `npx shadcn@latest add https://www.beautifului.dev/r/entity-chip.json` |  |
| value-pill | ValuePill | atom | 共享数值药丸标签原子组件（推荐卡使用）value pill badge | `npx shadcn@latest add https://www.beautifului.dev/r/value-pill.json` |  |
| shimmer | Shimmer | atom | 共享文字闪光扫过效果原子组件 shimmer text loading | `npx shadcn@latest add https://www.beautifului.dev/r/shimmer.json` |  |
| stream-text | StreamText | atom | 共享流式逐字显现文本原子组件 streaming text typewriter | `npx shadcn@latest add https://www.beautifului.dev/r/stream-text.json` |  |
| loading-state | Loading State | ai-state | AI 加载态：像素点阵 loader + 文字 shimmer + 计时，变体 Drive/Dots/Orbit/Surfer pixel loader elapsed time | `npx shadcn@latest add https://www.beautifului.dev/r/loading-state.json` |  |
| thinking-state | Thinking | ai-state | 可展开的 agent 思考轨迹，四种变体 Steps/Reasoning/Search/Coding，结束后折叠为 Thought for Ns thinking trace reasoning | `npx shadcn@latest add https://www.beautifului.dev/r/thinking-state.json` | 用户收藏锚点；仅需 foundation |
| streaming-text | Streaming Text | ai-chat | 流式回答：模糊渐显、行内引用来源、操作按钮与追问建议 streaming answer citations sources follow-ups | `npx shadcn@latest add https://www.beautifului.dev/r/streaming-text.json` |  |
| approval-card | Approval Card | human-in-the-loop | agent 执行前向用户提问的多步审批/选择卡片（选项、自定义答案、跳过、分页）HITL approval question | `npx shadcn@latest add https://www.beautifului.dev/r/approval-card.json` | 需 button、glide-menu |
| tool-chips | Tool Chips | agent-trace | 把代码编辑和工具调用渲染为紧凑 chip，可展开看文件 diff tool calls code edits | `npx shadcn@latest add https://www.beautifului.dev/r/tool-chips.json` |  |
| task-rows | Task Rows | agent-trace | agent 任务实时状态行（运行中/失败/完成、进度、子项），变体 Capsules/List task status progress | `npx shadcn@latest add https://www.beautifului.dev/r/task-rows.json` |  |
| chat-composer | Chat | ai-chat | 带标签页的聊天面板，含推理过程回复与输入框 chat panel composer tabs | `npx shadcn@latest add https://www.beautifului.dev/r/chat-composer.json` |  |
| prompt-bar | Prompt Bar | ai-chat | AI 输入框：@ 引用来源、/ 命令、模型选择、语音听写，Rounded/Pill 两种外形 prompt input composer model picker | `npx shadcn@latest add https://www.beautifului.dev/r/prompt-bar.json` | 依赖 glimm（WebGL 过渡） |
| recommendation-card | Recommendation Card | human-in-the-loop | agent 建议卡：置信度条、备选方案、接受/拒绝操作 recommendation confidence accept | `npx shadcn@latest add https://www.beautifului.dev/r/recommendation-card.json` | 需 button、entity-chip、value-pill |
| context-cards | Context Cards | rag | RAG 检索到的知识片段卡片，显示字符数与来源文件 retrieved chunks citations knowledge | `npx shadcn@latest add https://www.beautifului.dev/r/context-cards.json` |  |
| diff-table | Diff Table | data | AI 提议的表格数据修改，逐行扫过显示增删 diff，可接受 table diff proposed edits | `npx shadcn@latest add https://www.beautifului.dev/r/diff-table.json` | 需 button |
| records-table | Records Table | data | CRM 风格数据网格：标签、排序、列宽拖拽、多选、关系强度、汇总计算 data grid CRM table | `npx shadcn@latest add https://www.beautifului.dev/r/records-table.json` | 需 glide-menu；含 records-table.css，需在 globals.css 加 @import |
| filter-table | Filter Table | data | 状态 chip 筛选并实时重排的任务表格 filter tabs status table | `npx shadcn@latest add https://www.beautifului.dev/r/filter-table.json` |  |
| sidebar-nav | Sidebar Nav | navigation | 可折叠的工作区+聊天记录侧边导航，滑动 hover 高亮 sidebar navigation chat history | `npx shadcn@latest add https://www.beautifului.dev/r/sidebar-nav.json` | 需 glide-menu；含 sidebar-nav.css；依赖 @central-icons-react（专有许可，见使用注意） |
| search | Search | navigation | 命令式搜索列表，实时过滤与空状态 command palette search empty state | `npx shadcn@latest add https://www.beautifului.dev/r/search.json` | 需 glide-menu |
| flowchart | Flowchart | workflow | 点阵画布上的工作流触发器与 If/Else 条件节点 workflow builder flowchart nodes | `npx shadcn@latest add https://www.beautifului.dev/r/flowchart.json` |  |
| insight-cards | Insight Cards | data | 分页的 agent 洞察卡片，带可拖动读数的实时折线图 insights chart sparkline | `npx shadcn@latest add https://www.beautifului.dev/r/insight-cards.json` | 依赖 liveline |
| code-block | Code Block | code | 带行号的代码块与统一 diff 视图，可复制 code block syntax diff | `npx shadcn@latest add https://www.beautifului.dev/r/code-block.json` |  |
| fine-tune-card | Fine-tune Card | design-tool | agent 在属性检查器中调整设计参数（宽高、圆角、透明度、字体）inspector design properties | `npx shadcn@latest add https://www.beautifului.dev/r/fine-tune-card.json` | 需 glide-menu |
| selection-actions | Selection Actions | ai-edit | 选中文本后弹出操作（解释/改进/缩短/语气/语法），交给 agent 改写并流式替换 text selection rewrite | `npx shadcn@latest add https://www.beautifului.dev/r/selection-actions.json` | 需 button、shimmer、stream-text；依赖 iconoir-react |
| agent-screen | Agent Screen | agent-trace | 观看 agent 屏幕的实时查看器：打开全屏、教学任务、录制（REC 徽标）agent computer use screen viewer | https://www.beautifului.dev/#agent-screen 点 Copy code；或用下文 RSC 提取脚本 | 站点显示的 /r/agent-screen.json 返回 404；需从首页 Copy code 或 RSC payload 提取；依赖 Button；broken |

## 未解决
- Agent Screen 的 registry 文件 `/r/agent-screen.json` 返回 404（站点 bug），只能用页面 Copy code 或 RSC 提取脚本获取；它依赖 `@/components/atoms/Button`，需另装 `/r/button.json`。
- 没有 sitemap/llms.txt/公开仓库，新增组件只能靠重新拉 `/r/registry.json` 或首页 `section[id]` 发现。
- 未在真实项目里跑 `shadcn add` 后的构建，只验证到 registry JSON、`shadcn view` 和浏览器复制内容一致。
