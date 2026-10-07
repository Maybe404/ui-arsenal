# 图标（icon）

## 什么时候需要
图标用来加快识别：导航项、工具栏按钮、状态标记、文件类型、输入框前缀。它不能替代文字：一个动作只有图标、没有文字也没有 tooltip 时，大多数用户要猜。

不需要的情况：每个标题、每个列表项前都放一个图标做装饰（这是 `_scenes.md` 第 6 节"图标 + 标题 + 一段话"卡片的来源）；用 emoji 或 Unicode 字符（✓ ★ → ⚙）代替图标，这是第 2 级设计系统偏差。

这个收藏库里的图标只有一个来源：Lucide（1866 个正式图标 + Lucide Lab 357 个已发布的实验图标）。`find.sh --task icon` 的 2249 条全部来自它。图标只有英文名和英文 tags，搜要用英文：`find.sh icon calendar`、`find.sh avocado`。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `lucide-react`（`lucide:<name>`） | shadcn 的 nova、vega、luma、rhea、sera 预设默认就是 lucide；组件里写的 `IconPlaceholder` 会被 CLI 换成对应库。ISC 许可，24×24 网格、2px 描边、圆角端点、`currentColor`，全库风格统一（已看 `house.svg`） |
| uiarc | `lucide-react` | uiarc 组件本身依赖 lucide-react，图标惯例是 `size={16} strokeWidth={1.75}` 并加 `aria-hidden="true"`（chat-thread、hero-section 源码里都是这样写的） |
| 没有底座或其他 | `lucide`（vanilla）或 `lucide-static`（SVG / sprite / 图标字体） | 非 React 项目也有官方包：Vue `@lucide/vue`、Svelte `@lucide/svelte`、Astro `@lucide/astro`、Angular `@lucide/angular`；纯 HTML 用 `lucide-static` 的单个 SVG 或 sprite |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 正式库里没有的具体物件（食物、动植物、运动器材、职业、节日等） | `lucide:lab:<name>`（`@lucide/lab` 0.7.0） | 和正式库同一套网格与描边（`avocado` 的 SVG 已核对：24×24、stroke-width 2、round 端点），混用不会突兀。用 `import { Icon } from "lucide-react"; import { avocado } from "@lucide/lab"; <Icon iconNode={avocado} />` |
| 同一个位置两个图标切换（复制 → 已复制、菜单 ↔ 关闭、播放 ↔ 暂停） | `jakubantalik:transition:icon-swap` | 纯 CSS，两个图标叠在同一格里交叉淡入、轻微模糊和缩放，250ms，带 `prefers-reduced-motion` 关闭过渡（已看文档）。状态由 `data-state` 驱动，不需要 JS 动画库 |
| 品牌 logo（GitHub、X、Figma 等） | 不用 Lucide | Lucide 已移除品牌图标（`/api/tags` 里没有 github、twitter、figma、chrome）。用品牌官方提供的 SVG，或 simple-icons；并且按品牌规范使用 |
| 小尺寸密集界面（16px） | `lucide-react` 加 `strokeWidth={1.5}` 或 `nonScalingStroke` | 默认 2px 描边在 16px 下显得粗，配 13–14px 正文时用 1.5–1.75 |

## 慎用
- 一页混用两套图标库：描边粗细、端点、网格不同，一眼能看出来。需要替换的常见来源：
  - shadcn 的 maia、mira 预设（hugeicons）、lyra 预设（tabler）：init 时选 lucide 预设，或用 `npx shadcn@latest migrate icons` 切换；
  - `reactbits:prompt-bar`、`reactbits:thought-line`、`reactbits:refine-frame` 等（依赖 `@hugeicons/react`、`@hugeicons/core-free-icons`）；
  - `beautifului:selection-actions`（`iconoir-react`）、`beautifului:sidebar-nav`（Central Icons，商业图标集，授权要单独确认）；beautifului 多数组件把图标写成内联 SVG，也要逐个换；
  - `obsidianui:dashboard-shell` 的示例（`@duo-icons/react`）、`obsidianui:template:project-one`（同时装了 `lucide-react` 和 `react-icons`）。
