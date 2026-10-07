# 弹层（overlay）

## 什么时候需要
内容必须暂时盖在页面上：危险操作二次确认、短表单、保持上下文的详情面板、锚定在按钮上的小面板、图标按钮的文字提示、移动端底部面板。**先问能不能行内解决**：新增一行、改名、展开详情、筛选条件，多数可以在原位置编辑或渐进展开（参考 `bencho:find:cj-issue-rows`：添加 issue 时直接插入可编辑行）。能行内解决就不要弹窗。

怎么选：
- 必须回应才能继续、且后果不可逆 → alert dialog
- 一屏能装下的短表单或决定 → dialog
- 长表单、记录详情、筛选，需要看着原页面 → sheet / drawer（侧边）
- 锚定在触发器上的小面板，有可交互内容 → popover
- 图标按钮的一行说明 → tooltip（不能放可交互内容，触屏上看不到）
- 移动端次要任务 → 底部 drawer / bottom sheet

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:dialog`、`shadcn:alert-dialog`、`shadcn:sheet`、`shadcn:popover`、`shadcn:tooltip`、`shadcn:drawer` | 已拉源码（base-nova）：都基于 Base UI，焦点约束和还原由 Base UI 处理；dialog 关闭按钮带 sr-only 文案；只依赖 `cn`（drawer 另需 `@base-ui/react`）。新版 drawer 已改用 Base UI Drawer，支持 `snapPoints`、`swipeDirection`，不再是 Vaul |
| uiarc | `uiarc:dialog`、`uiarc:drawer`、`uiarc:popover`、`uiarc:tooltip`、`uiarc:bottom-sheet` | 已拉源码：dialog、drawer 基于 `@radix-ui/react-dialog`，popover 基于 Radix Popover；都有 `useReducedMotion` 分支，没有写死颜色。catalog 写明 drawer 拖拽关闭"永远不是唯一关闭方式"，bottom-sheet 的档位变化有 live region 播报 |
| 没有底座或其他 | 原生 `<dialog>`（`showModal()`）+ `jakubantalik:transition:modal-open-close` | 已拉文档：纯 CSS，开 250 ms、关 150 ms（开慢关快），`cubic-bezier(0.22,1,0.36,1)`，有减弱动效守卫。它只管过渡，焦点约束、Esc、`aria-labelledby` 交给原生 `<dialog>` |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 设置面板（左侧分区 + 右侧内容） | `shadcn:sidebar-13` | 侧栏放在 dialog 里的 block |
| 移动端优先、需要 peek 和全屏两档 | `uiarc:bottom-sheet` / `shadcn:drawer`（`snapPoints`） | catalog：Tab 进入折叠区内容时 sheet 自动展开，保证焦点元素可见 |
| 悬停预览人物或链接 | `shadcn:hover-card` / `uiarc:hover-card` | 只放只读内容；uiarc 版触屏上点按切换，不依赖悬停 |
| 同一工具栏多个图标提示 | `shadcn:tooltip`；想要"第一次延迟、后续即时"时考虑 `reactbits:warm-tooltip` | warm-tooltip 未拉源码，依赖 motion，未验证 |
| 窄屏 dialog、宽屏 sheet 自适应 | `shadcn:drawer-dialog`（示例） | 官方示例，按断点切换两种容器 |
| 无底座只要弹层过渡 | `jakubantalik:transition:panel-reveal`、`jakubantalik:transition:tooltip-open-close` | 同一套 Transitions.dev 变量，tooltip 版"延迟出现、瞬间消失" |

## 慎用
- 用 dialog 承载本可行内完成的操作（改名、加一行、切换一个开关）：impeccable 明确列为反模式。
- `shadcn:hover-card` / `uiarc:hover-card`：放必须看到的信息时不可用，触屏没有悬停；uiarc catalog 也写明焦点不会进入卡片，里面不能放按钮。
- 嵌套弹层（dialog 里再开 dialog、popover 里开 dialog）：焦点还原链路容易断，先考虑在同一 dialog 里切换步骤。
- `jakubantalik:transition:*` 系列：只有动画，没有焦点管理和语义；必须配原生 `<dialog>` 或主底座的弹层。和 uiarc 同页时不要粘 `_root.css` 公共块（`_styles.md`：`--duration-fast` 同名不同值）。
- `obsidianui:dialog` / `obsidianui:sheet` 等：与 shadcn 同构但是 Radix 版，已用新版 shadcn（Base UI）时会出现 `asChild` / `render` 两种写法混用，直接用 shadcn 本体。
- 参考类条目 `bencho:find:kylethacker-view-picker`（⚠ glass）：毛玻璃弹层只借鉴结构，Operate 页面不用装饰性毛玻璃。

## 页面模式约束
- Operate：弹层只做开合状态动效，时长 100–300 ms（shadcn dialog 是 100 ms 淡入 + 95% 缩放，合适）；遮罩不要做重模糊。
- Persuade：可以用 dialog 承载视频或表单，但首屏不要自动弹窗（订阅弹窗、cookie 以外的拦截）。
- Read：基本只用 tooltip、popover（脚注、术语解释）。
- Experience：作品大图查看可以用全屏 dialog，退出路径（Esc、关闭按钮）必须明显。

## 接入要点
- **减弱动效（shadcn）**：dialog、popover 的进出场靠 tw-animate-css 的 `animate-in/out`，sheet 靠 CSS transition；tw-animate-css 1.4.0 源码里没有任何 `prefers-reduced-motion` 规则（已核对）。在全局加一条，或给 Content 加 `motion-reduce:animate-none motion-reduce:transition-none`：
  ```css
  @media (prefers-reduced-motion: reduce) {
    [data-slot$="-content"], [data-slot$="-overlay"], [data-slot$="-popup"] {
      animation: none !important; transition: none !important;
    }
  }
  ```
  已核对的 slot 名：`dialog-content/overlay`、`alert-dialog-content/overlay`、`sheet-content/overlay`、`popover-content`、`drawer-content/overlay/popup`。
- **遮罩**：shadcn dialog 遮罩是 `bg-black/10` + `backdrop-blur-xs`，属于轻度毛玻璃；Operate 页面可以去掉 blur，只留半透明遮罩。
- **标题必填**：dialog、sheet、drawer 都要有 Title（可 sr-only）和 Description，否则读屏只念出 "dialog"。
- **uiarc 焦点**：arc-foundation 全局去掉了焦点框，弹层里的按钮和输入框会看不到焦点。补回：
  ```css
  html body :focus-visible { outline: 2px solid var(--accent) !important; outline-offset: 2px !important; }
  ```
- **关闭方式**：Esc、关闭按钮、点遮罩三条都要有；危险确认（alert dialog）不允许点遮罩关闭，默认焦点放在"取消"上。
- **移动端**：dialog 宽度 `max-w-[calc(100%-2rem)]` 已处理；长内容改用 drawer，避免 dialog 内部滚动套页面滚动。
- **层级**：toast 要在 dialog 之上，否则确认后的结果提示被遮住。

## 候选清单
- `shadcn:dialog` — 短表单、需要聚焦的决定
- `shadcn:alert-dialog` — 不可逆操作的二次确认
- `shadcn:sheet` — 侧边详情、筛选、长表单
- `shadcn:popover` — 锚定的小面板
- `shadcn:tooltip` — 图标按钮说明
- `shadcn:drawer` — 移动端底部面板，Base UI Drawer，支持档位
- `uiarc:dialog` / `uiarc:drawer` / `uiarc:popover` / `uiarc:tooltip` — uiarc 底座的对应件
- `uiarc:bottom-sheet` — 移动端 peek / 全屏两档
- `jakubantalik:transition:modal-open-close` — 无底座时配原生 `<dialog>` 的过渡
- `shadcn:sidebar-13` — 设置类 dialog
- `shadcn:drawer-dialog` — 窄屏 drawer、宽屏 dialog 的示例
- `shadcn:hover-card` / `uiarc:hover-card` — 只读预览
- `jakubantalik:transition:panel-reveal` / `jakubantalik:transition:tooltip-open-close` — 无底座过渡补充
- `reactbits:warm-tooltip` — tooltip 组共享延迟，未验证
- `bencho:find:cj-issue-rows` — 仅参考：用行内编辑代替弹窗
