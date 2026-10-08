---
id: shadcn
name: shadcn/ui
url: https://ui.shadcn.com/
kind: component-library
stack: React + Tailwind CSS v4 + Base UI / Radix UI / React Aria（三选一）+ cva + cn；图表用 Recharts
license: MIT
pro: none
fetch: shadcn-registry
coverage: 全量：官方 registry 的 base-nova、radix-nova、aria-nova、new-york-v4 四个 style；refresh 自动比对
catalog_checked: 2026-10-07
source_status: active
visual_style: restrained neutral, style presets vary
foundation: own-tokens
styling: tailwind-v4
motion_lib: css
dark_mode: class
mixing_notes: 通常就是主底座，其他来源向它映射；它的 --accent 是浅色 hover 底而不是品牌色，别家的 --accent 应映射到 --primary
---
## 是什么 / 什么时候用
shadcn/ui 是"把源码复制进项目"的 React 组件集合和代码分发平台：CLI 把组件源码写进 `components/ui/`，代码归你所有、可随意改。覆盖表单、浮层、导航、反馈、数据展示、聊天界面（MessageScroller/Message/Bubble/Attachment/Marker/Questionnaire）等 63 个基础组件，另有登录/注册/侧边栏/仪表盘 block、70 个 Recharts 图表、主题与字体。做任何 React + Tailwind 的后台、SaaS、表单、AI 聊天界面时，都应先用它做基础层，再叠加其他走 shadcn registry 的第三方库（magicui、aceternity、react-bits 等）。不适合：非 React 项目（Vue/Svelte 需用社区移植版 shadcn-vue / shadcn-svelte，不在本索引内）。

## 按需获取方法

### 0. 关键概念（2026-10 现状，已实测）
- **base（底层原语库）**：`base`（Base UI，2026-07 起为默认）、`radix`、`aria`（React Aria，2026-07 新增）。
- **style（视觉风格）**：`vega` `nova` `maia` `lyra` `mira` `luma` `rhea` `sera`。项目的 `components.json` 里 `"style"` 写成 `{base}-{style}`，如 `base-nova`、`radix-vega`、`aria-luma`。
- **旧 style**：`new-york-v4`（Tailwind v4 + Radix 的上一代，仍在线，**图表 chart-\* 和主题 theme-\* 只在这里**）、`new-york` / `default`（Tailwind v3 旧版，文档在 https://v3.shadcn.com）。
- CLI 根据 `components.json` 的 style 自动拼 URL：`https://ui.shadcn.com/r/styles/{style}/{name}.json`。没有 components.json 时 `view/search` 默认用 `new-york-v4`。

### 1. 机器可读入口（全部 curl 实测 200）
| 用途 | URL |
|---|---|
| 某 style 的完整清单（含 ui/block/example/font/lib/hook） | `https://ui.shadcn.com/r/styles/{style}/registry.json`，如 `.../base-nova/registry.json`（216 条）、`.../radix-nova/registry.json`（214）、`.../aria-nova/registry.json`（210）、`.../new-york-v4/registry.json`（471，含 chart/theme） |
| 单个条目 JSON（含完整源码 `files[].content`、`dependencies`、`registryDependencies`、`cssVars`） | `https://ui.shadcn.com/r/styles/{style}/{name}.json` |
| 旧版 ui 索引（63 条，仅名称和依赖） | `https://ui.shadcn.com/r/index.json` |
| 24 个预设（base×style、字体、图标库） | `https://ui.shadcn.com/r/config.json` |
| 第三方 registry 目录（430 个命名空间，含健康度） | `https://ui.shadcn.com/r/registries.json` |
| base color 主题 token | `https://ui.shadcn.com/r/colors/{neutral\|stone\|zinc\|mauve\|olive\|mist\|taupe\|gray\|slate}.json` |
| 旧主题 | `https://ui.shadcn.com/r/themes/{neutral\|stone\|zinc\|gray\|slate}.json`、`https://ui.shadcn.com/r/themes.css` |
| Tailwind 色板 | `https://ui.shadcn.com/r/colors/index.json` |
| 文档索引 | `https://ui.shadcn.com/llms.txt`（`/llms-full.txt` 404） |
| 任意文档页的 Markdown 版 | 在页面 URL 后加 `.md`，如 `https://ui.shadcn.com/docs/components/base/button.md`（组件文档按 base 分：`/docs/components/{base\|radix\|aria}/{name}`） |
| sitemap | `https://ui.shadcn.com/sitemap.xml` |
| GitHub 源码 | `https://raw.githubusercontent.com/shadcn-ui/ui/main/apps/v4/registry/bases/{base}/ui/{name}.tsx`（实测 200）；图表 `apps/v4/registry/new-york-v4/charts/{name}.tsx` |
| Schema | `https://ui.shadcn.com/schema/registry.json`、`https://ui.shadcn.com/schema/registry-item.json` |

不可用（实测 404）：`/r/registry.json`、`/registry.json`、`/llms-full.txt`、`/r/{name}.json`（顶层无 style）、`/r/styles/{新style}/chart-*.json`、`/r/styles/{新style}/theme-*.json`、`/r/styles/{新style}/*-demo.json`。

### 2. 安装（推荐）
```bash
# 新项目：初始化（默认 Base UI；要 Radix 加 -b radix，要 React Aria 加 -b aria）
npx shadcn@latest init                 # 交互
npx shadcn@latest init -b radix -p radix-nova
npx shadcn@latest init -t vite         # 模板：next | vite | start | react-router | laravel | astro

# 加组件 / block（自动按项目 style 取对应实现，并递归装 registryDependencies 与 npm 依赖）
npx shadcn@latest add {name}
npx shadcn@latest add button card dialog
npx shadcn@latest add sidebar-07 login-03 dashboard-01

# 图表：只存在于 new-york-v4，新 style 项目必须用完整 URL（依赖 card/chart 会按项目 style 解析）
npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/{name}.json

# 先看再装
npx shadcn@latest add {name} --dry-run      # 预览将写入的文件与依赖
npx shadcn@latest add {name} --view components/ui/{name}.tsx
npx shadcn@latest view {name}               # 打印 registry JSON（含源码）
npx shadcn@latest docs {name} -b base       # 输出文档与示例链接
npx shadcn@latest search @shadcn -q sidebar -t block --json
```
**实测例子**（CLI 4.21.3，2026-10-07）：
- `curl https://ui.shadcn.com/r/styles/base-nova/button.json` → 200，`files[0].path = registry/base-nova/ui/button.tsx`，源码 `import { Button as ButtonPrimitive } from "@base-ui/react/button"`、`import { cn } from "cn"`。
- `npx shadcn@latest search @shadcn -q sidebar -l 5` → "Found 31 items matching "sidebar" in @shadcn"。
- 在 `style: base-nova` 项目中 `npx shadcn@latest view chart-area-default` → 报错 "…/r/styles/base-nova/chart-area-default.json was not found"；改用 `npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-area-default.json --dry-run` → 成功，写入 `components/ui/card.tsx`、`components/ui/chart.tsx`、`components/chart-area-default.tsx`，依赖 `cn`、`recharts@3.8.0`。

### 3. 不用 CLI 直接取源码
```bash
curl -s https://ui.shadcn.com/r/styles/base-nova/{name}.json | jq -r '.files[] | "// \(.path)\n\(.content)"'
curl -s https://ui.shadcn.com/r/styles/base-nova/{name}.json | jq '{dependencies, registryDependencies, cssVars}'
```
注意 JSON 里的 import 路径是 `@/registry/{style}/ui/...`，手动复制时要改成项目别名 `@/components/ui/...`（CLI 会自动改写）。依赖：`dependencies` 里的包用 npm 装（如 `@base-ui/react`、`radix-ui`、`react-aria-components`、`cn`、`class-variance-authority`、`lucide-react`、`recharts`）；`registryDependencies` 里的条目要递归取。

### 4. 非 registry 的内容
- **Typeset**（markdown 排版 CSS）：`curl https://ui.shadcn.com/typeset.css`（实测 200，text/plain），或在 https://ui.shadcn.com/typeset 构建器里生成预设；`@import "./typeset.css"` 后用 `<div className="typeset typeset-docs">`。
- **shimmer / scroll-fade 工具类**：在 `shadcn` npm 包的 `shadcn/tailwind.css` 里，`init` 已自动 `@import "shadcn/tailwind.css"`。
- **@shadcn/react**（headless Questionnaire、MessageScroller）与 **@shadcn/helpers**（ai-sdk / tanstack-ai 假会话）：`npm install @shadcn/react` / `npm install @shadcn/helpers`。
- **主题/预设**：https://ui.shadcn.com/create 可视化生成，得到预设码后 `npx shadcn@latest apply {code}` 或 `init --preset {code}`；`npx shadcn@latest preset decode {code}` 可解码。
- **MCP**：`npx shadcn@latest mcp init --client claude`（也支持 codex/cursor/opencode/vscode）。**Skill**：`npx skills add shadcn/ui`（含 Radix→Base UI 迁移知识）。

### 5. Registry 目录与第三方命名空间（其他库也走这一套）
- **内置目录**：https://ui.shadcn.com/docs/directory 列出的社区 registry 已内置在 CLI，无需配置，直接 `npx shadcn@latest add @{namespace}/{item}`。完整机器可读目录：`https://ui.shadcn.com/r/registries.json`（实测 430 个，字段 `name`、`homepage`、`url`（含 `{name}` 占位）、`description`、`health.status`（healthy 342 / degraded 43 / unavailable 38 / observing 7）、`ranking.itemCount`）。其中包含 `@magicui` `@aceternity` `@react-bits` `@animate-ui` `@kibo-ui` `@motion-primitives` `@coss` `@reui` `@tailark` `@shadcnblocks` `@8bitcn` `@ai-elements` 等。
  ```bash
  curl -s https://ui.shadcn.com/r/registries.json | jq -r '.[] | select(.name=="@magicui") | .url'
  npx shadcn@latest search @magicui -q marquee     # 实测：Found 6 items
  npx shadcn@latest view @magicui/marquee
  npx shadcn@latest add @magicui/marquee
  ```
