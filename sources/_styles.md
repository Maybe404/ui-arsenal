本表是 2026-10-07 的判断，依据是各来源 md 和抽查的源码（抽查清单见文末）。

# 来源风格与兼容表

用途：做页面前先定一个主底座，再按本表判断其他来源能不能放进同一页、要做哪些映射。字段定义见各来源 md 的 frontmatter（`visual_style` `foundation` `styling` `motion_lib` `dark_mode` `mixing_notes`）。

## 总表

| 来源 | visual_style | foundation | styling | motion_lib | dark_mode | 混用要点 |
|---|---|---|---|---|---|---|
| shadcn | restrained neutral, style presets vary | own-tokens | tailwind-v4 | css | class | 通常就是主底座；它的 `--accent` 是浅色 hover 底，不是品牌色 |
| uiarc | restrained neutral with spring motion | own-tokens | css-modules | motion | data-theme | `:root` 上的 `--background/--foreground/--border/--accent` 与 shadcn 同名不同义；键盘焦点由 foundation 的全局 `:focus-visible` 描边统一处理（带 `!important`，作用到整页） |
| beautifului | ai-native soft neutral, hairline borders, dense 13-14px type | own-tokens | tailwind-v4 | css | class | foundation.css 会再 `@import "tailwindcss"`、改 body 背景和字号、定义 `--accent`、`--font-sans` |
| obsidianui | showcase motion blocks over shadcn-style primitives | shadcn-compatible | mixed | mixed(motion,gsap,three) | class | primitive 是 Radix 版 shadcn 同构件；block 带 `--obsidian-*` 硬编码色板 |
| bencho | tactile spring-physics micro-interactions | host-tokens | global-css | mixed(framer-motion,liquid-gooey) | data-theme | token 只引用不附带，必须映射；`--ink-rgb` 要 RGB 三元组 |
| loadingui | minimal currentColor spinners and shimmers | none | tailwind-v4 | mixed(css,motion) | none | currentColor 继承文字色；skeleton 用 `bg-muted` |
| reactbits | expressive webgl and text effects | none | mixed | mixed(motion,gsap,ogl,three) | none | 颜色、明暗全靠 props；TW 变体需 Tailwind v4 |
| originkit | flashy webgl/3d showcase effects | none | unknown | mixed(framer-motion,three,motion,gsap,ogl) | unknown | 取码要登录；framer-motion 与 motion 两种写法都有 |
| librariesdev | ai-state glow and canvas/webgl effects | none | inline | mixed(none,three) | prop | 明暗靠 `theme` prop；border-beam 的 auto 只看系统设置 |
| jakubantalik | refined product-design micro-transitions | none | css-only | css | none | `:root` 动效变量与 uiarc 同名不同值 |
| lucide | uniform 2px outline icons | n/a | n/a | none | n/a | 一页只用一套图标 |
| getdesign | brand-replica design specs, varies per brand | n/a | n/a | none | n/a | 是给主底座填 token 值的规范，不是底座 |
| collectui | curated x/twitter ui references, mixed styles | n/a | n/a | none | n/a | 只借鉴结构和节奏 |
| inspora | trend-driven motion and product ui references | n/a | n/a | none | n/a | 只借鉴结构和节奏 |
| designspells | playful delight micro-details from real products | n/a | n/a | none | n/a | 彩蛋式动效一页最多一两处 |

字段取值说明：
- foundation：`own-tokens` 自带一套 token 定义，必须一起装；`host-tokens` 组件引用一套自己的变量名，但不附带定义，必须由宿主项目映射；`shadcn-compatible` 沿用 shadcn 的 CSS 变量；`none` 自包含，颜色靠参数或继承；`n/a` 灵感、图标、规范类。
- dark_mode：`class`（`.dark`）| `data-theme` | `media`（系统设置）| `prop`（组件参数）| `none` | `n/a`。


`unknown`：originkit 的 `styling` 和 `dark_mode`。所有取码途径都要登录，条款也禁止从页面抓源码，所以没有看到源码。公开 registry 只给出依赖（framer-motion 101、three 98、motion 43、gsap 13、ogl 2），看不出用 Tailwind 还是内联样式；`--dark` 是 CLI 的参数预设，说明明暗可能是写死的 prop 值，但没有源码证实。

## 可以当主底座的

