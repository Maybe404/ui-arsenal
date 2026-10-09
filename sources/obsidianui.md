---
id: obsidianui
name: ObsidianUI
url: https://www.obsidianui.dev/
kind: component-library
stack: React + Next.js（App Router）+ Tailwind CSS v4 + Motion / GSAP / Three.js，shadcn 兼容
license: MIT（GitHub Atharvsinh-codez/ObsidianUI；模板 Project-1 也是 MIT）
pro: none
fetch: shadcn-registry
coverage: 全量：官方 registry 的全部条目；refresh 自动比对
catalog_checked: 2026-10-07
source_status: active
visual_style: showcase motion blocks over shadcn-style primitives
foundation: shadcn-compatible
styling: mixed
motion_lib: mixed(motion,gsap,three)
dark_mode: class
mixing_notes: 基础 primitive 是 Radix 版 shadcn 同构件，已有 shadcn（尤其 Base UI）时跳过不装；dashboard-shell 等 block 自带 --obsidian-* 硬编码色板，同页要改成引用 shadcn 变量
---
## 是什么 / 什么时候用
开源 React 动效/交互组件库，shadcn registry 形式分发，源码完全归你。强项是"有记忆点"的展示型组件：拖拽画廊、跑马灯、hover 跟随图、滚动文字流、WebGL 棱镜、状态页条带、登录设备列表、Dashboard 外壳。
需要给落地页/作品集加一个动效亮点，或要一个现成 dashboard 布局 / 状态页 / 会话管理设置块时用。registry 里另有约 50 个 shadcn 同构基础组件（button、dialog 等），项目已有 shadcn/ui 时不需要从这里装它们。
站点对 agent 极友好：llms.txt、Markdown 文档、OpenAPI、无需登录。

## 按需获取方法
机器可读入口（全部 curl 直接可得，无需渲染/JS）：
- 目录：`curl -s https://www.obsidianui.dev/r/registry.json`（74 个 item，含 files/content/dependencies；`/r/index.json` 同内容）
- 单项清单：`curl -s https://www.obsidianui.dev/r/{name}.json` → `files[].content` 为完整源码，`files[].target` 为目标路径（`@ui/` `@components/` `@lib/` `@hooks/` 前缀，按 components.json aliases 解析，不要建字面量 `@ui` 目录）
- 文档（含用法示例与 props）：`curl -s https://www.obsidianui.dev/markdown/docs/{slug}.md`（或对 `/docs/{slug}` 带 `Accept: text/markdown`；或 `/api/docs/{slug}/markdown`）。只有 11 个主组件有文档
- 索引：`https://www.obsidianui.dev/llms.txt`；全量文档+源码：`/llms-full.txt`（约 270KB，尽量别整拉）；agent 指南：`/agent-instructions.md`；OpenAPI：`/openapi.json`

安装：
```bash
# shadcn 项目（推荐）
npx shadcn@latest add "https://www.obsidianui.dev/r/{name}.json"
# 或在 components.json 注册命名空间后：
#   "registries": { "@obsidian": "https://www.obsidianui.dev/r/{name}.json" }
npx shadcn@latest add @obsidian/{name}
# 只看不装
npx shadcn@latest view "https://www.obsidianui.dev/r/{name}.json"
```
手动安装：拉 `/r/{name}.json`，把每个 `files[].content` 写到解析后的 target（默认 `@components/block/x.tsx` → `src/components/block/x.tsx`，`@ui/x.tsx` → `src/components/ui/x.tsx`），再 `npm i <dependencies...>`。CSS 文件（如 `active-sessions.css`、`hover-img.css`）要一起复制并保持 import。

实测（2026-10-07）：
- `curl -s https://www.obsidianui.dev/r/flip-text.json` → 2 个文件：`@components/block/flip-text.tsx`（4153 字符，"use client"）+ `@lib/utils.ts`；dependencies `clsx, tailwind-merge`
- `npx shadcn@latest view "https://www.obsidianui.dev/r/flip-text.json"` 正常返回 registry-item JSON
- `curl -s https://www.obsidianui.dev/markdown/docs/flip-text.md` 返回用法示例 `<FlipText className="text-4xl font-bold">Hover Me</FlipText>`

