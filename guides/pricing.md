# 定价（pricing）

## 什么时候需要
让人比较套餐、看懂差异、选一个并付款：营销站的定价页（Persuade），产品内的升级、选套餐、结算步骤（Operate）。不需要的情况：只有一个价格时，一行价格 + 一句包含什么 + 一个按钮就够，不要为了"像定价页"硬拆出三档卡片。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | 组合：`shadcn:card`（每档一张）+ `shadcn:toggle-group` 或 `shadcn:tabs`（月付 / 年付）+ `shadcn:badge`（推荐档）+ `shadcn:table`（功能对比） | 索引里 shadcn 没有定价 block。已拉源码：card、toggle-group、badge、table 都只依赖 `cn`，Base UI 实现；用基础件组合比引入第二个设计语言的定价区块更稳 |
| uiarc | `uiarc:billing-toggle` + `uiarc:plan-comparison`；产品内选套餐用 `uiarc:radio-cards` | 已拉源码：billing-toggle 是 `role="radiogroup"` + `role="radio"`、`aria-checked`，节省徽章写在选项文字里一起被读出，旧价格用 `<del>`；plan-comparison 用 table / row / columnheader 角色，价格区 `aria-live` + `aria-atomic`，选中结果走 `role="status"`。都有减弱动效分支，没有写死颜色 |
| 没有底座或其他 | 上面任一底座的组合（shadcn 的 card + toggle-group + badge + table，或 uiarc 的 billing-toggle + plan-comparison） | 现在就能免费取码。登录后可换：`originkit:pricing-03`，含月付年付切换、多档套餐和 enterprise 档；取码要用户自己 `originkit login` 后执行 `npx originkit add pricing-03`，agent 不登录；**未看到源码，质量未验证**。`originkit:pricing-01`、`originkit:pricing-02` 同理 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 产品内升级、结算流程里选套餐 | `uiarc:radio-cards` / shadcn 用 `shadcn:radio-group` 做成卡片样式 | uiarc 版：方向键行为、不可用选项有 `aria-disabled` 和原因说明，选中靠圆环 + 实心点，不只靠颜色 |
| 两档套餐的逐项差异 | `uiarc:plan-comparison` | 有"只看差异"开关；但源码把套餐类型写死成 `"team" | "studio"` 两档，三档以上要改类型和数据结构 |
| 和竞品比功能 | `uiarc:comparison-table` | 见 table 指南 |
| 按座位数、用量计价 | 自己用 slider + 数字输入组合 | `uiarc:usage-pricing`、`uiarc:pricing-calculator` 是 Pro，不推荐 |
| 价格随周期切换时要有变化感 | `uiarc:billing-toggle` 自带的 `BillingPrice` | 数字滚动来自 `AnimatedCounter`，减弱动效下直接替换 |

## 慎用
- 推荐档加发光边框、渐变描边、脉冲徽章（⚠ glow / pulse-dot）：参考类 `jakubantalik:work:tx-result-cards` 就是彩色光晕。定价卡是要被仔细比较的内容，推荐档用"推荐"徽章 + 实色边框或略深的背景就够，不要让光效降低价格和条目文字的对比度。
- 虚假紧迫感：倒计时、"仅剩 3 个名额"、划掉一个从未存在的原价。这属于第 1 级的状态虚假，不是审美问题。
- 年付价格只显示"每月折算价"而不写年付总额：读者会误解实际扣款。
- `uiarc:plan-comparison` 直接上线：内置 Team / Studio 的演示功能清单和价格，要换成真实数据。
- `originkit:pricing-*`：需要登录，且 originkit 的 `styling`、`dark_mode` 在 `_styles.md` 里是 unknown，进 shadcn 或 uiarc 底座后可能需要较多改写；先用免费组合，确有需要再让用户自己取码。

## 页面模式约束
- Persuade（定价页）：允许整页有一处主导效果，但**不放在定价卡区域**；价格、包含项、按钮这一屏保持克制，密度 3–5。各档卡片可以等大（这是同类条目的比较，不是用卡片堆页面结构），推荐档靠内容和徽章区分。
- Operate（产品内选套餐、结算）：用 radio cards 或表格，装饰动效为 0，选中状态 150 ms 左右。
- Read：帮助文档里的价格说明用表格，不做卡片。
- Experience：不涉及。

## 接入要点
- **OriginKit 进 shadcn 项目**：`npx originkit init` 会生成自己的 `components.json`，可能覆盖 shadcn 的配置。先用 `npx originkit add <name> --dry-run` 看它要写哪些文件，不要直接 init。有些条目注明搬自公开的 GitHub 仓库，不要自行改从上游取码，先核实上游许可证，交给用户决定。
- **价格读法**：货币符号、金额、周期写在同一个可读的文本里（"¥99 / 月，按年付费"），不要拆成多个视觉碎片让读屏念成"九十九 斜杠 月"。划掉的原价用 `<del>`，并配文字"原价"。
- **切换后播报**：月付 / 年付切换后价格变化要被读到；uiarc 已用 `aria-live`，shadcn 组合时在价格区加 `aria-live="polite"`。
- **数字**：价格用 `tabular-nums`，切换时宽度不跳。
- **对比表**：功能对比用真正的 `<table>`，"包含 / 不包含"用图标 + 文字（或 sr-only 文字），不只靠勾和叉的颜色。
- **移动端**：三档卡片在窄屏纵向排列时把推荐档放第一；功能对比表在窄屏改成按套餐分组的列表，或第一列 sticky 横向滚动。
- **uiarc 焦点**：装了 `uiarc:arc-foundation` 时，键盘焦点由它统一画描边（文本框靠边框变色，菜单项和选项靠高亮），不用再补，也不要删它的焦点规则或加全局 `!important` 覆盖；旧版的全局 `outline: none !important` 已经移除。接入后用键盘走一遍；只借单个组件、不装 foundation 时要自己补。细节和核对版本见 `sources/uiarc.md`「焦点」。
- **按钮文案**：每档按钮写清动作（"开始 14 天试用"、"联系销售"），不要三个都叫"选择"。

## 候选清单
- `shadcn:card` + `shadcn:toggle-group` + `shadcn:badge` + `shadcn:table` — shadcn 底座的组合方案
- `uiarc:billing-toggle` — 月付 / 年付切换 + 滚动价格
- `uiarc:plan-comparison` — 两档套餐对比，需改成真实数据
- `uiarc:radio-cards` — 产品内选套餐
- `uiarc:comparison-table` — 竞品对比
- `originkit:pricing-03` — 需登录，含切换和 enterprise 档，未验证
- `originkit:pricing-01` / `originkit:pricing-02` — 需登录，未验证
- `uiarc:usage-pricing` / `uiarc:pricing-calculator` — Pro，不推荐
- `collectui:category:pricing` — 仅参考：定价页版式
- `jakubantalik:work:tx-result-cards` — 仅参考，带光晕，不照搬
