---
id: bencho
name: Bencho
url: https://bencho.dev/
kind: blocks
stack: React + TypeScript + 纯 CSS（多数用 framer-motion，部分 lucide-react / liquid-gooey）
license: MIT（blocks 代码；站点内图片、Bencho 商标不在授权内）
pro: none
fetch: page-copy
verified: 2026-10-07
---
## 是什么 / 什么时候用
Bencho 是 Lorenzo Cabra 做的 React 微交互 blocks 库：48 个公开 block（另有 15 个未上架的 parked block 源码也在 bundle 里），每个都是可调参数的真组件，偏"手感"——弹簧、磁吸、液态 metaball、物理、刻度旋钮、拖拽手势。
适合：需要一个有质感的单点交互（磁吸选择、滑动确认、OTP 输入、灵动岛、Dock、点赞、签名板、下拉刷新、液态开关等）而不想自己调弹簧参数时。不适合：要成套表单/布局/设计系统组件（去 shadcn）、要整页 section。
站点另有 Finds（约 152 条他人作品的灵感视频，无源码）和 Sounds（82 个合成 UI 音效，可下载 WAV）。全站免费，无 Pro。

## 按需获取方法

官方途径：打开 `https://bencho.dev/blocks/{name}` → 右侧 Code 面板有 Install / Usage / tsx / css 四块，可逐块复制；顶部 **Copy prompt** 会把"给 agent 的集成说明 + 完整 tsx + css"拼成一段提示词写进剪贴板（需要浏览器渲染，curl 拿不到按钮结果）。

机器可读途径（实测可用，无需登录）：
1. 全部公开 block 清单：`curl -s https://bencho.dev/llms.txt`（48 条，含名称、SEO 名和描述）；或 `https://bencho.dev/sitemap.xml` 里的 `/blocks/*`。
2. 源码：站点是 Vite SPA，所有 block 的源码以字符串形式打包在一个懒加载 chunk `/assets/blocks-<hash>.js` 中，导出 `BLOCKS` 对象：`BLOCKS[id] = { name, props, tsx, css, tokens, deps, stubs }`。chunk 文件名带 hash，需先从首页的 `index-<hash>.js` 里找。

   取码用 `scripts/adapters/bencho.py`：只把 chunk 当文本下载，用纯字面量解析器读出 `BLOCKS`，**不执行站点的任何 JS**；遇到函数、变量引用或 `${...}` 插值会直接报错退出。输出和站点 Copy prompt 的内容一致（2026-10-07 与旧的 node 执行方式逐字节对比一致）。

```sh
scripts/fetch.sh bencho:{name}                        # 推荐：tsx + css + 依赖 + 需映射的 CSS 变量 + 占位资源
python3 scripts/adapters/bencho.py {name} tsx         # 只要 tsx
python3 scripts/adapters/bencho.py {name} css         # 只要 css
python3 scripts/adapters/bencho.py {name} meta        # 导出名、deps、tokens、stubs、props
```
依赖安装：按 meta 里的 `deps` 执行 `npm i <deps>`（全集只有 `framer-motion`、`lucide-react`、`liquid-gooey` 三个）；deps 为空的只需 React。

实测（2026-10-07）：`bencho.py magnet-select meta` → 导出名 `MagneticSelect`，deps `framer-motion`，tokens `--card --fill-slab --font-ui --ink --ink-rgb --pane-edge`，stubs `MARKS`；tsx 为 `export function MagneticSelect({ size, pull, bounce, give })`，css 142 行。parked 的 `tag-input` 同样可取。