## 使用注意
- 目标 Tailwind v4（文档用 `@tailwindcss/postcss`），需 `cn` 工具（clsx + tailwind-merge，registry 会一并给 `@lib/utils.ts`，已有则别覆盖）。
- 动效依赖混用：`motion`（`motion/react`，不是 framer-motion）、`gsap`（含 `gsap/Draggable`）、`three` + `postprocessing`（v-prism）、`@paper-design/shaders-react`（liquid-metal）、`lenis`（smooth-scroll）、`@number-flow/react`（status-bars）。按 item 的 dependencies 装，不要全装。
- 部分组件绑定 Next.js：`file-input`、`skeumorphic-music-card` 用 `next/image`；`click-spark`、`sonner`、`v-prism` 用 `next-themes`。非 Next 项目需替换。
- `meta.remoteAssets`：art-gallery、v-prism、playground-navbar 的演示图片走 `cdn-new.obsidianui.dev`，上线前换成自己的资源。
- `visitor-count` 需要自己实现 `POST /api/visitors`（`meta.requiredEndpoints`）。
- dashboard-shell 用法示例里引用了 `@duo-icons/react`（不在 dependencies 里），抄示例时需另装或换图标。
- 基础 primitive（button/dialog/...）与 shadcn/ui 同名同构，已有 shadcn 项目安装 block 时注意 CLI 会提示覆盖 `@ui/button.tsx` 等文件，选择跳过。
- 站点 MCP 仅指"shadcn MCP（`npx shadcn@latest mcp init`）+ 本地 stdio MCP（仓库内 `npm run mcp`）"，没有托管的 HTTP MCP。

## 组件清单
74 个 registry item（11 个有文档的主组件 + 13 个无文档 block/ui 特效 + 50 个 shadcn 同构基础组件）+ 1 个模板。