主底座要能撑起整页的基础组件：按钮、输入、选择、弹层（dialog / popover / dropdown / tooltip）、表格、tabs、toast，并且有一套完整的颜色、圆角、字体、阴影 token 和明暗切换。本节只说明收藏库里哪些来源能当**新项目**的底座；已有项目用的组件库（Ant Design、MUI、自研等）就是它的主底座，下面的映射规则照样适用，只是映射目标换成它的变量。

- **shadcn（首选）**：63 个基础组件、表单、浮层、表格、侧边栏、图表都有；token 是业界事实标准，reactbits、obsidianui、loadingui 等第三方 registry 都按它的变量写；Tailwind v4 + `.dark`。默认选它。
- **uiarc（可以，但要整站用）**：免费部分就有 button、input、textarea、select、combobox、checkbox、switch、dialog、popover、tooltip、tabs、toast、sortable-data-table、date-picker、command-palette 和十几种图表，够撑一个完整产品；token 也完整（颜色、间距、字号、圆角、阴影、时长、缓动、8 种 accent）。限制：CSS Modules，不用 Tailwind；暗色是 `data-theme`；风格规范很严（无渐变光晕、只用 regular/medium 字重）。选它就整站用它，不要和 shadcn 并列当底座。
- **obsidianui（不单独当底座）**：registry 里有约 50 个 button、dialog、table、sidebar 等 primitive，但都是 Radix 版 shadcn（new-york 写法、`@/lib/utils`）的同构件，本身没有新的 token。需要这些组件时直接用 shadcn；obsidianui 当作 shadcn 底座上的 block 来源。

不能当主底座：
- **beautifului**：有自己完整的 token（`--ink`、`--canvas`、`--surface`、`--line`、`--accent`、四档圆角、六档阴影），但组件只有 21 个 AI 场景件（thinking、tool call、审批卡、聊天输入等），没有通用的输入框、对话框、选择器。只能做 AI 区域的局部组件。
- **bencho、loadingui、reactbits、originkit、librariesdev、jakubantalik**：都是单点交互、加载态或特效，没有基础组件集。
- **getdesign**：DESIGN.md 只是规范，没有组件；它决定主底座的 token 取什么值，本身不是底座。
- **lucide、collectui、inspora、designspells**：图标和灵感，不涉及。

## 兼容矩阵

"可以"指按常规接入即可；"有条件"指满足列出的条件才放同一页；"不建议"指默认不要同页，确有需要时按条件处理，处理不了就不用。

