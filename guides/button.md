# 按钮（button）

## 什么时候需要
触发一个动作：提交、保存、打开弹层、危险操作。跳转到别的页面用链接（`<a>`），不要用按钮模拟；只是切换开/关状态用 toggle（见 `toggle-slider.md`）。大多数页面只需要主底座的一个 Button 组件加几个 variant，不需要专项按钮。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:button` | Base UI `Button` + cva，依赖只有 `cn`；6 个 variant（default / outline / secondary / ghost / destructive / link）和 8 个 size（含 icon 尺寸）；自带 `focus-visible:ring-3 ring-ring/50`、`aria-invalid` 样式、disabled 态；按下只有 `translate-y-px`，不抢注意力。颜色全部走 `--primary` `--secondary` `--destructive` `--muted` 等变量（2026-10-07 拉取 base-nova 源码确认） |
| uiarc | `uiarc:button` | 原生 `<button>` + motion；`loading` 用 `aria-busy` + `aria-disabled` 而不是 `disabled`，加载中键盘焦点不丢；按下 0.96–0.985 的弹簧缩放，作为弹层触发器（`aria-haspopup`/`data-state`）时自动不缩放；有 `useReducedMotion` 分支和 CSS `prefers-reduced-motion`。模块 CSS 里没有焦点样式，键盘焦点靠 arc-foundation 的全局描边（见「接入要点」） |
| 没有底座或其他 | 原生 `<button>` + 项目 token | 非 Tailwind、非 React 的项目不必为按钮引入整个底座。加载时按「接入要点」的加载态处理：表单层防重复提交，按钮显示状态并保住焦点 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 分段按钮、按钮和输入框拼接 | `shadcn:button-group`（uiarc 用 `uiarc:button-group`） | 处理相邻圆角和分隔线；示例见 `shadcn:button-group-split`、`shadcn:button-group-input` |
| 一个默认动作 + 几个变体（合并方式、导出格式） | `uiarc:split-button`；shadcn 用 `shadcn:button-group` + `shadcn:dropdown-menu` 组合（参考 `shadcn:button-group-dropdown`） | uiarc 版本两个原生按钮，箭头按钮有 "`<label>` more actions" 标签，菜单是 Radix DropdownMenu（catalog 说明，未拉源码） |
| 异步提交后按钮本身要显示"已保存" | `uiarc:action-button` | `role="status"` 播报 pending 和 success，pending 期间焦点不丢（catalog accessibility）。shadcn 没有对应件，用 `shadcn:button` + `shadcn:spinner` 自己写状态，并用 live region 播报 |
| 复制 API key、命令、链接 | `uiarc:copy-button` | 预留三种状态里最宽的宽度，不跳布局；`role="status"` 播报 Copied / Could not copy（catalog） |
| 危险操作要防误触（删除、吊销） | `uiarc:hold-to-confirm` | 键盘可以长按 Space/Enter 完成，`aria-describedby` 指向操作提示，完成后播报（catalog）。shadcn 底座下按「混用规则」做作用域映射后借用；做不到就用 `shadcn:alert-dialog` 二次确认 |
| 删除后原地给撤销 | `uiarc:confirm-morph` | 先给 Cancel 焦点，回车不会误确认；焦点跟着形态切换；鼠标悬停和标签页隐藏时暂停倒计时（catalog） |
| Persuade 页的主 CTA 想要一点表现力 | `obsidianui:discover-button` | 悬停/聚焦时填充层展开、箭头圈覆盖文字；有 `:focus-visible` 描边和减弱动效分支，颜色是 `--obsidian-discover-*` 变量带硬编码兜底，映射到 `--primary` / `--secondary` 即可。注意它动画的是 `width`（480ms），只适合单个 CTA |
| Persuade 页想要"标签滑动替换"类 CTA | `obsidianui:discover-button`；或 `obsidianui:interactive-hover-button`（未拉源码，未验证） | 免费、现在就能取。登录后可换：`originkit:label-slide-button`、`originkit:arrow-reveal-button`（用户自己登录取码） |

## 慎用
- `bencho:slide-confirm`：手柄是 `<button>` 但没有 `onClick`/`onKeyDown`，**键盘用户无法完成确认**（第 1 级）；组件也没有 `onConfirm` 回调，props 只有外观参数；还要映射 8 个 token（含两个 RGB 三元组）。要"滑动确认"的手感，改用 `uiarc:hold-to-confirm` 或 `reactbits:slide-commit`（后者未拉源码，未验证键盘）。
- `bencho:confirm`：索引描述写"行内删除确认"，源码注释写明**没有确认步骤**，点击即删除，之后给 4 秒撤销；源码里没有任何 `aria-*` 或 live region；要映射 24 个 token。需要这个交互时用 `uiarc:confirm-morph`。
- `bencho:escape`、`reactbits:dodge-field`：逃跑按钮。放在真实操作上就是第 1 级（无法点击、触屏无意义）。只能当彩蛋，不能绑定任何真实动作。
- `reactbits:magnet`、`originkit:liquid-carve-button`、`originkit:radial-reveal-button`：光标驱动效果，触屏没有效果，Operate 页面不用；Persuade 页面最多一个 CTA。
- `reactbits:star-border`、`librariesdev:border-beam-sm`、`librariesdev:border-beam-pulse-inner`、`originkit:neon-border`、`originkit:orbit-border-button`、`originkit:moving-gradient-button`、`originkit:crystal-glow`：⚠ glow，第 3 级风险。只用在 Persuade 页面唯一的主 CTA 上，并确认光晕不拉低文字对比度；librariesdev 的 border-beam 按作者规则不和别的效果叠加。
- `librariesdev:metal-fx-button`、`librariesdev:metal-fx-circle`：液态金属描边，适合定价页 Upgrade 这类单点 CTA，不进 Operate 页面。
- `reactbits:fuse-button`、`reactbits:sling-button`、`reactbits:pulse-heart`、`reactbits:voice-pill`：依赖 hugeicons，接入时换成项目在用的图标库（项目还没定就用 lucide）；都是单点微交互，Operate 页面里只在它表达的状态确实存在时用（如撤销倒计时、发送）。
- `reactbits:hold-button`：有 `onKeyDown` 和 `aria-describedby`，但颜色全靠 hex props（`backgroundColor`、`fillColor` 等），要从主底座变量取值传入；同等需求优先 `uiarc:hold-to-confirm`。
- `obsidianui:button`、`obsidianui:button-group`：Radix 版 shadcn 同构件。shadcn 项目直接用 `shadcn:button`，装 obsidianui block 时 CLI 提示覆盖 `ui/button.tsx` 一律跳过。
- `beautifului:button`：beautifului 内部共享的原子件，只在已经引入 beautifului AI 组件的区域里跟着用，不当通用按钮。
- Pro 条目（`originkit:magnetic-hover-button`、`originkit:neon-glow-button`、`originkit:encrypt-button`、`jakubantalik:transition:get-pro-button`、`uiarc:cancel-flow` 等）：不推荐，只能当灵感，用免费组件做近似效果。

## 页面模式约束
- **Operate**：只用主底座按钮。装饰动效为 0；允许的动效只有按下反馈（100–150ms）、加载、成功/失败状态。同一个任务区块（一张表单、一个对话框、一条工具栏）里只有一个 default/primary 按钮，其余用 outline、ghost、secondary；一屏里并列的几个独立任务区块可以各有一个。
- **Persuade**：首屏主 CTA 可以用一个有表现力的按钮（discover-button、border-beam、metal-fx 三选一），但它算这一屏的"每屏 1 处装饰动效"；如果首屏已经有 WebGL 背景这类主导效果，CTA 用普通按钮。
- **Read**：用 `link` 或 `ghost` variant，基本不用动效。
- **Experience**：按钮退后，用 ghost/outline，不要和作品抢注意力。

## 接入要点
- **token**：shadcn 的 `--accent` 是浅色 hover 底，不是品牌色；品牌色按钮用 default variant（`--primary`）。uiarc 的 primary 是 `--foreground` 底 + `--background` 字（黑底白字），想要彩色主按钮要改 `.primary` 的取值，不要改 `--foreground`。
- **uiarc 焦点**：装了 `uiarc:arc-foundation` 时，键盘焦点由它统一画描边（文本框靠边框变色，菜单项和选项靠高亮），不用再补，也不要删它的焦点规则或加全局 `!important` 覆盖；旧版的全局 `outline: none !important` 已经移除。接入后用键盘走一遍；只借单个组件、不装 foundation 时要自己补。细节和核对版本见 `sources/uiarc.md`「焦点」。
- **触控目标**：`shadcn:button` 默认高 32px（`h-8`），`lg` 36px，`icon` 32×32，在触屏为主的页面低于 44px 建议值。移动端用 `size="lg"` 并加 `min-h-11`，或给图标按钮加 `after:absolute after:-inset-2` 扩大点击区（shadcn 的 switch、slider 就是这么做的）。uiarc 默认 44px（`--control-height-md`）。
- **图标按钮**必须有 `aria-label`；图标沿用项目在用的那一套，项目还没定图标库时用 lucide。
- **加载态**：要同时做到三件事。① 防重复提交放在表单层：在 `onSubmit` 或业务入口用一个"进行中"标志拒绝第二次提交，鼠标点击、键盘回车、程序触发都走这里，不能只靠按钮。② 按钮显示状态：spinner + 保留文字（"Saving…"），容器设 `aria-busy`。③ 焦点不丢：`disabled` 写法（shadcn 示例、`loading.md` 的按钮内联写法）简单，但按钮会变得不可聚焦；在 Chromium 152 里实测，键盘回车提交后把按钮设成 `disabled`，焦点随即落到 body（其他浏览器未测），键盘用户要重新找位置。需要保住焦点时用 `aria-disabled="true"`（uiarc:button 的做法），但它只表达状态、不会阻止点击，处理函数里要自己直接返回。加载中时保留文字宽度，避免布局跳动。
- **减弱动效**：shadcn 按钮只有 `transition-all` 的颜色过渡和 1px 位移，可接受；uiarc 已处理（减弱时标签只做淡入淡出，spinner 停转）。uiarc 按钮在标签变化时会弹簧动画宽度，这是有意的"标签变形"，在长表格的行内按钮上可以关掉（不改 children 的 key 即可）。
- **常见坑**：shadcn 新版默认 Base UI，按钮包链接用 `render={<a href="…" />}`，不是 Radix 的 `asChild`；网上旧示例 `shadcn:button-as-child` 是 Radix 写法。

## 候选清单
- `shadcn:button` — shadcn 底座的默认按钮，所有页面模式
- `uiarc:button` — uiarc 底座的默认按钮，带 loading 和标签变形
- `shadcn:button-group` — 分段、拼接、split button 的容器
- `uiarc:button-group` — uiarc 的按钮组，悬停高亮在分段间滑动
- `uiarc:split-button` — 默认动作 + 下拉备选
- `uiarc:action-button` — 异步提交后在按钮上显示结果
- `uiarc:copy-button` — 复制并原地确认
- `uiarc:hold-to-confirm` — 危险操作长按确认，键盘可用
- `uiarc:confirm-morph` — 行内确认 + 撤销
- `shadcn:spinner-button` — shadcn 加载按钮示例（参考写法，注意 disabled 丢焦点）
- `obsidianui:discover-button` — Persuade 页单个主 CTA
- `librariesdev:border-beam-sm` — Persuade 页 CTA 边框光束（⚠ glow）
- `librariesdev:metal-fx-button` — 定价/升级 CTA 的液态金属描边
- `originkit:label-slide-button` — 需登录；CTA 标签滑动替换，免费替代见上
- `reactbits:hold-button` — 长按填充确认，颜色走 props
- `reactbits:fuse-button` — 完成后带撤销倒计时，需换图标库
- `bencho:slide-confirm` — 仅参考手感，键盘不可用
- `designspells:329-delete-confirmation-animation-in-things-take-time` — 仅参考：删除确认的动效节奏
- `inspora:multi-action-button` — 仅参考：多动作按钮结构
