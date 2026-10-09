# 空状态与引导（empty-onboarding）

## 什么时候需要
页面没有内容可显示时（首次使用、列表为空、搜索无结果、筛选后为空、404），以及新用户第一次进入需要被带着走几步时。空状态的任务是**教用户怎么用**：说清这里会放什么、为什么现在是空的、下一步做什么，并给出一个主操作。只写 "No data" 或放一张插画不算空状态。

先区分四种情况，它们不是同一个组件：
- 还在加载 → 骨架屏（loading 指南），不是空状态
- 第一次使用，什么都没有 → 解释用途 + 创建或导入的主操作 + 可选的示例数据或文档链接
- 搜索或筛选后没有结果 → 回显查询条件 + "清除筛选"或修改建议，不要放创建按钮
- 出错导致没有数据 → alert（feedback 指南），写原因和重试

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:empty` | 已拉源码：104 行，插槽齐全（`Empty` / `EmptyHeader` / `EmptyMedia` / `EmptyTitle` / `EmptyDescription` / `EmptyContent`），描述里的链接自带下划线，`text-balance` 处理换行；无动画。注意 `EmptyTitle` 渲染的是 div，没有标题语义（见接入要点）；源码 import 了 `class-variance-authority`，自己的 registry 依赖只列了 `cn`；cva 由 `shadcn init` 安装的 style 提供（2026-10-08 核对 base-nova 的 style 依赖），没跑过 init 的项目单独装时要手动装 cva |
| uiarc | `uiarc:empty-state` | 已拉源码：有 `title`、`description`、`action`、`icon`、`label` 属性；catalog：渲染 `<section>` + h3，可传 `label` 命名区域，图标 `aria-hidden`；改 props 时文案形变（如从"空"变"成功"），有减弱动效分支，没有写死颜色 |
| 没有底座或其他 | 语义 HTML：`<section aria-labelledby>` + 标题 + 一段说明 + 一个主按钮 | 空状态不需要组件库也能做好，关键在文案 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 关键页面需要更有分量的插画空状态 | `uiarc:empty-states`（抽一个场景用） | 已拉源码：四个场景（无结果、离线、收件箱清空、404）共用一套插画并在切换时形变，插画 `role="img"` 并有标签；catalog 建议抽出单个场景用在关键页面，不是整套放上去 |
| 多步骤的首次设置 | 用主底座组合：清单（`shadcn:item` 列表 + `shadcn:checkbox` + `shadcn:progress`） | 索引里没有免费的引导清单组件；uiarc catalog 提到的 `onboarding-checklist` 在 catalog 条目里并不存在 |
| 分步向导页面之间的前进后退 | `jakubantalik:transition:page-side-by-side` | 已拉文档：横向滑动切换，纯 CSS，有减弱动效守卫；只管过渡，切换后要把焦点移到新步骤的标题 |
| AI 产品的空状态或"代理正在处理" | `librariesdev:bot-avatars` 作为小吉祥物 | 已读文档：canvas，`role="img"` + 按状态的 `aria-label`，减弱动效下画静帧，离屏和标签页隐藏时暂停 |
| 空状态里放一个默认头像组提示"邀请成员" | `shadcn:empty-avatar-group`（示例） | 已拉源码：空状态 + 头像组 + 邀请按钮的写法 |
| 404 页加一个小游戏彩蛋 | 普通 404 + 搜索框 + 常用入口；标题可以用 `reactbits:fuzzy-text`（见慎用） | 先让迷路的用户回到正路，小游戏是彩蛋不是需求。登录后可换：`originkit:pixel-run-game`、`originkit:flap`（用户自己登录取码） |

## 慎用
- 只有插画没有操作的空状态：插画不能代替说明和主按钮。
- 搜索无结果时放"创建"按钮：用户想找东西，不是想新建；给"清除筛选"和拼写或范围建议。
- `reactbits:fuzzy-text`：已拉源码，335 行 canvas 抖动文字；源码里没有 `prefers-reduced-motion` 处理，也没有 `aria-*` 或 `role`，读屏读不到 canvas 里的字。用于 404 标题时必须在旁边放 sr-only 的真实标题，并在减弱动效下停掉抖动。只用于 Persuade / Experience 的 404 页。
- `bencho:eye-tracker`：跟随光标的眼睛，趣味空状态；需 token 映射（bencho.md），只适合 Experience 或品牌感强的 404。
- `originkit:pixel-run-game`、`originkit:flap`：需登录；canvas 小游戏，要确认键盘可玩、可暂停、不自动抢焦点，返回首页的链接要在游戏之外始终可见。
- 参考类 `designspells:*`（Discord、Vercel、Wendy's 的 404 小游戏，Perplexity 引导教程等）：只借鉴思路，不能当生产组件，也不复制品牌资产。
- 引导浮层逐个高亮界面元素（product tour）：多数情况下用户会直接跳过；优先把引导写进空状态本身和真实的第一步操作里。

## 页面模式约束
- Operate：空状态用主底座的 empty 组件，图标或小插画即可，不加动画；文案写清下一步，主按钮一个。
- Persuade：404、等候名单等营销场景可以有一处趣味元素（小游戏、文字效果），算作该页的主导效果。
- Read：文档搜索无结果时给出相近条目和搜索建议，不做插画。
- Experience：作品集的空分类、404 可以更有个性，但返回路径要明显。

## 接入要点
- **标题语义**：shadcn `EmptyTitle` 是 div。改成标题元素，或保留 div 并加 `role="heading" aria-level={2}`（按页面层级选级别）。uiarc 固定是 h3，页面层级不合适时外层调整。
- **文案结构**：标题说这里是什么（"还没有项目"），描述说为什么空和能做什么（"项目用来组织……从模板开始，或导入已有文件"），按钮用动词（"新建项目"）。中文站把 uiarc 示例里的英文文案全部换掉。
- **主操作只有一个**：次要操作（导入、看文档）用链接样式，避免两个同等分量的按钮让人犹豫。
- **区域命名**：uiarc 传 `label`；shadcn 在 `Empty` 上加 `aria-labelledby` 指向标题。
- **减弱动效**：uiarc empty-state 的文案形变和 empty-states 的插画形变已处理；自己加的入场动画遵守 `prefers-reduced-motion`，且内容默认可见。
- **uiarc 焦点**：装了 `uiarc:arc-foundation` 时，键盘焦点由它统一画描边（文本框靠边框变色，菜单项和选项靠高亮），不用再补，也不要删它的焦点规则或加全局 `!important` 覆盖；旧版的全局 `outline: none !important` 已经移除。接入后用键盘走一遍；只借单个组件、不装 foundation 时要自己补。细节和核对版本见 `sources/uiarc.md`「焦点」。
- **不要和骨架屏混用**：数据还在请求时显示骨架，请求成功且为空才显示空状态；不要先闪一下空状态再出数据。

## 候选清单
- `shadcn:empty` — shadcn 空状态，需补标题语义
- `uiarc:empty-state` — uiarc 空状态，带标题和操作
- `uiarc:empty-states` — 插画空状态，抽单个场景用
- `shadcn:empty-avatar-group` — 邀请成员型空状态示例
- `librariesdev:bot-avatars` — AI 产品的小吉祥物
- `jakubantalik:transition:page-side-by-side` — 向导页切换过渡
- `reactbits:fuzzy-text` — 404 标题文字效果，需补可访问性
- `bencho:eye-tracker` — 趣味空状态，仅 Experience
- `originkit:pixel-run-game` / `originkit:flap` — 需登录，404 小游戏
- `collectui:category:empty-states` / `collectui:category:onboarding` — 仅参考
- `designspells:274-interactive-empty-state-graphics-in-basedash` — 仅参考：可交互空状态插图