| 组合 | 结论 | 原因 | 条件 / 做法 |
|---|---|---|---|
| shadcn + reactbits | 可以 | reactbits 不带 token，颜色、明暗都走 props（如 Aurora 的 `colorStops`、`lightMode`），在 shadcn 官方 registry 目录里 | 颜色从 shadcn 变量取值传入（如 `getComputedStyle` 读 `--primary`，或直接用主题色值）；明暗切换时同步改 props；一页最多一个 WebGL 背景；Micro 类的 hugeicons 换成项目在用的图标库（项目还没定就用 lucide） |
| shadcn + loadingui | 可以 | 46/47 个组件只用 currentColor，skeleton 用的 `bg-muted` 正是 shadcn 变量；都是 Tailwind v4 + `cn` | 用 `text-*` 改色；7 个 motion 组件装 `motion` 包；注意新版 shadcn 用 `cn` 包，loadingui 用 `@/lib/utils`，两个都要有 |
| shadcn + obsidianui | 可以 | primitive 与 shadcn 同构，同为 Tailwind v4 + `.dark` | 装 block 时 CLI 提示覆盖 `ui/button.tsx` 等文件一律跳过（新版 shadcn 默认 Base UI，obsidianui 是 Radix，`asChild` 和 `render` 写法不同）；dashboard-shell 等 block 的 `--obsidian-*` 色板改成引用 `--background`、`--sidebar`、`--border`、`--foreground`、`--muted-foreground`、`--primary` |
| shadcn + beautifului | 有条件 | 两边都是 Tailwind v4 + `.dark`，暗色策略一致；但 foundation.css 会重复 `@import "tailwindcss"`、改 body 背景（斜纹）和字号 14px、在 `@theme` 里重定义 `--color-accent`、`--font-sans` | 不要整份 `@import` foundation.css；只复制组件用到的 `@theme inline` 条目和 keyframes，并把值改成 shadcn 变量：`--ink`→`--foreground`，`--ink-2`/`--ink-3`→`--muted-foreground`，`--canvas`/`--page`→`--background`，`--surface`→`--card`，`--line`→`--border`，`--accent-tint`→`--primary` 降透明度，`--radius-control`/`--radius-card`/`--radius-window`→基于 `--radius` 的 calc。`--accent` 两边同名不同义（beautifului 是品牌蓝，shadcn 是浅色 hover 底）：**不要**在 `:root` 或 `@theme` 里把 `--accent`、`--color-accent` 改成 `--primary`，那会改掉 shadcn 所有菜单、按钮的 hover 底色；要改的是复制来的组件代码，把其中的 `bg-accent`、`text-accent`、`var(--accent)` 换成 `primary`；图标换成项目在用的图标库（项目还没定就用 lucide） |
| shadcn + bencho | 有条件 | bencho block 只引用自己命名的 token，不带定义；用 framer-motion；8 个 block 的暗色写成 `[data-theme="dark"]` | 在包住 bencho block 的作用域类上定义映射（例如 `.bencho { … }`），不写到 `:root`：`--ink: var(--foreground)`、`--fill-slab: var(--card)`、`--fill-on: var(--primary)`、`--on-ink: var(--background)`（它是压在 `--ink` 底色上的文字色）、`--pane-edge: var(--border)`、`--signal: var(--ring)`、`--font-ui: var(--font-sans)`。`--card` 是 bencho 63 个 block 里唯一和 shadcn 同名的 token，含义也相同（卡片底色，也用作 `--ink` 底上的反色字），直接沿用 shadcn 的定义，**不要再声明**：`--card: var(--card)` 是自引用循环，会让 `--card` 失效，卡片背景随之消失。写在作用域类上的原因：别名在声明它的元素上就解析成具体颜色再往下继承，写在 `:root` 而 `.dark` 加在 body 或更深的元素上时，暗色不会生效；block 用 portal 渲染到 body 时，portal 容器也要带这个类。`--ink-rgb`、`--fill-on-rgb` 要用逗号分隔的 RGB 三元组按明暗各写一份（shadcn 是 oklch，不能直接引用）；切暗色时 `.dark` 和 `data-theme="dark"` 同时设；按 meta 的 tokens 列表逐个补齐，补不齐的 block 不用 |
| shadcn + uiarc | 不建议 | 两个主底座。arc-foundation（`registry/foundation.css`）在 `:root` 定义 `--background`、`--foreground`、`--border`、`--accent`、`--surface`，和 shadcn 同名不同义（uiarc 的 `--accent` 是强调色，shadcn 的是浅色 hover 底），谁后加载谁覆盖；它的全局 `:focus-visible` 描边带 `!important`，会给 shadcn 组件（自带 `outline-none` + `focus-visible:ring`）再叠一圈描边；暗色用 `data-theme`，shadcn 用 `.dark`；视觉语言（大圆角 18–34px、Geist 标题）也不同 | 只想借一个 uiarc 组件时：不导入 arc-foundation，在组件外包一层作用域类，把它需要的非颜色 token（`--space-*`、`--text-*`、`--control-height-*`、`--duration-*`、`--ease-*`、`--radius-control`）复制进来，颜色映射到 shadcn（`--accent`→`--primary`、`--surface`→`--card`、`--text-secondary`→`--muted-foreground`、`--danger`→`--destructive`），`--radius-control` 改成 shadcn 的 `--radius`；不装 foundation 时组件没有焦点描边，要在作用域里补（见 `sources/uiarc.md`「焦点」）；做不到就换 shadcn 生态里的同类组件 |
| uiarc + beautifului | 不建议 | 两套自带 token 互相覆盖（都定义 `--accent`、`--surface`、`--radius-control`、`--shadow-raised`）；暗色一个 `data-theme` 一个 `.dark`；beautifului 需要 Tailwind v4，uiarc 不用 Tailwind | 以 uiarc 为底座时，beautifului 组件要改写成 CSS Modules 并把 `--ink`→`--foreground`、`--canvas`→`--background`、`--line`→`--border` 逐个映射（`--accent` 两边都是品牌强调色，保持原名即可，不要写成 `--accent: var(--accent)` 这种自引用），工作量接近重写，通常直接用 uiarc 的 chat-thread、text-shimmer 等替代 |
| uiarc + bencho | 有条件 | 都是全局/模块 CSS + 变量，暗色都用 `data-theme`，策略一致；风格都偏克制 | 在包住 block 的作用域类上映射 `--ink`→`--foreground`、`--card`/`--fill-slab`→`--surface`（uiarc 没有 `--card`，这里声明不会覆盖底座）、`--fill-on`→`--foreground`、`--on-ink`→`--background`、`--pane-edge`→`--border`、`--signal`→`--accent`、`--font-ui`→`--font-body`，RGB 三元组另写；会同时装 motion（uiarc）和 framer-motion（bencho），能接受包体积再用 |
| uiarc + loadingui | 有条件 | loadingui 需要 Tailwind 和 `cn`，uiarc 项目通常没有 Tailwind | 只挑纯 CSS 的组件（ring 等，keyframes 内联在组件里），把 `size-*`、`text-*` 类改成内联 style 或模块 CSS；颜色继续用 currentColor；uiarc 自带 skeleton、text-shimmer 时优先用自带的 |
| uiarc + reactbits | 有条件 | reactbits 不带 token；但 uiarc 的风格规范明确不要装饰性渐变和光晕 | 选 CSS 变体（不需要 Tailwind）；颜色从 uiarc 的 `--accent`、`--foreground` 取值传 props；只用在 hero、背景等不与 uiarc 控件相邻的位置，带光晕、渐变字的组件不用 |
| shadcn + originkit | 有条件 | 不带 token，颜色走 props 和 preset；依赖 three 的条目很多 | 用户自己登录取码；项目里 framer-motion 和 motion 只留一种（按已有的来，另一种改 import）；颜色传 shadcn 的主题值；Next.js 里 WebGL 组件 `dynamic(..., { ssr: false })`；一页一个重背景 |
| reactbits + originkit | 有条件 | 都是强视觉特效，同页容易各说各话 | 每个区块只放一个特效来源；同一页的特效用同一组颜色（来自主底座）；WebGL 组件总数控制在 1–2 个 |
| 任意 + librariesdev | 可以 | 自包含，inline 样式和 canvas，不读也不写任何全局 token | 按作者规则：等待不足 2 秒不加效果，同一元素或相邻元素不叠两个效果；站点手动切明暗时显式传 `theme`（border-beam 默认 `dark`，`auto` 只看系统设置）；颜色变体选和主底座强调色接近的 |
| 任意 + loadingui | 可以（Tailwind 项目） | currentColor，keyframes 名带 `loading-ui-` 前缀，不易冲突 | 非 Tailwind 项目见上面 uiarc + loadingui 的条件 |
| 任意 + lucide | 可以 | 只用 currentColor，不带样式 | 一页只用一套图标；beautifului 的 Central Icons、iconoir，reactbits Micro 的 hugeicons 换成项目在用的图标库（项目还没定就用 lucide） |
| 任意 + jakubantalik（Transitions.dev） | 可以；uiarc 底座有条件 | 纯 CSS，`t-*` 类名前缀，没有颜色 | 和 uiarc 同页时，`_root.css` 里的 `--duration-fast`（250ms，uiarc 是 160ms）、`--ease-in-out` 与 arc-foundation 同名不同值，不要粘 `_root.css` 的公共块，只用每个过渡自己的变量（如 `--resize-dur`） |
| 任意底座 + getdesign | 可以 | DESIGN.md 只提供 token 值和规则 | 一个项目只用一份 DESIGN.md，把它的颜色、字号、圆角填进主底座的变量；不要同时用 DESIGN.md 和 uiarc/beautifului 自带的取值 |
| 任意 + collectui / inspora / designspells | 可以 | 只是参考 | 只借鉴结构、层级、动效节奏，视觉取值全部来自主底座 |

