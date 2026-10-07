---
id: jakubantalik
name: Jakub Antalik（个人站）
url: https://jakubantalik.com
kind: portfolio
stack: 个人站为纯 HTML/CSS/JS（GitHub Pages）；其产品 Transitions.dev 为纯 CSS（附 React 版）；Libraries.dev 为 React 18+ 组件（WebGL/SVG，img-fx 依赖 three）
license: 个人站源码未声明；Transitions.dev 过渡与 skill 为自定义许可（可免费商用、可修改，禁止作为竞品库再分发），其 CLI/agent/refine 工具 MIT；Libraries.dev 七个 npm 包 MIT
pro: partial（Transitions.dev 43 个过渡中 11 个 Pro，$9/月起；Libraries.dev 的 Studio、Pro 预设和 Pro skill 付费，$9/月起，七个库本身免费）
fetch: github-raw
verified: 2026-10-07
source_status: active
visual_style: refined product-design micro-transitions
foundation: none
styling: css-only
motion_lib: css
dark_mode: none
mixing_notes: Transitions.dev 的 :root 动效变量（--duration-fast 250ms、--ease-in-out）与 uiarc foundation 同名不同值，同页时只用组件级变量（如 --resize-dur）或改前缀
---
## 是什么 / 什么时候用
Jakub Antalik 是产品设计师兼工程师（曾任 0x.org 设计负责人，先后在 Frame.io、Intercom 工作），个人站本身只有简介、两个项目卡和一组 "Selected work" 动效视频，没有 sitemap、llms.txt 和文章。真正能复用的是他的两个开源项目：**Transitions.dev**（43 个精调 CSS 过渡、一个 agent skill 和动效 token，适合给下拉、模态、toast、tabs、开关、AI 思考态等加"成熟"的过渡）和 **Libraries.dev**（7 个 React 特效包：光束边框、思考光球、机器人头像、液态 gooey、语音辉光、液态金属、AI 生图加载）。做 AI 产品界面（思考/流式/生图）或想把动效时长和缓动统一成 token 时优先看这里。Selected work 里的 Web3 钱包、交易状态和 toast 交互没有源码，只能看视频复刻。

## 按需获取方法
### A. Transitions.dev（GitHub: Jakubantalik/transitions.dev）
- 全量清单（机器可读，43 项，免费项带 `css` 和 `react` 源码字段，Pro 项源码为空）：
  `curl -s https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/scripts/transitions-data.json | jq -r '.[] | [.slug,.name,.sub,(.pro|tostring)]|@tsv'`
- 免费清单（CLI 用的 slug）：`https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free-manifest.json`
- 单个免费过渡的说明文档（含 HTML hooks、可调变量、`:root` token、CSS、reduced-motion）：`https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/{cli-slug}.md`
  注意 CLI slug 与站点 slug 有 8 处不同：modal-open-close→modal、input-clear-with-dissolve→input-clear-dissolve、skeleton-loader-and-reveal→skeleton-reveal、tooltip-open-close→tooltip、3d-tilt→card-tilt、dropdown-menu-morph→plus-menu-morph、toast-open-close→toast、matrix-dot-loader→matrix-loader（tsv 的 fetch 列已换算好）。
- 直接拿 CSS 或 React：`jq -r '.[] | select(.slug=="{slug}") | .css' transitions-data.json`（或 `.react`，自注入样式的单文件组件）
- CLI：`npx transitions-dev add {cli-slug}` / `npx transitions-dev add --free` / `npx transitions-dev list`（Pro 需要 `npx transitions-dev login`，即浏览器设备码登录）
- Skill：`npx skills add Jakubantalik/transitions.dev`（安装 `skills/transitions-dev/`：SKILL.md、32 个参考文件、`_root.css`）；动效打磨用 `skills/transitions-polish/SKILL.md`
- 演示页：`https://transitions.dev/transitions/{slug}/`；动效时长、缩放和位移的正反例文章见 `https://transitions.dev/article.html`

实测（card-resize）：`curl -s https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/card-resize.md` 返回 200。内容是：给元素加 `.t-resize` 类，token 为 `--resize-dur: 300ms; --resize-ease: cubic-bezier(0.22, 1, 0.36, 1)`，并带 `prefers-reduced-motion` 守卫。在 transitions-data.json 里，card-resize 的 `css` 有 576 字节，`react` 是自注入样式的组件。

