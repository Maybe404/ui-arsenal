# 反馈（feedback）

## 什么时候需要
告诉用户刚才的操作结果和系统当前的状态：toast（短暂结果）、alert（页面内持续提示）、badge（状态标签）、通知中心（可回看的历史）。先按消息性质选容器：
- 某个字段填错了 → 字段下方的行内错误（form-input 指南），不要弹 toast
- 后台操作完成、可撤销 → toast，带"撤销"按钮
- 页面或表单级、需要一直看见的状态（试用快到期、同步失败） → alert，放在相关内容附近
- 必须先回应才能继续 → alert dialog（overlay 指南）
- 需要回看的通知 → 通知中心
- 一条记录的状态 → badge
- 正在加载 → loading 指南（Operate 页面用骨架屏，不用居中转圈）

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:sonner` + `shadcn:alert` + `shadcn:badge`；Base UI 项目也可用 `shadcn:toast` 代替 sonner | 已拉源码：sonner 封装依赖 `sonner` 和 `next-themes`（跟随明暗）；已核对 sonner 2.0.8 源码：自带 `@media (prefers-reduced-motion)` 关掉过渡和动画，容器 `aria-live="polite"`。`shadcn:toast` 只在 base 有，基于 Base UI Toast，支持 action、promise、堆叠、滑动关闭，焦点样式完整，但 500 ms 的 transform 过渡没有减弱动效处理，要自己补。打平时选 sonner：所有 base 都能用，减弱动效已处理 |
| uiarc | `uiarc:toast-stack`（全站通知）+ `uiarc:alert` + `uiarc:badge` | 已拉源码：都有减弱动效分支，没有写死颜色。catalog：toast-stack 的视口是带标签的 section，`aria-live="polite"`，每条前缀 sr-only 类型（"Error:"），悬停、聚焦、拖拽或切走标签页时计时暂停，关闭聚焦中的 toast 后焦点移到下一条或回到原处；alert 的 danger 用 `role="alert"`，其余用 `role="status"` |
| 没有底座或其他 | 自己写一个 `role="status" aria-live="polite"` 的容器 + `jakubantalik:transition:toast-open-close` | 已拉文档：纯 CSS，上升 + 淡入 + 轻微缩放和模糊，开慢关快，有减弱动效守卫；只有过渡，播报和计时要自己做 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 单个局部确认（"已保存"），不需要队列 | `uiarc:toast` | catalog：`role="status"` + `aria-live`；计时不会在悬停时暂停，所以只放很短的文字 |
| 顶栏铃铛 + 未读数 + 可回看列表 | `uiarc:notification-center` | 已拉源码，基于 Radix Popover；catalog：触发器的 `aria-label` 含未读数，已读、关闭后焦点移到下一行 |
| 异步操作从"进行中"变成"成功 / 失败" | `shadcn:sonner` 的 `toast.promise` / `uiarc:toast-stack` 的 loading toast | 一条消息原地变化，不要先弹一条再弹一条 |
| 移动端下滑关闭、显示剩余时间 | `reactbits:swipe-toast`（见慎用） | 已拉源码：`role="status"` + `aria-live`，有减弱动效处理 |
| 状态标签 | `shadcn:badge` / `uiarc:badge` | 文字本身说明状态，颜色只做辅助 |

## 慎用
- 用 toast 报错并要求用户处理：toast 会自己消失，错误还没被处理信息就没了。需要操作的错误用 alert 放在出错位置附近。
- toast 自动消失时间太短：含操作按钮的 toast 至少 6–8 秒，并在悬停、聚焦时暂停（sonner 和 uiarc toast-stack 已处理，`uiarc:toast` 没有）。
- `reactbits:swipe-toast`：依赖 motion 和 `@hugeicons/*`，要换成 lucide（`_styles.md` 混用规则 8）；源码里有 4 处写死颜色，要改成主底座变量。只在移动端为主、需要滑动关闭时用。
- `reactbits:bell-toggle`：同样依赖 hugeicons；铃铛摇动是装饰动效，Operate 页面不用。
- `librariesdev:metal-fx-badge`：WebGL 液态金属徽章，只用于落地页的 "New / Beta" 标记，一页一个；状态徽章不用它。
- `jakubantalik:transition:notification-badge`：描述为"斜向滑入 + 弹簧 pop"，有回弹；Operate 页面的未读数变化用简单的淡入或缩放即可。未拉源码。
- 脉冲圆点（⚠ pulse-dot）表示"在线"、"实时"：Operate 页面默认不用；确实需要时遵守减弱动效，并配文字。
- `shadcn:toast` 和 `shadcn:sonner` 同时装：一个项目只留一套 toast，否则会出现两个视口、两套播报。
- `bencho:toasts`：其实是"通知我"按钮（铃铛摆动 + 文案替换），不是 toast 组件，按 button 任务看待。

## 页面模式约束
- Operate：toast 固定一个角落，一次最多显示 3 条并折叠其余；进出 150–300 ms，退出比进入快；不做弹跳。alert 不加动画或只做高度展开。
- Persuade：表单提交成功后在原位置显示结果（行内替换），比 toast 更可靠。
- Read：文档里的提示用 alert 样式的 callout，不要彩色粗左边框（impeccable：超过 1px 的彩色左边框是 AI 味高发区）。
- Experience：尽量少打断，结果反馈就地呈现。

## 接入要点
- **播报**：一般结果用 `role="status"` / `aria-live="polite"`；只有真正紧急的错误用 `role="alert"`（会打断读屏）。toast 不要抢焦点。
- **减弱动效**：sonner、uiarc 已处理；`shadcn:toast` 的 500 ms transform 过渡没有处理，给 Toast 根元素加 `motion-reduce:transition-none`。
- **next-themes**：`shadcn:sonner` 依赖 `next-themes` 的 `useTheme` 同步明暗；没用 next-themes 的项目把 `theme` 改成从自己的主题状态传入。
- **图标**：shadcn 封装里图标用 `IconPlaceholder` 按项目图标库替换，全站统一一套（默认 lucide）。
- **颜色与对比度**：成功、警告、错误三种色调的文字在各自底色上都要 ≥ 4.5:1；不要只用颜色区分类型，配图标和文字（"错误："）。
- **位置**：移动端 toast 放底部并避开底部导航和安全区；桌面放右下或右上，全站一致。
- **层级**：toast 视口的 z-index 高于 dialog，否则弹层里的操作结果被遮住。
- **uiarc 焦点**：arc-foundation 全局去掉焦点框，toast 里的"撤销"、alert 的关闭按钮会看不到焦点。补回：
  ```css
  html body :focus-visible { outline: 2px solid var(--accent) !important; outline-offset: 2px !important; }
  ```

## 候选清单
- `shadcn:sonner` — shadcn 底座默认 toast，减弱动效已处理
- `shadcn:toast` — Base UI 原生 toast，仅 base，需补减弱动效
- `shadcn:alert` — 页面内持续提示
- `shadcn:badge` — 状态标签
- `uiarc:toast-stack` — uiarc 全站通知队列
- `uiarc:alert` / `uiarc:badge` — uiarc 底座对应件
- `uiarc:toast` — 单条局部确认
- `uiarc:notification-center` — 通知中心
- `jakubantalik:transition:toast-open-close` — 无底座时的 toast 过渡
- `reactbits:swipe-toast` — 移动端滑动关闭，需换图标和颜色
- `librariesdev:metal-fx-badge` — 落地页 New / Beta 徽章，仅 Persuade
- `jakubantalik:transition:notification-badge` — 未读徽章过渡，带回弹，未验证
- `bencho:find:rauno-notif-stack` / `bencho:find:alex-x-toasts` — 仅参考：通知堆叠节奏
