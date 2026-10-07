# 导航（navigation）

## 什么时候需要
让人知道"我在哪、还能去哪"：应用侧栏、站点顶栏、页内 tabs、面包屑、分页、操作下拉菜单。不需要的情况：只有两三个页面时用普通链接就够；两到四个视图的就地切换用分段控件或 toggle-group（见 select、toggle-slider 指南），不要为此造一套导航；路由级跳转不要用 tabs 冒充（tabs 是同一对象的同级视图）。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:sidebar`（整块从 `shadcn:sidebar-07` 起步）+ `shadcn:tabs`、`shadcn:breadcrumb`、`shadcn:pagination`、`shadcn:dropdown-menu` | 已拉源码：sidebar 731 行，只依赖 `cn`，自带移动端 Sheet、折叠成图标栏、Cmd/Ctrl+B 快捷键、cookie 记住展开状态；sidebar-07 带 team-switcher、nav-user 等完整外壳；tabs 82 行，基于 Base UI |
| uiarc | `uiarc:tabs`、`uiarc:breadcrumb`、`uiarc:pagination`；营销站顶栏用 `uiarc:site-header`，详情页头用 `uiarc:page-header` | 已拉源码：tabs 基于 `@radix-ui/react-tabs`，有减弱动效分支，没有写死颜色；catalog 写明离场面板设为 inert、溢出滚动按钮有标签。site-header 有 nav landmark、`aria-current`、Esc 关闭、移动端 sheet 锁滚动并还焦点。**uiarc 免费层没有应用侧栏**（`workspace-sidebar`、`sidebar-rail` 是 Pro） |
| 没有底座或其他 | 原生 `<nav aria-label>` + 链接列表；tabs 滑块动效用 `jakubantalik:transition:tabs-sliding` | 已拉文档：纯 CSS，`t-*` 前缀，有 `prefers-reduced-motion` 守卫；只管滑块过渡，tablist 的方向键要自己写 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| shadcn 后台要一整套外壳（可拖宽侧栏 + 头部 + 药丸 tabs + 筛选栏，窄屏变抽屉） | `obsidianui:dashboard-shell` | 已拉源码：侧栏分隔条是 `role="separator"` 并支持键盘调整宽度，有减弱动效分支；但 CSS 里有约 50 处写死颜色（`--obsidian-dashboard-shell-*: #ffffff` 等），必须按 `_styles.md` 映射到 shadcn 变量；依赖 Radix 和 motion，装 block 时跳过覆盖 `ui/*` 的提示 |
| 带下拉大菜单的营销站顶栏 | `shadcn:navigation-menu`（shadcn）/ `uiarc:site-header`（uiarc） | navigation-menu 在 aria base 里没有（shadcn.md）；site-header 自带 mega menu 和移动端菜单 |
| 文件树或文档目录侧栏 | `shadcn:sidebar-11` | 带可折叠文件树的 sidebar block |
| 记录或项目详情页头（面包屑 + 状态 + 成员 + tabs） | `uiarc:page-header` | catalog：滚动后折叠成紧凑栏，tabs 用 Radix 角色，操作结果走 `role="status"` |
| uiarc 底座下的应用侧栏 | 自己写 `<nav aria-label>` + uiarc token；层级多时配 `uiarc:tree-view` | 免费层没有侧栏组件；Pro 的 `sidebar-rail` 只能读文档，站方要求不得仿写源码 |
| 表格或列表翻页 | `shadcn:pagination` / `uiarc:pagination` | uiarc 版 catalog 写明：nav landmark、"Page 3" 标签、当前页 `aria-current="page"`、首尾禁用 |

## 慎用
- `reactbits:pill-nav`：依赖 `react-router-dom` 和 gsap（reactbits.md），Next.js 里要改成 `next/link`。只在落地页顶栏、愿意做这件改造时用。未拉源码。
- `reactbits:gooey-nav`、`reactbits:bubble-menu`、`reactbits:staggered-menu`、`reactbits:flowing-menu`（⚠ marquee）、`reactbits:infinite-menu`（3D/WebGL）：都是表现型菜单，依赖 gsap 或 WebGL。只用于 Persuade / Experience 页面，并算进主导效果预算；导航的键盘可达和焦点顺序**未验证**，用前要自己测。
- `bencho:dock`、`reactbits:dock`：macOS 式放大 Dock，悬停时目标尺寸变化，点击位置会漂。只适合作品集类 Experience 页面。
- `bencho:icon-bar`（⚠ bounce）：选中胶囊回弹，Operate 页面不用。
- `bencho:browser-tabs`：parked block，bencho.md 写明未发布、质量无保证。
- `uiarc:user-menu`：catalog 明写"No focus rings are drawn"，加上 arc-foundation 全局去焦点框，键盘用户看不到位置，必须补焦点样式（见接入要点）。
- `shadcn:menubar`：桌面应用式菜单栏，网页产品里很少需要；aria base 没有。
- `jakubantalik:transition:tabs-sliding`：滑块同时过渡 `transform` 和 `width`（绝对定位，不推动兄弟元素，影响小）；没有方向键处理。

