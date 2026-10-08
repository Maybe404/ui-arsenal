# 选择器（select）

## 什么时候需要
从一组已知选项里选一个或多个值，并把值存进表单或状态。2–5 个选项而且需要一直看得见时，用单选组或分段控件（见 `toggle-slider.md`）；选项是"要执行的动作"而不是"要保存的值"时，用 dropdown-menu（导航/菜单类）；需要在全站跳转或执行命令时，用 command（见 `search-command.md`）。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:select`（短列表）；`shadcn:combobox`（长列表、可搜索、多选） | 都基于 Base UI，依赖只有 `cn`（combobox 另需 `@base-ui/react`，和底座同一个包）。Select 的弹层默认 `alignItemWithTrigger`，选中项对齐触发器；触发器有 `focus-visible` ring、`aria-invalid`、`data-placeholder` 样式。Combobox 有 `ComboboxChips` 多选、`ComboboxEmpty` 空状态、分组和清除按钮（2026-10-07 拉取 base-nova 源码确认） |
| uiarc | `uiarc:select`（短列表）；`uiarc:combobox`（长列表）；`uiarc:multi-select`（多选） | select 基于 Radix Select，真实值放在隐藏的 Radix Value 里、动画文字 `aria-hidden`；combobox 自己实现了完整的 `role="combobox"` + `aria-activedescendant` + `role="option"`，空状态是 `role="status"`（catalog + 源码）。**select 触发器聚焦只把边框换成 `--border-strong`**，combobox 的焦点 box-shadow 用的是值为 `transparent` 的 `--focus-ring`，都必须补焦点 |
| 没有底座或其他 | `shadcn:native-select` 的写法，或直接原生 `<select>` | 原生 select 的键盘、读屏、移动端滚轮都由系统负责，是最稳的兜底；不要自写 div 下拉框 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 移动端为主、选项是简单文本 | `shadcn:native-select` | 原生 `<select>` 套 shadcn 样式，手机上弹系统选择器，体验好于自定义弹层；不能放图标或多行内容 |
| 国家、时区这类长列表 | `shadcn:combobox`；uiarc 用 `uiarc:combobox` | 输入过滤；uiarc 版支持 keywords 别名搜索（catalog） |
| 多选并在字段里显示已选项 | `shadcn:combobox`（chips 写法）；uiarc 用 `uiarc:multi-select` | uiarc 版选中项超出时显示 +N，读屏读的是汇总而不是一堆 chip（catalog） |
| 筛选条件，选项要一直可见 | `uiarc:chip-group`；shadcn 用 `shadcn:toggle-group`（`type="multiple"`） | chip 是 `aria-pressed` 按钮 + roving tabindex（catalog） |
| 属性面板、工具栏里的紧凑选择 | `uiarc:morph-select` | 触发器像 pill，展开成带搜索的列表，ARIA 完整（catalog，未拉源码） |
| 颜色 | `uiarc:color-picker` | 有格式切换、吸管和对比度提示（catalog，未拉源码） |
| 手机号的国家码 | `uiarc:phone-input` | 见 `form-input.md` |
| 选项弹层需要在手机上变成底部抽屉 | `shadcn:combobox` + `shadcn:drawer`（参考 `shadcn:combobox-responsive`） | 官方示例，桌面 popover、移动 drawer |

## 慎用
- `bencho:magnet-select`：磁吸手感好，但选项来自被清空的图片数组 `MARKS`，不填自己的图片就一个选项都没有（`sources/bencho.md`）；要映射 token；用 framer-motion。只适合 Persuade/Experience 页里"选头像、选样式"这类视觉选择，不进表单。
- `reactbits:glide-select`：ARIA 写得不错（`role="combobox"`、`aria-activedescendant`、`role="listbox"`，Tailwind `motion-reduce:` 分支都有），但依赖 hugeicons（换成项目在用的图标库，项目还没定就用 lucide），颜色全走 hex props（`accentColor`、`surfaceColor` 等），要从主底座变量取值。主底座的 select 能满足时不用它。
- `bencho:picker`、`bencho:roster`、`bencho:aspect`、`bencho:asset-swap`：场景很具体的选择交互（指派人、多选列表、画幅），未拉源码；要用时先 fetch 看键盘和 ARIA，再映射 token。
- `reactbits:option-wheel`、`reactbits:infinite-menu`：滚轮/3D 球面选择，属于展示效果，不进 Operate 表单；infinite-menu 依赖 gl-matrix 和 WebGL。
- `beautifului:entity-chip`、`beautifului:tool-chips`、`beautifului:prompt-bar`：AI 场景件，只在 AI 输入区里用。
- `obsidianui:select`、`obsidianui:dropdown-menu`：Radix 版 shadcn 同构件，不要和 shadcn 版重复装。
- `jakubantalik:transition:menu-dropdown`、`jakubantalik:transition:dropdown-menu-morph`：只是过渡动效（CSS），不是可访问的选择器；可以把动效节奏套到底座组件的弹层上，不替换组件本身。
- 自写 `div` 下拉框：第 1 级风险（键盘、读屏、滚动锁定、碰撞翻转都要自己处理）。
- Pro 条目（`uiarc:team-members`、`originkit:button-carousel` 等）：只当灵感。

## 页面模式约束
- **Operate**：只用主底座的 select / combobox / native-select。弹层动画 100–200ms 的淡入加轻微缩放（shadcn 默认 `duration-100`），不加别的。
- **Persuade**：定价页的套餐选择优先用 radio-cards / 分段控件让选项可见（见 `toggle-slider.md`）；视觉化选择（magnet-select）一页最多一处。
- **Read**：文档里的版本切换、语言切换用 native-select 或 select 即可。
- **Experience**：筛选作品可以用 chip-group，保持安静。

## 接入要点
- **选哪个**：≤ 7 个选项、不需要搜索 → select；> 7 个或用户知道名字 → combobox；要多选 → combobox chips / multi-select；需要一直可见 → chip-group / toggle-group / radio。
- **标签**：触发器必须有可见 label 并关联（shadcn 用 `Field` + `FieldLabel`，uiarc 用 `label` prop）；placeholder 不是 label。
- **表单提交**：Base UI Select 和 Radix Select 都会渲染隐藏的原生 input，给 `name` 就能随表单提交；combobox 要确认 `name` 是否生效（未验证），不生效就受控后自己写隐藏 input。
- **uiarc 焦点**：装了 `uiarc:arc-foundation` 时，键盘焦点由它统一画描边（文本框靠边框变色，菜单项和选项靠高亮），不用再补，也不要删它的焦点规则或加全局 `!important` 覆盖；旧版的全局 `outline: none !important` 已经移除。接入后用键盘走一遍；只借单个组件、不装 foundation 时要自己补。细节和核对版本见 `sources/uiarc.md`「焦点」。
  `uiarc:combobox` 聚焦时边框变成 `--accent`；它自带的 `--focus-ring` 光圈默认透明（foundation 有意如此），想更明显时在 `:root` 把 `--focus-ring` 设成可见色。
- **token**：shadcn 选项高亮用 `--accent`（浅色 hover 底）和 `--accent-foreground`，这是它本来的含义，不要把 `--accent` 改成品牌色，否则选项高亮会变成大色块。
- **减弱动效**：shadcn 弹层用 tw-animate-css 的 `animate-in fade-in zoom-in-95`，tw-animate-css 1.4.0 不处理 `prefers-reduced-motion`（2026-10-08 核对，见 `sources/_claims.tsv`）；在 `SelectContent` 上加 `motion-reduce:animate-none`，或按 `overlay.md` 在全局补一条。uiarc 有 `useReducedMotion` 分支。
- **常见坑**：select 放在 dialog 里时注意 z-index（shadcn 用 `isolate z-50` + Portal）；长列表要设最大高度并能滚动（shadcn 用 `max-h-(--available-height)`）；Base UI 和 Radix 的 API 不同，别照抄旧版 Radix 示例里的 `asChild`。

## 候选清单
- `shadcn:select` — 短列表单选
- `shadcn:combobox` — 可搜索、多选、分组
- `shadcn:native-select` — 原生 select，移动端优先
- `shadcn:combobox-responsive` — 桌面 popover / 移动 drawer 示例
- `uiarc:select` — uiarc 短列表
- `uiarc:combobox` — uiarc 长列表
- `uiarc:multi-select` — uiarc 多选 +N
- `uiarc:chip-group` — 常驻可见的筛选 chip
- `uiarc:morph-select` — 紧凑 pill 式选择
- `uiarc:color-picker` — 取色
- `shadcn:toggle-group` — shadcn 下的多选筛选按钮
- `reactbits:glide-select` — 有手感的单选，颜色走 props
- `bencho:magnet-select` — 视觉化选择，需填图片和映射 token
- `jakubantalik:transition:dropdown-menu-morph` — 只借弹层过渡节奏
- `inspora:1-41` — 仅参考：国家选择器
- `collectui:category:dropdown` — 仅参考：下拉样式