| id | 名称 | 分类 | 一句话用途 | 获取（具体命令或URL） | 备注 |
|---|---|---|---|---|---|
| active-sessions | Active Sessions | block | 已登录设备会话列表，单个/批量登出时行折叠动画，适合账户安全设置页 settings sessions devices | `npx shadcn@latest add "https://www.obsidianui.dev/r/active-sessions.json"` | 有文档 /markdown/docs/active-sessions.md |
| art-gallery | Art Gallery | block | 可拖拽平移的无限平铺照片墙，WebGL 桶形畸变透镜效果 three.js gallery drag | `npx shadcn@latest add "https://www.obsidianui.dev/r/art-gallery.json"` | 有文档 /markdown/docs/art-gallery.md；meta.remoteAssets 指向 cdn-new.obsidianui.dev 演示图 |
| dashboard-shell | Dashboard Shell | block | 后台/仪表盘整体布局：可拖拽缩放侧栏、分组导航、头部状态与操作、滑动药丸 tabs、筛选工具栏，窄屏变抽屉 admin layout | `npx shadcn@latest add "https://www.obsidianui.dev/r/dashboard-shell.json"` | 有文档 /markdown/docs/dashboard-shell.md |
| discover-button | Discover Button | block | 圆角 CTA 按钮，hover 时箭头圆圈展开覆盖文字，可作链接或按钮 call-to-action | `npx shadcn@latest add "https://www.obsidianui.dev/r/discover-button.json"` | 有文档 /markdown/docs/discover-button.md |
| draggable-marquee | Draggable Marquee | block | 可拖拽带惯性的无缝循环图片跑马灯，支持键盘左右键 GSAP marquee carousel | `npx shadcn@latest add "https://www.obsidianui.dev/r/draggable-marquee.json"` | 有文档 /markdown/docs/draggable-marquee.md |
| flip-text | Flip Text | block | 逐字符翻转旋转的文字动效，hover 或循环触发 text animation typography | `npx shadcn@latest add "https://www.obsidianui.dev/r/flip-text.json"` | 有文档 /markdown/docs/flip-text.md |
| hover-img | Hover Image | block | 悬停项目标题时出现跟随鼠标的缩略图预览，适合作品集/项目列表 portfolio GSAP | `npx shadcn@latest add "https://www.obsidianui.dev/r/hover-img.json"` | 有文档 /markdown/docs/hover-img.md |
| split-showcase | Split Showcase | block | 虚线分隔的双卡片展示，hover 向外弹簧位移、圆角扩展，适合合作伙伴/对比展示 partners | `npx shadcn@latest add "https://www.obsidianui.dev/r/split-showcase.json"` | 有文档 /markdown/docs/split-showcase.md |
| status-bars | Status Bars | block | 服务状态页按天的可用性条带（正常/降级/宕机），hover 查看当日 uptime 与事故，数字滚动 status page uptime | `npx shadcn@latest add "https://www.obsidianui.dev/r/status-bars.json"` | 有文档 /markdown/docs/status-bars.md |
| text-stream | Text reel | block | 随页面滚动改变速度和方向的竖向文字流/滚动字幕 scroll velocity text reel GSAP | `npx shadcn@latest add "https://www.obsidianui.dev/r/text-stream.json"` | 有文档 /markdown/docs/text-stream.md |
| v-prism | v-prism | block | 可拖拽瞄准光束的玻璃棱镜色散效果，Three.js 后处理，复刻 Vercel v-prism hero 背景 3D | `npx shadcn@latest add "https://www.obsidianui.dev/r/v-prism.json"` | 有文档 /markdown/docs/v-prism.md；remoteAssets（lensflare 贴图） |
| click-spark | click-spark | block | 点击位置迸发火花粒子的全局点击特效 click effect | `npx shadcn@latest add "https://www.obsidianui.dev/r/click-spark.json"` | 依赖 next-themes |
| file-input | file-input | block | 带动画的文件上传输入框，含类型校验与文件预览（用 next/image，限 Next.js）upload dropzone | `npx shadcn@latest add "https://www.obsidianui.dev/r/file-input.json"` |  |
| footer | footer | block | 黑底大尺寸页脚，带灯光扫射背景效果 footer lighting | `npx shadcn@latest add "https://www.obsidianui.dev/r/footer.json"` |  |
| interactive-hover-button | interactive-hover-button | block | hover 时内容滑动替换的交互按钮 button hover | `npx shadcn@latest add "https://www.obsidianui.dev/r/interactive-hover-button.json"` |  |
| liquid-metal | liquid-metal | block | 液态金属着色器效果（@paper-design/shaders-react）shader background | `npx shadcn@latest add "https://www.obsidianui.dev/r/liquid-metal.json"` |  |
| playground-button | playground-button | block | playground 示例：Primary/Secondary/Outline/Ghost 按钮变体演示 button variants | `npx shadcn@latest add "https://www.obsidianui.dev/r/playground-button.json"` |  |
| playground-navbar | playground-navbar | block | 实验性响应式动画导航栏（playground 页）navbar header | `npx shadcn@latest add "https://www.obsidianui.dev/r/playground-navbar.json"` | remoteAssets（logo） |
| sidebar-stackbits | sidebar-stackbits | block | 可折叠的应用侧边栏+内容面板，motion 动画切换 sidebar navigation | `npx shadcn@latest add "https://www.obsidianui.dev/r/sidebar-stackbits.json"` |  |
| skeumorphic-music-card | skeumorphic-music-card | block | 拟物风音乐播放器卡片，按压式控制按钮（用 next/image）music player card skeuomorphic | `npx shadcn@latest add "https://www.obsidianui.dev/r/skeumorphic-music-card.json"` |  |
| smooth-scroll | smooth-scroll | block | 基于 Lenis 的全页平滑滚动包装器 smooth scroll | `npx shadcn@latest add "https://www.obsidianui.dev/r/smooth-scroll.json"` |  |
| visitor-count | visitor-count | block | 访客计数徽标，需自行实现 /api/visitors 端点 visitor counter | `npx shadcn@latest add "https://www.obsidianui.dev/r/visitor-count.json"` | meta.requiredEndpoints: /api/visitors |
| loaders-gooey-blobs | loaders-gooey-blobs | ui | 粘滞融合的 blob 加载动画 loader spinner gooey | `npx shadcn@latest add "https://www.obsidianui.dev/r/loaders-gooey-blobs.json"` |  |
| raised-button | raised-button | ui | 立体凸起风格按钮，可按颜色自动生成阴影 3D button | `npx shadcn@latest add "https://www.obsidianui.dev/r/raised-button.json"` |  |
| alert | alert | ui-primitive | shadcn 风格基础组件：提示框 alert（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/alert.json"` |  |
| avatar | avatar | ui-primitive | shadcn 风格基础组件：头像 avatar（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/avatar.json"` |  |
| badge | badge | ui-primitive | shadcn 风格基础组件：徽章标签 badge（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/badge.json"` |  |
| breadcrumb | breadcrumb | ui-primitive | shadcn 风格基础组件：面包屑 breadcrumb（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/breadcrumb.json"` |  |
| button | button | ui-primitive | shadcn 风格基础组件：按钮 button（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/button.json"` |  |
| button-group | button-group | ui-primitive | shadcn 风格基础组件：按钮组 button group（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/button-group.json"` |  |
| calendar | calendar | ui-primitive | shadcn 风格基础组件：日历日期选择 calendar react-day-picker（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/calendar.json"` |  |
| card | card | ui-primitive | shadcn 风格基础组件：卡片 card（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/card.json"` |  |
| carousel | carousel | ui-primitive | shadcn 风格基础组件：轮播 carousel embla（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/carousel.json"` |  |
| chart | chart | ui-primitive | shadcn 风格基础组件：图表封装 chart recharts（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/chart.json"` |  |
| checkbox | checkbox | ui-primitive | shadcn 风格基础组件：复选框 checkbox（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/checkbox.json"` |  |
| collapsible | collapsible | ui-primitive | shadcn 风格基础组件：折叠面板 collapsible（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/collapsible.json"` |  |
| command | command | ui-primitive | shadcn 风格基础组件：命令面板/搜索 command cmdk（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/command.json"` |  |
| context-menu | context-menu | ui-primitive | shadcn 风格基础组件：右键菜单 context menu（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/context-menu.json"` |  |
| dialog | dialog | ui-primitive | shadcn 风格基础组件：对话框 modal dialog（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/dialog.json"` |  |
| drawer | drawer | ui-primitive | shadcn 风格基础组件：底部抽屉 drawer vaul（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/drawer.json"` |  |
| dropdown-menu | dropdown-menu | ui-primitive | shadcn 风格基础组件：下拉菜单 dropdown（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/dropdown-menu.json"` |  |
| empty | empty | ui-primitive | shadcn 风格基础组件：空状态 empty state（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/empty.json"` |  |
| field | field | ui-primitive | shadcn 风格基础组件：表单字段布局 field（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/field.json"` |  |
| form | form | ui-primitive | shadcn 风格基础组件：表单 react-hook-form（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/form.json"` |  |
| hover-card | hover-card | ui-primitive | shadcn 风格基础组件：悬停卡片 hover card（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/hover-card.json"` |  |
| input | input | ui-primitive | shadcn 风格基础组件：输入框 input（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/input.json"` |  |
| input-group | input-group | ui-primitive | shadcn 风格基础组件：带前后缀的输入组 input group（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/input-group.json"` |  |
| input-otp | input-otp | ui-primitive | shadcn 风格基础组件：验证码输入 OTP（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/input-otp.json"` |  |
| item | item | ui-primitive | shadcn 风格基础组件：列表项 item（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/item.json"` |  |
| kbd | kbd | ui-primitive | shadcn 风格基础组件：键盘按键标识 kbd（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/kbd.json"` |  |
| label | label | ui-primitive | shadcn 风格基础组件：表单标签 label（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/label.json"` |  |
| menubar | menubar | ui-primitive | shadcn 风格基础组件：菜单栏 menubar（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/menubar.json"` |  |
| navigation-menu | navigation-menu | ui-primitive | shadcn 风格基础组件：导航菜单 navigation menu（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/navigation-menu.json"` |  |
| pagination | pagination | ui-primitive | shadcn 风格基础组件：分页 pagination（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/pagination.json"` |  |
| popover | popover | ui-primitive | shadcn 风格基础组件：弹出层 popover（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/popover.json"` |  |
| progress | progress | ui-primitive | shadcn 风格基础组件：进度条 progress（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/progress.json"` |  |
| radio-group | radio-group | ui-primitive | shadcn 风格基础组件：单选组 radio（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/radio-group.json"` |  |
| resizable | resizable | ui-primitive | shadcn 风格基础组件：可拖拽分栏 resizable panels（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/resizable.json"` |  |
| scroll-area | scroll-area | ui-primitive | shadcn 风格基础组件：自定义滚动区域 scroll area（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/scroll-area.json"` |  |
| select | select | ui-primitive | shadcn 风格基础组件：下拉选择 select（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/select.json"` |  |
| separator | separator | ui-primitive | shadcn 风格基础组件：分隔线 separator（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/separator.json"` |  |
| sheet | sheet | ui-primitive | shadcn 风格基础组件：侧边抽屉 sheet（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/sheet.json"` |  |
| sidebar | sidebar | ui-primitive | shadcn 风格基础组件：应用侧边栏 sidebar（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/sidebar.json"` |  |
| skeleton | skeleton | ui-primitive | shadcn 风格基础组件：骨架屏 skeleton loading（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/skeleton.json"` |  |
| slider | slider | ui-primitive | shadcn 风格基础组件：滑块 slider（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/slider.json"` |  |
| sonner | sonner | ui-primitive | shadcn 风格基础组件：toast 通知 sonner（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/sonner.json"` | 依赖 next-themes |
| spinner | spinner | ui-primitive | shadcn 风格基础组件：加载转圈 spinner（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/spinner.json"` |  |
| switch | switch | ui-primitive | shadcn 风格基础组件：开关 switch toggle（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/switch.json"` |  |
| table | table | ui-primitive | shadcn 风格基础组件：表格 table（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/table.json"` |  |
| tabs | tabs | ui-primitive | shadcn 风格基础组件：选项卡 tabs（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/tabs.json"` |  |
| textarea | textarea | ui-primitive | shadcn 风格基础组件：多行文本框 textarea（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/textarea.json"` |  |
| toggle | toggle | ui-primitive | shadcn 风格基础组件：切换按钮 toggle（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/toggle.json"` |  |
| toggle-group | toggle-group | ui-primitive | shadcn 风格基础组件：切换按钮组 toggle group（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/toggle-group.json"` |  |
| tooltip | tooltip | ui-primitive | shadcn 风格基础组件：工具提示 tooltip（支撑型 primitive，与 shadcn/ui 同构） | `npx shadcn@latest add "https://www.obsidianui.dev/r/tooltip.json"` |  |
| template:project-one | Project One | template | 创作者经济主题落地页模板 | https://github.com/Atharvsinh-codez/Project-1 （预览 https://project-one.obsidianui.dev/） | 独立仓库，非 registry 条目，MIT |

## 未解决
- 13 个无文档条目（click-spark、file-input、footer、interactive-hover-button、liquid-metal、playground-*、sidebar-stackbits、skeumorphic-music-card、smooth-scroll、visitor-count、loaders-gooey-blobs、raised-button）没有 Markdown 文档和用法示例，描述是从源码开头推断的；使用时需读源码确认 props。
- 未在真实项目里跑 `shadcn add` 后的构建/渲染，只验证到 registry JSON 与 `shadcn view` 层面。

## 风格字段说明（2026-10-07）
- `styling: mixed`：主体是 Tailwind v4 类，但部分 block 另带全局 CSS 文件（如 `dashboard-shell.css`、`active-sessions.css`、`hover-img.css`），文件里用 `.obsidian-*` 作用域和 `--obsidian-*` 硬编码色板，暗色写成 `.dark .obsidian-…`。基础 primitive（button 等）是 Radix + `@/lib/utils` 的 shadcn new-york 写法，用 shadcn 的 CSS 变量。
