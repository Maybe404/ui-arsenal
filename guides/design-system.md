# 设计基线（design-system）

## 什么时候需要
开始一个新项目，或者一个项目的颜色、字体、圆角、阴影已经各写各的，需要先定一份设计基线：一套 token（颜色、字号阶梯、圆角、间距、阴影、动效时长）加一份规则（什么时候用强调色、卡片怎么分层、按钮几种）。后面所有组件都从这份基线取值，`_scenes.md` 第 2 级"设计系统偏差"就是拿它来对照的。

不需要的情况：项目已经有稳定的主题和组件库，只是加一个页面，那就沿用现有的；只做一个一次性原型，用 shadcn 默认主题即可。

两条前提：
- **一个项目只有一个底座。** 主底座只能是 shadcn 或 uiarc 之一（见 `_styles.md`）。设计基线的工作是"给这个底座的变量填值"，不是再引入一套 token。
- **参考品牌只借方向。** getdesign 的 DESIGN.md 是对知名品牌公开设计的分析，可以借它的配色关系、字号节奏、密度和组件规则；不复制品牌的 Logo、品牌图形、专有字体、品牌名、产品截图和标志性配色组合到让人误认的程度。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:presets`（`npx shadcn@latest init --preset base-nova`）+ `shadcn:base-color-*` + `shadcn:font-*` | 官方预设一次定好 base（Base UI / Radix / React Aria）、style、底色、图标库和字体。`r/config.json` 实际列出 24 个预设：vega、nova、luma、rhea 用 lucide，maia、mira 用 hugeicons，lyra 用 tabler，sera 是 Noto Sans + Playfair Display 加 taupe 底色。底色 9 种（neutral、stone、zinc、mauve、olive、mist、taupe、gray、slate），都是 Tailwind v4 的 oklch 变量；字体 26 种正文 + 26 种标题，每种是一个 `registry:font` 条目，写入 `--font-sans` 或 `--font-heading`（已看 config.json、mauve.json、font-geist.json） |
| uiarc | `uiarc:arc-foundation` | 完整 token：11 级中性色、语义色、三档阴影、间距、字号、控件高度、圆角（18 / 26 / 34px 和胶囊）、时长缓动和 `motionTokens`（snappy / smooth / morph）；8 种强调色用 `data-accent` 切换，明暗用 `data-theme`。键盘焦点由 foundation 的全局 `:focus-visible` 描边统一处理（2026-10-08 核对；旧版本的全局 `outline: none !important` 已移除），见 `sources/uiarc.md`「焦点」 |
| 没有底座或其他 | `getdesign:<slug>` 选一份 DESIGN.md 作参考方向，落到 shadcn 变量上 | 76 份免费，格式就是 impeccable 用的 DESIGN.md（Google design.md 规范：YAML front-matter 里 `colors`、`typography`、`rounded`、`spacing`、`components`，正文按 Overview → Colors → Typography → Layout → Elevation & Depth → Shapes → Components → Do's and Don'ts 排）。可以直接放到项目根目录当 impeccable 的 DESIGN.md，再按下面的"接入要点"改写成自己的 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 用户说"做成 X 那种感觉" | 对应的 `getdesign:<slug>`（如 `linear.app`、`vercel`、`stripe`、`claude`、`notion`、`apple`） | 一份 DESIGN.md 就把那种感觉的颜色关系、字重、字距、卡片层级写清楚了，比凭印象调更准。注意免费 slug 的写法：`linear.app`、`mistral.ai`、`x.ai`、`together.ai`、`opencode.ai`、`cal`、`bmw-m`、`theverge`、`runwayml` |
| 后台 / 工具类，想要克制的中性风格 | `shadcn:presets` 的 nova 或 luma + `shadcn:base-color-neutral` 或 `zinc` | 默认就是 Operate 页面需要的克制和密度；不需要参考品牌 |
| 内容 / 编辑类产品，要一点人文气质 | `shadcn:presets` 的 sera（taupe + Playfair Display 标题），或 `getdesign:claude`、`getdesign:notion` 作方向 | 衬线标题 + 暖色底在 shadcn 里有现成预设，不用自己拼 |
| 只做 AI 界面局部，要 beautifului 的质感 | `beautifului:foundation` 只借取值 | token 很完整（`--page`、`--canvas`、`--surface`、三级 `--ink`、三级 `--line`、`--accent`、语义色和 tint、六档阴影），可以作为 shadcn 变量的参考取值；但不能整份导入（见下方慎用） |
| 想看 shadcn 旧版 12 色主题（blue、green、rose、violet…） | `shadcn:themes-css` | 只作参考：文件是 HSL 三元组写法（`--primary: 240 5.9% 10%`），是 Tailwind v3 时代的格式，不能直接粘进 v4 的 oklch 项目 |
| 想把设计方向写给 agent 读 | `uiarc:arc-skill` | uiarc 的 SKILL.md 写了设计、动效、文案、无障碍规则（句首大写、不用眉标、不用 em dash、无装饰渐变光晕、只用 regular / medium 字重），可作为写自己 DESIGN.md "Do's and Don'ts" 的参考 |

## 慎用
- 同时用两份 DESIGN.md，或 DESIGN.md 再叠 uiarc / beautifului 的 token：会出现两套强调色、两套圆角。一个项目一份 DESIGN.md，值全部落到主底座变量里。
- getdesign 的 DESIGN.md 原样当成自己的品牌：它们描述的是别人的品牌，`description` 里会写品牌名，`Known Gaps` 里会提到品牌 Logo（如 claude 那份写明"radial-spike-mark 是 logo 资产"）。用之前改 `name`、`description`，删掉 Logo、品牌图形相关的组件条目，主色至少调整色相或明度，不做到让人误认。
- DESIGN.md 里的专有字体：多数品牌字体不公开（linear 那份写"Linear Display"，claude 那份写 Copernicus、StyreneB），文件里通常给了开源替代，直接用替代字体，在 shadcn 里用对应的 `font-*` 条目装。
- DESIGN.md 的覆盖面：多数只分析了品牌的**营销站**，`Known Gaps` 里常写"没有浅色模式""表单错误态没提取""产品界面不在范围内"（linear、claude 两份都这样）。拿来做 Operate 页面时，缺的状态（错误、禁用、空、加载）要自己按主底座补，暗色或浅色缺的一套要自己推出来并测对比度。
- DESIGN.md 里的颜色对不一定达标：例如 claude 那份主按钮 `#cc785c` 上放白字，算出来对比度约 3.3:1，不到正文 4.5:1。落到 token 之前每一对前景 / 背景都要量一遍，不达标就加深主色或改用深色文字。
- `beautifului:foundation` 整份导入：开头 `@import "tailwindcss"` 和 shadcn 重复，body 改成斜纹背景和 14px 字号，在 `@theme` 里重定义 `--color-accent` 和 `--font-sans`，还依赖没列在依赖里的 `shadow-plugin`。另外 `--ink-3`（oklch 0.695）在 `--canvas`（0.961）上对比度约 2.4:1，只能用于装饰和占位，不能当正文颜色。
- `uiarc:arc-foundation` 的取值注意：`--text-muted`（`oklch(59% 0 0)`）在白底上约 4.1:1，不够正文；amber、green 强调色当文字色在白底上不达标（它给了 `--accent-foreground` 处理按钮上的字，文字链接要自己加深）。uiarc 规范说不用装饰渐变，但 foundation 里仍定义了 `--arc-gradient*`，不用就别引用。
- `shadcn:presets` 里的 maia、mira（hugeicons）、lyra（tabler）：图标库不是 lucide。项目图标统一 lucide 时，选 nova / vega / luma / rhea / sera，或 init 后 `npx shadcn@latest migrate icons`。
- 用 Inter、Geist 当展示字体：`_scenes.md` 第 3 级风险。它们作正文没问题；落地页大标题想要个性时，换 `font-heading-*` 里的衬线或有特点的无衬线。
- `getdesign:product-*`、`getdesign:template-*`（Private DESIGN.md、Brand Kit、Starter Kit 等）、`reactbits:pro-kit-*`（Apple Minimal、Editorial、Swiss Grid 等风格 skill）：Pro，不推荐。唯一免费的 `reactbits:pro-kit-terminal-dark` 获取方式是文档页，内容未验证。