## 使用注意
- 每个 block = 一个 `.tsx`（命名导出，名字见 meta.name）+ 一段全局 CSS（类名带 block 前缀，如 `.mag-*`、`.slp-*`）。CSS 要加到全局样式表，不是 CSS Module，也不是 Tailwind。
- CSS 读取站点的设计 token（`--ink`、`--ink-rgb`、`--card`、`--font-ui`、`--fill-on` 等），不定义就会显示异常；必须映射到自己项目的主题变量（meta.tokens 列出了具体哪些）。
- `stubs` 是被清空的图片数组（如 `MARKS`、`AVATARS`、`COVER`、`SHOTS`、`SHEEP`），因为站点图片不随 MIT 授权；不填的话部分组件渲染为空。例如 magnet-select 的选项数是 `min(size, MARKS.length)`，MARKS 为空就一个选项都没有，必须填入自己的图片 URL。
- 用的是 `framer-motion`（不是 `motion` 包）；与项目里已有的 `motion/react` 可共存但别混用两套。`liquid-gooey` 是第三方 SVG metaball 库（npm 0.2.x），用于 liq-*、command、roster、sleep、drag-ball。
- 源码注释很长（解释每个数值为什么这么设），官方 prompt 要求保留注释。
- chunk 文件名会随部署变化，不要硬编码 hash，adapter 会动态找。站点如果改成非字面量的打包方式，adapter 会报错而不是执行代码，这时更新解析器。
- parked block 没有公开页面，属于未发布/实验品，质量和稳定性无保证。

