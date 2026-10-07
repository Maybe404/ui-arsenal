---
id: uiarc
name: Arc (uiarc.dev)
url: https://uiarc.dev
kind: component-library
stack: React + CSS Modules + CSS 变量 + Motion（motion/react），部分用 Radix 与 lucide-react；不依赖 Tailwind
license: 自定义（免费项标注 "Free, open source"，可用于商业/客户项目；Pro 为商业许可，见 https://uiarc.dev/pricing）
pro: partial（238 项中 129 项免费：107 个组件 + 22 个 block 免费；43 个 Pro 组件、66 个 Pro block、3 个模板 Arc SaaS/AI/Startup 付费，Pro $129/年）
fetch: shadcn-registry
verified: 2026-10-07
---
## 是什么 / 什么时候用
Arc 是面向 AI 辅助开发的 React 组件与区块（block）库，风格克制、动效讲究（spring、morph、共享高亮），每个条目都附带机器可读的 when to use / when not / a11y / motion / responsive 说明。适合：需要质感好的基础控件（按钮、输入、菜单、toast、tabs 等）、数据可视化（折线、treemap、heatmap 等）、以及完整页面区块（登录、command palette、hero、FAQ、定价）的 React 项目。因为是 CSS Modules + 自带 token，和 Tailwind 项目并存不冲突，但风格自成体系，混用 shadcn/ui 时注意视觉一致性。Pro 项（大量炫技交互和 SaaS 页面区块）不能获取源码。

## 按需获取方法
机器可读入口（全部实测 200）：
- 索引：`https://uiarc.dev/llms.txt`（全部 238 项按分类列出，Pro 标 `(Pro)`）；`https://uiarc.dev/llms-small.txt`；`https://uiarc.dev/llms-full.txt`（约 1.5MB，内联每个组件 markdown）
- 元数据目录（含 Pro）：`https://uiarc.dev/r/catalog.json` → `items[]`，字段 `name/kind(component|block)/tier(free|pro)/category/description/keywords/whenToUse/whenNotToUse/dependencies/usage/registry`
- shadcn registry（仅免费 131 项，含 arc-foundation、arc-skill）：`https://uiarc.dev/r/registry.json`
- 单项源码（含文件内容）：`https://uiarc.dev/r/{name}.json`
- 单项文档 markdown：组件 `https://uiarc.dev/components/{name}/markdown`，区块 `https://uiarc.dev/components/blocks/{name}/markdown`（Pro 项也能读文档，但不含源码）
- MCP：`https://uiarc.dev/api/mcp`（Streamable HTTP，需 OAuth 登录 Arc 账号，免费账号即可；本次未连接）
- Agent skill：`npx shadcn@latest add https://uiarc.dev/r/arc-skill.json` 或直接读 `https://uiarc.dev/r/skills/arc/SKILL.md`、`https://uiarc.dev/r/skills/index.json`

步骤：
1. 选组件：`curl -s https://uiarc.dev/r/catalog.json | jq -r '.items[] | select(.tier=="free") | [.name,.kind,.category,.description]|@tsv' | grep -i {keyword}`
2. 读文档（props、何时不用）：`curl -s https://uiarc.dev/components/{name}/markdown`
3. 安装：`npx shadcn@latest add https://uiarc.dev/r/{name}.json`
   或在 `components.json` 加 `"registries": { "@uiarc": "https://uiarc.dev/r/{name}.json" }` 后 `npx shadcn@latest add @uiarc/{name}`
4. 根布局引入一次 token：`import "@/components/arc/foundation.css";`
5. 使用：`import { InViewTitle } from "@/components/arc/in-view-title/in-view-title";`
6. 不用 shadcn CLI 时：`curl -s https://uiarc.dev/r/{name}.json | jq -r '.files[] | .target, .content'` 手动落盘（target 中 `@components` 即 components 别名目录），并同样取 `arc-foundation.json` 和 `registryDependencies` 中的项。

实测（in-view-title）：
- `curl -s https://uiarc.dev/r/in-view-title.json` → 200，`type: registry:ui`，`dependencies: ["motion"]`，`registryDependencies: ["https://uiarc.dev/r/arc-foundation.json"]`，files 含 `in-view-title.tsx`（变体 `word|line|blur|tracking|wipe`，props `text/variant/as/lines/once`）与 `.module.css`
- `curl -s https://uiarc.dev/components/in-view-title/markdown` → "Access: Free, open source"，安装命令 `npx shadcn@latest add @uiarc/in-view-title`
- Pro 实测：`curl https://uiarc.dev/r/pro/dock.json` → 401（需 `Authorization: Bearer $ARC_PRO_TOKEN`）

依赖：`motion`（125 项）、`lucide-react`（81 项）、少量 `@radix-ui/react-*`（dropdown-menu、dialog、popover、tooltip、tabs、select、checkbox、switch、accordion），shadcn CLI 会自动装。

## 使用注意
- 用 CSS Modules + CSS 变量，不是 Tailwind 类；Tailwind v3/v4 都不冲突。语义 token：`--background --surface --foreground --text-secondary --border --accent --success --warning --danger`。
- 暗色：`<html data-theme="dark">`；强调色：`data-accent` = neutral/violet/blue/green/amber/orange/coral/rose。不是 `class="dark"`，与 shadcn/next-themes 默认的 class 策略不同，需要同步设置。
- 动效库是 `motion`（import from `motion/react`），不是 `framer-motion`；项目里已有 framer-motion 也能共存，但别重复装两份。
- 文件装到 `components/arc/...`，互相用相对路径引用；动效预设在 `components/arc/lib/motion-tokens.ts`（`snappy/smooth/morph`）。
- 组件标了 `"use client"`，Next.js App Router 下可直接用。
- 风格规范（agent 规则）：句首大写文案、无 eyebrow、无 em dash、无装饰渐变/光晕、只用 regular/medium 字重；每个动画有 reduced-motion 分支。
- Pro 条目只能读文档、不得仿写源码（站方明确要求），需要时改用免费替代或让用户购买。