## 页面模式约束
- 设计基线是全站共用的，但取值要按页面模式检查：Operate 页面看密度（字号 13–14px 正文是否够读、控件高度是否够点）、状态色是否齐全；Persuade 页面看展示字号阶梯和强调色是否只用在一个主行动上；Read 页面看正文行高、行宽和链接色。
- 明暗按使用场景定，不按产品类别定：开发者工具不一定要深色。DESIGN.md 只给了一种模式时，另一种要补齐并测对比度。
- 效果预算不在基线里定，但基线可以约束它：例如在 DESIGN.md 的 Don'ts 里写"不用装饰渐变、不用彩色光晕、不用眉标"。

## 接入要点
- **流程**：选主底座 → 选一份参考（shadcn 预设，或一份 getdesign DESIGN.md）→ 把参考的颜色、字体、圆角、阴影映射到主底座变量（shadcn：`--background`、`--foreground`、`--card`、`--muted`、`--muted-foreground`、`--border`、`--input`、`--ring`、`--primary`、`--primary-foreground`、`--secondary`、`--accent`、`--destructive`、`--radius`、`--font-sans`、`--font-heading`）→ 补齐缺的模式和状态 → 测对比度 → 写成项目自己的 DESIGN.md。
- **shadcn 的 `--accent` 不是品牌色**：DESIGN.md 的 `primary` 映射到 shadcn 的 `--primary`；shadcn 的 `--accent` 是菜单、hover 的浅底。
- **取值格式**：shadcn v4 用 oklch；DESIGN.md 多数是 hex，转换后写入，不要同一个 token 两种写法并存。
- **和 impeccable 配合**：getdesign 的文件可以直接作为 impeccable 的 DESIGN.md，但要先改 `name`、`description`，删掉品牌专属的描述和 Logo 相关条目；它多出来的 Responsive Behavior、Iteration Guide、Known Gaps 章节按规范会被保留，不影响读取。改完后跑 `npx @google/design.md lint DESIGN.md`（getdesign 文件的 Iteration Guide 里写了这条，未实测）。
- **一个开关**：shadcn 用 `.dark`，uiarc 用 `data-theme="dark"`；全站只认一个。
- **焦点**：无论选哪套，焦点环必须可见。uiarc 底座当前由 arc-foundation 统一画键盘焦点描边，不要再删它的焦点规则（旧版的全局 `outline: none !important` 已移除），细节见 `sources/uiarc.md`「焦点」；shadcn 用 `--ring`，改品牌色时一起改。
- **字体加载**：shadcn 的 `font-*` 条目走 `@fontsource-variable/*` 或 next/font；中文项目要额外定中文字体回退，DESIGN.md 里基本没有中文排版规则。
- **最常见的坑**：只改了颜色没改圆角和阴影，结果组件还是默认 shadcn 的样子配上别人的品牌色，两边都不像；或者 DESIGN.md 放了，但 agent 读的是 CLI 写到子目录的那份（已有 DESIGN.md 时 `getdesign add` 不覆盖，会写到 `{slug}/DESIGN.md`）。