最重要的三条：
1. shadcn 和 uiarc 不要同页当底座：变量同名不同义，加载顺序决定谁覆盖谁，uiarc 的全局焦点描边还会叠到 shadcn 组件上。
2. bencho 和 beautifului 都要做 token 映射才能进 shadcn 页面：bencho 的 token 根本不随代码分发，beautifului 的 foundation.css 不能整份导入。各家的 `--accent` 在引用处改成 shadcn 的 `--primary`，不要在全局重定义 `--accent`。
3. reactbits、loadingui、librariesdev 这类不带底座的来源最好混，只要把颜色从主底座传进去；风险在动效库重复（motion / framer-motion / gsap / three 同时进包）和明暗不同步，而不在样式冲突。

## 混用规则

1. 一页只能有一个主底座。已有项目的主底座就是它现在的组件库或设计系统（不为了用收藏库而换）；新的 React 项目从 shadcn、uiarc 里选，本库里只有这两家能撑起整页基础件。整个项目最好也只有一个。
2. 从其他来源引入的组件，行为和结构（DOM、交互、动画时序、可访问性）保留；颜色、圆角、字体、阴影全部映射到主底座的 token，不保留来源自带的取值。
3. 映射不了就不用：组件依赖的 token 在主底座里找不到语义对应、或者要改动全局样式（`:root`、`body`、全局 outline、重复 `@import "tailwindcss"`）才能工作时，换别的来源或自己写。
4. 不整份导入其他来源的 foundation / theme CSS（uiarc 的 arc-foundation、beautifului 的 foundation.css、Transitions.dev 的 `_root.css`）。需要它的非颜色 token 时，只复制用得到的变量，放进组件作用域，并确认不和主底座同名。
5. 各家 `--accent` 含义不同：shadcn 是浅色 hover 底，uiarc、beautifului 是品牌强调色。引入时按含义映射（强调色→shadcn 的 `--primary`），不要按名字直接对上。
6. 映射怎么写：别名（如 `--ink: var(--foreground)`）写在包住引入组件的作用域类上，不写 `:root`，这样不会多出第二套全局 theme，暗色切换也能传到组件里。同名且同义的 token（如 bencho 和 shadcn 的 `--card`）直接沿用，不要写 `--x: var(--x)`：自引用是循环，变量会失效。同名不同义的（各家 `--accent`）改组件代码里的引用，不要重定义全局变量。
7. 明暗切换只有一个开关。主底座用 `.dark` 时，引入用 `data-theme` 的组件（uiarc、bencho 部分 block）要同步设置；只认 props 的组件（reactbits、librariesdev）要在切换时传新值。
8. 动效库全站统一：motion 和 framer-motion 只留一个（新代码用 `motion/react`）；gsap、three、ogl 只在确实需要的组件里引入，并按需懒加载。
9. 图标全站一套：已有项目用它现在的那套，还没定时默认 lucide。引入的组件自带别的图标库时，换成项目这一套。
10. 特效有预算：一页最多一个 WebGL / 全屏背景，同一元素或相邻元素不叠两个特效，带光晕、渐变字、跑马灯的组件按各来源 notes 里的 risk 标签写明理由再用。
11. 灵感来源（collectui、inspora、designspells）和 DESIGN.md 只影响结构与取值，不引入第二套设计语言。