- 未发布的 Lab 图标：仓库 main 里有 26 个还没发到 npm（索引里 access=broken，默认搜索不显示）。`import` 时会报错，不要用；等 `@lucide/lab` 发新版。另有 10 个 npm 0.7.0 里有、仓库里已改名或删除的（如 `bat`、`chinese-character`、`peace-sign`），代码照常从 npm 引入可用，预览要看 unpkg 上 `@lucide/lab@0.7.0/dist/esm/icons/{name}.js`。
- Lab 图标的预览 SVG：索引的取码地址指向仓库 main 分支，main 上的图形可能比 npm 0.7.0 新。代码以 npm 包为准，设计稿要核对时看 unpkg 上 0.7.0 的版本。
- `DynamicIcon`（`lucide-react/dynamic`）：按名字字符串渲染，会把全部图标打进构建。只在图标名来自数据库、确实无法枚举时用。
- `import * as icons from "lucide-react"`：破坏 tree-shaking，不要用。
- 旧名：`home` 等已是 `house` 的废弃别名；看到 import 报错查 `icons/{name}.json` 的 `aliases`。
- 用填充风格：Lucide 是线性图标，`fill` 只对部分图标有效。需要"选中态填充"时，用颜色、背景或粗细表达选中，而不是给图标灌颜色。
- 动画图标：收藏库里没有动画图标库。需要动的图标优先用 icon-swap 这种状态切换；`bencho:icon-bar` 带弹跳（`bounce` 风险），Operate 页面不用。

## 页面模式约束
- Operate：图标最多，规则最严。同一层级的图标同尺寸、同描边；工具栏图标按钮要有 tooltip；状态图标旁要有文字或至少有可访问名称（不能只靠颜色和形状传达"失败"）。
- Persuade：图标少用，靠排版和截图说话。不要在功能区每一段前都放一个图标。
- Read：文档里的图标只用于提示框类型（信息、警告）、外链、复制按钮。
- Experience：图标退后，只做导航和控制。

## 接入要点
- **尺寸与字体搭配**：图标视觉高度接近所在文字的大写字母高度或略大。常用对照：13–14px 正文配 16px 图标、`strokeWidth` 1.5–1.75；15–16px 正文配 18–20px 图标、描边 1.75–2；20px 以上标题旁配 20–24px、描边 2。一个项目定下一组（如 16 / 20 / 24 三档）就不要再出现 17、22。
- **粗细与字重**：细字重（300）界面配 1.5 描边，常规字重配 1.75–2；全站一个默认值，写进设计基线（`guides/design-system.md`）。
- **对齐**：图标和文字放在 `inline-flex items-center gap-*` 里；不要靠 `margin-top` 微调。shadcn 组件用 `[&_svg:not([class*='size-'])]:size-4` 统一默认尺寸，自己的组件沿用这个写法。
- **颜色**：图标用 `currentColor` 继承文字色；不要单独给图标配一个品牌色，除非它本身就是状态（成功、失败）。状态色要满足非文字对比度 3:1。
- **可访问性**：
  - Lucide React 默认给图标加 `aria-hidden="true"`；装饰性图标保持这样。
  - **图标按钮必须有可访问名称**：名称写在按钮上（`<button aria-label="删除">`），不写在图标上；或者按钮里放 `sr-only` 文字。只有图标本身独立传达含义（不在按钮里）时，才给图标 `aria-label` 或 `<title>`（官方无障碍文档的建议）。
  - 有 `aria-label` 的图标按钮最好再配 tooltip，让鼠标用户也看得到名称；tooltip 不能是唯一的名称来源。
  - 切换类按钮用 `aria-pressed` 或改变 `aria-label`（"静音" / "取消静音"）；icon-swap 里两个图标都留在 DOM，所以两个都要 `aria-hidden`，名称只放在按钮上。
  - 触控目标不小于 44×44（移动端）或 24×24（WCAG 2.2 最低）；图标 16px 时用按钮的内边距撑大点击区域。
- **性能**：按名具名 import；SSR 项目里图标是普通 SVG，不需要 `"use client"`。
- **搜索方法**：`find.sh icon <英文词>`，或 `curl -s https://lucide.dev/api/tags | jq ...`（见 `sources/lucide.md`）；Lab 图标 id 是 `lab:{name}`，导出名是 camelCase（`apple-core` → `appleCore`）。

## 候选清单
- `lucide:<name>` — 正式图标 1866 个，默认首选（例：`lucide:house`、`lucide:calendar-check`、`lucide:loader-circle`）
- `lucide:lab:<name>` — npm 0.7.0 已发布的 357 个实验图标，补正式库缺的具体物件（例：`lucide:lab:avocado`、`lucide:lab:apple-core`）
- `jakubantalik:transition:icon-swap` — 同位置两个图标的状态切换过渡
- 按分类浏览：42 个分类（text、arrows、files、devices、account 等）不在索引里，用 `https://lucide.dev/api/categories` 查
- 不推荐：仓库未发布的 26 个 Lab 图标（索引标 broken）