- **自定义命名空间**：在 `components.json` 中加
  ```json
  { "registries": {
      "@acme": "https://registry.acme.com/r/{name}.json",
      "@themes": "https://registry.example.com/{style}/{name}.json",
      "@private": { "url": "https://api.co/r/{name}.json", "headers": { "Authorization": "Bearer ${REGISTRY_TOKEN}" } } } }
  ```
  `{name}` 必填，`{style}` 可选（替换为项目 style）；支持 env 变量做鉴权。或用 `npx shadcn@latest registry add @acme=https://...`。
- **直接 URL / 本地文件**：`npx shadcn@latest add https://example.com/r/foo.json`、`npx shadcn@latest add ./foo.json`。
- **GitHub 源 registry**（2026-06 起）：仓库根目录有 `registry.json` 即可 `npx shadcn@latest add {owner}/{repo}/{item}`，不需要 build；私有仓库也支持（2026-08）。
- **搜索**：`npx shadcn@latest search @a @b -q {kw} -t ui,block --json`；registry 可实现 `?q=&limit=&offset=` 的服务端动态搜索。
- 编程接口：npm 包 `shadcn/registry` 导出 `getRegistries`、`searchRegistries`、`getRegistryItems`、`resolveRegistryItems` 等（文档 https://ui.shadcn.com/docs/registry/api-reference.md）。

## 使用注意
- **默认 base 已变**：2026-07 起 `init` 默认 Base UI。Base UI 组件用 `render` prop 而不是 Radix 的 `asChild`；网上大量旧示例是 Radix 写法，混用会报类型错。CI 里想保持 Radix 要显式 `-b radix`。
- **按 base 的差异**：`toast` 只有 base（radix/aria 文档写明已弃用，改用 `sonner`）；`menubar`、`navigation-menu` 在 aria 没有；`form`（react-hook-form 封装）是旧组件，新代码用 `field`。
- **图表/主题只在 new-york-v4**：新 style 项目装 chart-* 必须用完整 URL；装完的图表代码导入 `@/components/ui/chart`，与新 style 的 chart 组件兼容（dry-run 已验证）。
- **cn 包**：2026-09 起组件 `import { cn } from "cn"`（不再是 `@/lib/utils` 的 clsx+tailwind-merge）。老项目可 `npx shadcn@latest migrate cn`。手动复制源码时记得装 `cn`。
- **Tailwind v4 必需**（当前站点）；Tailwind v3 项目请用 https://v3.shadcn.com 与 `new-york`/`default` style，二者 CSS 变量格式不同（v4 用 oklch + `@theme inline`）。
- 依赖 `tw-animate-css`（替代 tailwindcss-animate）和 `shadcn/tailwind.css`；图标库随预设可能是 lucide / tabler / hugeicons / phosphor，可 `migrate icons` 切换。
- 第三方 registry 代码不受 shadcn 审核，`add` 前先 `view` 或 `--dry-run`；部分 registry 依赖 `motion`（不是 `framer-motion`）、`gsap`、`three` 等。
- 示例条目（`*-demo`、`*-example`）安装后会写入 `components/` 下的示例文件，一般只用来参考，不建议直接 `add` 进生产项目。

## 组件清单
共 565 条（tsv 逐条）：组件 63、block 30（含 3 个 preview）、图表 70、主题/配色/预设 17、字体 52、lib/hook 2、非 registry 工具/包/指南 12、示例 319。下表先列示例以外的 246 条，示例按组件分组列在后面。
获取列格式：`命令 ; URL`。`base-nova` 只是示范 style，换成你项目的 `{base}-{style}` 即可（radix-nova、aria-luma 等，URL 结构相同）。