## 组件清单
| id | 名称 | 分类 | 一句话用途 | 获取（具体命令或URL） | 备注 |
|---|---|---|---|---|---|
| asset-swap | Asset swap | Press | 加密货币兑换 swap 卡片，点箭头翻转买卖方向，点币种弹出 coin picker 选择器，DeFi/钱包 UI | `fetch.sh bencho:asset-swap` / https://bencho.dev/blocks/asset-swap | deps: framer-motion lucide-react |
| heat-word | Heat map | Hover | 灰点阵 hover 热力图效果，光标附近的点膨胀融合，按下切换形状/文字，四套配色，Canvas 背景装饰 | `fetch.sh bencho:heat-word` / https://bencho.dev/blocks/heat-word | deps: 仅 React |
| image-compare | Image compare | Drag | 前后对比图片滑块 before/after，拖动分割线透视两张图，甩动后惯性滑到边缘 | `fetch.sh bencho:image-compare` / https://bencho.dev/blocks/image-compare | deps: 仅 React |
| like | Like | Press | 点赞按钮动画，心形弹出并迸发粒子环，计数像里程表 odometer 滚动进位 | `fetch.sh bencho:like` / https://bencho.dev/blocks/like | deps: framer-motion lucide-react |
| signature | Signature pad | Drag | 手写签名板 signature pad，笔速越快墨迹越细，停顿提示 Signed，Clear 按笔画倒放清除 | `fetch.sh bencho:signature` / https://bencho.dev/blocks/signature | deps: lucide-react |
| voice-note | Voice note | Press | 按住录音的语音消息 voice note，实时波形，左滑丢弃，松手得到可拖动进度的播放条 | `fetch.sh bencho:voice-note` / https://bencho.dev/blocks/voice-note | deps: lucide-react |
| eye-tracker | Eye tracker | Hover | 跟随光标转动的眼睛 eyes follow cursor，软立方体上两只眼睛带透视倾斜，趣味吉祥物/空状态 | `fetch.sh bencho:eye-tracker` / https://bencho.dev/blocks/eye-tracker | deps: 仅 React |
| dynamic-island | Dynamic island | Press | iOS 灵动岛 Dynamic Island 胶囊，点击用同一弹簧展开为计时器/来电/音乐实时活动，再收回 | `fetch.sh bencho:dynamic-island` / https://bencho.dev/blocks/dynamic-island | deps: framer-motion lucide-react；占位: COVER AVATARS |
| time-scrubber | Time scrubber | Slide | 时间选择刻度尺 time picker scrubber，拖动刻度数字滚动，甩动惯性滑行并吸附到步长 | `fetch.sh bencho:time-scrubber` / https://bencho.dev/blocks/time-scrubber | deps: 仅 React |
| upload-dropzone | Upload dropzone | Drag | 拖拽上传 drag and drop file upload，文件被吸入后显示进度条和勾，超大文件被拒绝并抖动 | `fetch.sh bencho:upload-dropzone` / https://bencho.dev/blocks/upload-dropzone | deps: framer-motion lucide-react |
| particles | Particles | Hover | 交互粒子 particles 形状，点阵被指针推散后弹回，按下产生冲击波并聚合成下一个形状，hero 装饰 | `fetch.sh bencho:particles` / https://bencho.dev/blocks/particles | deps: 仅 React |
| label-input | Label input | Type | 浮动标签输入框 floating label input，聚焦时 placeholder 上浮到描边缺口，字母小跳动画 | `fetch.sh bencho:label-input` / https://bencho.dev/blocks/label-input | deps: lucide-react |
| one-time-code | One-time code | Type | OTP 验证码输入框，六格实为单一 input，支持粘贴/自动填充/退格，输错整行抖动 | `fetch.sh bencho:one-time-code` / https://bencho.dev/blocks/one-time-code | deps: lucide-react |
| generate | Generate | Press | AI 生图加载态 image generation loader，先大色块后细节逐步显现，玻璃磨砂层渐清 | `fetch.sh bencho:generate` / https://bencho.dev/blocks/generate | deps: lucide-react；占位: FLOWER |
| step-player | Step player | Press | 步骤进度指示器 step progress，当前点拉伸为进度条填充，再缓动到下一个点，类似 stories 分页 | `fetch.sh bencho:step-player` / https://bencho.dev/blocks/step-player | deps: 仅 React |
| todo-tower | Todo tower | Press | 物理待办清单 physics todo list，任务像砖块堆叠，勾掉或抽出一张其余受重力掉落 | `fetch.sh bencho:todo-tower` / https://bencho.dev/blocks/todo-tower | deps: lucide-react |
| image-accordion | Image accordion | Hover | 图片手风琴画廊 image accordion，hover 的图展开，邻居按衰减让位，整排向指针倾斜 | `fetch.sh bencho:image-accordion` / https://bencho.dev/blocks/image-accordion | deps: 仅 React；占位: SHOTS |
| glass-bubble | Glass bubble | Drag | 液态玻璃折射效果 liquid glass refraction，拖动玻璃球扭曲下方图片，SVG/Canvas 透镜 | `fetch.sh bencho:glass-bubble` / https://bencho.dev/blocks/glass-bubble | deps: 仅 React；占位: COW |
| action-node | Action node | Hover | 自动化流程节点卡片 automation node card，类似 n8n/Zapier 工作流步骤，控件折叠在角落 | `fetch.sh bencho:action-node` / https://bencho.dev/blocks/action-node | deps: lucide-react；占位: AVATARS |
| magnet-select | Magnetic select | Select | 磁吸标签选择 magnetic chip select，按下的选项膨胀，其余选项被径向推开，标签/兴趣多选 | `fetch.sh bencho:magnet-select` / https://bencho.dev/blocks/magnet-select | deps: framer-motion；占位: MARKS |
| slide-confirm | Slide to confirm | Drag | 滑动确认按钮 slide to confirm，手柄跟手推过轨道，越过阈值后自动完成，支付/危险操作确认 | `fetch.sh bencho:slide-confirm` / https://bencho.dev/blocks/slide-confirm | deps: framer-motion lucide-react |
| picker | Assignees | Select | 指派人选择器 assignee picker，下拉列表选人后头像在胶囊里堆叠 avatar stack | `fetch.sh bencho:picker` / https://bencho.dev/blocks/picker | deps: framer-motion lucide-react；占位: AVATARS |
| checklist | Checklist | Press | 动画清单 animated checklist，勾选时方框填充、对勾描边、文字划线 | `fetch.sh bencho:checklist` / https://bencho.dev/blocks/checklist | deps: framer-motion |
| carousel | Carousel | Swipe | 3D 卡片轮播 card carousel，转盘式卡片静止漂移、指针下倾斜、可滑动旋转 | `fetch.sh bencho:carousel` / https://bencho.dev/blocks/carousel | deps: 仅 React；占位: SHOTS |
| palette | Palette | Press | 配色生成器 color palette generator，3-5 个协调色块，按钮生成新一组配色 | `fetch.sh bencho:palette` / https://bencho.dev/blocks/palette | deps: lucide-react |
| aspect | Aspect ratio | Select | 裁剪比例切换 aspect ratio crop selector，分段控件切换 4:3/1:1/3:4，保持面积不变 | `fetch.sh bencho:aspect` / https://bencho.dev/blocks/aspect | deps: 仅 React；占位: SHEEP |
| tilt | Tilt card | Hover | 3D 倾斜卡片 tilt card hover，照片卡在指针下下沉而非上浮，带按压阴影和边缘高光 | `fetch.sh bencho:tilt` / https://bencho.dev/blocks/tilt | deps: 仅 React；占位: BUTTERFLY |
| sound | Now playing | Press | 音乐播放器小组件 now playing，迷你播放条展开成完整播放器再折回，单一数值驱动尺寸圆角 | `fetch.sh bencho:sound` / https://bencho.dev/blocks/sound | deps: lucide-react；占位: COVER |
| drag-ball | Dragging ball | Drag | 可拖拽的 squishy ball 软球，抓取时膨胀、按住时挤压，liquid-gooey 粘滞效果 | `fetch.sh bencho:drag-ball` / https://bencho.dev/blocks/drag-ball | deps: framer-motion liquid-gooey |
| seek | Search | Press | 展开式搜索框 expanding search bar，放大镜图标移动到位同时展开为输入框 | `fetch.sh bencho:seek` / https://bencho.dev/blocks/seek | deps: 仅 React |
| pull | Pull to refresh | Drag | 下拉刷新 pull to refresh，卡片随手拉伸，越线后提交并带回弹刷新余额，移动端列表 | `fetch.sh bencho:pull` / https://bencho.dev/blocks/pull | deps: 仅 React |
| escape | Escape button | Hover | 逃跑按钮 runaway button，按钮躲避光标然后放弃，彩蛋/趣味交互 | `fetch.sh bencho:escape` / https://bencho.dev/blocks/escape | deps: 仅 React |
| slosh | Slosh slider | Slide | 液体填充滑块 liquid fill slider，填充有质量，快速拖动时液体晃荡越过手柄 | `fetch.sh bencho:slosh` / https://bencho.dev/blocks/slosh | deps: 仅 React |
| liq-create | Create menu | Press | 粘滞 gooey 创建菜单，胶囊按下后像液体一样展开成菜单，metaball 效果 | `fetch.sh bencho:liq-create` / https://bencho.dev/blocks/liq-create | deps: framer-motion lucide-react |
| liq-arrange | Reorder list | Drag | 拖拽排序列表 drag to reorder，相邻行像液体 metaball 融合，SVG gooey filter | `fetch.sh bencho:liq-arrange` / https://bencho.dev/blocks/liq-arrange | deps: framer-motion；占位: AVATARS #arr-goo |
| toolbar | Canvas toolbar | Select | 浮动画布工具栏 floating canvas toolbar，形状工具记住上次选择，类似 Figma/白板工具条 | `fetch.sh bencho:toolbar` / https://bencho.dev/blocks/toolbar | deps: lucide-react |
| radial | Radial menu | Press | 径向菜单 radial menu，按中心按钮工具以半圆扇形展开 | `fetch.sh bencho:radial` / https://bencho.dev/blocks/radial | deps: lucide-react |
| stepper | Drag stepper | Press | 数字步进器 number stepper，点击加一，按住拖动快速扫值，兼顾精确和速度 | `fetch.sh bencho:stepper` / https://bencho.dev/blocks/stepper | deps: lucide-react |
| confirm | Inline confirm | Press | 行内删除确认 inline delete confirmation，删除按钮变成自身的确认按钮，之后提供撤销 undo | `fetch.sh bencho:confirm` / https://bencho.dev/blocks/confirm | deps: framer-motion lucide-react |
| toasts | Notify | Press | 通知我按钮 notify me，铃铛阻尼摆动，按钮保持按下态并替换文案，宽度平滑过渡 | `fetch.sh bencho:toasts` / https://bencho.dev/blocks/toasts | deps: lucide-react |
| icon-bar | Icon bar | Select | 动画标签栏 animated tab bar，选中胶囊前沿先行、拉伸跨越两格后尾部追上并回弹 | `fetch.sh bencho:icon-bar` / https://bencho.dev/blocks/icon-bar | deps: lucide-react |
| dock | Magnifying dock | Hover | macOS 放大 Dock 栏 magnifying dock，图标按与光标距离衰减放大 | `fetch.sh bencho:dock` / https://bencho.dev/blocks/dock | deps: lucide-react |
| progress | Progress ticks | Hover | 刻度滑块 tick slider，沿刻度刮擦设置值，拖动时显示数值和变化量 | `fetch.sh bencho:progress` / https://bencho.dev/blocks/progress | deps: 仅 React |
| humidity | Wheel | Drag | 圆形刻度旋钮 circular dial slider，拖动环形刻度设值，点亮带波浪推进，湿度/温度控制 | `fetch.sh bencho:humidity` / https://bencho.dev/blocks/humidity | deps: 仅 React |
| command | Command bar | Type | 命令栏 command bar，按钮与输入框液态融合展开，完成后滑回，cmd+k 搜索 | `fetch.sh bencho:command` / https://bencho.dev/blocks/command | deps: liquid-gooey lucide-react |
| roster | Selection list | Select | 多选人员列表 multi-select list，选中行抬起，有选择后底部按钮从中间长出 | `fetch.sh bencho:roster` / https://bencho.dev/blocks/roster | deps: framer-motion liquid-gooey；占位: AVATARS |
| sleep | Range dial | Drag | 圆形范围滑块 circular range slider，双手柄环形刻度设区间，睡眠时长/时间段 | `fetch.sh bencho:sleep` / https://bencho.dev/blocks/sleep | deps: framer-motion liquid-gooey |
| liq-toggle | Liquid toggle | Press | 液态开关 liquid toggle switch，滑动时水滴拉伸变形，gooey metaball 效果 | `fetch.sh bencho:liq-toggle` / https://bencho.dev/blocks/liq-toggle | deps: framer-motion；占位: #liq-goo |
| ascii-wake | ASCII wake | Hover | ASCII 字符尾迹 hover 效果，光标经过处字符升温并向指针倾斜后冷却，未在站点上架（parked） | `fetch.sh bencho:ascii-wake` / https://bencho.dev/blocks/ascii-wake | deps: 仅 React；parked 未上架 |
| browser-tabs | Browser tabs | Drag | 浏览器标签页条 browser tabs，拖拽排序与选中填充动画，未在站点上架（parked） | `fetch.sh bencho:browser-tabs` / https://bencho.dev/blocks/browser-tabs | deps: lucide-react；占位: CABRA CABRA_BOX CABRA_VIEW；parked 未上架 |
| card-stack | Card stack | Hover | 扇形卡片堆 card stack，hover 时卡片绕底部支点展开成扇形，未在站点上架（parked） | `fetch.sh bencho:card-stack` / https://bencho.dev/blocks/card-stack | deps: 仅 React；parked 未上架 |
| emoji-reactions | Emoji reactions | Hover | 表情回应条 emoji reactions，hover 的表情放大弹出，点击落入计数，未在站点上架（parked） | `fetch.sh bencho:emoji-reactions` / https://bencho.dev/blocks/emoji-reactions | deps: framer-motion lucide-react；占位: AVATARS；parked 未上架 |
| foggy-glass | Foggy glass | Hover | 起雾玻璃擦拭效果 foggy glass，指针擦出清晰区域后慢慢重新起雾，Canvas，未在站点上架（parked） | `fetch.sh bencho:foggy-glass` / https://bencho.dev/blocks/foggy-glass | deps: 仅 React；parked 未上架 |
| fold | Folding frame | Drag | 折叠屏框架 folding frame，拖动铰链折叠并扭曲背后画面，未在站点上架（parked） | `fetch.sh bencho:fold` / https://bencho.dev/blocks/fold | deps: 仅 React；占位: SHEEP；parked 未上架 |
| hold-delete | Hold to delete | Press | 长按删除按钮 hold to delete，按住进度填充、松手回退，临近完成垃圾桶抖动，未在站点上架（parked） | `fetch.sh bencho:hold-delete` / https://bencho.dev/blocks/hold-delete | deps: lucide-react；parked 未上架 |
| mb-compare | Before and after | Drag | 海报前后对比 before/after 拖动分割线，甩动惯性滑到边，未在站点上架（parked） | `fetch.sh bencho:mb-compare` / https://bencho.dev/blocks/mb-compare | deps: 仅 React；parked 未上架 |
| mb-deck | Poster deck | Swipe | 海报卡堆 poster deck，从抓取点倾斜，甩出后飞走并回到底部，类 Tinder swipe，未在站点上架（parked） | `fetch.sh bencho:mb-deck` / https://bencho.dev/blocks/mb-deck | deps: 仅 React；parked 未上架 |
| mb-holo | Holo card | Hover | 全息镭射卡 holo card，随指针倾斜、眩光滑过、彩虹光泽，未在站点上架（parked） | `fetch.sh bencho:mb-holo` / https://bencho.dev/blocks/mb-holo | deps: 仅 React；parked 未上架 |
| mb-spot | Spotlight | Hover | 聚光灯海报 spotlight，黑暗中指针像手电筒照亮，按住全亮，未在站点上架（parked） | `fetch.sh bencho:mb-spot` / https://bencho.dev/blocks/mb-spot | deps: 仅 React；parked 未上架 |
| rolling-counter | Rolling counter | Drag | 滚动数字计数器 rolling counter，逐列滚动落定带模糊拖影，未在站点上架（parked） | `fetch.sh bencho:rolling-counter` / https://bencho.dev/blocks/rolling-counter | deps: lucide-react；parked 未上架 |
| scratch-card | Scratch card | Drag | 刮刮卡 scratch card，Canvas 擦除涂层，刮够比例后整片揭开，未在站点上架（parked） | `fetch.sh bencho:scratch-card` / https://bencho.dev/blocks/scratch-card | deps: 仅 React；占位: COVER；parked 未上架 |
| swipe-row | Swipe row | Swipe | 列表行左右滑动操作 swipe row，越过阈值提交并回弹，移动端邮件/消息列表，未在站点上架（parked） | `fetch.sh bencho:swipe-row` / https://bencho.dev/blocks/swipe-row | deps: lucide-react；占位: AVATARS；parked 未上架 |
| tag-input | Tag input | Type | 标签输入框 tag input，chip 加入/移除时 layout 动画推挤与换行，未在站点上架（parked） | `fetch.sh bencho:tag-input` / https://bencho.dev/blocks/tag-input | deps: framer-motion lucide-react；parked 未上架 |
| category:finds | Finds | inspiration | Finds 灵感墙：约 152 条他人发布的 UI 微交互视频（多来自 X），只能看不提供源码，按 Morph/Reveal/Press/Hover/Drag 等标签 | https://bencho.dev/finds/{id}（列表见 https://bencho.dev/sitemap.xml） | 无源码 |
| category:sounds | Sounds | sound | Sounds UI 音效库：82 个合成音效（点击、通知、反馈、导航、系统等），页面可试听并下载 WAV，无代码 | https://bencho.dev/sounds（浏览器内合成后 Download WAV） | 无源码 |