## 页面模式约束
- Operate：主底座的 sidebar / tabs / breadcrumb，装饰动效为 0；只保留展开收起、选中指示这类状态动效（150–300 ms）。
- Persuade：顶栏可以有"滚动变实心"这类状态变化；表现型菜单（gooey、staggered 全屏菜单）算一处主导效果，首屏已有 WebGL 背景时就不要再加。
- Read：文档站用侧栏目录 + 面包屑 + 页内目录，不加任何导航特效。
- Experience：可以用 dock、全屏菜单，但必须保留一条朴素的键盘可达路径。

## 接入要点
- **landmark**：shadcn `Sidebar` 渲染的是 div，不是 `<nav>`；在菜单外包一层 `<nav aria-label="主导航">`。当前项加 `aria-current="page"`，不要只靠高亮色。
- **快捷键冲突**：shadcn sidebar 默认 Cmd/Ctrl+B 切换侧栏（源码 `SIDEBAR_KEYBOARD_SHORTCUT = "b"`），和富文本编辑器的"加粗"冲突；有编辑器的页面改掉这个常量。
- **移动端文案**：移动端 Sheet 里的 `SheetTitle` 是英文 "Sidebar"（sr-only），中文站改成中文。
- **减弱动效**：shadcn sidebar 用 `transition-[width]`、`transition-[left,right,width]` 200 ms linear，动的是宽度，且 tw-animate-css 1.4.0 本身不处理 `prefers-reduced-motion`；给这些元素加 `motion-reduce:transition-none`。
- **uiarc 焦点**：arc-foundation.css 第 179 行全局 `outline: none !important`。用 uiarc 时删掉这条，或在项目样式里补回（选择器要比 `:is(*:focus-visible)` 更具体）：
  ```css
  html body :focus-visible { outline: 2px solid var(--accent) !important; outline-offset: 2px !important; }
  ```
  `--accent` 对背景对比度不到 3:1 时改用 `--foreground`。
- **触控目标**：图标栏折叠态的按钮至少 24×24 px，最好 44×44；折叠后靠 tooltip 显示名称，同时保留 `aria-label`。
- **Tabs 键盘**：Base UI / Radix 的 tabs 已带方向键；自己用 Transitions.dev 拼的 tabs 要补 ←/→、Home/End 和 roving tabindex。

## 候选清单
- `shadcn:sidebar` — shadcn 应用侧栏，后台默认
- `shadcn:sidebar-07` — 可折叠为图标栏的完整侧栏 block，最常用的起点
- `shadcn:tabs` — 同一对象的同级视图
- `shadcn:breadcrumb` — 层级位置
- `shadcn:pagination` — 分页
- `shadcn:dropdown-menu` — 行或卡片的操作菜单
- `uiarc:tabs` — uiarc 底座的 tabs，高度随面板弹性变化
- `uiarc:site-header` — uiarc 营销站顶栏，带 mega menu 和移动端菜单
- `uiarc:page-header` — 详情页头，滚动折叠
- `uiarc:breadcrumb` / `uiarc:pagination` — uiarc 底座的面包屑和分页
- `jakubantalik:transition:tabs-sliding` — 无底座时的 tabs 滑块过渡
- `shadcn:navigation-menu` — shadcn 顶部导航 + mega menu
- `shadcn:sidebar-11` — 文件树侧栏
- `obsidianui:dashboard-shell` — shadcn 后台整页外壳，需映射颜色
- `uiarc:tree-view` — uiarc 底座下做层级导航的补充
- `reactbits:pill-nav` / `reactbits:staggered-menu` — 落地页表现型导航，慎用
- `bencho:dock` / `reactbits:dock` — 作品集 Dock，仅 Experience
- `uiarc:workspace-sidebar` / `uiarc:sidebar-rail` — Pro，不推荐，只读文档作参考
