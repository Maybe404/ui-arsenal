# 头像与用户（avatar-user）

## 什么时候需要
在界面里标识"谁"：评论、记录负责人、协作者头像组、在线状态、账号菜单入口、成员列表行、AI 代理的形象。不需要的情况：只需要名字的地方（表格里的负责人列，名字往往比头像更好扫读）；用户上传头像不是产品功能时，用首字母或统一占位，不要放随机生成的卡通头像冒充。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:avatar`（含 `AvatarGroup`、`AvatarGroupCount`、`AvatarBadge`）+ `shadcn:item` 做用户行；账号菜单用 `shadcn:dropdown-menu`（参考 `shadcn:sidebar-07` 的 `nav-user.tsx`） | 已拉源码：avatar 109 行，基于 Base UI Avatar，图片失败时显示 `AvatarFallback`；item 202 行，列表行带头像、标题、描述、操作插槽；只依赖 `cn` |
| uiarc | `uiarc:avatar`、`uiarc:avatar-group`、`uiarc:user-menu` | 已拉源码：avatar 根元素 `role="img"`，`aria-label` 是"名字 + 状态"，图片和首字母都 `aria-hidden`，状态点不靠颜色单独表达；avatar-group 是 `role="group"`，溢出 `+N` 是带标签的 `role="img"`；user-menu 在 640 px 以下变成底部 sheet，主题和状态切换是 `menuitemradio`。都有减弱动效分支，没有写死颜色。**avatar 依赖 `next/image`**，非 Next 项目要改成 `<img>` |
| 没有底座或其他 | `<img alt>` + 首字母兜底；AI 代理用 `librariesdev:bot-avatars` | 已读文档：bot-avatars 是 canvas，`role="img"` + 按状态的默认 `aria-label`，可传自己的标签或 `aria-hidden`；减弱动效下画静帧，离屏和标签页隐藏时暂停，全页共享一个 rAF 循环 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 指派负责人（选人 + 头像堆叠） | shadcn：`shadcn:combobox` + `shadcn:avatar` 的 `AvatarGroup` 组合 | 组合件的键盘和 ARIA 由 combobox 保证；`bencho:picker` 交互好看但键盘不可用（见慎用） |
| 悬停名字或头像预览人物信息 | `shadcn:hover-card` / `uiarc:hover-card` | 只读预览；触屏上要有点按替代（overlay 指南） |
| 顶栏账号入口（账号、设置、主题、退出） | `uiarc:user-menu`（uiarc）/ `shadcn:dropdown-menu`（shadcn） | uiarc 版异步退出时设 `aria-busy` 并显示加载 |
| AI 代理、机器人的头像和工作状态 | `librariesdev:bot-avatars` | `state` 跟随真实状态（`working` / `default`），文档给了状态映射表；免费 8 种形状，另外 10 种和 `sleeping` 状态属于 Pro |
| 头像组悬停时轻微抬起 | `jakubantalik:transition:avatar-group-hover` | 已拉文档：纯 CSS 变量驱动 `translateY` + `scale`；但回位用过冲弹簧（有回弹），见慎用 |
| 成员列表、设置里的用户行 | `shadcn:item` / `shadcn:item-avatar`（示例） | 行结构统一，操作按钮在行尾 |

## 慎用
- `bencho:picker`：已拉源码，触发器是带 `aria-expanded` 的 button，列表有 `role="listbox"` / `role="option"`，但源码里没有任何键盘处理（无 `onKeyDown`、方向键、Esc），选项不是按钮，键盘用户选不了人，属于第 1 级问题；另外依赖 framer-motion，`AVATARS` 被清空（bencho.md：图片不随授权），要填自己的图片并映射 token。只借鉴"选中的人在胶囊里堆成头像组"这个反馈方式。
- `uiarc:user-menu`：catalog 写明"No focus rings are drawn"，靠高亮表示键盘位置；加上 arc-foundation 全局去焦点框，触发器本身也看不到焦点，必须补焦点样式。
- `jakubantalik:transition:avatar-group-hover`：文档写明回位是带过冲的弹簧（"bouncy ease-out on return"），属于 ⚠ bounce 一类；Operate 页面去掉过冲，只保留轻微抬起。
- `reactbits:profile-card`：3D 悬停和反光的个人资料卡，只适合作品集或个人主页（Experience），未拉源码。
- 随机色首字母头像：颜色要从主底座的有限色板里按用户 id 稳定取值，并检查首字母和底色对比度 ≥ 4.5:1；不要每次渲染随机变色。
- 只用绿点 / 灰点表示在线状态：状态要进入可读文本（uiarc 已写进 `aria-label`；shadcn `AvatarBadge` 要自己加 sr-only 文字）。
- 参考类 `designspells:*`（Telegram 头像融入灵动岛、Slack 周年彩带等）：品牌彩蛋，只借鉴思路。

## 页面模式约束
- Operate：头像只做标识，尺寸统一（列表 24–32 px，详情页 40–48 px），无悬停特效；头像组超过 3–5 个折叠成 `+N`。
- Persuade：客户评价、团队介绍里的头像用真实照片，配姓名和职位；不要用 AI 生成的假人头像充当真实客户（属于状态虚假）。
- Read：作者头像配署名，小尺寸，不加动效。
- Experience：个人主页可以用 profile card 一类的展示效果，作为该页主导效果。

## 接入要点
- **替代文本**：头像旁边已经写了名字时，图片设 `alt=""` 或 `aria-hidden`，避免名字被读两遍；只有头像没有名字时，`alt` 写名字。
- **首字母**：uiarc 取空格分隔的前两段首字母，中文名"张三"会得到"张"，"Maya Chen"得到"MC"；shadcn 的 `AvatarFallback` 内容由你传入，中文名通常取最后一个或两个字。
- **图片失败**：shadcn 用 Base UI 的加载状态自动切到 Fallback；uiarc 在 `onError` 后切首字母。自己写时也要处理 404 和慢网（先显示首字母，图片加载完再替换，不要空白框）。
- **`next/image`**：uiarc avatar 用 `next/image` 的 `fill`，外部头像域名要在 `next.config` 的 `images.remotePatterns` 里放行；非 Next 项目改成 `<img>`，保留 `sizes` 的思路。
- **触控目标**：作为按钮的头像（账号菜单入口）点击区域至少 44×44 px，可以比头像本身大。
- **uiarc 焦点**：arc-foundation 全局 `outline: none !important`。补回：
  ```css
  html body :focus-visible { outline: 2px solid var(--accent) !important; outline-offset: 2px !important; }
  ```
- **bot-avatars 尺寸**：只针对 96 / 64 / 32 px 调过；用 `size` 设尺寸，不要用 CSS 改宽高；画布会画到尺寸的 1.5 倍做跳跃，父元素 `overflow: hidden` 会裁掉（librariesdev 文档）。

## 候选清单
- `shadcn:avatar` — shadcn 头像、头像组、状态徽章
- `shadcn:item` — 带头像的用户行
- `shadcn:dropdown-menu` — 账号菜单
- `uiarc:avatar` — uiarc 头像，名字和状态进入标签，依赖 next/image
- `uiarc:avatar-group` — uiarc 头像组，`+N` 有标签
- `uiarc:user-menu` — 账号菜单，手机端底部 sheet，需补焦点样式
- `librariesdev:bot-avatars` — AI 代理头像
- `shadcn:combobox` — 选人组合件的选择部分
- `shadcn:hover-card` / `uiarc:hover-card` — 人物预览
- `jakubantalik:transition:avatar-group-hover` — 头像组悬停抬起，Operate 去掉回弹
- `shadcn:empty-avatar-group` — 空状态里的邀请成员示例
- `bencho:picker` — 仅借鉴交互，键盘不可用
- `reactbits:profile-card` — 个人主页资料卡，仅 Experience
- `collectui:category:user-profile` — 仅参考：资料页版式
