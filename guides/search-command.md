# 搜索与命令面板（search-command）

## 什么时候需要
两类需求：一是在页面里搜索/过滤内容（列表、表格、文档）；二是全局命令面板（⌘K / Ctrl+K），跳转页面、执行动作。为表单字段选一个值用 combobox（见 `select.md`），不要用命令面板；只有十几个条目的页面不需要搜索，直接列出来。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | 命令面板 `shadcn:command`（弹窗形态用 `CommandDialog`）；页内搜索框用 `shadcn:input-group` + 搜索图标 addon | Command 基于 cmdk：输入框保持焦点，方向键移动高亮，`CommandEmpty` 空状态、分组、`CommandShortcut` 快捷键提示都有；CommandDialog 套 shadcn Dialog，标题和描述 `sr-only`（2026-10-07 拉取 base-nova 源码确认）。依赖 `cmdk`。⌘K 快捷键要自己在页面里绑（文档示例用 `useEffect` 监听） |
| uiarc | 命令面板 `uiarc:command-palette`；页内搜索 `uiarc:search-field`；顶栏可展开搜索 `uiarc:expanding-search` | command-palette 输入框是 `role="combobox"` + `aria-activedescendant`，结果是分组的 `role="option"`，自带 ⌘K/Ctrl+K 监听；**它是行内渲染，不带弹窗**，要自己放进 `uiarc:dialog` 才能锁焦点、点外部关闭（catalog 原话 + 源码）。search-field 是原生 `type="search"`，清除按钮把焦点还给输入框。**焦点框被 arc-foundation 全局去掉**，必须补 |
| 没有底座或其他 | 原生 `<input type="search">` + `<label>` | 页内过滤够用；命令面板这种复杂组件不要自写，至少用 cmdk |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 表格/列表上方的过滤框 | `shadcn:input-group`（加清除按钮）；uiarc 用 `uiarc:search-field` | 输入即过滤，结果数用 live region 播报（"找到 12 条"） |
| 顶栏空间紧，点图标展开搜索 + 下拉结果 | `uiarc:expanding-search` | 收起时设 `inert`，展开后是完整的 combobox + 分组 listbox，结果数和空状态用 live region 播报（catalog） |
| 命令面板在手机上 | `shadcn:command` 放进 `shadcn:drawer` | 底部抽屉比居中弹窗好按 |
| 搜索结果要显示在页面主体（搜索结果页） | 不要用命令面板；`shadcn:input-group` + 普通列表/`shadcn:item` | 命令面板是临时浮层，结果页需要可分享 URL、分页 |
| FAQ 可搜索 | `uiarc:faq-section` | 自带主题栏和搜索（catalog，未拉源码）；shadcn 用 `shadcn:accordion` + 过滤框自己拼 |
| AI 助手里的"搜索中"状态 | 见 `ai-ux` 任务 | 那是思考过程展示，不是搜索组件 |

## 慎用
- `bencho:command`：索引描述写"cmd+k 搜索"，但源码里**没有任何 ⌘K 监听**；它是"输入框 + 发送按钮"的液态融合动效，依赖 `liquid-gooey`，缓动带 1.3 的回弹（`cubic-bezier(0.22, 1.3, 0.71, 1)`），要映射 16 个 token。更像 AI 输入栏，不是命令面板。只在 Persuade/Experience 的单个输入栏上考虑。
- `bencho:seek`：放大镜展开成输入框，几何思路讲究（只动一个盒子的宽度），但只是一个输入框，没有结果列表和 combobox 语义（只有 `aria-label="Search"`），要映射 12 个 token。需要"展开 + 结果"用 `uiarc:expanding-search`。
- `beautifului:search`：AI 场景的命令式搜索列表，属于 beautifului 那套 token；不当通用搜索用。
- `librariesdev:border-beam-line`：⚠ glow，搜索进行中的线性光束；只在搜索耗时 > 2 秒、而且是页面焦点时用，Operate 页面优先用普通 spinner。
- `obsidianui:command`：Radix 版 shadcn 同构件，不要重复装。
- 用 combobox 实现全局命令面板，或用命令面板实现表单选择：语义和行为都不对，按「什么时候需要」分开。
- Pro 条目（`uiarc:search-results`、`uiarc:settings-command`、`uiarc:team-directory`、`reactbits:category:pro-app-ui/command-menu`）：只当灵感。

## 页面模式约束
- **Operate**：命令面板和过滤框都用主底座。面板出现 150–250ms 淡入 + 轻微缩放，退出更快；结果列表不做逐项入场动画。
- **Persuade**：文档站或产品站的顶栏搜索可以用 expanding-search；不要在首屏放液态/光束搜索框和主导效果抢注意力。
- **Read**：文档搜索用命令面板（⌘K）是惯例，样式保持安静。
- **Experience**：通常不需要搜索；作品很多时用简单的过滤框。

## 接入要点
- **快捷键**：⌘K / Ctrl+K 打开，Esc 关闭，关闭后焦点还给打开前的元素；输入法组合输入时（中文拼音）不要拦截回车（检查 `event.isComposing`，cmdk 是否已处理未验证）。在页面上用 `shadcn:kbd` 显示快捷键提示。
- **结果语义**：命令面板的输入框是 combobox，结果是 listbox/option，焦点一直留在输入框（cmdk 和 uiarc 都这么做）；结果数量变化用 `aria-live="polite"` 播报；空状态给出下一步（"没有结果，试试 …"）。
- **异步搜索**：防抖 150–300ms；加载中在列表顶部显示 spinner，不清空旧结果；请求竞态要丢弃过期响应。
- **shadcn CommandDialog 的标题**：源码把 `DialogHeader`（含 `DialogTitle`）放在 `DialogContent` 外面、Dialog 根里面；Base UI 下读屏是否能读到对话框名称未验证，接入后用读屏实测一遍，读不到就把标题移进 `DialogContent`。
- **uiarc 焦点**：装了 `uiarc:arc-foundation` 时，键盘焦点由它统一画描边（文本框靠边框变色，菜单项和选项靠高亮），不用再补，也不要删它的焦点规则或加全局 `!important` 覆盖；旧版的全局 `outline: none !important` 已经移除。接入后用键盘走一遍；只借单个组件、不装 foundation 时要自己补。细节和核对版本见 `sources/uiarc.md`「焦点」。
  command-palette 的活动结果用共享高亮底色表示（输入框的 `aria-activedescendant` 指向它），不是描边。
- **token**：shadcn 命令面板高亮用 `--accent`（浅色 hover 底），输入框底色 `--input` 的 30% 透明度。
- **减弱动效**：shadcn Dialog 的进出动画见 `select.md` 的说明；uiarc command-palette 有 14 处减弱动效判断（源码计数）。

## 候选清单
- `shadcn:command` — 命令面板（cmdk）
- `shadcn:command-dialog` — 弹窗形态示例
- `shadcn:input-group` — 页内搜索框（图标 + 清除按钮）
- `shadcn:kbd` — 快捷键提示
- `uiarc:command-palette` — uiarc 命令面板，行内渲染，自带 ⌘K（自套 dialog）
- `uiarc:search-field` — uiarc 页内过滤框
- `uiarc:expanding-search` — 顶栏可展开搜索 + 结果
- `uiarc:faq-section` — 可搜索 FAQ，未验证
- `bencho:seek` — 只借展开动效，单纯输入框
- `bencho:command` — AI 输入栏式的液态融合，不是命令面板
- `collectui:category:command-bar` — 仅参考：命令栏样式
- `collectui:category:search` — 仅参考：搜索样式
