# 表格（table）

## 什么时候需要
多条结构化记录需要按列比较、排序、筛选、选择或批量操作：用户、订单、发票、日志、项目列表。不需要的情况：只有一两列、或每条记录内容差异很大（用列表或卡片）；只是展示几组键值对（用描述列表 `<dl>`）；要像电子表格一样编辑单元格（这是 data grid，不是表格，见慎用）。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:table` + `shadcn:data-table`（指南，配 TanStack Table v9） | 已拉源码：table 116 行，外层 `overflow-x-auto` 容器，有 `TableCaption`；已读文档：data-table 指南覆盖排序、筛选、分页、列显隐、行选择，v9 按 `tableFeatures()` 声明功能、未用的会被 tree-shake。复选框有 `aria-label`。**缺 `aria-sort`**，要自己加（见接入要点） |
| uiarc | `uiarc:sortable-data-table` | 已拉源码：原生 `<table>` + `<caption>`、`scope="col"`、可排序列带 `aria-sort`，排序按钮标签如 "Sort by Budget, currently ascending"，Shift 点击范围选择，排序和选择变化走 `role="status"` 播报；有减弱动效分支，没有写死颜色。**没有分页、筛选和虚拟滚动**，数据量大时自己配 `uiarc:pagination` 和服务端分页 |
| 没有底座或其他 | 原生 `<table>` + `<caption>` + `<th scope>` | 语义表格本身就是最好的可访问性基线，排序、选择等交互按需补 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 后台整页（侧栏 + 指标 + 图表 + 可拖拽行的表格） | `shadcn:dashboard-01` 里的 `data-table.tsx` | 已拉源码：954 行，TanStack v9 + `@dnd-kit` 行拖拽排序 + zod schema；功能全但重，只要表格时从 data-table 指南起步更轻。整页 block 的指标卡见 layout-card 指南的慎用 |
| 自家产品 vs 竞品的功能对比 | `uiarc:comparison-table` | catalog：表格角色完整，"包含 / 部分 / 不包含"用形状区分而不只靠颜色，带图例；窄屏变堆叠视图；sticky 表头 |
| 套餐对比 | 见 pricing 指南（`uiarc:plan-comparison`） | — |
| AI 提议对表格数据的修改 | `beautifului:diff-table`（见 ai-ux 指南） | 未拉源码 |
| 加载中（Operate） | 骨架行：`shadcn:skeleton` / `uiarc:skeleton` | 保留表头和列宽，只把单元格换成骨架条；不要在表格中央放转圈 |
| 空表 / 无搜索结果 | `shadcn:empty` / `uiarc:empty-state`（见 empty-onboarding 指南） | 写清为什么空、下一步做什么，不只是 "No results." |

## 慎用
- `beautifului:records-table`：已拉源码，1053 行 TSX + 826 行 CSS，CRM 风格（标签、列宽拖拽、多选、汇总计算）。源码里没有 `prefers-reduced-motion` 处理，没有 `aria-sort`；演示数据（冰淇淋店）写死在组件里；依赖 beautifului 的 foundation token 和 `GlideMenu`，进 shadcn 项目要按 `_styles.md` 做映射。只在确实需要这套 CRM 交互、且愿意补可访问性时用。
- `beautifului:filter-table`：已拉源码，145 行，状态 chip 有 `aria-pressed`，滚动区有 `role="region"` 和标签；但没有减弱动效处理，筛选后行"实时重排"的动画要自己关掉。
- `uiarc:data-grid`：Pro，不推荐。需要单元格编辑时用 TanStack Table 的单元格渲染自己做，或先确认是否真的需要电子表格交互。
- `shadcn:data-table-demo` 等示例直接 `add`：shadcn.md 提醒示例会写入 `components/` 下的示例文件，只用来参考。
- 参考类 `bencho:find:jamie-row-borders`、`bencho:find:seb-hover-borders`：悬停行时隐藏上下细线让高亮成整块，是好细节，但只借鉴做法。

## 页面模式约束
- Operate：表格是主角，密度 6–9。行悬停只变背景，排序、选择、展开只用 150 ms 左右的状态过渡；不加入场动画（每行"淡入上移"是噪音）。
- Persuade：营销页里的表格通常只有对比表，用 `uiarc:comparison-table` 或静态 `<table>`，不要把表格做成动画展示。
- Read：文档里的表格用原生 `<table>` 加排版样式，横向溢出时容器滚动。
- Experience：基本不用。

## 接入要点
- **data-table 示例只有 new-york-v4（Radix 写法）**：`fetch.sh shadcn:data-table-demo` 不带 `--style` 时拉的就是它，带 `--style base-nova` 会 404。拉下来只作参考，按项目的 base 改写（Base UI 用 `render`，不用 `asChild`）。
- **多选筛选（faceted filter）**：shadcn 官方的 tasks 示例里有完整的写法（Popover + Command + Badge），在 GitHub 仓库 `shadcn-ui/ui` 的 `apps/v4/app/(app)/examples/tasks/` 下，不在 registry 里，按需参考。uiarc 底座用 `uiarc:filter-toolbar`。
- **`aria-sort`（shadcn）**：data-table 指南的排序按钮只调用 `column.toggleSorting()`，没有设置 `aria-sort`。在 `<TableHead>` 上加：
  ```tsx
  <TableHead aria-sort={s === "asc" ? "ascending" : s === "desc" ? "descending" : "none"}>
  ```
  `s` 取 `header.column.getIsSorted()`。排序按钮的文字要说明当前方向，不能只有箭头图标。
- **caption**：每张表都给 `<caption>`（可 sr-only），说明这张表是什么；uiarc 默认 caption 是英文 "Data table"，中文站要改。
- **TanStack 版本**：shadcn 文档和 dashboard-01 都用 v9（`useTable`、`tableFeatures`）；网上大量 v8 示例（`useReactTable`、`getCoreRowModel`）写法不同，不要混。
- **加载与空状态**：首次加载用骨架行，翻页和排序时保留旧数据并在表头或工具栏显示轻量的加载提示，避免整表闪烁；空状态写清原因和下一步。
- **数字列**：右对齐，`tabular-nums`；单位放表头而不是每个单元格。
- **移动端**：shadcn table 外层已有 `overflow-x-auto`；把第一列（名称）设为 sticky，其余横向滚动；或者窄屏改成卡片列表。
- **大数据量**：几百行以上用服务端分页或虚拟滚动；uiarc sortable-data-table 是纯客户端排序，不适合上千行。
- **uiarc 焦点**：装了 `uiarc:arc-foundation` 时，键盘焦点由它统一画描边（文本框靠边框变色，菜单项和选项靠高亮），不用再补，也不要删它的焦点规则或加全局 `!important` 覆盖；旧版的全局 `outline: none !important` 已经移除。接入后用键盘走一遍；只借单个组件、不装 foundation 时要自己补。细节和核对版本见 `sources/uiarc.md`「焦点」。
- **状态不靠颜色**：状态列用 badge 文字（"失败"、"进行中"），不要只用红绿点。

## 候选清单
- `shadcn:table` — 基础表格
- `shadcn:data-table` — TanStack Table v9 指南，排序、筛选、分页、选择
- `uiarc:sortable-data-table` — uiarc 可排序表格，可访问性最完整
- `shadcn:dashboard-01` — 带行拖拽的完整后台表格
- `uiarc:comparison-table` — 竞品功能对比
- `uiarc:pagination` / `shadcn:pagination` — 分页
- `shadcn:skeleton` / `uiarc:skeleton` — 骨架行
- `beautifului:records-table` — CRM 数据网格，需补可访问性和映射
- `beautifului:filter-table` — 状态筛选表，需补减弱动效
- `beautifului:diff-table` — AI 修改预览，见 ai-ux 指南
- `bencho:find:jamie-row-borders` / `bencho:find:seb-hover-borders` — 仅参考：行悬停细节