## 组件清单
| id | 名称 | 分类 | 一句话用途 | 获取（具体命令或URL） | 备注 |
|---|---|---|---|---|---|
| arc-foundation | Arc foundation | Foundation | 设计 token 与 motion 预设 深浅色主题 accent 所有组件的基础依赖 | `npx shadcn@latest add https://uiarc.dev/r/arc-foundation.json` |  |
| arc-skill | Arc agent skill | Skill | Arc 的 agent skill 文件 SKILL.md 设计/动效/文案/无障碍规则 | `npx shadcn@latest add https://uiarc.dev/r/arc-skill.json` |  |
| button | Button | Actions | 按钮 主操作 按压回弹 加载 spinner 标签变形 | `npx shadcn@latest add https://uiarc.dev/r/button.json` |  |
| action-button | Action button | Actions | 工具栏紧凑按钮 异步提交 pending/success 状态 | `npx shadcn@latest add https://uiarc.dev/r/action-button.json` |  |
| split-button | Split button | Actions | 分裂按钮 主操作+下拉备选菜单 | `npx shadcn@latest add https://uiarc.dev/r/split-button.json` |  |
| button-group | Button group | Actions | 按钮组 细分隔线 悬停高亮在分段间滑动 可附菜单 | `npx shadcn@latest add https://uiarc.dev/r/button-group.json` |  |
| floating-button-group | Floating button group | Actions | 浮动按钮组 共享高亮随指针在按钮间 morph | `npx shadcn@latest add https://uiarc.dev/r/floating-button-group.json` |  |
| expanding-button-group | Expanding button group | Actions | 图标按钮组 悬停/聚焦项展开显示文字标签 | `npx shadcn@latest add https://uiarc.dev/r/expanding-button-group.json` |  |
| dropdown-menu | Dropdown menu | Actions | 下拉菜单 锚定触发器的操作列表 | `npx shadcn@latest add https://uiarc.dev/r/dropdown-menu.json` |  |
| context-menu | Context menu | Actions | 右键上下文菜单 | `npx shadcn@latest add https://uiarc.dev/r/context-menu.json` |  |
| copy-button | Copy button | Actions | 复制按钮 复制后即时确认反馈 | `npx shadcn@latest add https://uiarc.dev/r/copy-button.json` |  |
| drawer | Drawer | Disclosure | 抽屉 侧边临时面板 | `npx shadcn@latest add https://uiarc.dev/r/drawer.json` |  |
| theme-switch | Theme switcher | Actions | 深浅色主题切换 四种过渡动画 | `npx shadcn@latest add https://uiarc.dev/r/theme-switch.json` |  |
| theme-switch-eclipse | Eclipse | Actions | 主题切换 日食式圆形扩散过渡 dark mode toggle | `npx shadcn@latest add https://uiarc.dev/r/theme-switch-eclipse.json` |  |
| theme-switch-split | Split | Actions | 主题切换 中缝向两侧展开过渡 | `npx shadcn@latest add https://uiarc.dev/r/theme-switch-split.json` |  |
| theme-switch-rise | Rise | Actions | 主题切换 新主题自下而上升起 | `npx shadcn@latest add https://uiarc.dev/r/theme-switch-rise.json` |  |
| avatar | Avatar | Data | 头像 | `npx shadcn@latest add https://uiarc.dev/r/avatar.json` |  |
| avatar-group | Avatar group | Data | 头像组 叠放 团队成员 | `npx shadcn@latest add https://uiarc.dev/r/avatar-group.json` |  |
| input | Input | Inputs | 单行输入框 标签与状态 | `npx shadcn@latest add https://uiarc.dev/r/input.json` |  |
| textarea | Textarea | Inputs | 多行文本框 | `npx shadcn@latest add https://uiarc.dev/r/textarea.json` |  |
| select | Select | Inputs | 下拉选择 键盘友好 | `npx shadcn@latest add https://uiarc.dev/r/select.json` |  |
| combobox | Combobox | Inputs | 可搜索下拉 自动补全 combobox | `npx shadcn@latest add https://uiarc.dev/r/combobox.json` |  |
| checkbox | Checkbox | Inputs | 复选框 | `npx shadcn@latest add https://uiarc.dev/r/checkbox.json` |  |
| switch | Switch | Inputs | 开关 toggle 设置即时生效 | `npx shadcn@latest add https://uiarc.dev/r/switch.json` |  |
| multi-select | Multi-select | Inputs | 多选下拉 选中项保持可读 | `npx shadcn@latest add https://uiarc.dev/r/multi-select.json` |  |
| number-field | Number field | Inputs | 数字输入 步进按钮 范围限制 | `npx shadcn@latest add https://uiarc.dev/r/number-field.json` |  |
| password-field | Password field | Inputs | 密码框 显示/隐藏切换 | `npx shadcn@latest add https://uiarc.dev/r/password-field.json` |  |
| search-field | Search field | Inputs | 搜索框 | `npx shadcn@latest add https://uiarc.dev/r/search-field.json` |  |
| tag-input | Tag input | Inputs | 标签输入 回车生成可删除 tag | `npx shadcn@latest add https://uiarc.dev/r/tag-input.json` |  |
| file-dropzone | File dropzone | Inputs | 文件拖放区 上传 | `npx shadcn@latest add https://uiarc.dev/r/file-dropzone.json` |  |
| radio-group | Radio group | Inputs | 单选组 | `npx shadcn@latest add https://uiarc.dev/r/radio-group.json` |  |
| segmented-control | Segmented control | Inputs | 分段控件 视图切换 | `npx shadcn@latest add https://uiarc.dev/r/segmented-control.json` |  |
| calendar | Calendar | Inputs | 月历 日期浏览 | `npx shadcn@latest add https://uiarc.dev/r/calendar.json` |  |
| date-picker | Date picker | Inputs | 日期选择器 | `npx shadcn@latest add https://uiarc.dev/r/date-picker.json` |  |
| time-picker | Time picker | Inputs | 时间选择器 | `npx shadcn@latest add https://uiarc.dev/r/time-picker.json` |  |
| accordion | Accordion | Disclosure | 手风琴 折叠展开 | `npx shadcn@latest add https://uiarc.dev/r/accordion.json` |  |
| dialog | Dialog | Disclosure | 对话框 modal | `npx shadcn@latest add https://uiarc.dev/r/dialog.json` |  |
| popover | Popover | Disclosure | 气泡弹层 popover | `npx shadcn@latest add https://uiarc.dev/r/popover.json` |  |
| tooltip | Tooltip | Disclosure | 工具提示 tooltip | `npx shadcn@latest add https://uiarc.dev/r/tooltip.json` |  |
| tabs | Tabs | Disclosure | 标签页 tabs | `npx shadcn@latest add https://uiarc.dev/r/tabs.json` |  |
| expandable-card | Expandable card | Disclosure | 可展开卡片 | `npx shadcn@latest add https://uiarc.dev/r/expandable-card.json` |  |
| breadcrumb | Breadcrumb | Disclosure | 面包屑导航 | `npx shadcn@latest add https://uiarc.dev/r/breadcrumb.json` |  |
| alert | Alert | Feedback | 警告提示条 持久消息 | `npx shadcn@latest add https://uiarc.dev/r/alert.json` |  |
| toast | Toast | Feedback | 轻提示 toast 通知 | `npx shadcn@latest add https://uiarc.dev/r/toast.json` |  |
| progress | Progress | Feedback | 进度条 | `npx shadcn@latest add https://uiarc.dev/r/progress.json` |  |
| skeleton | Skeleton | Feedback | 骨架屏 加载占位 | `npx shadcn@latest add https://uiarc.dev/r/skeleton.json` |  |
| badge | Badge | Data | 徽章 状态标签 | `npx shadcn@latest add https://uiarc.dev/r/badge.json` |  |
| card | Card | Data | 卡片容器 | `npx shadcn@latest add https://uiarc.dev/r/card.json` |  |
| metric-card | Metric card | Data | 指标卡 KPI 数字+上下文 | `npx shadcn@latest add https://uiarc.dev/r/metric-card.json` |  |
| empty-state | Empty state | Data | 空状态 引导下一步 | `npx shadcn@latest add https://uiarc.dev/r/empty-state.json` |  |
| tree-view | Tree view | Data | 树形视图 嵌套文件夹 | `npx shadcn@latest add https://uiarc.dev/r/tree-view.json` |  |
| pagination | Pagination | Data | 分页 | `npx shadcn@latest add https://uiarc.dev/r/pagination.json` |  |
| filter-toolbar | Filter toolbar | Data | 筛选工具栏 可重置 | `npx shadcn@latest add https://uiarc.dev/r/filter-toolbar.json` |  |
| sortable-data-table | Sortable data table | Data | 可排序数据表格 table | `npx shadcn@latest add https://uiarc.dev/r/sortable-data-table.json` |  |
| sparkline | Sparkline | Data | 迷你趋势图 sparkline | `npx shadcn@latest add https://uiarc.dev/r/sparkline.json` |  |
| gauge | Gauge | Data | 仪表盘 量规 gauge | `npx shadcn@latest add https://uiarc.dev/r/gauge.json` |  |
| animated-counter | Animated counter | Data | 数字滚动动画 计数器 | `npx shadcn@latest add https://uiarc.dev/r/animated-counter.json` |  |
| code-block | Code block | Data | 代码块 带复制 | `npx shadcn@latest add https://uiarc.dev/r/code-block.json` |  |
| text-reveal | Text reveal | Text | 文字揭示入场动画 hero 文案 | `npx shadcn@latest add https://uiarc.dev/r/text-reveal.json` |  |
| in-view-title | In-view title | Text | 滚动进入视口时标题入场动画 scroll reveal 逐词/模糊/擦除 | `npx shadcn@latest add https://uiarc.dev/r/in-view-title.json` |  |
| text-morph | Text morph | Text | 文字逐字母 morph 到新状态 | `npx shadcn@latest add https://uiarc.dev/r/text-morph.json` |  |
| text-shimmer | Text shimmer | Text | 文字流光 shimmer 加载中状态 | `npx shadcn@latest add https://uiarc.dev/r/text-shimmer.json` |  |
| hold-to-confirm | Hold to confirm | Actions | 长按确认 危险操作 hold to delete | `npx shadcn@latest add https://uiarc.dev/r/hold-to-confirm.json` |  |
| swipe-actions | Swipe actions | Actions | 列表行滑动操作 swipe 删除/归档 | `npx shadcn@latest add https://uiarc.dev/r/swipe-actions.json` |  |
| slider | Slider | Inputs | 滑块 单值/范围 range slider | `npx shadcn@latest add https://uiarc.dev/r/slider.json` |  |
| inline-edit | Inline edit | Inputs | 原地编辑 重命名 文本变输入框 | `npx shadcn@latest add https://uiarc.dev/r/inline-edit.json` |  |
| expanding-search | Expanding search | Inputs | 图标 morph 展开为搜索框+结果 | `npx shadcn@latest add https://uiarc.dev/r/expanding-search.json` |  |
| chip-group | Chip group | Inputs | 筛选 chip 组 选中 morph | `npx shadcn@latest add https://uiarc.dev/r/chip-group.json` |  |
| password-strength | Password strength | Inputs | 密码强度指示 | `npx shadcn@latest add https://uiarc.dev/r/password-strength.json` |  |
| bottom-sheet | Bottom sheet | Disclosure | 底部抽屉 bottom sheet 可拖拽 peek/全屏 | `npx shadcn@latest add https://uiarc.dev/r/bottom-sheet.json` |  |
| hover-card | Hover card | Disclosure | 悬停卡片 人物/链接预览 | `npx shadcn@latest add https://uiarc.dev/r/hover-card.json` |  |
| resizable-panels | Resizable panels | Disclosure | 可拖拽调整大小的分栏面板 | `npx shadcn@latest add https://uiarc.dev/r/resizable-panels.json` |  |
| toast-stack | Toast stack | Feedback | 堆叠 toast 通知 悬停展开 sonner 风格 | `npx shadcn@latest add https://uiarc.dev/r/toast-stack.json` |  |
| usage-meter | Usage meter | Feedback | 用量计量条 配额接近上限 | `npx shadcn@latest add https://uiarc.dev/r/usage-meter.json` |  |
| image-compare | Image compare | Data | 图片前后对比 拖拽分隔线 before/after | `npx shadcn@latest add https://uiarc.dev/r/image-compare.json` |  |
| carousel | Carousel | Data | 轮播 拖拽/轻扫 slider | `npx shadcn@latest add https://uiarc.dev/r/carousel.json` |  |
| card-stack | Card stack | Data | 卡片堆 逐张滑走 tinder 式 撤销 | `npx shadcn@latest add https://uiarc.dev/r/card-stack.json` |  |
| morph-nav | Morph nav | Special | 导航栏 morph 成富菜单/搜索/紧凑态 一体化 | https://uiarc.dev/components/morph-nav/markdown | pro |
| dock | Dock | Special | 浮动 dock 工具栏 标签滑动 托盘展开 macOS dock | https://uiarc.dev/components/dock/markdown | pro |
| wallet-stack | Wallet stack | Special | 钱包卡片扇形展开 抽出单张看交易 | https://uiarc.dev/components/wallet-stack/markdown | pro |
| liquid-tab-bar | Liquid tab bar | Special | 液态选中效果的 tab bar 图标填充 | https://uiarc.dev/components/liquid-tab-bar/markdown | pro |
| now-playing | Now playing | Special | 迷你播放器连续 morph 成全屏播放器 | https://uiarc.dev/components/now-playing/markdown | pro |
| photo-grid | Photo grid | Special | 照片网格 捏合缩放层级 从格子打开 | https://uiarc.dev/components/photo-grid/markdown | pro |
| control-center | Control center | Special | 控制中心 快捷设置磁贴 morph 详情 iOS 风格 | https://uiarc.dev/components/control-center/markdown | pro |
| cover-flow | Cover flow | Special | Cover Flow 3D 图片轨道 倒影 | https://uiarc.dev/components/cover-flow/markdown | pro |
| activity-rings | Activity rings | Special | 活动圆环 Apple Watch 风格 目标进度 | https://uiarc.dev/components/activity-rings/markdown | pro |
| bar-chart | Bar chart | Data | 柱状图 可擦洗查看数值 | `npx shadcn@latest add https://uiarc.dev/r/bar-chart.json` |  |
| activity-heatmap | Activity heatmap | Data | 年度活动热力图 GitHub 贡献图 | `npx shadcn@latest add https://uiarc.dev/r/activity-heatmap.json` |  |
| timeline | Timeline | Data | 时间线 按天分组 | `npx shadcn@latest add https://uiarc.dev/r/timeline.json` |  |
| stretch-refresh | Stretch refresh | Special | 下拉刷新 拉伸线提示松手 | https://uiarc.dev/components/stretch-refresh/markdown | pro |
| orbit-menu | Orbit menu | Special | 长按按钮 操作项环绕弹出 径向菜单 | https://uiarc.dev/components/orbit-menu/markdown | pro |
| time-dial | Time dial | Special | 旋转表盘选时间 显示团队城市时区 | https://uiarc.dev/components/time-dial/markdown | pro |
| booking-pill | Booking pill | Special | 预订胶囊 一个 pill 连续变形 人数/日期/时间/票 | https://uiarc.dev/components/booking-pill/markdown | pro |
| voice-recorder | Voice recorder | Special | 录音 实时波形 回放擦洗 发送 | https://uiarc.dev/components/voice-recorder/markdown | pro |
| user-menu | User menu | Actions | 用户头像菜单 账号/设置/主题/登出 手机端 bottom sheet | `npx shadcn@latest add https://uiarc.dev/r/user-menu.json` |  |
| data-grid | Data grid | Data | 电子表格网格 区域选择 原地编辑 填充柄 | https://uiarc.dev/components/data-grid/markdown | pro |
| lightbox-gallery | Lightbox gallery | Special | 瀑布流+灯箱 从格子缩放进入查看器 手势 | https://uiarc.dev/components/lightbox-gallery/markdown | pro |
| stepper | Stepper | Feedback | 步骤条 多步流程进度 | `npx shadcn@latest add https://uiarc.dev/r/stepper.json` |  |
| morph-loader | Morph loader | Special | 形状 morph 的小 loader 完成时变成对勾/叉 | https://uiarc.dev/components/morph-loader/markdown | pro |
| voice-orb | Voice orb | Special | 语音模式光球 听/想/说 实时字幕 AI voice | https://uiarc.dev/components/voice-orb/markdown | pro |
| signature-pad | Signature pad | Inputs | 签名板 笔迹随速度变细 撤销 导出 PNG/SVG | `npx shadcn@latest add https://uiarc.dev/r/signature-pad.json` |  |
| date-range-picker | Date range picker | Inputs | 日期范围选择 双月 预设 从触发器展开 | `npx shadcn@latest add https://uiarc.dev/r/date-range-picker.json` |  |
| color-picker | Color picker | Inputs | 取色器 格式切换 吸管 对比度 | `npx shadcn@latest add https://uiarc.dev/r/color-picker.json` |  |
| morph-select | Morph select | Inputs | 触发器展开成列表的 select 高亮滑动 | `npx shadcn@latest add https://uiarc.dev/r/morph-select.json` |  |
| action-morph | Action morph | Special | 悬浮按钮 morph 成快捷菜单再到内联表单 FAB | https://uiarc.dev/components/action-morph/markdown | pro |
| share-sheet | Share sheet | Special | 分享面板 复制链接 权限 渠道 联系人 | https://uiarc.dev/components/share-sheet/markdown | pro |
| line-chart | Line chart | Data | 多系列折线图 十字准线 图例切换 路径 morph | `npx shadcn@latest add https://uiarc.dev/r/line-chart.json` |  |
| donut-chart | Donut chart | Data | 环形图 数据集切换弧线 morph | `npx shadcn@latest add https://uiarc.dev/r/donut-chart.json` |  |
| streamgraph | Streamgraph | Data | 流图 堆叠面积 wiggle 基线 | `npx shadcn@latest add https://uiarc.dev/r/streamgraph.json` |  |
| brush-chart | Brush chart | Data | 带概览刷选的时间序列图 拖拽缩放 | `npx shadcn@latest add https://uiarc.dev/r/brush-chart.json` |  |
| race-bar-chart | Race bar chart | Data | 排名竞赛条形图 bar chart race 时间轴播放 | https://uiarc.dev/components/race-bar-chart/markdown | pro |
| ridgeline | Ridgeline | Data | 山脊图 分布 joyplot 四分位 | `npx shadcn@latest add https://uiarc.dev/r/ridgeline.json` |  |
| treemap | Treemap | Data | 矩形树图 点击下钻 | `npx shadcn@latest add https://uiarc.dev/r/treemap.json` |  |
| sunburst | Sunburst | Data | 旭日图 层级环 点击重心旋转 | https://uiarc.dev/components/sunburst/markdown | pro |
| sankey-flow | Sankey flow | Data | 桑基图 流动粒子 | https://uiarc.dev/components/sankey-flow/markdown | pro |
| waffle-chart | Waffle chart | Data | 华夫图 10x10 百分比单元 | `npx shadcn@latest add https://uiarc.dev/r/waffle-chart.json` |  |
| funnel-chart | Funnel chart | Data | 漏斗图 转化流失 | https://uiarc.dev/components/funnel-chart/markdown | pro |
| radar-chart | Radar chart | Data | 雷达图 多剖面对比 morph | https://uiarc.dev/components/radar-chart/markdown | pro |
| realtime-stream | Realtime stream | Data | 实时流折线 60fps 滚动 | https://uiarc.dev/components/realtime-stream/markdown | pro |
| slope-chart | Slope chart | Data | 斜率图 前后对比 排名变化 | `npx shadcn@latest add https://uiarc.dev/r/slope-chart.json` |  |
| countdown | Countdown | Feedback | 倒计时 数字滚动 归零变 live | `npx shadcn@latest add https://uiarc.dev/r/countdown.json` |  |
| announcement-bar | Announcement bar | Feedback | 顶部公告条 轮播消息 倒计时 可关闭 | `npx shadcn@latest add https://uiarc.dev/r/announcement-bar.json` |  |
| json-viewer | JSON viewer | Data | JSON 树查看器 搜索 复制路径 | `npx shadcn@latest add https://uiarc.dev/r/json-viewer.json` |  |
| product-gallery | Product gallery | Special | 商品图集 放大镜 缩略图 变体切换 电商 | https://uiarc.dev/components/product-gallery/markdown | pro |
| sheet-stack | Sheet stack | Special | 嵌套 sheet 层叠 拖拽关闭 宽屏变对话框 | https://uiarc.dev/components/sheet-stack/markdown | pro |
| phone-input | Phone input | Inputs | 手机号输入 国家选择 格式化 E.164 | `npx shadcn@latest add https://uiarc.dev/r/phone-input.json` |  |
| money-input | Money input | Inputs | 金额输入 千分位 滚动数字 最小单位输出 | `npx shadcn@latest add https://uiarc.dev/r/money-input.json` |  |
| shortcut-recorder | Shortcut recorder | Inputs | 快捷键录制 键帽 冲突提示 cheatsheet | `npx shadcn@latest add https://uiarc.dev/r/shortcut-recorder.json` |  |
| confirm-morph | Confirm morph | Actions | 删除按钮 morph 成内联确认→spinner→结果+撤销 | `npx shadcn@latest add https://uiarc.dev/r/confirm-morph.json` |  |
| mention-input | Mention input | Inputs | @提及 #频道 输入框 光标处建议 | `npx shadcn@latest add https://uiarc.dev/r/mention-input.json` |  |
| chat-thread | Chat thread | Data | 聊天消息线程 反应 已读 输入中 附件 | `npx shadcn@latest add https://uiarc.dev/r/chat-thread.json` |  |
| rich-text-editor | Rich text editor | Inputs | 轻量富文本编辑器 markdown 快捷 浮动工具栏 斜杠菜单 | `npx shadcn@latest add https://uiarc.dev/r/rich-text-editor.json` |  |
| billing-toggle | Billing toggle | Inputs | 月付/年付切换 节省徽章 价格滚动 | `npx shadcn@latest add https://uiarc.dev/r/billing-toggle.json` |  |
| scroll-area | Scroll area | Disclosure | 滚动容器 细滚动条 边缘渐隐 | `npx shadcn@latest add https://uiarc.dev/r/scroll-area.json` |  |
| radio-cards | Radio cards | Inputs | 单选卡片 选中环滑动 价格 | `npx shadcn@latest add https://uiarc.dev/r/radio-cards.json` |  |
| comment-thread | Comment thread | Data | 评论线程 回复 反应 提及 解决 | `npx shadcn@latest add https://uiarc.dev/r/comment-thread.json` |  |
| dot-grid | Dot grid | Special | 点阵背景 光标处透镜鼓起 点击涟漪 | https://uiarc.dev/components/dot-grid/markdown | pro |
| slot-text | Slot text | Special | 老虎机滚轮文字/数字切换 | `npx shadcn@latest add https://uiarc.dev/r/slot-text.json` |  |
| page-curl | Page curl | Special | 翻页卷角 杂志阅读 拖拽翻页 | https://uiarc.dev/components/page-curl/markdown | pro |
| glass-card | Glass card | Special | 玻璃拟态卡片 指针高光 倾斜 3D tilt | https://uiarc.dev/components/glass-card/markdown | pro |
| glass-tabbar | Glass tab bar | Special | Liquid Glass 浮动 tab bar 折射 透镜 iOS 26 | https://uiarc.dev/components/glass-tabbar/markdown | pro |
| skeleton-morph | Skeleton morph | Special | 骨架屏逐块长成真实内容 | https://uiarc.dev/components/skeleton-morph/markdown | pro |
| orbit-logos | Orbit logos | Special | 集成 logo 环绕轨道展示 | https://uiarc.dev/components/orbit-logos/markdown | pro |
| sand-text | Sand text | Special | 沙粒标题 倾倒成字 光标挖散自愈 粒子文字 | https://uiarc.dev/components/sand-text/markdown | pro |
| gravity-well | Gravity well | Special | 重力井网格 随光标弯曲 点击冲击波 | https://uiarc.dev/components/gravity-well/markdown | pro |
| data-flow | Data flow | Special | 数据流示意动画 源→处理核心→目标 | https://uiarc.dev/components/data-flow/markdown | pro |
| payment-flow | Payment flow | Special | 支付链路动画 刷卡→处理方→卡组织→银行 授权结算 | https://uiarc.dev/components/payment-flow/markdown | pro |
| date-reel | Date reel | Special | iOS 滚轮式 3D 日期时间选择器 惯性吸附 | https://uiarc.dev/components/date-reel/markdown | pro |
| multi-region-failover | Multi-region failover | Special | 多区域故障转移 2.5D 架构动画 负载均衡 | https://uiarc.dev/components/multi-region-failover/markdown | pro |
| vector-search | Vector search | Special | 向量检索示意 文档嵌入平面聚类 RAG 可视化 | https://uiarc.dev/components/vector-search/markdown | pro |
| typewriter-terminal | Typewriter terminal | Special | 打字机终端 脚本化 CLI 会话 语法着色 | https://uiarc.dev/components/typewriter-terminal/markdown | pro |
| link-unfurl | Link unfurl | Special | 粘贴链接展开为富预览卡片 | https://uiarc.dev/components/link-unfurl/markdown | pro |
| release-readiness | Release readiness | Blocks | 发布就绪清单 进度+最终发布按钮 | https://uiarc.dev/components/blocks/release-readiness/markdown | pro |
| signup-form | Sign up form | Blocks | 注册表单 校验 密码强度 完成态 | `npx shadcn@latest add https://uiarc.dev/r/signup-form.json` |  |
| wallet-card | Wallet card | Blocks | 钱包卡片 余额 交易 转账操作 金融 | https://uiarc.dev/components/blocks/wallet-card/markdown | pro |
| logo-marquee | Logo marquee | Blocks | 品牌 logo 跑马灯 可暂停 | `npx shadcn@latest add https://uiarc.dev/r/logo-marquee.json` |  |
| team-directory | Team directory | Blocks | 团队通讯录 搜索 筛选 资料面板 | https://uiarc.dev/components/blocks/team-directory/markdown | pro |
| project-board | Project board | Blocks | 项目看板 kanban 拖拽阶段 | https://uiarc.dev/components/blocks/project-board/markdown | pro |
| invoice-studio | Invoice studio | Blocks | 可编辑发票 实时合计 | https://uiarc.dev/components/blocks/invoice-studio/markdown | pro |
| plan-comparison | Plan comparison | Blocks | 套餐对比 计费周期 | `npx shadcn@latest add https://uiarc.dev/r/plan-comparison.json` |  |
| availability-picker | Availability picker | Blocks | 多人可用时间 会议时间选择 | https://uiarc.dev/components/blocks/availability-picker/markdown | pro |
| metrics-dashboard | Metrics dashboard | Blocks | 分析仪表盘 KPI 标签 图表 Top 页面 | https://uiarc.dev/components/blocks/metrics-dashboard/markdown | pro |
| media-player | Media player | Blocks | 音频播放器 播放列表 | https://uiarc.dev/components/blocks/media-player/markdown | pro |
| support-conversation | Support conversation | Blocks | 客服对话线程 快捷回复 | https://uiarc.dev/components/blocks/support-conversation/markdown | pro |
| inbox-triage | Inbox triage | Blocks | 收件箱处理 归档 稍后 恢复 | https://uiarc.dev/components/blocks/inbox-triage/markdown | pro |
| command-palette | Command palette | Blocks | 命令面板 ⌘K 搜索分组 快捷键 | `npx shadcn@latest add https://uiarc.dev/r/command-palette.json` |  |
| notification-center | Notification center | Blocks | 通知中心 已读状态 分组 | `npx shadcn@latest add https://uiarc.dev/r/notification-center.json` |  |
| file-upload | File upload | Blocks | 文件上传流程 约束 进度 错误 | `npx shadcn@latest add https://uiarc.dev/r/file-upload.json` |  |
| otp-input | OTP input | Blocks | 六位验证码输入 OTP 粘贴 | `npx shadcn@latest add https://uiarc.dev/r/otp-input.json` |  |
| multi-step-form | Multi-step form | Blocks | 多步表单 向导 保留进度 | https://uiarc.dev/components/blocks/multi-step-form/markdown | pro |
| team-showcase | Team showcase | Blocks | 图片主导的团队介绍 原地展开 | https://uiarc.dev/components/blocks/team-showcase/markdown | pro |
| testimonial-stage | Studio perspectives | Blocks | 用户证言 肖像 编辑风 | https://uiarc.dev/components/blocks/testimonial-stage/markdown | pro |
| changelog-feed | Changelog feed | Blocks | 更新日志 筛选 按月滚动 | `npx shadcn@latest add https://uiarc.dev/r/changelog-feed.json` |  |
| usage-pricing | Usage pricing | Blocks | 拖拽座位/流量的定价计算器 | https://uiarc.dev/components/blocks/usage-pricing/markdown | pro |
| ai-composer | AI composer | Blocks | AI 助手对话 消息从输入框升起 流式回复 | https://uiarc.dev/components/blocks/ai-composer/markdown | pro |
| sign-in | Sign in | Blocks | 登录卡片 邮箱→验证码→账号 morph | `npx shadcn@latest add https://uiarc.dev/r/sign-in.json` |  |
| workspace-sidebar | Workspace sidebar | Blocks | 产品侧边栏 工作区切换 搜索 拖拽收藏 | https://uiarc.dev/components/blocks/workspace-sidebar/markdown | pro |
| settings-page | Settings page | Blocks | 账号设置页 滑动导航 保存条 morph | https://uiarc.dev/components/blocks/settings-page/markdown | pro |
| sidebar-rail | Sidebar rail | Blocks | 应用外壳 侧栏折叠成图标栏 手机端 sheet | https://uiarc.dev/components/blocks/sidebar-rail/markdown | pro |
| docs-sidebar | Docs sidebar | Blocks | 文档布局 导航树过滤 版本切换 页内目录 | https://uiarc.dev/components/blocks/docs-sidebar/markdown | pro |
| integrations | Integrations | Blocks | 集成目录 Connect→Connected | https://uiarc.dev/components/blocks/integrations/markdown | pro |
| billing-overview | Billing overview | Blocks | 账单页 套餐卡 morph 选择 用量 发票 | https://uiarc.dev/components/blocks/billing-overview/markdown | pro |
| api-keys | API keys | Blocks | API 密钥管理 创建表单 仅显示一次 | https://uiarc.dev/components/blocks/api-keys/markdown | pro |
| inbox-sidebar | Inbox sidebar | Blocks | 邮件侧栏 撰写按钮展开成编辑器 拖放到文件夹 | https://uiarc.dev/components/blocks/inbox-sidebar/markdown | pro |
| team-members | Team members | Blocks | 成员列表 邮箱变 chip 邀请 | https://uiarc.dev/components/blocks/team-members/markdown | pro |
| page-header | Page header | Blocks | 项目页头 滚动折叠成紧凑栏 tab 计数滚动 | `npx shadcn@latest add https://uiarc.dev/r/page-header.json` |  |
| revenue-explorer | Revenue explorer | Blocks | SaaS 收入图 刷选缩放 | https://uiarc.dev/components/blocks/revenue-explorer/markdown | pro |
| journey-flow | Journey flow | Blocks | 用户旅程桑基图 按渠道 morph | https://uiarc.dev/components/blocks/journey-flow/markdown | pro |
| empty-states | Empty states | Blocks | 四种空状态插画 切换 morph | `npx shadcn@latest add https://uiarc.dev/r/empty-states.json` |  |
| login-centered | Centered login | Blocks | 居中登录卡 passkey 优先 环形背景 | `npx shadcn@latest add https://uiarc.dev/r/login-centered.json` |  |
| login-immersive | Immersive login | Blocks | 沉浸式玻璃 magic link 登录 照片背景 | https://uiarc.dev/components/blocks/login-immersive/markdown | pro |
| security-settings | Security settings | Blocks | 安全设置 两步验证 改密 会话 | https://uiarc.dev/components/blocks/security-settings/markdown | pro |
| cancel-flow | Cancel flow | Blocks | 取消订阅挽留流程 定制优惠 长按取消 | https://uiarc.dev/components/blocks/cancel-flow/markdown | pro |
| login-split | Login split | Blocks | 左右分栏全屏登录 邮箱→密码 | https://uiarc.dev/components/blocks/login-split/markdown | pro |
| cohort-retention | Cohort retention | Blocks | 同期群留存三角 转留存曲线 | https://uiarc.dev/components/blocks/cohort-retention/markdown | pro |
| support-widget | Support widget | Blocks | 应用内帮助浮窗 文章搜索 聊天 | https://uiarc.dev/components/blocks/support-widget/markdown | pro |
| usage-forecast | Usage forecast | Blocks | 用量预测图 预测锥 预算线 | https://uiarc.dev/components/blocks/usage-forecast/markdown | pro |
| mrr-waterfall | MRR waterfall | Blocks | MRR 瀑布图 收入桥 | https://uiarc.dev/components/blocks/mrr-waterfall/markdown | pro |
| webhooks | Webhooks | Blocks | Webhook 控制台 投递历史 payload 检查 重试 | https://uiarc.dev/components/blocks/webhooks/markdown | pro |
| roles-permissions | Roles and permissions | Blocks | 角色权限矩阵 | https://uiarc.dev/components/blocks/roles-permissions/markdown | pro |
| metric-explorer | Metric explorer | Blocks | KPI 卡片展开成可擦洗图表 | https://uiarc.dev/components/blocks/metric-explorer/markdown | pro |
| activity-terrain | Activity terrain | Blocks | 3D 活动地形图 可旋转 转热力图 | https://uiarc.dev/components/blocks/activity-terrain/markdown | pro |
| revenue-globe | Revenue globe | Blocks | 点阵地球 支付弧线 3D globe | https://uiarc.dev/components/blocks/revenue-globe/markdown | pro |
| customer-galaxy | Customer galaxy | Blocks | 2400 客户星系 粒子聚类 | https://uiarc.dev/components/blocks/customer-galaxy/markdown | pro |
| semantic-zoom | Semantic zoom | Blocks | 无限缩放公司地图 语义缩放 | https://uiarc.dev/components/blocks/semantic-zoom/markdown | pro |
| layout-morph | Layout morph | Blocks | 24 卡片在网格/瀑布/列表/扇形/轮播/3D 螺旋间切换 | https://uiarc.dev/components/blocks/layout-morph/markdown | pro |
| agent-run | Agent run | Blocks | AI agent 运行过程 步骤流 工具调用 diff 审批 | https://uiarc.dev/components/blocks/agent-run/markdown | pro |
| week-calendar | Week calendar | Blocks | 周日历 拖拽创建/移动/调整事件 | https://uiarc.dev/components/blocks/week-calendar/markdown | pro |
| scroll-story | Scroll story | Blocks | 滚动叙事 固定产品视图随文案步骤变化 scrollytelling | https://uiarc.dev/components/blocks/scroll-story/markdown | pro |
| spotlight-grid | Spotlight grid | Blocks | 光随指针的特性网格 卡片 morph 详情 | https://uiarc.dev/components/blocks/spotlight-grid/markdown | pro |
| invite-people | Invite people | Blocks | 邀请成员 角色 批量粘贴 席位 | https://uiarc.dev/components/blocks/invite-people/markdown | pro |
| cart-drawer | Cart drawer | Blocks | 购物车抽屉 商品飞入 运费进度 | https://uiarc.dev/components/blocks/cart-drawer/markdown | pro |
| pricing-calculator | Pricing calculator | Blocks | 定价计算器 座位滑块 推荐徽章移动 | https://uiarc.dev/components/blocks/pricing-calculator/markdown | pro |
| ai-chat | AI chat | Blocks | 完整 AI 聊天 流式 markdown 推理折叠 工具 chip 引用 模型切换 | https://uiarc.dev/components/blocks/ai-chat/markdown | pro |
| checkout-summary | Checkout summary | Blocks | 订单摘要 优惠码 税费 支付按钮状态 | https://uiarc.dev/components/blocks/checkout-summary/markdown | pro |
| site-header | Site header | Blocks | 网站顶栏 滚动变实心 mega menu 移动端菜单 | `npx shadcn@latest add https://uiarc.dev/r/site-header.json` |  |
| site-footer | Site footer | Blocks | 网站页脚 链接列 订阅 | `npx shadcn@latest add https://uiarc.dev/r/site-footer.json` |  |
| hero-section | Hero section | Blocks | 三种全屏 SaaS hero 首屏 | `npx shadcn@latest add https://uiarc.dev/r/hero-section.json` |  |
| faq-section | FAQ section | Blocks | FAQ 手风琴/主题栏/可搜索 | `npx shadcn@latest add https://uiarc.dev/r/faq-section.json` |  |
| contact-section | Contact section | Blocks | 联系表单 morph 确认 办公室卡片 | `npx shadcn@latest add https://uiarc.dev/r/contact-section.json` |  |
| settings-command | Settings command | Blocks | 设置搜索框展开成命令面板 | https://uiarc.dev/components/blocks/settings-command/markdown | pro |
| usage-billing | Usage billing | Blocks | 按量计费仪表盘 预计支出 限额 | https://uiarc.dev/components/blocks/usage-billing/markdown | pro |
| ai-side-panel | AI side panel | Blocks | 侧边 AI 助手面板 上下文 chip 应用修改 | https://uiarc.dev/components/blocks/ai-side-panel/markdown | pro |
| kpi-drilldown | KPI drilldown | Blocks | KPI 卡片展开详情图 同比 拆解表 | https://uiarc.dev/components/blocks/kpi-drilldown/markdown | pro |
| blog-grid | Blog grid | Blocks | 博客列表 精选 分类 分页 阅读器 | `npx shadcn@latest add https://uiarc.dev/r/blog-grid.json` |  |
| comparison-table | Comparison table | Blocks | 竞品对比表 sticky 表头 | `npx shadcn@latest add https://uiarc.dev/r/comparison-table.json` |  |
| feature-bento | Feature bento | Blocks | 六格 bento 特性展示 悬停演示 | https://uiarc.dev/components/blocks/feature-bento/markdown | pro |
| stats-band | Stats band | Blocks | 统计数字带 进入视口计数 | `npx shadcn@latest add https://uiarc.dev/r/stats-band.json` |  |
| cta-section | CTA section | Blocks | 行动号召 CTA 区块 | `npx shadcn@latest add https://uiarc.dev/r/cta-section.json` |  |
| newsletter-signup | Newsletter signup | Blocks | 邮件订阅 往期堆叠 | `npx shadcn@latest add https://uiarc.dev/r/newsletter-signup.json` |  |
| product-listing | Product listing | Blocks | 商品列表 筛选 排序 快速加购 | https://uiarc.dev/components/blocks/product-listing/markdown | pro |
| product-detail | Product detail | Blocks | 商品详情页 图集 变体 加入购物袋 | https://uiarc.dev/components/blocks/product-detail/markdown | pro |
| hero-signup | Hero signup | Blocks | 等待列表 hero 网格渐变 邮箱校验 | https://uiarc.dev/components/blocks/hero-signup/markdown | pro |
| search-results | Search results | Blocks | 分面搜索结果页 | https://uiarc.dev/components/blocks/search-results/markdown | pro |
| market-terminal | Market terminal | Blocks | 交易终端 K 线 canvas 下单 | https://uiarc.dev/components/blocks/market-terminal/markdown | pro |
| budget-variance | Budget variance | Blocks | 预算与实际 子弹图 差异 | https://uiarc.dev/components/blocks/budget-variance/markdown | pro |
| choropleth-explorer | Choropleth explorer | Blocks | 分级统计地图 按州/区域着色 | https://uiarc.dev/components/blocks/choropleth-explorer/markdown | pro |
| small-multiples | Small multiples | Blocks | 小多图 同步十字线 | https://uiarc.dev/components/blocks/small-multiples/markdown | pro |
| connected-scatter | Connected scatter | Blocks | 连接散点图 CAC vs LTV | https://uiarc.dev/components/blocks/connected-scatter/markdown | pro |
| line-replay | Line replay | Blocks | 折线回放 播放头 关键时刻注释 | https://uiarc.dev/components/blocks/line-replay/markdown | pro |
| template:arc-saas | Arc SaaS | Templates | SaaS 完整入门模板 | https://uiarc.dev/templates | pro |
| template:arc-ai | Arc AI | Templates | AI 应用完整模板 | https://uiarc.dev/templates | pro |
| template:arc-startup | Arc Startup | Templates | 创业公司营销站模板 | https://uiarc.dev/templates | pro |

## 未解决
- Pro 源码（43 组件、66 block、3 模板）需 Pro 订阅 token（`/r/pro/{name}.json` 返回 401），未获取，仅列出文档 markdown 链接。
- Pro skills（全页生成、设计系统生成、重构到 Arc、各类审计）仅对登录的 Pro 会员开放（`/api/skills`），未获取。
- MCP 服务 `https://uiarc.dev/api/mcp` 需 OAuth 登录（免费账号即可），按规则未注册未测试。
- `https://uiarc.dev/license` 页面 curl 返回空正文（客户端渲染），许可细节取自 pricing 页与组件 markdown 的 "Free, open source" 标注，未见明确的 MIT 字样。