| id | 名称 | 分类 | 一句话用途 | 获取（具体命令或URL） | 备注 |
|---|---|---|---|---|---|
| accordion | Accordion | component/layout | 手风琴折叠面板 Accordion，FAQ | npx shadcn@latest add accordion ; https://ui.shadcn.com/r/styles/base-nova/accordion.json |  |
| alert | Alert | component/feedback | 提示条 Alert，信息/警告/错误消息横幅 | npx shadcn@latest add alert ; https://ui.shadcn.com/r/styles/base-nova/alert.json |  |
| alert-dialog | Alert Dialog | component/overlay | 确认对话框 AlertDialog，危险操作二次确认 | npx shadcn@latest add alert-dialog ; https://ui.shadcn.com/r/styles/base-nova/alert-dialog.json |  |
| aspect-ratio | Aspect Ratio | component/display | 固定宽高比容器 AspectRatio，图片/视频 | npx shadcn@latest add aspect-ratio ; https://ui.shadcn.com/r/styles/base-nova/aspect-ratio.json |  |
| avatar | Avatar | component/display | 头像 Avatar，头像组 avatar group | npx shadcn@latest add avatar ; https://ui.shadcn.com/r/styles/base-nova/avatar.json |  |
| badge | Badge | component/feedback | 徽标 Badge，状态标签 tag | npx shadcn@latest add badge ; https://ui.shadcn.com/r/styles/base-nova/badge.json |  |
| breadcrumb | Breadcrumb | component/layout | 面包屑导航 Breadcrumb | npx shadcn@latest add breadcrumb ; https://ui.shadcn.com/r/styles/base-nova/breadcrumb.json |  |
| button | Button | component/form | 按钮 Button，多种 variant/size，icon 按钮 | npx shadcn@latest add button ; https://ui.shadcn.com/r/styles/base-nova/button.json |  |
| button-group | Button Group | component/form | 按钮组 ButtonGroup，分段按钮、split button、与输入框拼接 | npx shadcn@latest add button-group ; https://ui.shadcn.com/r/styles/base-nova/button-group.json |  |
| calendar | Calendar | component/form | 日历 Calendar，日期选择，基于 react-day-picker，支持范围/多月/伊斯兰历 | npx shadcn@latest add calendar ; https://ui.shadcn.com/r/styles/base-nova/calendar.json |  |
| card | Card | component/display | 卡片容器 Card | npx shadcn@latest add card ; https://ui.shadcn.com/r/styles/base-nova/card.json |  |
| carousel | Carousel | component/display | 轮播 Carousel，基于 Embla | npx shadcn@latest add carousel ; https://ui.shadcn.com/r/styles/base-nova/carousel.json |  |
| chart | Chart | component/display | 图表基础组件 Chart（Recharts 封装 ChartContainer/Tooltip/Legend） | npx shadcn@latest add chart ; https://ui.shadcn.com/r/styles/base-nova/chart.json |  |
| checkbox | Checkbox | component/form | 复选框 Checkbox | npx shadcn@latest add checkbox ; https://ui.shadcn.com/r/styles/base-nova/checkbox.json |  |
| collapsible | Collapsible | component/misc | 可折叠容器 Collapsible，展开/收起 | npx shadcn@latest add collapsible ; https://ui.shadcn.com/r/styles/base-nova/collapsible.json |  |
| combobox | Combobox | component/form | 可搜索下拉 Combobox，自动补全 autocomplete、多选 chips | npx shadcn@latest add combobox ; https://ui.shadcn.com/r/styles/base-nova/combobox.json |  |
| command | Command | component/overlay | 命令面板 Command（cmdk），⌘K 搜索、快捷操作 | npx shadcn@latest add command ; https://ui.shadcn.com/r/styles/base-nova/command.json |  |
| context-menu | Context Menu | component/overlay | 右键菜单 ContextMenu | npx shadcn@latest add context-menu ; https://ui.shadcn.com/r/styles/base-nova/context-menu.json |  |
| dialog | Dialog | component/overlay | 模态对话框 Dialog modal | npx shadcn@latest add dialog ; https://ui.shadcn.com/r/styles/base-nova/dialog.json |  |
| drawer | Drawer | component/overlay | 移动端抽屉 Drawer，基于 Vaul，底部弹出 | npx shadcn@latest add drawer ; https://ui.shadcn.com/r/styles/base-nova/drawer.json |  |
| dropdown-menu | Dropdown Menu | component/overlay | 下拉菜单 DropdownMenu，带勾选/单选/子菜单 | npx shadcn@latest add dropdown-menu ; https://ui.shadcn.com/r/styles/base-nova/dropdown-menu.json |  |
| empty | Empty | component/feedback | 空状态 Empty，无数据/404/空列表占位 | npx shadcn@latest add empty ; https://ui.shadcn.com/r/styles/base-nova/empty.json |  |
| field | Field | component/form | 表单字段容器 Field：label、描述、错误信息、fieldset 组合，表单布局 | npx shadcn@latest add field ; https://ui.shadcn.com/r/styles/base-nova/field.json |  |
| form | Form | component/form | 旧版 Form（react-hook-form 封装），新项目推荐 Field | npx shadcn@latest add form ; https://ui.shadcn.com/r/styles/base-nova/form.json | legacy，推荐 field |
| hover-card | Hover Card | component/overlay | 悬停卡片 HoverCard，鼠标悬停预览用户/链接 | npx shadcn@latest add hover-card ; https://ui.shadcn.com/r/styles/base-nova/hover-card.json |  |
| input | Input | component/form | 文本输入框 Input | npx shadcn@latest add input ; https://ui.shadcn.com/r/styles/base-nova/input.json |  |
| input-group | Input Group | component/form | 输入框组 InputGroup，前后缀 addon、图标、按钮、内嵌 spinner | npx shadcn@latest add input-group ; https://ui.shadcn.com/r/styles/base-nova/input-group.json |  |
| input-otp | Input Otp | component/form | 一次性验证码输入 InputOTP，OTP/短信验证码 | npx shadcn@latest add input-otp ; https://ui.shadcn.com/r/styles/base-nova/input-otp.json |  |
| item | Item | component/display | 通用列表项 Item，列表/菜单/设置项行，带图标头像操作 | npx shadcn@latest add item ; https://ui.shadcn.com/r/styles/base-nova/item.json |  |
| label | Label | component/form | 表单标签 Label | npx shadcn@latest add label ; https://ui.shadcn.com/r/styles/base-nova/label.json |  |
| menubar | Menubar | component/overlay | 桌面应用式菜单栏 Menubar（aria base 无） | npx shadcn@latest add menubar ; https://ui.shadcn.com/r/styles/base-nova/menubar.json | 仅 base/radix |
| navigation-menu | Navigation Menu | component/layout | 导航菜单 NavigationMenu，带下拉的站点顶部导航 mega menu（aria base 无） | npx shadcn@latest add navigation-menu ; https://ui.shadcn.com/r/styles/base-nova/navigation-menu.json | 仅 base/radix |
| pagination | Pagination | component/misc | 分页 Pagination | npx shadcn@latest add pagination ; https://ui.shadcn.com/r/styles/base-nova/pagination.json |  |
| popover | Popover | component/overlay | 气泡弹层 Popover | npx shadcn@latest add popover ; https://ui.shadcn.com/r/styles/base-nova/popover.json |  |
| progress | Progress | component/feedback | 进度条 Progress | npx shadcn@latest add progress ; https://ui.shadcn.com/r/styles/base-nova/progress.json |  |
| radio-group | Radio Group | component/form | 单选组 RadioGroup | npx shadcn@latest add radio-group ; https://ui.shadcn.com/r/styles/base-nova/radio-group.json |  |
| resizable | Resizable | component/layout | 可拖拽调整大小的面板 Resizable panels，分栏布局 | npx shadcn@latest add resizable ; https://ui.shadcn.com/r/styles/base-nova/resizable.json |  |
| scroll-area | Scroll Area | component/layout | 自定义滚动条区域 ScrollArea | npx shadcn@latest add scroll-area ; https://ui.shadcn.com/r/styles/base-nova/scroll-area.json |  |
| select | Select | component/form | 下拉选择 Select | npx shadcn@latest add select ; https://ui.shadcn.com/r/styles/base-nova/select.json |  |
| separator | Separator | component/layout | 分隔线 Separator | npx shadcn@latest add separator ; https://ui.shadcn.com/r/styles/base-nova/separator.json |  |
| sheet | Sheet | component/overlay | 侧滑面板 Sheet（上下左右滑出的 drawer） | npx shadcn@latest add sheet ; https://ui.shadcn.com/r/styles/base-nova/sheet.json |  |
| sidebar | Sidebar | component/layout | 应用侧边栏 Sidebar，可折叠为图标、inset/floating，后台布局 | npx shadcn@latest add sidebar ; https://ui.shadcn.com/r/styles/base-nova/sidebar.json |  |
| skeleton | Skeleton | component/feedback | 骨架屏 Skeleton，加载占位 | npx shadcn@latest add skeleton ; https://ui.shadcn.com/r/styles/base-nova/skeleton.json |  |
| slider | Slider | component/form | 滑块 Slider，范围选择 range | npx shadcn@latest add slider ; https://ui.shadcn.com/r/styles/base-nova/slider.json |  |
| sonner | Sonner | component/feedback | Toast 通知 Sonner（sonner 库），radix/aria 推荐用它 | npx shadcn@latest add sonner ; https://ui.shadcn.com/r/styles/base-nova/sonner.json |  |
| spinner | Spinner | component/feedback | 加载转圈 Spinner，loading 指示器 | npx shadcn@latest add spinner ; https://ui.shadcn.com/r/styles/base-nova/spinner.json |  |
| switch | Switch | component/form | 开关 Switch toggle | npx shadcn@latest add switch ; https://ui.shadcn.com/r/styles/base-nova/switch.json |  |
| table | Table | component/display | 基础表格 Table（数据表格见 data-table 示例） | npx shadcn@latest add table ; https://ui.shadcn.com/r/styles/base-nova/table.json |  |
| tabs | Tabs | component/layout | 标签页 Tabs | npx shadcn@latest add tabs ; https://ui.shadcn.com/r/styles/base-nova/tabs.json |  |
| textarea | Textarea | component/form | 多行文本输入 Textarea | npx shadcn@latest add textarea ; https://ui.shadcn.com/r/styles/base-nova/textarea.json |  |
| toast | Toast | component/feedback | Toast 通知（Base UI 原生，仅 base），支持 action、promise、堆叠、滑动关闭 | npx shadcn@latest add toast ; https://ui.shadcn.com/r/styles/base-nova/toast.json | 仅 base |
| toggle | Toggle | component/misc | 切换按钮 Toggle（按下/弹起） | npx shadcn@latest add toggle ; https://ui.shadcn.com/r/styles/base-nova/toggle.json |  |
| toggle-group | Toggle Group | component/misc | 切换按钮组 ToggleGroup，工具栏格式按钮 | npx shadcn@latest add toggle-group ; https://ui.shadcn.com/r/styles/base-nova/toggle-group.json |  |
| tooltip | Tooltip | component/overlay | 文字提示 Tooltip | npx shadcn@latest add tooltip ; https://ui.shadcn.com/r/styles/base-nova/tooltip.json |  |
| kbd | Kbd | component/display | 键盘按键显示 Kbd，快捷键提示 | npx shadcn@latest add kbd ; https://ui.shadcn.com/r/styles/base-nova/kbd.json |  |
| native-select | Native Select | component/form | 原生 select 样式化 NativeSelect | npx shadcn@latest add native-select ; https://ui.shadcn.com/r/styles/base-nova/native-select.json |  |
| direction | Direction | component/misc | 文字方向 Provider Direction，RTL 支持 | npx shadcn@latest add direction ; https://ui.shadcn.com/r/styles/base-nova/direction.json |  |
| attachment | Attachment | component/chat | 附件展示 Attachment，文件/图片、上传状态、元数据 | npx shadcn@latest add attachment ; https://ui.shadcn.com/r/styles/base-nova/attachment.json |  |
| bubble | Bubble | component/chat | 聊天气泡 Bubble，variants、对齐、reactions | npx shadcn@latest add bubble ; https://ui.shadcn.com/r/styles/base-nova/bubble.json |  |
| message-scroller | Message Scroller | component/chat | 聊天滚动容器 MessageScroller，AI 对话流式回复锚定、历史加载、跳转消息 | npx shadcn@latest add message-scroller ; https://ui.shadcn.com/r/styles/base-nova/message-scroller.json |  |
| questionnaire | Questionnaire | component/chat | 多步问卷 Questionnaire，单选/多选/自由输入/跳过，AI human-in-the-loop 追问 | npx shadcn@latest add questionnaire ; https://ui.shadcn.com/r/styles/base-nova/questionnaire.json |  |
| marker | Marker | component/chat | 对话中的状态标记 Marker，系统提示、分隔行、标签行 | npx shadcn@latest add marker ; https://ui.shadcn.com/r/styles/base-nova/marker.json |  |
| message | Message | component/chat | 聊天消息行 Message，头像、对齐、header/footer，AI chat | npx shadcn@latest add message ; https://ui.shadcn.com/r/styles/base-nova/message.json |  |
| dashboard-01 | Dashboard 01 | block/dashboard | 后台仪表盘整页：侧边栏 + 指标卡 + 交互面积图 + 可拖拽数据表 data table（A dashboard with sidebar, charts and data table.） | npx shadcn@latest add dashboard-01 ; https://ui.shadcn.com/r/styles/base-nova/dashboard-01.json | 全部 base/style 均可用 |
| sidebar-01 | Sidebar 01 | block/sidebar | 侧边栏：按分组的简单导航（A simple sidebar with navigation grouped by section.） | npx shadcn@latest add sidebar-01 ; https://ui.shadcn.com/r/styles/base-nova/sidebar-01.json | 全部 base/style 均可用 |
| sidebar-02 | Sidebar 02 | block/sidebar | 侧边栏：可折叠分组（A sidebar with collapsible sections.） | npx shadcn@latest add sidebar-02 ; https://ui.shadcn.com/r/styles/base-nova/sidebar-02.json | 全部 base/style 均可用 |
| sidebar-03 | Sidebar 03 | block/sidebar | 侧边栏：带子菜单（A sidebar with submenus.） | npx shadcn@latest add sidebar-03 ; https://ui.shadcn.com/r/styles/base-nova/sidebar-03.json | 全部 base/style 均可用 |
| sidebar-04 | Sidebar 04 | block/sidebar | 浮动 floating 侧边栏带子菜单（A floating sidebar with submenus.） | npx shadcn@latest add sidebar-04 ; https://ui.shadcn.com/r/styles/base-nova/sidebar-04.json | 全部 base/style 均可用 |
| sidebar-05 | Sidebar 05 | block/sidebar | 侧边栏：可折叠子菜单（A sidebar with collapsible submenus.） | npx shadcn@latest add sidebar-05 ; https://ui.shadcn.com/r/styles/base-nova/sidebar-05.json | 全部 base/style 均可用 |
| sidebar-06 | Sidebar 06 | block/sidebar | 侧边栏：子菜单以下拉菜单呈现（A sidebar with submenus as dropdowns.） | npx shadcn@latest add sidebar-06 ; https://ui.shadcn.com/r/styles/base-nova/sidebar-06.json | 全部 base/style 均可用 |
| sidebar-07 | Sidebar 07 | block/sidebar | 可折叠为图标栏的侧边栏（最常用后台布局）（A sidebar that collapses to icons.） | npx shadcn@latest add sidebar-07 ; https://ui.shadcn.com/r/styles/base-nova/sidebar-07.json | 全部 base/style 均可用 |
| sidebar-08 | Sidebar 08 | block/sidebar | inset 内嵌侧边栏 + 次级导航（An inset sidebar with secondary navigation.） | npx shadcn@latest add sidebar-08 ; https://ui.shadcn.com/r/styles/base-nova/sidebar-08.json | 全部 base/style 均可用 |
| sidebar-09 | Sidebar 09 | block/sidebar | 多级嵌套可折叠侧边栏（邮件客户端式）（Collapsible nested sidebars.） | npx shadcn@latest add sidebar-09 ; https://ui.shadcn.com/r/styles/base-nova/sidebar-09.json | 全部 base/style 均可用 |
| sidebar-10 | Sidebar 10 | block/sidebar | 放在 popover 里的侧边栏（A sidebar in a popover.） | npx shadcn@latest add sidebar-10 ; https://ui.shadcn.com/r/styles/base-nova/sidebar-10.json | 全部 base/style 均可用 |
| sidebar-11 | Sidebar 11 | block/sidebar | 带可折叠文件树 file tree 的侧边栏（A sidebar with a collapsible file tree.） | npx shadcn@latest add sidebar-11 ; https://ui.shadcn.com/r/styles/base-nova/sidebar-11.json | 全部 base/style 均可用 |
| sidebar-12 | Sidebar 12 | block/sidebar | 带日历的侧边栏（A sidebar with a calendar.） | npx shadcn@latest add sidebar-12 ; https://ui.shadcn.com/r/styles/base-nova/sidebar-12.json | 全部 base/style 均可用 |
| sidebar-13 | Sidebar 13 | block/sidebar | 放在对话框 dialog 里的侧边栏（设置面板）（A sidebar in a dialog.） | npx shadcn@latest add sidebar-13 ; https://ui.shadcn.com/r/styles/base-nova/sidebar-13.json | 全部 base/style 均可用 |
| sidebar-14 | Sidebar 14 | block/sidebar | 右侧侧边栏（A sidebar on the right.） | npx shadcn@latest add sidebar-14 ; https://ui.shadcn.com/r/styles/base-nova/sidebar-14.json | 全部 base/style 均可用 |
| sidebar-15 | Sidebar 15 | block/sidebar | 左右双侧边栏（A left and right sidebar.） | npx shadcn@latest add sidebar-15 ; https://ui.shadcn.com/r/styles/base-nova/sidebar-15.json | 全部 base/style 均可用 |
| sidebar-16 | Sidebar 16 | block/sidebar | 带吸顶站点 header 的侧边栏（A sidebar with a sticky site header.） | npx shadcn@latest add sidebar-16 ; https://ui.shadcn.com/r/styles/base-nova/sidebar-16.json | 全部 base/style 均可用 |
| login-01 | Login 01 | block/login | 登录表单：简单卡片（A simple login form.） | npx shadcn@latest add login-01 ; https://ui.shadcn.com/r/styles/base-nova/login-01.json | 全部 base/style 均可用 |
| login-02 | Login 02 | block/login | 登录页：两栏 + 封面图（A two column login page with a cover image.） | npx shadcn@latest add login-02 ; https://ui.shadcn.com/r/styles/base-nova/login-02.json | 全部 base/style 均可用 |
| login-03 | Login 03 | block/login | 登录页：灰色背景居中（A login page with a muted background color.） | npx shadcn@latest add login-03 ; https://ui.shadcn.com/r/styles/base-nova/login-03.json | 全部 base/style 均可用 |
| login-04 | Login 04 | block/login | 登录页：表单 + 配图卡片（A login page with form and image.） | npx shadcn@latest add login-04 ; https://ui.shadcn.com/r/styles/base-nova/login-04.json | 全部 base/style 均可用 |
| login-05 | Login 05 | block/login | 登录页：仅邮箱登录 magic link（A simple email-only login page.） | npx shadcn@latest add login-05 ; https://ui.shadcn.com/r/styles/base-nova/login-05.json | 全部 base/style 均可用 |
| signup-01 | Signup 01 | block/signup | 注册表单：简单卡片（A simple signup form.） | npx shadcn@latest add signup-01 ; https://ui.shadcn.com/r/styles/base-nova/signup-01.json | 全部 base/style 均可用 |
| signup-02 | Signup 02 | block/signup | 注册页：两栏 + 封面图（A two column signup page with a cover image.） | npx shadcn@latest add signup-02 ; https://ui.shadcn.com/r/styles/base-nova/signup-02.json | 全部 base/style 均可用 |
| signup-03 | Signup 03 | block/signup | 注册页：灰色背景（A signup page with a muted background color.） | npx shadcn@latest add signup-03 ; https://ui.shadcn.com/r/styles/base-nova/signup-03.json | 全部 base/style 均可用 |
| signup-04 | Signup 04 | block/signup | 注册页：表单 + 配图（A signup page with form and image.） | npx shadcn@latest add signup-04 ; https://ui.shadcn.com/r/styles/base-nova/signup-04.json | 全部 base/style 均可用 |
| signup-05 | Signup 05 | block/signup | 注册表单：带第三方社交登录按钮（A simple signup form with social providers.） | npx shadcn@latest add signup-05 ; https://ui.shadcn.com/r/styles/base-nova/signup-05.json | 全部 base/style 均可用 |
| preview | Preview | block/preview | shadcn/create 预设预览用的组件拼盘页面（展示整套风格） | npx shadcn@latest add preview ; https://ui.shadcn.com/r/styles/base-nova/preview.json | 仅新 style（base/radix/aria-*），非正式 block |
| preview-02 | Preview 02 | block/preview | shadcn/create 预设预览用的组件拼盘页面（展示整套风格） | npx shadcn@latest add preview-02 ; https://ui.shadcn.com/r/styles/base-nova/preview-02.json | 仅新 style（base/radix/aria-*），非正式 block |
| preview-03 | Preview 03 | block/preview | shadcn/create 预设预览用的组件拼盘页面（展示整套风格） | npx shadcn@latest add preview-03 ; https://ui.shadcn.com/r/styles/base-nova/preview-03.json | 仅新 style（base/radix/aria-*），非正式 block |
| chart-area-axes | Chart Area Axes | chart/area | 面积图：带坐标轴（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-area-axes.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-area-axes.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-area-default | Chart Area Default | chart/area | 面积图：默认（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-area-default.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-area-default.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-area-gradient | Chart Area Gradient | chart/area | 面积图：渐变填充（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-area-gradient.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-area-gradient.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-area-icons | Chart Area Icons | chart/area | 面积图：带图标（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-area-icons.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-area-icons.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-area-interactive | Chart Area Interactive | chart/area | 面积图：交互（可切换时间范围/指标）（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-area-interactive.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-area-interactive.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-area-legend | Chart Area Legend | chart/area | 面积图：带图例（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-area-legend.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-area-legend.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-area-linear | Chart Area Linear | chart/area | 面积图：直线插值（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-area-linear.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-area-linear.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-area-stacked-expand | Chart Area Stacked Expand | chart/area | 面积图：百分比堆叠（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-area-stacked-expand.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-area-stacked-expand.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-area-stacked | Chart Area Stacked | chart/area | 面积图：堆叠（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-area-stacked.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-area-stacked.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-area-step | Chart Area Step | chart/area | 面积图：阶梯（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-area-step.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-area-step.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-bar-active | Chart Bar Active | chart/bar | 柱状图：高亮选中项（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-active.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-active.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-bar-default | Chart Bar Default | chart/bar | 柱状图：默认（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-default.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-default.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-bar-horizontal | Chart Bar Horizontal | chart/bar | 柱状图：横向（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-horizontal.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-horizontal.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-bar-interactive | Chart Bar Interactive | chart/bar | 柱状图：交互（可切换时间范围/指标）（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-interactive.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-interactive.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-bar-label-custom | Chart Bar Label Custom | chart/bar | 柱状图：自定义标签（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-label-custom.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-label-custom.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-bar-label | Chart Bar Label | chart/bar | 柱状图：带数值标签（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-label.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-label.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-bar-mixed | Chart Bar Mixed | chart/bar | 柱状图：混合颜色（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-mixed.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-mixed.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-bar-multiple | Chart Bar Multiple | chart/bar | 柱状图：多系列（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-multiple.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-multiple.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-bar-negative | Chart Bar Negative | chart/bar | 柱状图：含负值（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-negative.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-negative.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-bar-stacked | Chart Bar Stacked | chart/bar | 柱状图：堆叠（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-stacked.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-bar-stacked.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-line-default | Chart Line Default | chart/line | 折线图：默认（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-line-default.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-line-default.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-line-dots-colors | Chart Line Dots Colors | chart/line | 折线图：彩色数据点（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-line-dots-colors.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-line-dots-colors.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-line-dots-custom | Chart Line Dots Custom | chart/line | 折线图：自定义数据点（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-line-dots-custom.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-line-dots-custom.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-line-dots | Chart Line Dots | chart/line | 折线图：带数据点（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-line-dots.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-line-dots.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-line-interactive | Chart Line Interactive | chart/line | 折线图：交互（可切换时间范围/指标）（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-line-interactive.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-line-interactive.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-line-label-custom | Chart Line Label Custom | chart/line | 折线图：自定义标签（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-line-label-custom.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-line-label-custom.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-line-label | Chart Line Label | chart/line | 折线图：带数值标签（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-line-label.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-line-label.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-line-linear | Chart Line Linear | chart/line | 折线图：直线插值（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-line-linear.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-line-linear.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-line-multiple | Chart Line Multiple | chart/line | 折线图：多系列（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-line-multiple.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-line-multiple.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-line-step | Chart Line Step | chart/line | 折线图：阶梯（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-line-step.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-line-step.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-pie-donut-active | Chart Pie Donut Active | chart/pie | 饼图/环形图：环形高亮扇区（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-donut-active.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-donut-active.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-pie-donut-text | Chart Pie Donut Text | chart/pie | 饼图/环形图：环形中心文字（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-donut-text.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-donut-text.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-pie-donut | Chart Pie Donut | chart/pie | 饼图/环形图：环形（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-donut.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-donut.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-pie-interactive | Chart Pie Interactive | chart/pie | 饼图/环形图：交互（可切换时间范围/指标）（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-interactive.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-interactive.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-pie-label-custom | Chart Pie Label Custom | chart/pie | 饼图/环形图：自定义标签（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-label-custom.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-label-custom.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-pie-label-list | Chart Pie Label List | chart/pie | 饼图/环形图：标签列表（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-label-list.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-label-list.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-pie-label | Chart Pie Label | chart/pie | 饼图/环形图：带数值标签（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-label.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-label.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-pie-legend | Chart Pie Legend | chart/pie | 饼图/环形图：带图例（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-legend.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-legend.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-pie-separator-none | Chart Pie Separator None | chart/pie | 饼图/环形图：无分隔线（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-separator-none.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-separator-none.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-pie-simple | Chart Pie Simple | chart/pie | 饼图/环形图：简单（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-simple.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-simple.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-pie-stacked | Chart Pie Stacked | chart/pie | 饼图/环形图：堆叠（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-stacked.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-pie-stacked.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radar-default | Chart Radar Default | chart/radar | 雷达图：默认（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-default.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-default.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radar-dots | Chart Radar Dots | chart/radar | 雷达图：带数据点（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-dots.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-dots.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radar-grid-circle-fill | Chart Radar Grid Circle Fill | chart/radar | 雷达图：圆形网格填充（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-grid-circle-fill.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-grid-circle-fill.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radar-grid-circle-no-lines | Chart Radar Grid Circle No Lines | chart/radar | 雷达图：圆形网格无径线（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-grid-circle-no-lines.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-grid-circle-no-lines.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radar-grid-circle | Chart Radar Grid Circle | chart/radar | 雷达图：圆形网格（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-grid-circle.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-grid-circle.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radar-grid-custom | Chart Radar Grid Custom | chart/radar | 雷达图：自定义网格（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-grid-custom.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-grid-custom.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radar-grid-fill | Chart Radar Grid Fill | chart/radar | 雷达图：网格填充（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-grid-fill.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-grid-fill.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radar-grid-none | Chart Radar Grid None | chart/radar | 雷达图：无网格（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-grid-none.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-grid-none.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radar-icons | Chart Radar Icons | chart/radar | 雷达图：带图标（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-icons.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-icons.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radar-label-custom | Chart Radar Label Custom | chart/radar | 雷达图：自定义标签（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-label-custom.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-label-custom.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radar-legend | Chart Radar Legend | chart/radar | 雷达图：带图例（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-legend.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-legend.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radar-lines-only | Chart Radar Lines Only | chart/radar | 雷达图：仅线条（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-lines-only.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-lines-only.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radar-multiple | Chart Radar Multiple | chart/radar | 雷达图：多系列（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-multiple.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-multiple.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radar-radius | Chart Radar Radius | chart/radar | 雷达图：带半径轴（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-radius.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radar-radius.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radial-grid | Chart Radial Grid | chart/radial | 径向/环形进度图：网格（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radial-grid.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radial-grid.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radial-label | Chart Radial Label | chart/radial | 径向/环形进度图：带数值标签（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radial-label.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radial-label.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radial-shape | Chart Radial Shape | chart/radial | 径向/环形进度图：形状（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radial-shape.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radial-shape.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radial-simple | Chart Radial Simple | chart/radial | 径向/环形进度图：简单（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radial-simple.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radial-simple.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radial-stacked | Chart Radial Stacked | chart/radial | 径向/环形进度图：堆叠（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radial-stacked.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radial-stacked.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-radial-text | Chart Radial Text | chart/radial | 径向/环形进度图：中心文字（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-radial-text.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-radial-text.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-tooltip-default | Chart Tooltip Default | chart/tooltip | 图表 tooltip 样式：默认（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-tooltip-default.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-tooltip-default.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-tooltip-indicator-line | Chart Tooltip Indicator Line | chart/tooltip | 图表 tooltip 样式：线形指示器（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-tooltip-indicator-line.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-tooltip-indicator-line.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-tooltip-indicator-none | Chart Tooltip Indicator None | chart/tooltip | 图表 tooltip 样式：无指示器（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-tooltip-indicator-none.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-tooltip-indicator-none.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-tooltip-label-none | Chart Tooltip Label None | chart/tooltip | 图表 tooltip 样式：无标签（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-tooltip-label-none.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-tooltip-label-none.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-tooltip-label-custom | Chart Tooltip Label Custom | chart/tooltip | 图表 tooltip 样式：自定义标签（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-tooltip-label-custom.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-tooltip-label-custom.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-tooltip-label-formatter | Chart Tooltip Label Formatter | chart/tooltip | 图表 tooltip 样式：标签格式化（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-tooltip-label-formatter.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-tooltip-label-formatter.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-tooltip-formatter | Chart Tooltip Formatter | chart/tooltip | 图表 tooltip 样式：数值格式化（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-tooltip-formatter.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-tooltip-formatter.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-tooltip-icons | Chart Tooltip Icons | chart/tooltip | 图表 tooltip 样式：带图标（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-tooltip-icons.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-tooltip-icons.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| chart-tooltip-advanced | Chart Tooltip Advanced | chart/tooltip | 图表 tooltip 样式：高级自定义（Recharts + Card，可复制图表 dashboard 数据可视化） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/chart-tooltip-advanced.json ; https://ui.shadcn.com/r/styles/new-york-v4/chart-tooltip-advanced.json | 仅 new-york-v4；新 style 项目须用完整 URL 安装 |
| theme-neutral | Theme Neutral | theme | 主题 CSS 变量 neutral（亮/暗两套 cssVars，配色 theming） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/theme-neutral.json ; https://ui.shadcn.com/r/themes/neutral.json | registry:theme，仅 new-york-v4 |
| theme-stone | Theme Stone | theme | 主题 CSS 变量 stone（亮/暗两套 cssVars，配色 theming） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/theme-stone.json ; https://ui.shadcn.com/r/themes/stone.json | registry:theme，仅 new-york-v4 |
| theme-zinc | Theme Zinc | theme | 主题 CSS 变量 zinc（亮/暗两套 cssVars，配色 theming） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/theme-zinc.json ; https://ui.shadcn.com/r/themes/zinc.json | registry:theme，仅 new-york-v4 |
| theme-gray | Theme Gray | theme | 主题 CSS 变量 gray（亮/暗两套 cssVars，配色 theming） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/theme-gray.json ; https://ui.shadcn.com/r/themes/gray.json | registry:theme，仅 new-york-v4 |
| theme-slate | Theme Slate | theme | 主题 CSS 变量 slate（亮/暗两套 cssVars，配色 theming） | npx shadcn@latest add https://ui.shadcn.com/r/styles/new-york-v4/theme-slate.json ; https://ui.shadcn.com/r/themes/slate.json | registry:theme，仅 new-york-v4 |
| base-color-neutral | Base color Neutral | theme/base-color | 基础色 neutral：inlineColors + cssVars（light/dark）主题 token，init/migrate base-color 使用 | npx shadcn@latest migrate base-color --to neutral ; https://ui.shadcn.com/r/colors/neutral.json | 当前 init 可选 base color |
| base-color-stone | Base color Stone | theme/base-color | 基础色 stone：inlineColors + cssVars（light/dark）主题 token，init/migrate base-color 使用 | npx shadcn@latest migrate base-color --to stone ; https://ui.shadcn.com/r/colors/stone.json | 当前 init 可选 base color |
| base-color-zinc | Base color Zinc | theme/base-color | 基础色 zinc：inlineColors + cssVars（light/dark）主题 token，init/migrate base-color 使用 | npx shadcn@latest migrate base-color --to zinc ; https://ui.shadcn.com/r/colors/zinc.json | 当前 init 可选 base color |
| base-color-mauve | Base color Mauve | theme/base-color | 基础色 mauve：inlineColors + cssVars（light/dark）主题 token，init/migrate base-color 使用 | npx shadcn@latest migrate base-color --to mauve ; https://ui.shadcn.com/r/colors/mauve.json | 当前 init 可选 base color |
| base-color-olive | Base color Olive | theme/base-color | 基础色 olive：inlineColors + cssVars（light/dark）主题 token，init/migrate base-color 使用 | npx shadcn@latest migrate base-color --to olive ; https://ui.shadcn.com/r/colors/olive.json | 当前 init 可选 base color |
| base-color-mist | Base color Mist | theme/base-color | 基础色 mist：inlineColors + cssVars（light/dark）主题 token，init/migrate base-color 使用 | npx shadcn@latest migrate base-color --to mist ; https://ui.shadcn.com/r/colors/mist.json | 当前 init 可选 base color |
| base-color-taupe | Base color Taupe | theme/base-color | 基础色 taupe：inlineColors + cssVars（light/dark）主题 token，init/migrate base-color 使用 | npx shadcn@latest migrate base-color --to taupe ; https://ui.shadcn.com/r/colors/taupe.json | 当前 init 可选 base color |
| base-color-gray | Base color Gray | theme/base-color | 基础色 gray：inlineColors + cssVars（light/dark）主题 token，init/migrate base-color 使用 | npx shadcn@latest migrate base-color --to gray ; https://ui.shadcn.com/r/colors/gray.json | legacy base color |
| base-color-slate | Base color Slate | theme/base-color | 基础色 slate：inlineColors + cssVars（light/dark）主题 token，init/migrate base-color 使用 | npx shadcn@latest migrate base-color --to slate ; https://ui.shadcn.com/r/colors/slate.json | legacy base color |
| tailwind-colors | Colors palette | theme/palette | Tailwind 全色板（hex/rgb/hsl/oklch），/colors 页面数据，配色取色 | https://ui.shadcn.com/r/colors/index.json ; https://ui.shadcn.com/colors |  |
| themes-css | themes.css | theme | 预置主题 CSS 合集（themes 页面用的变量集合） | https://ui.shadcn.com/r/themes.css |  |
| presets | Presets (shadcn/create) | theme/preset | 24 个 base×style 预设（vega/nova/maia/lyra/mira/luma/rhea/sera × base/radix/aria），字体/图标库/圆角/菜单色组合 | npx shadcn@latest init --preset base-nova ; https://ui.shadcn.com/r/config.json ; https://ui.shadcn.com/create |  |
| font-geist | Font Geist | font | 正文字体 geist（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-geist ; https://ui.shadcn.com/r/styles/base-nova/font-geist.json |  |
| font-inter | Font Inter | font | 正文字体 inter（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-inter ; https://ui.shadcn.com/r/styles/base-nova/font-inter.json |  |
| font-noto-sans | Font Noto Sans | font | 正文字体 noto-sans（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-noto-sans ; https://ui.shadcn.com/r/styles/base-nova/font-noto-sans.json |  |
| font-nunito-sans | Font Nunito Sans | font | 正文字体 nunito-sans（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-nunito-sans ; https://ui.shadcn.com/r/styles/base-nova/font-nunito-sans.json |  |
| font-figtree | Font Figtree | font | 正文字体 figtree（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-figtree ; https://ui.shadcn.com/r/styles/base-nova/font-figtree.json |  |
| font-roboto | Font Roboto | font | 正文字体 roboto（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-roboto ; https://ui.shadcn.com/r/styles/base-nova/font-roboto.json |  |
| font-raleway | Font Raleway | font | 正文字体 raleway（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-raleway ; https://ui.shadcn.com/r/styles/base-nova/font-raleway.json |  |
| font-dm-sans | Font Dm Sans | font | 正文字体 dm-sans（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-dm-sans ; https://ui.shadcn.com/r/styles/base-nova/font-dm-sans.json |  |
| font-public-sans | Font Public Sans | font | 正文字体 public-sans（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-public-sans ; https://ui.shadcn.com/r/styles/base-nova/font-public-sans.json |  |
| font-outfit | Font Outfit | font | 正文字体 outfit（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-outfit ; https://ui.shadcn.com/r/styles/base-nova/font-outfit.json |  |
| font-oxanium | Font Oxanium | font | 正文字体 oxanium（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-oxanium ; https://ui.shadcn.com/r/styles/base-nova/font-oxanium.json |  |
| font-manrope | Font Manrope | font | 正文字体 manrope（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-manrope ; https://ui.shadcn.com/r/styles/base-nova/font-manrope.json |  |
| font-space-grotesk | Font Space Grotesk | font | 正文字体 space-grotesk（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-space-grotesk ; https://ui.shadcn.com/r/styles/base-nova/font-space-grotesk.json |  |
| font-montserrat | Font Montserrat | font | 正文字体 montserrat（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-montserrat ; https://ui.shadcn.com/r/styles/base-nova/font-montserrat.json |  |
| font-ibm-plex-sans | Font Ibm Plex Sans | font | 正文字体 ibm-plex-sans（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-ibm-plex-sans ; https://ui.shadcn.com/r/styles/base-nova/font-ibm-plex-sans.json |  |
| font-source-sans-3 | Font Source Sans 3 | font | 正文字体 source-sans-3（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-source-sans-3 ; https://ui.shadcn.com/r/styles/base-nova/font-source-sans-3.json |  |
| font-instrument-sans | Font Instrument Sans | font | 正文字体 instrument-sans（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-instrument-sans ; https://ui.shadcn.com/r/styles/base-nova/font-instrument-sans.json |  |
| font-jetbrains-mono | Font Jetbrains Mono | font | 正文字体 jetbrains-mono（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-jetbrains-mono ; https://ui.shadcn.com/r/styles/base-nova/font-jetbrains-mono.json |  |
| font-geist-mono | Font Geist Mono | font | 正文字体 geist-mono（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-geist-mono ; https://ui.shadcn.com/r/styles/base-nova/font-geist-mono.json |  |
| font-noto-serif | Font Noto Serif | font | 正文字体 noto-serif（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-noto-serif ; https://ui.shadcn.com/r/styles/base-nova/font-noto-serif.json |  |
| font-roboto-slab | Font Roboto Slab | font | 正文字体 roboto-slab（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-roboto-slab ; https://ui.shadcn.com/r/styles/base-nova/font-roboto-slab.json |  |
| font-merriweather | Font Merriweather | font | 正文字体 merriweather（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-merriweather ; https://ui.shadcn.com/r/styles/base-nova/font-merriweather.json |  |
| font-lora | Font Lora | font | 正文字体 lora（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-lora ; https://ui.shadcn.com/r/styles/base-nova/font-lora.json |  |
| font-playfair-display | Font Playfair Display | font | 正文字体 playfair-display（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-playfair-display ; https://ui.shadcn.com/r/styles/base-nova/font-playfair-display.json |  |
| font-eb-garamond | Font Eb Garamond | font | 正文字体 eb-garamond（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-eb-garamond ; https://ui.shadcn.com/r/styles/base-nova/font-eb-garamond.json |  |
| font-instrument-serif | Font Instrument Serif | font | 正文字体 instrument-serif（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-instrument-serif ; https://ui.shadcn.com/r/styles/base-nova/font-instrument-serif.json |  |
| font-heading-geist | Font Heading Geist | font | 标题字体 geist（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-geist ; https://ui.shadcn.com/r/styles/base-nova/font-heading-geist.json |  |
| font-heading-inter | Font Heading Inter | font | 标题字体 inter（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-inter ; https://ui.shadcn.com/r/styles/base-nova/font-heading-inter.json |  |
| font-heading-noto-sans | Font Heading Noto Sans | font | 标题字体 noto-sans（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-noto-sans ; https://ui.shadcn.com/r/styles/base-nova/font-heading-noto-sans.json |  |
| font-heading-nunito-sans | Font Heading Nunito Sans | font | 标题字体 nunito-sans（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-nunito-sans ; https://ui.shadcn.com/r/styles/base-nova/font-heading-nunito-sans.json |  |
| font-heading-figtree | Font Heading Figtree | font | 标题字体 figtree（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-figtree ; https://ui.shadcn.com/r/styles/base-nova/font-heading-figtree.json |  |
| font-heading-roboto | Font Heading Roboto | font | 标题字体 roboto（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-roboto ; https://ui.shadcn.com/r/styles/base-nova/font-heading-roboto.json |  |
| font-heading-raleway | Font Heading Raleway | font | 标题字体 raleway（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-raleway ; https://ui.shadcn.com/r/styles/base-nova/font-heading-raleway.json |  |
| font-heading-dm-sans | Font Heading Dm Sans | font | 标题字体 dm-sans（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-dm-sans ; https://ui.shadcn.com/r/styles/base-nova/font-heading-dm-sans.json |  |
| font-heading-public-sans | Font Heading Public Sans | font | 标题字体 public-sans（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-public-sans ; https://ui.shadcn.com/r/styles/base-nova/font-heading-public-sans.json |  |
| font-heading-outfit | Font Heading Outfit | font | 标题字体 outfit（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-outfit ; https://ui.shadcn.com/r/styles/base-nova/font-heading-outfit.json |  |
| font-heading-oxanium | Font Heading Oxanium | font | 标题字体 oxanium（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-oxanium ; https://ui.shadcn.com/r/styles/base-nova/font-heading-oxanium.json |  |
| font-heading-manrope | Font Heading Manrope | font | 标题字体 manrope（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-manrope ; https://ui.shadcn.com/r/styles/base-nova/font-heading-manrope.json |  |
| font-heading-space-grotesk | Font Heading Space Grotesk | font | 标题字体 space-grotesk（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-space-grotesk ; https://ui.shadcn.com/r/styles/base-nova/font-heading-space-grotesk.json |  |
| font-heading-montserrat | Font Heading Montserrat | font | 标题字体 montserrat（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-montserrat ; https://ui.shadcn.com/r/styles/base-nova/font-heading-montserrat.json |  |
| font-heading-ibm-plex-sans | Font Heading Ibm Plex Sans | font | 标题字体 ibm-plex-sans（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-ibm-plex-sans ; https://ui.shadcn.com/r/styles/base-nova/font-heading-ibm-plex-sans.json |  |
| font-heading-source-sans-3 | Font Heading Source Sans 3 | font | 标题字体 source-sans-3（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-source-sans-3 ; https://ui.shadcn.com/r/styles/base-nova/font-heading-source-sans-3.json |  |
| font-heading-instrument-sans | Font Heading Instrument Sans | font | 标题字体 instrument-sans（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-instrument-sans ; https://ui.shadcn.com/r/styles/base-nova/font-heading-instrument-sans.json |  |
| font-heading-jetbrains-mono | Font Heading Jetbrains Mono | font | 标题字体 jetbrains-mono（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-jetbrains-mono ; https://ui.shadcn.com/r/styles/base-nova/font-heading-jetbrains-mono.json |  |
| font-heading-geist-mono | Font Heading Geist Mono | font | 标题字体 geist-mono（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-geist-mono ; https://ui.shadcn.com/r/styles/base-nova/font-heading-geist-mono.json |  |
| font-heading-noto-serif | Font Heading Noto Serif | font | 标题字体 noto-serif（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-noto-serif ; https://ui.shadcn.com/r/styles/base-nova/font-heading-noto-serif.json |  |
| font-heading-roboto-slab | Font Heading Roboto Slab | font | 标题字体 roboto-slab（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-roboto-slab ; https://ui.shadcn.com/r/styles/base-nova/font-heading-roboto-slab.json |  |
| font-heading-merriweather | Font Heading Merriweather | font | 标题字体 merriweather（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-merriweather ; https://ui.shadcn.com/r/styles/base-nova/font-heading-merriweather.json |  |
| font-heading-lora | Font Heading Lora | font | 标题字体 lora（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-lora ; https://ui.shadcn.com/r/styles/base-nova/font-heading-lora.json |  |
| font-heading-playfair-display | Font Heading Playfair Display | font | 标题字体 playfair-display（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-playfair-display ; https://ui.shadcn.com/r/styles/base-nova/font-heading-playfair-display.json |  |
| font-heading-eb-garamond | Font Heading Eb Garamond | font | 标题字体 eb-garamond（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-eb-garamond ; https://ui.shadcn.com/r/styles/base-nova/font-heading-eb-garamond.json |  |
| font-heading-instrument-serif | Font Heading Instrument Serif | font | 标题字体 instrument-serif（registry:font，配置 next/font 或 @fontsource 与 CSS 变量） | npx shadcn@latest add font-heading-instrument-serif ; https://ui.shadcn.com/r/styles/base-nova/font-heading-instrument-serif.json |  |
| utils | utils (cn) | lib | cn 工具函数（现为 re-export cn 包，className 合并 tailwind-merge） | npx shadcn@latest add utils ; https://ui.shadcn.com/r/styles/base-nova/utils.json |  |
| use-mobile | useIsMobile | hook | 移动端断点检测 hook useIsMobile（sidebar 依赖） | npx shadcn@latest add use-mobile ; https://ui.shadcn.com/r/styles/base-nova/use-mobile.json |  |
| typeset | Typeset | util/css | Markdown/HTML 排版 CSS（prose 替代），博客/文档/流式聊天，三参数 size/leading/flow | curl https://ui.shadcn.com/typeset.css ; 构建器 https://ui.shadcn.com/typeset | 非 registry 条目 |
| shimmer | shimmer | util/css | 文字闪光 shimmer 动效工具类（loading 文本效果），随 shadcn 包的 tailwind.css 提供 | npm install shadcn ; @import "shadcn/tailwind.css" ; https://ui.shadcn.com/docs/utils/shimmer.md | 非 registry 条目 |
| scroll-fade | scroll-fade | util/css | 滚动容器边缘渐隐 scroll fade 工具类 | npm install shadcn ; @import "shadcn/tailwind.css" ; https://ui.shadcn.com/docs/utils/scroll-fade.md | 非 registry 条目 |
| react-questionnaire | @shadcn/react/questionnaire | headless | 无样式 headless 问卷逻辑 Questionnaire（自带标记） | npm install @shadcn/react ; https://ui.shadcn.com/docs/react/questionnaire.md | npm 包 |
| react-message-scroller | @shadcn/react/message-scroller | headless | 无样式 headless 聊天滚动行为 MessageScroller | npm install @shadcn/react ; https://ui.shadcn.com/docs/react/message-scroller.md | npm 包 |
| helpers-ai-sdk | @shadcn/helpers/ai-sdk | helper | AI SDK useChat 的假会话 transport：无模型/无 API key 演示流式聊天、tool call、reasoning | npm install @shadcn/helpers ; https://ui.shadcn.com/docs/helpers/ai-sdk.md | npm 包 |
| helpers-tanstack-ai | @shadcn/helpers/tanstack-ai | helper | TanStack AI useChat 的假会话 connection（AG-UI 事件流） | npm install @shadcn/helpers ; https://ui.shadcn.com/docs/helpers/tanstack-ai.md | npm 包 |
| data-table | Data Table（指南） | guide | 数据表格指南：TanStack Table + Table，排序/筛选/分页/列显隐/行选择 | https://ui.shadcn.com/docs/components/base/data-table.md ; 示例 https://ui.shadcn.com/r/styles/new-york-v4/data-table-demo.json | 无独立 ui 条目，按文档组合 table |
| date-picker | Date Picker（指南） | guide | 日期选择器组合：Popover + Calendar，单日/范围/预设 | https://ui.shadcn.com/docs/components/base/date-picker.md ; 示例 https://ui.shadcn.com/r/styles/new-york-v4/date-picker-demo.json | 无独立 ui 条目 |
| typography | Typography（指南） | guide | 排版样式示例 h1-h4/p/blockquote/list/inline code | https://ui.shadcn.com/docs/components/base/typography.md ; 示例 https://ui.shadcn.com/r/styles/new-york-v4/typography-demo.json | 无独立 ui 条目，仅示例 |
| icons-map | Icons map | data | 跨图标库映射表（lucide/tabler/hugeicons/phosphor 等），migrate icons 用 | https://ui.shadcn.com/r/icons/index.json |  |
| templates | Project templates | template | init 用的项目模板 tar.gz（next/vite/start/react-router/astro，单仓/monorepo） | npx shadcn@latest init -t next ; GitHub apps/v4/public/r/templates/ |  |

