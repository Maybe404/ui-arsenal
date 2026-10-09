---
id: aielements
name: AI Elements
url: https://ai-sdk.dev/elements
kind: component-library
stack: React + shadcn/ui + Tailwind CSS v4 + Vercel AI SDK（`ai`）；工作流类用 @xyflow/react，Markdown 流式渲染用 streamdown
license: Apache-2.0（GitHub vercel/ai-elements）
pro: none
fetch: shadcn-registry
coverage: 全量：官方 registry 的 30 个组件和 47 个示例（含 chatbot、v0 clone、ChatGPT/Claude/Grok 风格演示、workflow）；refresh 自动比对
catalog_checked: 2026-10-08
source_status: active
visual_style: neutral shadcn chat surfaces
foundation: shadcn-compatible
styling: tailwind-v4
motion_lib: none
dark_mode: class
mixing_notes: 直接依赖 shadcn 的 button、collapsible、dropdown-menu、tooltip 等，用 shadcn 主底座时最顺；uiarc 主底座只借结构和状态模型
---
## 是什么 / 什么时候用
Vercel 官方的 AI 界面组件：对话容器（conversation、message）、输入框（prompt-input）、推理过程（reasoning、chain-of-thought）、工具调用（tool、confirmation）、来源与引用（sources、inline-citation）、计划与任务（plan、task、queue）、代码块、网页预览、模型选择、上下文用量（context）、工作流画布（canvas、node、edge）。组件直接对接 AI SDK 的 `useChat` 消息 parts 和工具状态（input-streaming / input-available / output-available / output-error），所以是做真实流式聊天界面时的首选，而不是演示件。

## 按需获取方法
- 目录：`curl -s https://registry.ai-sdk.dev/registry.json`（77 项：30 个 registry:component、47 个 registry:block 示例）
- 单项：`curl -s https://registry.ai-sdk.dev/{name}.json`（注意没有 `/r/` 前缀）
- 安装：`npx shadcn@latest add https://registry.ai-sdk.dev/{name}.json`，或官方 CLI `npx ai-elements@latest add {name}`
- 文档：`https://ai-sdk.dev/elements/components/{name}`；完整示例页：`/elements/examples/chatbot`、`/elements/examples/workflow`
- 本库：`fetch.sh aielements:{name}`

实测（2026-10-08）：`curl -s https://registry.ai-sdk.dev/tool.json` 返回 `registry/default/ai-elements/tool.tsx`（4843 字符），依赖 `ai`、`lucide-react`，registryDependencies `badge`、`collapsible` 和 `https://registry.ai-sdk.dev/code-block.json`。

## 使用注意
- registryDependencies 里有 shadcn 组件名（button、collapsible、dropdown-menu、tooltip、hover-card、command 等）和其他 AI Elements 条目的完整 URL；`fetch.sh` 不会连带下载，要按提示单独装，或直接用 shadcn CLI 安装。
- 类型来自 `ai` 包（`UIMessage`、`ToolUIPart` 等），版本要和项目里的 AI SDK 一致。
- 2026-10-08 拉取全部 77 项源码：都不含减弱动效相关代码（大部分本身没有装饰动画；loader、shimmer 自带循环动画，要自己加 `prefers-reduced-motion`）。
- 示例（example-*）是演示数据，接入时把消息、工具状态换成 `useChat` 的真实数据，见 `guides/ai-ux.md`。

## 组件清单
组件 30 个：artifact、canvas、chain-of-thought、checkpoint、code-block、confirmation、connection、context、controls、conversation、edge、image、inline-citation、loader、message、model-selector、node、open-in-chat、panel、plan、prompt-input、queue、reasoning、shimmer、sources、suggestion、task、tool、toolbar、web-preview。示例 47 个（example-*），逐条见 `sources/aielements.tsv`。