## 本次抽查

拉取命令都是 `scripts/fetch.sh <source>:<id>` 或只读 curl，没有安装和登录。

- shadcn：`button`（base-nova，Base UI + `cn` 包 + Tailwind 变量类）；另 curl `r/colors/neutral.json` 核对 CSS 变量清单
- uiarc：`arc-foundation`（`:root` token、`[data-theme="dark"]`、`data-accent`、全局 `:focus-visible` 描边；2026-10-08 复核，旧版的全局 `outline: none !important` 已移除）、`button`（motion + CSS Modules，模块 CSS 无焦点样式）
- beautifului：`foundation`（`@import "tailwindcss"`、`.dark` 自定义变体、`@theme inline`、body 斜纹背景）、`thinking-state`；另 curl 全部 28 个 registry 项核对依赖
- obsidianui：`flip-text`、`dashboard-shell`（`--obsidian-*` 色板、`.dark` 选择器）；另 curl registry 统计依赖并看 button 源码（Radix Slot + cva）
- bencho：`magnet-select`；另用 adapter 扫描全部 63 个 block 的 tokens 和 CSS（8 个 block 有 `[data-theme="dark"]`）
- loadingui：`text-shimmer`（motion）、`ring`（内联 keyframes）；另 curl 全部 47 个组件扫描颜色用法
- reactbits：`split-text`（gsap）、`aurora`（ogl，props 控色）；另 curl `StatusMark-TS-TW`（motion，组件内变量）
- librariesdev：`thinking-orbs`（文档）；另 curl 七个包的 package.json 和 `border-beam/src/BorderBeam.tsx`
- jakubantalik：`transition:card-resize`；另 curl `transitions-data.json`、`skills/transitions-dev/_root.css`
- getdesign：`stripe`（DESIGN.md）
- lucide：`house`
- originkit：只读公开 registry 元数据（依赖、registryDependencies），未取源码
- collectui、inspora、designspells：只读 md，没有可验证的代码