## 未解决
- Finds（约 152 条）是他人作品的视频收藏，只能看，没有源码，清单只到分类级；单条元数据在主 bundle 的数组里（id/title/by/from/tags/src），可用 `https://bencho.dev/sitemap.xml` 列出全部 `/finds/*`。
- Sounds（82 个）在浏览器里用 Web Audio 合成后下载 WAV，没有静态音频文件或代码可直接 curl；需要时请在页面上手动下载。
- Copy prompt 按钮的原文需要浏览器渲染才能拿到；脚本输出的是同一份 tsx/css/deps/tokens/stubs，只是外层说明文字不同。
- Bench（画布工作台）是站点功能，不是组件，未收录。

## Finds（2026-10-07 补充）
151 条 Finds 已逐条写进 bencho.tsv，id 为 `find:{id}`，用法是"仅参考"，描述已译成中文。
- 元数据在首页主 bundle（`/assets/index-*.js`）的数组里，字段是 `{id,title,by,from,note,tags,media,src,poster}`。
- 视频在 `https://media.bencho.dev{src}`；唯一一条静态图（media=still）在 `https://bencho.dev{src}`。`poster` 路径对部分条目会回落成 HTML，不要依赖。
- 获取：`fetch.sh bencho:find:{id}` 会下载视频；原帖链接写在获取列里。