### B. Libraries.dev（GitHub: Jakubantalik/Libraries.dev，monorepo `packages/*`）
- 安装：`npm i {pkg}`。可用的 pkg：border-beam、thinking-orbs、bot-avatars、liquid-gooey、voice-glow、metal-fx、img-fx（img-fx 还要装 `three`）
- 文档（props 全表）：`https://raw.githubusercontent.com/Jakubantalik/Libraries.dev/HEAD/packages/{pkg}/README.md`
- 源码：`https://github.com/Jakubantalik/Libraries.dev/tree/main/packages/{pkg}/src`
- 在线调参：`https://libraries.dev/{beam|orbs|avatars|gooey|voice|metal|image}`。旧子域 beam/orbs/gooey/metal/image.jakubantalik.com 仍返回 200
- 用法示例：`import { BorderBeam } from "border-beam"; <BorderBeam size="md" colorVariant="ocean"><button>Get started</button></BorderBeam>`
- 实测：npm registry 返回的最新版本为 border-beam 1.4.1、thinking-orbs 0.3.2、bot-avatars 0.2.2、liquid-gooey 0.2.2、voice-glow 0.3.0、metal-fx 2.0.11、img-fx 0.5.1，许可都是 MIT

### C. 个人站本身（GitHub: Jakubantalik/Jakubantalik.github.io）
- 源码是纯静态的：`index.html`、`styles.css`、`script.js`（约 115KB）、`lqip.js`，raw 地址为 `https://raw.githubusercontent.com/Jakubantalik/Jakubantalik.github.io/HEAD/{file}`
- 作品视频地址：`https://jakubantalik.com/videos/{file}`（文件名见清单）。这些视频没有标题、说明或源码，清单里的交互描述是本次逐个抽帧看过后写的

### 开发 agent 怎么借鉴
1. 需要基础过渡（下拉、模态、toast、tabs、开关、手风琴、tooltip）时，直接用 transitions-data.json 里的 CSS，并把 `_root.css` 的 token 当作全站动效刻度。经验值：开 250ms、关 150ms，缓动 `cubic-bezier(0.22,1,0.36,1)`，缩放从 0.97 起而不是 0.9。
2. 做 AI 界面时：思考态用 thinking-orbs 或免费过渡 thinking-states / reasoning-stream / streaming-text / matrix-dot-loader，生图占位用 img-fx，语音输入用 voice-glow，"正在安装/生成"按钮用 border-beam。
3. 复刻 Selected work 的交易状态流时，模式是：一张卡片在几个状态间切换（处理中 → 成功或失败），配合图标交叉模糊、步骤圈描绘对勾，成功时卡片顶部出现柔和的彩色径向光晕，toast 的宽高跟着内容 morph。可以组合 success-check、text-states-swap、banner-stacking、toast-open-close 来实现。
4. 个人站的定制面板、雨滴覆盖层、HSV 取色器和手绘滤镜都是原生 JS，可以按需摘抄（仓库未声明许可，仅作参考，不要整段照搬）。

## 使用注意
- Transitions.dev 是纯 CSS，类名带 `t-*` 前缀，变量是语义化 token。多个过渡共用一个 `:root` 块，粘贴前先查重名变量。React 版会在首次 import 时往 document 注入 `<style>`（SSR 安全）。
- 许可方面：过渡和 skill 可以商用、可以修改，但不得重新打包成竞品过渡库；Pro 过渡要登录才能拿源码，不要仿写。
- Libraries.dev 要求 React 18+，多数包只依赖 react/react-dom；img-fx 依赖 three（WebGL），metal-fx 也用 WebGL 着色器，注意移动端性能和 SSR（README 里有 SSR 和性能章节）。
- 主题：Libraries.dev 各包的明暗都由 `theme` 参数决定，`auto` 的解析不一致：thinking-orbs 先看祖先元素的 `data-theme` 或 `.dark`，再看 `prefers-color-scheme`；border-beam 默认 `theme="dark"`，`auto` 只看系统设置。站点自己切换明暗时，显式传 `theme`。详见 librariesdev.md。
- `npx transitions-refine live` 会往运行中的应用注入 script 并启动本地 relay，`npx transitions-agent fix` 需要注册账号。两者都会改项目，用之前先征得用户同意。
- 个人站的 Selected work 只是展示，与 0x、Frame.io 等公司产品相关的设计稿不能当作素材直接使用，只借鉴交互思路。

