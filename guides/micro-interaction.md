# 微交互（micro-interaction）

## 什么时候需要
给单个操作一个即时、准确的反馈：按下、确认、撤销、勾选、点赞、滑动删除、长按确认、复制成功。好的微交互让人知道"操作被接收了、结果是什么、还能不能反悔"。
不需要的情况：没有对应操作的装饰性小动画；用物理效果包装一个本来一次点击就能完成的操作；为了"有趣"把删除做成拖进碎纸机。Operate 页面里，微交互是允许的少数动效之一，但只能表达状态。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | 用 shadcn 组件 + `jakubantalik:transition:*` 的反馈过渡（success-check、error-state-shake、checkbox-check；这三个本次未 fetch，同系列抽查的都带减弱动效守卫）；需要"按住确认"时用 `reactbits:hold-button` | shadcn 自身没有微交互库。Transitions.dev 的反馈过渡纯 CSS、带减弱动效守卫。hold-button 零依赖，源码有键盘路径（`onKeyDown`）、`aria-describedby` 指向操作提示、完成/空闲两套文字用 `aria-hidden` 切换、CSS 里有减弱动效分支 |
| uiarc | `uiarc:confirm-morph`（行内删除确认）、`uiarc:swipe-actions`（移动端滑动操作）、`uiarc:toast-stack` | confirm-morph 源码有 13 处减弱动效处理，文档写明适用和不适用场景（复杂后果用 dialog）。swipe-actions 除了滑动，还提供同样操作的菜单（Radix dropdown），键盘和桌面用户不靠手势也能操作 |
| 没有底座或其他 | `reactbits:hold-button`、`reactbits:status-mark` | 都是 reactbits 新的 Micro 类，源码里处理了减弱动效和 ARIA；status-mark 把 pending/running/done/failed/cancelled 做成形态变化，适合任务状态 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 行内删除，带撤销 | `uiarc:confirm-morph` | 按钮原地变成确认，完成后提供 Undo；比弹窗轻 |
| 防误触的危险操作 | `reactbits:hold-button` | 按住填充，键盘也能完成；`holdTime` 建议 1–1.5 秒 |
| 移动端列表行滑动删除/归档 | `uiarc:swipe-actions`；shadcn 项目用 `reactbits:swipe-row` | swipe-row 有减弱动效和 ARIA，但图标用 hugeicons，要换成项目在用的图标库（项目还没定就用 lucide） |
| AI agent 任务状态 | `reactbits:status-mark` | 状态之间形态过渡，减弱动效时直接切换 |
| 点赞、收藏 | `reactbits:pulse-heart` | 有键盘和减弱动效处理；hugeicons 换成项目在用的图标库（项目还没定就用 lucide）。Operate 页面去掉脉冲，只保留填充切换 |
| 链接"了解更多"悬停 | `jakubantalik:transition:learn-more-hover` | 箭头小位移，纯 CSS，有减弱动效守卫 |
| 表单校验错误 | `jakubantalik:transition:error-state-shake` | 抖动表达"被拒绝"，自动恢复；必须同时有文字错误信息（本次未 fetch） |
| 复制成功、保存成功 | `jakubantalik:transition:success-check` + 文字状态 | 对勾描绘 + 文字（"Copied"），只在真的成功后播放（本次未 fetch） |

