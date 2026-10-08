# 表单输入（form-input）

## 什么时候需要
收集文字、数字、密码、验证码等用户输入，并把标签、说明、错误信息和输入框正确关联。只是展示数据就不需要输入框；只有两三个固定选项时用单选或分段控件（见 `toggle-slider.md`、`select.md`），不要让人打字。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:field` + `shadcn:input`（多行用 `shadcn:textarea`，前后缀用 `shadcn:input-group`） | `Field` 负责 label、description、error 和 fieldset/legend 布局，`FieldError` 带 `role="alert"`；`Input` 是 Base UI Input，只依赖 `cn`，自带 `focus-visible` 3px ring 和 `aria-invalid` 红框；移动端 `text-base`、桌面 `md:text-sm`，避免 iOS 聚焦放大（2026-10-07 拉取 base-nova 源码确认）。新代码用 Field，不用旧的 `shadcn:form` |
| uiarc | `uiarc:input`（多行 `uiarc:textarea`） | 原生 input + 真实 label；描述和错误 id 合并进 `aria-describedby`，错误设 `aria-invalid` 并用 `role="alert"` 播报，动画文字 `aria-hidden` 另有纯文本副本（catalog + 源码）。默认高 44px。**焦点只把 1px 边框从 `--border-strong` 变成 `--foreground`，和鼠标悬停一样**，必须按「接入要点」补焦点 |
| 没有底座或其他 | 原生 `<label>` + `<input>` + `aria-describedby` | 输入框是最不该引入第三方的控件；非 Tailwind 项目照 uiarc 的结构手写：label `for`、描述和错误各一个 id、错误 `role="alert"` |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 验证码（OTP） | `shadcn:input-otp`；uiarc 用 `uiarc:otp-input` | shadcn 版基于 `input-otp` 库（一个真实 input 驱动多个格子），粘贴和短信自动填充可用；uiarc 版每格有 "digit N of 6" 标签，首格 `autocomplete="one-time-code"`（catalog） |
| 登录密码，需要显示/隐藏 | `uiarc:password-field`；shadcn 用 `shadcn:input-group` + 一个 `aria-pressed` 的 ghost 图标按钮 | uiarc 版切换按钮是原生 button，`aria-pressed`，标签在 Show/Hide 间切换（catalog）；记得设 `autoComplete="current-password"` 或 `"new-password"` |
| 注册或改密码，需要强度提示 | `uiarc:password-strength` | `role="meter"` + 文字强度，规则列表关联到 `aria-describedby`，不只靠颜色（catalog）。shadcn 没有对应件，用 `Field` + `shadcn:progress` 自己写，强度必须有文字 |
| 有上下限的数量、价格 | `uiarc:number-field` | `role="spinbutton"`，步进按钮有标签，越界会播报（catalog）。注意它的焦点也只靠边框变深；shadcn 下用 `shadcn:input` `type="number"` 或 `inputMode="decimal"` + `shadcn:button-group` 步进 |
| 金额、手机号 | `uiarc:money-input`、`uiarc:phone-input` | 金额输出最小单位、手机号输出 E.164，键盘和读屏都处理过（catalog，未拉源码）。shadcn 生态没有对应件 |
| 自由输入的标签列表（关键词、邮箱） | `uiarc:tag-input` | 回车或逗号生成，删除按钮有 "Remove `<tag>`" 标签，增删用 live region 播报（catalog）。选项来自固定列表时改用 `shadcn:combobox` 的 chips 多选（见 `select.md`） |
| @提及 | `uiarc:mention-input` | 光标处建议列表（catalog，未拉源码，未验证键盘） |
| 页面上的文字原地改名 | `uiarc:inline-edit` | 文字变输入框，比弹窗编辑更合适（catalog，未拉源码） |
| 签名 | `uiarc:signature-pad` | 有撤销、导出 PNG/SVG；`bencho:signature` 视觉更讲究但要映射 token，未拉源码 |
| 校验失败时给一点物理反馈 | `jakubantalik:transition:error-state-shake` | 纯 CSS，抖动 80ms + 60ms。**但它默认 3 秒后自动撤掉错误态，而且没有减弱动效分支**：接入时去掉自动恢复（错误要保留到用户改正），加 `@media (prefers-reduced-motion: reduce)` 关掉抖动，错误文字用 `role="alert"` |

## 慎用
- `bencho:label-input`：浮动标签（placeholder 上浮成 label）。浮动标签在空输入时把 label 当 placeholder，可读性和对比度常出问题，还要映射 token。Operate 表单默认用常驻 label；Persuade 页的单个邮箱框可以用，先确认上浮后的 label 对比度 ≥ 4.5:1。
- `bencho:one-time-code`：实现思路好（一个隐藏 input 覆盖六格，`autoComplete="one-time-code"`），但 props 只有 `length`、`answer`（Accept/Reject 演示开关）、`corner`，**没有 `onComplete` 或 value 回调**，接真实校验要改代码；还用了 blur+threshold 的 goo 滤镜。要接真实验证用 `shadcn:input-otp` 或 `reactbits:code-slots`。
- `reactbits:code-slots`：有 `onComplete`、`status`、`aria-invalid`、`aria-live` 计数，比 bencho 版好接，但依赖 motion + hugeicons（换成 lucide），颜色走 hex props。只在验证码是页面主角（如独立的验证页）时考虑。
- `reactbits:scrub-field`：拖拽调数值，适合设计工具类面板；普通表单用 number-field，未拉源码。
- `reactbits:stepper`：分步表单的进度指示，未拉源码；Operate 页面优先用主底座组件自己拼步骤条。
- `librariesdev:border-beam`、`librariesdev:border-beam-pulse-outside`、`librariesdev:voice-glow`：⚠ glow，只在 AI 输入框表达"正在处理/在听"时用，等待不足 2 秒不加（作者规则）；普通表单不用。
- `originkit:sync-scroll`、`originkit:flow-field`、`originkit:ripple-field` 等带 "field" 的条目：是背景或文字特效，和表单输入无关（见索引修正建议）。
- `obsidianui:input`、`obsidianui:field`、`obsidianui:form`：Radix 版 shadcn 同构件，shadcn 项目不要重复装。
- `shadcn:form`：旧的 react-hook-form 封装，新代码用 `shadcn:field`（官方说明）。
- Pro 条目（`uiarc:multi-step-form`、`uiarc:api-keys`、`reactbits:category:pro-app-ui/forms`）：只当灵感。

## 页面模式约束
- **Operate**：只用主底座输入框。动效只用于状态：聚焦、错误出现、提交中。不用浮动标签、光束、抖动以外的装饰。
- **Persuade**：邮箱订阅框这类单个输入可以有一处小表现（浮动标签或聚焦时的细微强调），但不和首屏主导效果叠在一起；对比度照常要求。
- **Read**：评论框、搜索框用最朴素的样式。
- **Experience**：表单很少出现，出现就用底座默认样式，不要抢作品。

## 接入要点
- **结构**：每个输入都要有可见 label（`FieldLabel` / uiarc 的 `label` prop）；placeholder 不是 label。说明文字和错误都挂到 `aria-describedby`；错误设 `aria-invalid="true"`，错误文案说清楚怎么改。
- **autocomplete 和输入法**：邮箱 `type="email" autoComplete="email"`，密码 `current-password` / `new-password`，验证码 `one-time-code`，手机号 `type="tel" autoComplete="tel"`，数字用 `inputMode="numeric"`/`"decimal"` 而不是一律 `type="number"`。shadcn 的 login/signup block 里没写 autoComplete，要自己补。
- **校验时机**：失焦后再提示，用户修改时实时消除；提交时把焦点移到第一个错误字段。不要用自动消失的错误提示。
- **uiarc 焦点**：装了 `uiarc:arc-foundation` 时，键盘焦点由它统一画描边（文本框靠边框变色，菜单项和选项靠高亮），不用再补，也不要删它的焦点规则或加全局 `!important` 覆盖；旧版的全局 `outline: none !important` 已经移除。接入后用键盘走一遍；只借单个组件、不装 foundation 时要自己补。细节和核对版本见 `sources/uiarc.md`「焦点」。
  uiarc 的 `input`、`textarea`、`password-field`、`search-field` 聚焦和 hover 一样，只把 1px 边框变成 `--foreground`，键盘用户不好分辨（焦点可见，但偏弱）。要更明显：在 `:root` 把 `--focus-ring` 设成可见色（`textarea`、`combobox` 已经用它画 3px 光圈），再在复制进项目的模块 CSS 里给 input 和 password-field、search-field 的外框补 `box-shadow: 0 0 0 3px var(--focus-ring)`。`number-field` 聚焦和 hover 的边框颜色不同，不用改。
- **token**：shadcn 输入框用 `--input`（边框）、`--ring`（焦点）、`--destructive`（错误）；改品牌色时 `--ring` 跟着改，不要只改 `--primary`。
- **减弱动效**：shadcn 输入框只有颜色过渡，不需要处理；uiarc 的错误文案"逐词改写"有减弱分支。自己加的抖动、上浮动画都要写 `prefers-reduced-motion` 分支。
- **移动端**：输入框字号不低于 16px（shadcn 已处理，uiarc 用 `--text-sm`，在 iOS 上会触发聚焦放大，需在移动端断点把字号改成 16px，未实测）。

## 候选清单
- `shadcn:field` — 表单字段容器：label、描述、错误、fieldset
- `shadcn:input` — 单行输入
- `shadcn:textarea` — 多行输入
- `shadcn:input-group` — 前后缀、图标、内嵌按钮
- `shadcn:input-otp` — 验证码
- `uiarc:input` — uiarc 单行输入（焦点偏弱，见接入要点）
- `uiarc:textarea` — uiarc 多行输入，带字数滚动
- `uiarc:password-field` — 密码显示/隐藏
- `uiarc:password-strength` — 注册时的强度和规则
- `uiarc:otp-input` — uiarc 验证码
- `uiarc:number-field` — 有上下限的数量
- `uiarc:money-input` — 金额
- `uiarc:phone-input` — 国际手机号
- `uiarc:tag-input` — 自由标签列表
- `uiarc:mention-input` — @提及
- `uiarc:inline-edit` — 原地改名
- `uiarc:signature-pad` — 签名板
- `jakubantalik:transition:error-state-shake` — 错误抖动（去掉自动恢复、补减弱动效）
- `reactbits:code-slots` — 验证码页的主角式 OTP
- `bencho:label-input` — 浮动标签，仅 Persuade 单输入
- `bencho:one-time-code` — 参考实现思路，需改造才能接真实校验
- `collectui:category:form` — 仅参考：表单布局
- `designspells:209-one-time-password-input-animations-on-family` — 仅参考：OTP 动效节奏