## 组件清单
| id | 名称 | 分类 | 一句话用途 | 获取（具体命令或URL） | 备注 |
|---|---|---|---|---|---|
| transitions-dev-skill | Transitions.dev skill | Transitions | transitions.dev 的 agent skill 32 个免费 CSS 过渡参考+_root.css 动效 token | npx skills add Jakubantalik/transitions.dev |  |
| transitions-polish-skill | Transitions polish skill | Transitions | 动效打磨 skill 按 duration/distance/scale/blur/easing token 审查现有动画 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/skills/transitions-polish/SKILL.md |  |
| transitions-data-json | transitions-data.json | Transitions | 全部 43 个 transition 的机器可读清单 免费项含 CSS 与 React 源码 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/scripts/transitions-data.json |  |
| transition:card-resize | Card resize | Transitions | 卡片宽高尺寸变化平滑过渡 纯 CSS | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/card-resize.md |  |
| transition:number-pop-in | Number pop-in | Transitions | 数字翻转弹入 带模糊与错峰 stagger | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/number-pop-in.md |  |
| transition:notification-badge | Notification badge | Transitions | 通知徽章斜向滑入+弹簧 pop | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/notification-badge.md |  |
| transition:text-states-swap | Text states swap | Transitions | 状态文字切换 模糊淡入淡出 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/text-states-swap.md |  |
| transition:confetti-burst | Confetti burst | Transitions | 物理彩纸从按钮爆开并落回按钮 庆祝动效（Pro） | https://transitions.dev/transitions/confetti-burst/ | pro |
| transition:menu-dropdown | Menu dropdown | Transitions | 下拉菜单按触发点原点展开/收起 origin-aware | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/menu-dropdown.md |  |
| transition:modal-open-close | Modal open/close | Transitions | 模态框缩放开合 开慢关快 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/modal.md |  |
| transition:panel-reveal | Panel reveal | Transitions | 面板/抽屉展开收起过渡 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/panel-reveal.md |  |
| transition:gooey-plus-menu | Gooey plus menu | Transitions | 加号按钮液态分裂成扇形操作 gooey 菜单（Pro） | https://transitions.dev/transitions/gooey-plus-menu/ | pro |
| transition:page-side-by-side | Page side-by-side | Transitions | 页面前进/后退横向滑动切换 wizard | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/page-side-by-side.md |  |
| transition:card-stack-hover | Card stack hover | Transitions | 卡片堆悬停时弹簧扇形展开（Pro） | https://transitions.dev/transitions/card-stack-hover/ | pro |
| transition:icon-swap | Icon swap | Transitions | 图标切换 缩放+模糊 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/icon-swap.md |  |
| transition:success-check | Success check | Transitions | 成功对勾 淡入旋转模糊 路径描绘 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/success-check.md |  |
| transition:avatar-group-hover | Avatar group hover | Transitions | 头像组悬停 被悬停项弹起 邻居按距离衰减跟随 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/avatar-group-hover.md |  |
| transition:error-state-shake | Error state shake | Transitions | 输入框校验错误抖动 自动恢复 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/error-state-shake.md |  |
| transition:organic-shimmer | Organic shimmer | Transitions | 波浪形骨架屏流光 边缘辉光（Pro） | https://transitions.dev/transitions/organic-shimmer/ | pro |
| transition:input-clear-with-dissolve | Input clear with dissolve | Transitions | 清空输入时按词消散 dissolve | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/input-clear-dissolve.md |  |
| transition:skeleton-loader-and-reveal | Skeleton loader and reveal | Transitions | 骨架屏脉冲后交叉淡入真实内容 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/skeleton-reveal.md |  |
| transition:texts-reveal | Texts reveal | Transitions | 两行文字错峰上升入场 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/texts-reveal.md |  |
| transition:tabs-sliding | Tabs sliding | Transitions | tabs 胶囊指示器跟随滑动 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/tabs-sliding.md |  |
| transition:drag-drop-with-physics | Drag & drop with physics | Transitions | 带物理倾斜的拖放 放置区 morph 成图片（Pro） | https://transitions.dev/transitions/drag-drop-with-physics/ | pro |
| transition:image-open-tilt | Image open tilt | Transitions | iPadOS 式图片打开 3D 倾斜与弯曲（Pro） | https://transitions.dev/transitions/image-open-tilt/ | pro |
| transition:shimmer-text | Shimmer text | Transitions | 文字遮罩渐变扫光 shimmer | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/shimmer-text.md |  |
| transition:tooltip-open-close | Tooltip open/close | Transitions | tooltip 延迟出现 位移 瞬间消失 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/tooltip.md |  |
| transition:3d-tilt | 3D tilt | Transitions | 卡片 3D 指针倾斜+光泽 glare | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/card-tilt.md |  |
| transition:dropdown-menu-morph | Dropdown menu morph | Transitions | 按钮 morph 成菜单面板 加号菜单 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/plus-menu-morph.md |  |
| transition:accordion | Accordion | Transitions | 手风琴 grid-rows 高度过渡+箭头变形 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/accordion.md |  |
| transition:toast-open-close | Toast open/close | Transitions | toast 上升淡入+模糊+缩放 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/toast.md |  |
| transition:like-button | Like button | Transitions | 点赞心形填充+粒子爆发 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/like-button.md |  |
| transition:learn-more-hover | Learn more hover | Transitions | "了解更多"链接悬停箭头位移展开 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/learn-more-hover.md |  |
| transition:checkbox-check | Checkbox check | Transitions | 复选框对勾描边绘制 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/checkbox-check.md |  |
| transition:spinner-to-check-morph | Spinner to check morph | Transitions | 加载 spinner 弹成对勾成功（Pro） | https://transitions.dev/transitions/spinner-to-check-morph/ | pro |
| transition:spinning-counter | Spinning counter | Transitions | 数字老虎机滚轮式滚动到目标值 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/spinning-counter.md |  |
| transition:toggle | Toggle | Transitions | 开关滑块双弹跳 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/toggle.md |  |
| transition:pro-gradient-text | Pro gradient text | Transitions | 渐变色流动环绕文字 动态渐变字（Pro） | https://transitions.dev/transitions/pro-gradient-text/ | pro |
| transition:delete-with-smoky-dissolve | Delete with smoky dissolve | Transitions | 删除时图片碎裂成烟雾下落（Pro） | https://transitions.dev/transitions/delete-with-smoky-dissolve/ | pro |
| transition:thinking-states | Thinking states | Transitions | AI 思考状态行流光后切换下一条 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/thinking-states.md |  |
| transition:reasoning-stream | Reasoning stream | Transitions | AI 推理过程两行滚动流 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/reasoning-stream.md |  |
| transition:streaming-text | Streaming text | Transitions | 流式文字逐词柔和交叉模糊浮现 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/streaming-text.md |  |
| transition:matrix-dot-loader | Matrix dot loader | Transitions | 16 点矩阵脉冲 loader 四种图案 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/matrix-loader.md |  |
| transition:banner-stacking | Banner stacking | Transitions | 横幅像 toast 一样三层堆叠 | https://raw.githubusercontent.com/Jakubantalik/transitions.dev/HEAD/cli/free/banner-stacking.md |  |
| transition:image-generation-placeholder | Image generation placeholder | Transitions | AI 生图占位 点阵噪声苏醒后显影成图（Pro） | https://transitions.dev/transitions/image-generation-placeholder/ | pro |
| transition:get-pro-button | Get Pro button | Transitions | Get Pro 胶囊按钮边缘渐变辉光（Pro） | https://transitions.dev/transitions/get-pro-button/ | pro |
| transitions-refine | transitions-refine | Tools | 注入时间轴+Refine 面板到运行中的应用 让 agent 按动效 token 调整过渡 | npx transitions-refine live |  |
| transitions-agent | transitions-agent | Tools | 扫描代码库中缺失/卡顿/不一致的过渡 给动效评分 可作 GitHub Action 在 PR 上评分与修复 | npx transitions-agent（扫描；fix 需注册免费账号；源码 https://github.com/Jakubantalik/transitions.dev/tree/main/agent） |  |
| article-motion-examples | Duration, scale & movement examples | Article | 文章 动效时长/缩放/位移的正反例 开合不对称 缩放起点 0.97 等 | https://transitions.dev/article.html |  |
| → librariesdev | Libraries.dev 七个库 | Libraries.dev | 这七个库已在 `sources/librariesdev.md` 中按变体逐条收录，这里不再重复 | `find.sh -s librariesdev` | |
| site:customizer | Site customizer panel | Site craft | 个人站右侧外观定制面板 字体/文字色/圆角滑块/logo 大小/背景样式 手机端 bottom sheet 可下滑关闭 重置时弹跳+交叉模糊 | https://github.com/Jakubantalik/Jakubantalik.github.io/blob/main/script.js |  |
| site:water-mode | Water raindrop overlay | Site craft | 页面雨滴/水珠覆盖层 随指针移动 桌面 28-44 颗 手机 10-15 颗 | https://github.com/Jakubantalik/Jakubantalik.github.io/blob/main/script.js |  |
| site:hsv-color-picker | HSV color picker | Site craft | 原生 canvas HSV 取色器 色相条+饱和度明度面板+hex 输入+预设 触屏支持 | https://github.com/Jakubantalik/Jakubantalik.github.io/blob/main/script.js |  |
| site:backgrounds | Background styles | Site craft | 背景样式 Sunset/Ocean/Forest/Lavender 渐变与 Dots/Grid/Waves/Noise 纹理切换 | https://github.com/Jakubantalik/Jakubantalik.github.io/blob/main/styles.css |  |
| site:sketchy-filter | Sketchy SVG filter | Site craft | feTurbulence+feDisplacementMap 手绘抖动描边滤镜 配 Caveat 手写字体 | https://github.com/Jakubantalik/Jakubantalik.github.io/blob/main/index.html |  |
| site:glyph-hover | Project glyph hover | Site craft | 项目卡图标悬停 立方体蒙版旋转而渐变不动 / 涂鸦路径 pathLength 重绘 | https://github.com/Jakubantalik/Jakubantalik.github.io/blob/main/index.html |  |
| site:live-stats | Live project stats | Site craft | 项目卡实时数字 npm 下载量 api.npmjs.org/downloads/range 与 goatcounter 访问量 | https://github.com/Jakubantalik/Jakubantalik.github.io/blob/main/script.js |  |
| site:work-tabs | Projects / Selected work tabs | Site craft | 两个 tab 切换舞台 视频瀑布按行发牌到多列 自动播放循环视频 LQIP 占位 | https://github.com/Jakubantalik/Jakubantalik.github.io |  |
| work:gooey-effect | Liquid gooey demo | Selected work | 液态 gooey 演示 文件/图片/文件夹图标从关闭按钮液态分裂 Share 胶囊头像 邮箱输入框与箭头按钮融合 滑块 → 用 liquid-gooey 复刻 | https://jakubantalik.com/videos/light/gooey-effect.mp4 | 浏览/复刻 |
| work:deposit-steps | Deposit progress modal | Selected work | 存款弹窗两步进度 步骤圈加载→对勾 状态文案切换 成功时绿色径向光晕 Fill status Processing→Success | https://jakubantalik.com/videos/light/tw.mp4 | 浏览/复刻 |
| work:qr-chain-select | Crypto deposit chain select | Selected work | 加密货币充值 选择 token 与链 下拉列表勾选 二维码随链切换动画 复制地址 | https://jakubantalik.com/videos/light/qr-code-animation.mov | 浏览/复刻 |
| work:connect-wallet | Connect wallet modal | Selected work | 连接钱包弹窗 点阵光环中心图标 转圈等待→连接成功绿色光晕扩散 | https://jakubantalik.com/videos/main%20connect%20wallet_7.mp4 | 浏览/复刻 |
| work:swap-pending | Swap order to pending | Selected work | 0x 风格兑换表单 Review order 后卡片 morph 成倒计时圆环 Transaction pending | https://jakubantalik.com/videos/main_1.mp4 | 浏览/复刻 |
| work:frameio-ipad | Frame.io iPad | Selected work | Frame.io iPad 应用 登录→项目网格 深色主题 Dribbble shot | https://jakubantalik.com/videos/dribbble-shot-ipad-1-1600-comp.mp4 | 浏览/复刻 |
| work:thinking-orbs-phone | Thinking orbs on phone | Selected work | 手机实拍 点阵 orb Connecting 然后缩成灵动岛式 Thinking 胶囊 → thinking-orbs | https://jakubantalik.com/videos/light/thinking-orbs.mp4 | 浏览/复刻 |
| work:transitions-showcase | Transitions.dev showcase | Selected work | transitions.dev 展示 头像组 点赞计数 tabs 下拉 分享菜单 Publish→对勾 等组合演示 | https://jakubantalik.com/videos/light/trasnsitions-update-2.mp4 | 浏览/复刻 |
| work:notification-states | Notification states | Selected work | 存款通知卡三态 失败→处理中→完成 图标角标切换 卡片堆叠缩小 | https://jakubantalik.com/videos/light/notification-states-3.mp4 | 浏览/复刻 |
| work:install-button | Installing button beam | Selected work | 深色 Installing 胶囊按钮 边框紫蓝光束流动 → border-beam | https://jakubantalik.com/videos/install-button-3.mp4 | 浏览/复刻 |
| work:ide-navigation | IDE sidebar navigation | Selected work | easemate IDE 侧边栏 图标导航切换 Search/Extensions/Explorer 面板内容过渡 | https://jakubantalik.com/videos/navigation-large.mp4 | 浏览/复刻 |
| work:tx-toast | Transaction toast | Selected work | 交易 toast pending 流光→成功 对勾+Trade detail 按钮 宽高 morph | https://jakubantalik.com/videos/light/toast.mp4 | 浏览/复刻 |
| work:wallet-menus | 0x wallet menus (image) | Selected work | 0x 钱包菜单/交易状态 toast/网络列表/导航菜单 静态稿 | https://jakubantalik.com/videos/GbyPjNuWYAYISl9.jpg | 浏览/复刻 |
| work:tx-result-cards | Transaction result cards (image) | Selected work | 交易结果卡片 成功/待定/失败/高价格影响 顶部柔和彩色光晕 | https://jakubantalik.com/videos/FvSMDQkWwAIBoXH.jpg | 浏览/复刻 |
| work:ide-explorer | IDE explorer (image) | Selected work | 深色 IDE 文件树+代码编辑器 静态稿 | https://jakubantalik.com/videos/GxBEp64W4AAO0LT.jpg | 浏览/复刻 |
| work:swap-widget | Swap widget (image) | Selected work | 兑换组件 Market/Limit 价格图表 成功卡 静态稿 | https://jakubantalik.com/videos/Fw5-LJVXoAUrXLO.jpg | 浏览/复刻 |
| work:dona-onboarding | Dona onboarding (image) | Selected work | Dona 待办应用引导页 彩色渐变卡片 快捷键自定义 列表 | https://jakubantalik.com/videos/FSjF9y6WQAArBX9.jpg | 浏览/复刻 |

## 未解决
- jakubantalik.com 没有 sitemap.xml、llms.txt、robots.txt 和 RSS（都返回 GitHub Pages 的 404），站上没有博客或文章；唯一的文章页在 transitions.dev/article.html。
- Selected work 的 12 个视频和 5 张图片没有标题、说明或源码，清单里的名称和交互描述是本次抽帧观察后写的，可能和作者原意有出入。图片文件名是 X(Twitter) 媒体 ID，原帖链接未找到。
- 11 个 Pro 过渡（confetti-burst、gooey-plus-menu、card-stack-hover、organic-shimmer、drag-drop-with-physics、image-open-tilt、spinner-to-check-morph、pro-gradient-text、delete-with-smoky-dissolve、image-generation-placeholder、get-pro-button）需要登录加订阅，没有获取源码，只列出演示页。
- Libraries.dev 页面上的 "Copy prompt" 在浏览器端生成，带当前调参状态，curl 拿不到。可以用各包的 README（props 全表）代替；Studio 和 Pro 预设需要付费，未获取。
- 个人站源码仓库 Jakubantalik.github.io 没有 LICENSE，默认保留所有权利，只能参考思路。