## 慎用
- `bencho:slide-confirm`：滑动手柄是一个没有 `onClick`、没有键盘处理的 `<button>`，**键盘用户无法确认**（第 1 级问题）；拖动时每帧改 `width`（wash 和手柄都是）。要用必须补：Enter/Space 直接确认（或按住确认）、给轨道 `role="slider"` 或换成 hold-button 模式。
- `bencho:confirm`：行内删除确认的思路很好，但源码没有任何 `aria-*`，状态变化不播报；按钮的 `left`/`width` 由弹簧驱动（动画布局属性）。用 `uiarc:confirm-morph` 替代，或补 live region 播报 "Deleted" 和撤销。
- bencho 全系列：只引用 `--ink`、`--card`、`--fill-on` 等 token 不附带定义，必须按 `_styles.md` 映射；图片数组被清空，部分组件不填图片就是空的。
- `reactbits:glare-hover`：默认 `width/height: 500px`、`background: #000`、`borderColor: #333`，没有减弱动效；反光扫过是纯装饰，只用于 Persuade 的一张展示卡。
- `bencho:pull`、`bencho:swipe-row`：第 3 级风险（回弹）。回弹来自拖拽松手的物理回位，表达"没越过阈值"，在移动端列表里有含义；Operate 的桌面表格里不用。
- `bencho:foggy-glass`、`bencho:glass-bubble`：第 3 级风险（毛玻璃），纯展示，不进产品界面。
- `reactbits:shredder`、`reactbits:sling-button`、`reactbits:folder-float`（matter-js）、`reactbits:paper-crumple`（three）：把普通操作做成表演，偶尔用于空状态彩蛋或 Experience 页面，不用于高频操作。
- `reactbits:fuse-button`：倒计时引线做撤销窗口，思路可以，但图标是 hugeicons；倒计时必须和真实可撤销时长一致。
- 需登录的 originkit 微交互（如 `originkit:isometric-squares`、`originkit:dynamic-weight`）：多为展示型，免费替代优先上面的 uiarc / reactbits Micro 条目。

## 页面模式约束
- Operate：允许，但只用于表达状态：按下、确认、撤销、成功/失败、勾选。强度 1–3，时长 100–300ms，不用物理弹跳。一个操作只配一个反馈，不叠加（例如点赞不要同时脉冲 + 粒子 + 计数滚动）。
- Persuade：演示性的微交互可以出现在产品介绍区块里，每屏最多 1 处。
- Read：只保留复制代码、展开目录这类功能反馈。
- Experience：可以更俏皮，彩蛋一页最多一两处（`designspells` 的提醒）。

## 接入要点
- **状态真实**：成功动画只在请求成功后播放；乐观更新要有失败回滚和提示。撤销窗口的倒计时等于真实可撤销时间。
- **键盘和读屏**：每个手势（滑动、拖动、长按）都要有键盘等价操作；状态变化（Deleted、Copied、Saved）用 live region 播报。
- **触控目标**：最小 44×44px；滑动操作要有可见的按钮替代（uiarc:swipe-actions 的菜单）。
- **减弱动效**：保留状态切换（图标、颜色、文字），去掉位移、缩放、粒子。
- **优先只动 transform、opacity**：bencho 的 confirm、slide-confirm 动画 width/left，会触发布局；用在单个元素上可以接受，用在列表每一行就要实测或换 transform 方案（条件见 `_scenes.md`「动效规范」）。
- **图标统一**：reactbits Micro 类默认 hugeicons，bencho 用 lucide；全站统一成主底座的图标库。
- **动效库**：uiarc 和 reactbits Micro 用 `motion`，bencho 用 `framer-motion`；同一项目统一一个。

## 候选清单
- `uiarc:confirm-morph` — 行内删除确认 + 撤销
- `uiarc:swipe-actions` — 滑动操作，带菜单替代
- `uiarc:toast-stack` — 堆叠 toast（本次未 fetch）
- `reactbits:hold-button` — 按住确认，零依赖，有键盘路径
- `reactbits:status-mark` — 任务状态形态变化
- `reactbits:swipe-row` — 滑动删除，需换图标
- `reactbits:pulse-heart` — 点赞，需换图标
- `jakubantalik:transition:learn-more-hover` — 链接箭头悬停
- `jakubantalik:transition:checkbox-check` — 复选框对勾描绘（本次未 fetch）
- `jakubantalik:transition:success-check` — 成功对勾（本次未 fetch）
- `jakubantalik:transition:error-state-shake` — 校验错误抖动（本次未 fetch）
- `bencho:slide-confirm` — 滑动确认，缺键盘路径，见慎用
- `bencho:confirm` — 行内确认，缺 ARIA，见慎用
- `reactbits:glare-hover` — 反光扫过，仅 Persuade 展示卡