### 示例（registry:example，共 319 条，逐条见 shadcn.tsv）

| 分组 | style | 条目 | 获取 |
|---|---|---|---|
| accordion | new-york-v4 | accordion-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| alert | new-york-v4 | alert-demo, alert-destructive | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| alert-dialog | new-york-v4 | alert-dialog-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| aspect-ratio | new-york-v4 | aspect-ratio-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| avatar | new-york-v4 | avatar-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| badge | new-york-v4 | badge-demo, badge-destructive, badge-outline, badge-secondary | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| breadcrumb | new-york-v4 | breadcrumb-demo, breadcrumb-separator, breadcrumb-dropdown, breadcrumb-ellipsis, breadcrumb-link, breadcrumb-responsive | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| button | new-york-v4 | button-demo, button-default, button-secondary, button-destructive, button-outline, button-ghost, button-link, button-with-icon, button-loading, button-icon, button-as-child, button-rounded, button-size | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| button-group | new-york-v4 | button-group-demo, button-group-nested, button-group-size, button-group-separator, button-group-split, button-group-input, button-group-dropdown, button-group-select, button-group-popover, button-group-input-group, button-group-orientation | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| calendar | new-york-v4 | calendar-demo, calendar-hijri | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| card | new-york-v4 | card-demo, card-with-form | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| carousel | new-york-v4 | carousel-demo, carousel-size, carousel-spacing, carousel-orientation, carousel-api, carousel-plugin | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| checkbox | new-york-v4 | checkbox-demo, checkbox-disabled, checkbox-with-text | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| collapsible | new-york-v4 | collapsible-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| combobox | new-york-v4 | combobox-demo, combobox-dropdown-menu, combobox-popover, combobox-responsive | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| command | new-york-v4 | command-demo, command-dialog | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| context-menu | new-york-v4 | context-menu-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| data-table | new-york-v4 | data-table-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| date-picker | new-york-v4 | date-picker-demo, date-picker-with-presets, date-picker-with-range | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| dialog | new-york-v4 | dialog-demo, dialog-close-button | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| drawer | new-york-v4 | drawer-demo, drawer-dialog | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| empty | new-york-v4 | empty-demo, empty-icon, empty-avatar, empty-avatar-group, empty-input-group, empty-outline, empty-background | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| field | new-york-v4 | field-demo, field-input, field-textarea, field-fieldset, field-radio, field-checkbox, field-switch, field-slider, field-select, field-choice-card, field-group, field-responsive | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| form | new-york-v4 | form-next-demo, form-next-complex, form-rhf-demo, form-rhf-input, form-rhf-select, form-rhf-checkbox, form-rhf-switch, form-rhf-textarea, form-rhf-radiogroup, form-rhf-array, form-rhf-complex, form-rhf-password, form-tanstack-demo, form-tanstack-input, form-tanstack-textarea, form-tanstack-select, form-tanstack-checkbox, form-tanstack-switch, form-tanstack-radiogroup, form-tanstack-array, form-tanstack-complex, form-formisch-demo, form-formisch-input, form-formisch-textarea, form-formisch-select, form-formisch-checkbox, form-formisch-radiogroup, form-formisch-switch, form-formisch-array, form-formisch-complex | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| dropdown-menu | new-york-v4 | dropdown-menu-demo, dropdown-menu-checkboxes, dropdown-menu-radio-group, dropdown-menu-dialog | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| hover-card | new-york-v4 | hover-card-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| input | new-york-v4 | input-demo, input-disabled, input-file, input-with-button, input-with-label, input-with-text | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| input-group | new-york-v4 | input-group-demo, input-group-label, input-group-text, input-group-tooltip, input-group-button, input-group-button-group, input-group-dropdown, input-group-spinner, input-group-textarea, input-group-icon, input-group-custom | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| input-otp | new-york-v4 | input-otp-demo, input-otp-pattern, input-otp-separator, input-otp-controlled | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| item | new-york-v4 | item-demo, item-size, item-variant, item-icon, item-image, item-avatar, item-group, item-header, item-dropdown, item-link | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| kbd | new-york-v4 | kbd-demo, kbd-tooltip, kbd-input-group, kbd-button, kbd-group | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| label | new-york-v4 | label-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| menubar | new-york-v4 | menubar-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| navigation-menu | new-york-v4 | navigation-menu-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| native-select | new-york-v4 | native-select-demo, native-select-groups, native-select-disabled, native-select-invalid | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| pagination | new-york-v4 | pagination-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| popover | new-york-v4 | popover-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| progress | new-york-v4 | progress-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| radio-group | new-york-v4 | radio-group-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| resizable | new-york-v4 | resizable-demo, resizable-demo-with-handle, resizable-vertical, resizable-handle | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| scroll-area | new-york-v4 | scroll-area-demo, scroll-area-horizontal-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| select | new-york-v4 | select-demo, select-scrollable | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| separator | new-york-v4 | separator-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| sheet | new-york-v4 | sheet-demo, sheet-side | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| skeleton | new-york-v4 | skeleton-demo, skeleton-card | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| slider | new-york-v4 | slider-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| sonner | new-york-v4 | sonner-demo, sonner-types | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| spinner | new-york-v4 | spinner-demo, spinner-basic, spinner-button, spinner-badge, spinner-input-group, spinner-empty, spinner-color, spinner-custom, spinner-size, spinner-item | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| switch | new-york-v4 | switch-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| table | new-york-v4 | table-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| tabs | new-york-v4 | tabs-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| textarea | new-york-v4 | textarea-demo, textarea-disabled, textarea-with-button, textarea-with-label, textarea-with-text | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| toggle-group | new-york-v4 | toggle-group-demo, toggle-group-disabled, toggle-group-lg, toggle-group-outline, toggle-group-sm, toggle-group-single, toggle-group-spacing | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| toggle | new-york-v4 | toggle-demo, toggle-disabled, toggle-lg, toggle-outline, toggle-sm, toggle-with-text | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| tooltip | new-york-v4 | tooltip-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| typography | new-york-v4 | typography-blockquote, typography-demo, typography-h1, typography-h2, typography-h3, typography-h4, typography-inline-code, typography-large, typography-lead, typography-list, typography-muted, typography-p, typography-small, typography-table | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| mode | new-york-v4 | mode-toggle | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| chart | new-york-v4 | chart-bar-demo, chart-bar-demo-grid, chart-bar-demo-axis, chart-bar-demo-tooltip, chart-bar-demo-legend, chart-tooltip-demo | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| sidebar | new-york-v4 | sidebar-demo, sidebar-header, sidebar-footer, sidebar-group, sidebar-group-collapsible, sidebar-group-action, sidebar-menu, sidebar-menu-action, sidebar-menu-sub, sidebar-menu-collapsible, sidebar-menu-badge, sidebar-rsc, sidebar-controlled | https://ui.shadcn.com/r/styles/new-york-v4/{name}.json |
| accordion | base-nova（同名适用 radix-*/aria-*） | accordion-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| alert | base-nova（同名适用 radix-*/aria-*） | alert-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| alert-dialog | base-nova（同名适用 radix-*/aria-*） | alert-dialog-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| aspect-ratio | base-nova（同名适用 radix-*/aria-*） | aspect-ratio-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| avatar | base-nova（同名适用 radix-*/aria-*） | avatar-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| badge | base-nova（同名适用 radix-*/aria-*） | badge-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| breadcrumb | base-nova（同名适用 radix-*/aria-*） | breadcrumb-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| button | base-nova（同名适用 radix-*/aria-*） | button-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| button-group | base-nova（同名适用 radix-*/aria-*） | button-group-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| calendar | base-nova（同名适用 radix-*/aria-*） | calendar-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| card | base-nova（同名适用 radix-*/aria-*） | card-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| carousel | base-nova（同名适用 radix-*/aria-*） | carousel-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| chart | base-nova（同名适用 radix-*/aria-*） | chart-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| checkbox | base-nova（同名适用 radix-*/aria-*） | checkbox-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| collapsible | base-nova（同名适用 radix-*/aria-*） | collapsible-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| combobox | base-nova（同名适用 radix-*/aria-*） | combobox-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| command | base-nova（同名适用 radix-*/aria-*） | command-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| context-menu | base-nova（同名适用 radix-*/aria-*） | context-menu-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| dialog | base-nova（同名适用 radix-*/aria-*） | dialog-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| drawer | base-nova（同名适用 radix-*/aria-*） | drawer-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| dropdown-menu | base-nova（同名适用 radix-*/aria-*） | dropdown-menu-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| empty | base-nova（同名适用 radix-*/aria-*） | empty-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| field | base-nova（同名适用 radix-*/aria-*） | field-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| hover-card | base-nova（同名适用 radix-*/aria-*） | hover-card-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| input | base-nova（同名适用 radix-*/aria-*） | input-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| input-group | base-nova（同名适用 radix-*/aria-*） | input-group-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| input-otp | base-nova（同名适用 radix-*/aria-*） | input-otp-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| item | base-nova（同名适用 radix-*/aria-*） | item-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| kbd | base-nova（同名适用 radix-*/aria-*） | kbd-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| label | base-nova（同名适用 radix-*/aria-*） | label-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| menubar | base-nova（同名适用 radix-*/aria-*） | menubar-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| native-select | base-nova（同名适用 radix-*/aria-*） | native-select-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| navigation-menu | base-nova（同名适用 radix-*/aria-*） | navigation-menu-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| pagination | base-nova（同名适用 radix-*/aria-*） | pagination-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| popover | base-nova（同名适用 radix-*/aria-*） | popover-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| progress | base-nova（同名适用 radix-*/aria-*） | progress-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| radio-group | base-nova（同名适用 radix-*/aria-*） | radio-group-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| resizable | base-nova（同名适用 radix-*/aria-*） | resizable-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| scroll-area | base-nova（同名适用 radix-*/aria-*） | scroll-area-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| select | base-nova（同名适用 radix-*/aria-*） | select-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| separator | base-nova（同名适用 radix-*/aria-*） | separator-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| sheet | base-nova（同名适用 radix-*/aria-*） | sheet-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| sidebar | base-nova（同名适用 radix-*/aria-*） | sidebar-example, sidebar-icon-example, sidebar-inset-example, sidebar-floating-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| skeleton | base-nova（同名适用 radix-*/aria-*） | skeleton-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| slider | base-nova（同名适用 radix-*/aria-*） | slider-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| sonner | base-nova（同名适用 radix-*/aria-*） | sonner-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| spinner | base-nova（同名适用 radix-*/aria-*） | spinner-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| switch | base-nova（同名适用 radix-*/aria-*） | switch-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| table | base-nova（同名适用 radix-*/aria-*） | table-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| tabs | base-nova（同名适用 radix-*/aria-*） | tabs-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| textarea | base-nova（同名适用 radix-*/aria-*） | textarea-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| toast | base-nova（同名适用 radix-*/aria-*） | toast-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| toggle | base-nova（同名适用 radix-*/aria-*） | toggle-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| toggle-group | base-nova（同名适用 radix-*/aria-*） | toggle-group-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| tooltip | base-nova（同名适用 radix-*/aria-*） | tooltip-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| other | base-nova（同名适用 radix-*/aria-*） | demo, component-example, example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| attachment | base-nova（同名适用 radix-*/aria-*） | attachment-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| bubble | base-nova（同名适用 radix-*/aria-*） | bubble-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| message-scroller | base-nova（同名适用 radix-*/aria-*） | message-scroller-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| questionnaire | base-nova（同名适用 radix-*/aria-*） | questionnaire-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| marker | base-nova（同名适用 radix-*/aria-*） | marker-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |
| message | base-nova（同名适用 radix-*/aria-*） | message-example | https://ui.shadcn.com/r/styles/base-nova/{name}.json |

## 未解决
- **图表与主题没有新 style 版本**：`chart-*`（70 个）和 `theme-*`（5 个）只在 `new-york-v4` 中发布，`/r/styles/{base}-{style}/chart-*.json` 均 404；新项目只能用完整 v4 URL 安装（dry-run 已验证可行，但视觉细节按 v4 写，可能与 nova/luma 等新 style 不完全一致）。
- **新 base color 无 theme JSON**：mauve/olive/mist/taupe 只有 `/r/colors/{c}.json`，`/r/themes/{c}.json` 404。
- **组件 description 为空**：registry JSON 里 ui/chart 条目没有 description，清单的中文用途是根据 llms.txt 和文档手写或按名称生成的；示例条目的描述是按名称自动生成的通用句。
- **/create 预设码**：预设码（如 `a2r6bw`）在 /create 页面交互生成，没有可枚举的公开列表；只有 `/r/config.json` 里 24 个命名预设可机读。
- **llms-full.txt 不存在**（404）；全文需逐页加 `.md` 抓取。
- 抓取过程中有少数 `.md` 请求偶发返回 000（网络波动），重试后正常，不影响结论。