## 候选清单
- `shadcn:presets` — 一次定 base、style、底色、图标、字体，默认首选
- `shadcn:base-color-neutral` / `zinc` / `stone` / `mauve` / `olive` / `mist` / `taupe` / `gray` / `slate` — v4 oklch 底色
- `shadcn:font-*`、`shadcn:font-heading-*` — 正文和标题字体，各 26 种
- `uiarc:arc-foundation` — uiarc 底座的完整 token
- `uiarc:arc-skill` — uiarc 的设计规则，可借鉴写 Don'ts
- `getdesign:linear.app` — 深色、密集、单一强调色的产品营销方向
- `getdesign:vercel` — 黑白极简开发者方向
- `getdesign:stripe` — 细字重、紫色渐变的金融 SaaS 方向（带 `gradient` 风险）
- `getdesign:claude` — 暖色底 + 衬线标题的人文方向（主按钮对比度要修）
- `getdesign:notion` — 编辑式、黑白插画方向
- `getdesign:apple` — 大留白、电影感大图的消费品方向
- `beautifului:foundation` — AI 界面局部的取值参考，不整份导入
- `shadcn:themes-css` — 旧版 12 色主题，HSL 格式，只作参考
- `shadcn:theme-neutral` 等 `theme-*` — new-york-v4 的主题条目
- 其余 70 份 DESIGN.md 用 `find.sh --task design-system` 浏览，按行业分类（金融科技、开发者工具、AI、汽车、媒体消费等）
