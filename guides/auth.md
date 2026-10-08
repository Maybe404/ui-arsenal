# 登录与注册（auth）

## 什么时候需要
登录、注册、验证码登录、找回密码这类身份流程的页面和表单。认证逻辑（会话、OAuth 回调、限流、密码哈希）由后端或认证服务负责，这里只选界面；用了 Clerk、Auth0 等托管认证时，优先用它们自带的界面组件，不必再拼一套。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:login-01`（卡片）/ `shadcn:login-03`（灰底居中）；注册用 `shadcn:signup-05`（带第三方登录） | 由 `Card` + `Field` + `Input` + `Button` 组成，没有额外依赖，结构干净：label 与输入框关联、`type="email"`、`required`、"忘记密码"链接、第三方按钮有文字（"Continue with Google"）（2026-10-07 拉取 base-nova 源码确认）。**但它只是静态骨架**：没有 `autoComplete`、没有错误态、没有提交中状态、`<form>` 没有 `onSubmit`，这些都要自己补（见「接入要点」） |
| uiarc | 注册 `uiarc:signup-form`；登录用 `uiarc:input` + `uiarc:password-field` + `uiarc:button` 组合（无密码登录见下） | signup-form 有真实接口：`onSubmit(details)`（抛错即显示提交错误）、`serverError`、`onProvider`；字段错误 `aria-invalid` + `aria-describedby` + `role="alert"`，成功面板 `role="status"`，第三方按钮有 "Sign up with Google" 标签，密码强度有文字（catalog + 源码）。它会把提交等待至少拉长到 700ms（`Promise.all` 里加了一个 700ms 定时器），这是有意防闪烁，不是假进度。uiarc 免费件里没有"邮箱 + 密码"登录卡（`uiarc:login-split` 是 Pro）。**焦点框被 arc-foundation 全局去掉**，必须补 |
| 没有底座或其他 | 原生 `<form>` + `<label>` + `<input>` | 登录表单字段少，原生控件加正确的 `autocomplete` 就能让密码管理器正常工作，这比任何视觉组件都重要 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 两栏：左表单右品牌图 | `shadcn:login-02` / `shadcn:signup-02`（封面图）或 `shadcn:login-04` / `shadcn:signup-04` | 同样是静态骨架；图片换成自己的资源，小屏隐藏图片 |
| 只用邮箱、magic link | `shadcn:login-05` | 一个字段，最少摩擦 |
| 邮箱验证码登录（无密码），uiarc 底座 | `uiarc:sign-in` 的界面 + 自己的逻辑 | 界面完整（邮箱 → 验证码 → 账号确认三步 morph，步骤和错误用 `role="status"` 播报，第三方按钮有文字）。**但逻辑全是模拟的**：props 只有 `demoCode`（默认 "123456"）和 `onSignIn`，发码用 800ms 定时器假装，没有"发送验证码""校验验证码"的回调。上线前必须把 `submitEmail`、校验、重发改成调用真实接口 |
| passkey 优先 | `uiarc:login-centered` | catalog 写明 passkey 为主、邮箱验证码兜底、busy 按钮用 `aria-busy`；同样是"simulated requests"，未拉源码，接入时按 sign-in 的方式改成真实接口 |
| 验证码那一步 | `shadcn:input-otp` 或 `uiarc:otp-input` | 见 `form-input.md` |
| 注册时的密码强度 | `uiarc:password-strength` | 见 `form-input.md` |
| 产品发布前的 waitlist 首屏 | `uiarc:newsletter-signup`，或 `shadcn:input-group` + `shadcn:button` 拼一行邮箱表单 | uiarc 版 catalog 写明它的可访问性很完整：可见性隐藏的 label、`autocomplete="email"`、失焦后才校验、提交中 `aria-busy`。登录后可换：`originkit:hero-07`（waitlist 首屏，用户自己登录取码） |
| shadcn 底座，免费的登录、注册、找回密码整页 | `tailark:oss-*-login-*`、`tailark:oss-*-sign-up-*`、`tailark:oss-*-forgot-password-*` | Tailark 开源版（MIT，dusk / mist / veil 三套，2026-10-08 收录、条目待人审）；只是页面结构和样式，表单校验、错误态、提交防重复要自己接（见 `form-input.md`、`button.md`） |

## 慎用
- 直接上线 shadcn login/signup block：骨架里 `href="#"`、没有 `onSubmit`、没有错误展示，原样上线就是坏链和无反馈（第 1 级）。
- 直接上线 `uiarc:sign-in` / `uiarc:login-centered`：演示逻辑会让任何人用 "123456" 登录成功，界面却显示"已登录"（第 1 级"状态虚假"）。
- `shadcn:login-03` / `shadcn:signup-03` 的 "background" 标签：只是 `bg-muted` 灰底，不是背景特效；想给登录页加 WebGL 背景时按 Persuade 规则单独选背景组件，并确认表单区域对比度。
- 登录页上的光标特效、彩蛋（如 `designspells:120-dvd-like-bouncing-logo-animation-on-retros-login-page`）：只当灵感，登录是任务页，默认不加。
- `obsidianui:active-sessions`：是"已登录设备列表"的设置页组件，不是登录表单；放在账号安全页里可以，未拉源码。
- Pro 条目（`uiarc:login-split`、`uiarc:login-immersive`、`uiarc:hero-signup`、`reactbits:category:pro-blocks/auth`、`reactbits:category:pro-app-ui/authentication`）：只当灵感，用 shadcn login-02 或 uiarc 组件组合出近似布局。

## 页面模式约束
- 登录、注册页按 **Operate** 处理：访客要完成任务。主导效果 0 个；动效只用于步骤切换（300–500ms）、提交中、错误出现。两栏布局里的品牌图是静态图，不是动效区。
- 营销页里嵌的 waitlist / 订阅表单按 **Persuade** 处理：表单本身保持朴素，表现力留给页面的那一处主导效果，表单不叠光束。
- **Read / Experience**：不涉及。

## 接入要点
- **autocomplete（最重要）**：邮箱 `autoComplete="email"`（登录时用 `"username"` 也可以），登录密码 `"current-password"`，注册密码 `"new-password"`，验证码 `"one-time-code"`，姓名 `"name"`。表单要是真正的 `<form>` 并有提交按钮，密码管理器才会识别。shadcn block 里这些都没写。
- **提交与错误**：提交中按钮显示加载并防重复提交（`aria-busy` + `aria-disabled`，见 `button.md`）；服务端错误显示在按钮上方并 `role="alert"`；错误文案不要泄露"邮箱不存在"这类信息（写"邮箱或密码不正确"）。字段错误按 `form-input.md` 的方式关联。
- **第三方登录**：按钮必须有文字（"使用 Google 继续"），不能只放图标；品牌图标用官方 SVG（uiarc 里有 Google 四色标），不要用 lucide 里近似的图标冒充品牌。
- **焦点流**：进入页面时焦点在第一个输入框；多步流程每一步切换后把焦点移到新步骤的第一个控件（uiarc sign-in 已处理）；"返回修改邮箱"要能键盘操作。
- **uiarc 焦点**：装了 `uiarc:arc-foundation` 时，键盘焦点由它统一画描边（文本框靠边框变色，菜单项和选项靠高亮），不用再补，也不要删它的焦点规则或加全局 `!important` 覆盖；旧版的全局 `outline: none !important` 已经移除。接入后用键盘走一遍；只借单个组件、不装 foundation 时要自己补。细节和核对版本见 `sources/uiarc.md`「焦点」。
  输入框聚焦和 hover 一样只是 1px 边框变色，偏弱，处理办法见 `form-input.md`「接入要点」。
- **token**：shadcn block 全部用底座变量，只需换 logo 和封面图；login-03 的背景是 `--muted`。uiarc 的 primary 按钮是 `--foreground` 底。
- **移动端**：卡片 `max-w-sm`，左右留白；两栏布局小屏只留表单；输入框字号 ≥ 16px（shadcn 已处理）。
- **减弱动效**：uiarc sign-in / signup-form 的步骤切换有 reduce 分支；自己加的步骤动画也要有。

## 候选清单
- `shadcn:login-01` — 卡片式登录骨架
- `shadcn:login-03` — 灰底居中登录页
- `shadcn:login-02` — 两栏 + 封面图登录页
- `shadcn:login-04` — 表单 + 配图卡片
- `shadcn:login-05` — 仅邮箱 / magic link
- `shadcn:signup-05` — 带第三方登录的注册
- `shadcn:signup-02` — 两栏注册页
- `uiarc:signup-form` — 有真实接口的注册表单
- `uiarc:sign-in` — 邮箱验证码登录界面，逻辑需替换
- `uiarc:login-centered` — passkey 优先登录页，逻辑需替换，未拉源码
- `uiarc:password-field` — 登录密码框
- `uiarc:newsletter-signup` — 邮件订阅（营销页），未拉源码
- `originkit:hero-07` — 需登录；waitlist 首屏，免费替代见上
- `inspora:1-19` — 仅参考：注册页布局
- `collectui:category:sign-up` — 仅参考：注册样式
- `tailark:oss-*-login-*`、`tailark:oss-*-sign-up-*`、`tailark:oss-*-forgot-password-*` — Tailark 开源登录注册页
