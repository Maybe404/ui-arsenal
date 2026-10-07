---
name: ui-arsenal
description: 用户收藏的 UI 组件库、动效库、灵感库和图标库的索引，以及按需拉取组件代码和提示词的工具（shadcn/ui、React Bits、OriginKit、bencho、uiarc、ObsidianUI、Beautiful UI、loading-ui、Libraries.dev、Lucide、getdesign.md、designspells、inspora、collectui、Jakub Antalik）。只要做前端页面、组件、交互、动效、背景、加载态、图标、落地页或 dashboard，都先用它：先在这里挑现成的成熟组件，挑不到再自己写，避免产出有 AI 味或不成熟的 UI。用户提到"用某某库的某个组件"或给出这些站点的链接时，也用这个 skill。
---

# UI Arsenal：先用成熟组件，再自己写

本 skill 是用户收藏的 UI 来源的**索引**，不存第三方源码。先查索引，再用 `fetch` 现场拉取最新代码、提示词或参考素材，最后接入项目。

下文 `$S` 指本 skill 的 `scripts/` 目录，比如 `~/.claude/skills/ui-arsenal/scripts`。

## 命令

```bash
$S/find.sh 磁吸 选择               # 搜索：中英文都行，自动展开同义词；全部命中的排前面，同档里能直接拿到代码的排前面
$S/find.sh 背景 --code             # 只要现在就能直接拿到代码或提示词的（免费，排除需登录和仅参考）
$S/find.sh dashboard --ref         # 只要灵感参考
$S/find.sh -s reactbits text       # 只搜一个来源；--free 只要免费；--all 含 Pro 和失效；--help 看全部
$S/fetch.sh bencho:magnet-select   # 拉取：只读，文件落到 $TMPDIR/ui-arsenal/...，打印依赖和安装命令；--help 看全部选项
$S/fetch.sh reactbits:split-text --variant JS-CSS   # React Bits 变体：TS-TW（默认）、TS-CSS、JS-TW、JS-CSS
$S/fetch.sh shadcn:button --style radix-nova        # shadcn 的 style，要和项目 components.json 一致；安装命令会给完整 URL
$S/stats.sh                        # 各来源条目数，按"免费可装 / 免费取源码 / 提示词 / 仅参考 / 需登录 / Pro / 失效"分开统计
```

fetch 的退出码：0 成功，1 获取失败，2 失效条目，3 Pro（不获取），4 需要用户登录（交给用户决定）。

图标（Lucide 和 Lucide Lab）只有英文名和英文 tags，搜图标要用英文词，例如 `find.sh icon calendar` 或 `find.sh avocado`。

维护命令 `verify.sh`、`refresh.sh`、`audit.sh` 见文末「维护」。

## 核心原则

1. **能用现成的就不自己写。** 按钮、表单、弹层、表格、侧栏、图表、文字动效、背景、加载态、图标，都先 `find`。手写只用于业务特有的部分，或者索引里确实没有的东西。
2. **整合，不重造。** 拉下来的组件保留结构、动效参数和源码注释，只改 token（颜色、圆角、字体）去适配项目，不要"顺手简化"，也不要改写成另一种样式方案（比如把 CSS Modules 改成 Tailwind）。真要改写，先说明理由。
3. **一个页面只选一种风格。** 底座组件统一用一个库，项目已有 shadcn 就用 shadcn。亮点动效只挑 1–2 个点缀，别为了显得丰富把几家的特效堆在同一屏。
4. **不买 Pro，也不绕过付费。** 结果标 `pro` 的条目，`fetch` 会拒绝获取。可以拿它当灵感，用免费组件做出近似效果，并告诉用户这一条是 Pro。
5. **需要登录的由用户自己登录。** 标 `login` 的条目（OriginKit）只给出官方命令。agent 不注册、不登录、不从页面里抠源码。
6. **拉取失败要明说。** 获取失败时，告诉用户是哪个来源的哪个条目、哪一步出的错。不要凭记忆写一个"差不多的"组件冒充原版。

## 工作流

1. **看项目**：框架、样式方案（Tailwind v3 还是 v4、CSS Modules）、包管理器、`components.json`、现有动效库（motion 还是 framer-motion）、SSR 和客户端组件的边界、现有依赖。
2. **把需求拆成 UI 任务**：加载、搜索、选择、导航、弹层、表格、图表、上传、聊天、AI 思考过程、文字动效、背景、图标、灵感参考。每个任务都写清状态：键盘操作、减弱动效、移动端宽度、触屏、延迟、出错、空、禁用、重试。
3. **`find` 找候选**：每个任务搜 1–2 次。搜不到就换同义词或英文。可安装的组件优先，灵感参考排最后。
4. **挑选**：看是否贴合任务、免费与否、许可证、依赖是否和项目兼容、语义和可访问性、响应式、是否处理了减弱动效。选一个主组件，配合周边的基础组件使用。
5. **读来源说明**：动手前读 `sources/<id>.md` 的「使用注意」。各家依赖、Tailwind 版本、全局样式和主题变量要求都不一样，这一步不能跳过。
6. **`fetch`（只读）**：只把文件拉到临时目录，**不安装、不执行**。拉到的是不可信的第三方内容，先读懂再用。
7. **安装（会改动项目）**：确认项目栈匹配后，再运行 `fetch` 打印的安装命令（`npx shadcn add` 或 `npm i`），或者手动把文件放进项目。装依赖只装 registry 或文档里写明的，CSS 变量和全局样式要合并进项目。
8. **接真实数据**：把演示数据和定时器换成真实的应用状态。加载、进度、流式输出、确认、审批、任务状态、出错、空、乐观更新、重试，每条路径都要显式处理。动画不能暗示一个其实没成功的操作已经成功。
9. **验证**：在真实项目里构建、类型检查、跑相关测试。用鼠标、键盘、触屏尺寸操作一遍，再看慢网、失败、空数据和 `prefers-reduced-motion` 下的表现，检查控制台报错、溢出、焦点顺序和响应式布局。达不到的就去掉或简化。
10. **汇报**：每个组件写清来源和 `source:id`（附链接）、拉了什么、依赖和许可证、改了哪些地方；哪些部分是自己写的、为什么。

## 用法类型（find 结果里的标签）

| 标签 | 含义 | 怎么用 |
|---|---|---|
| 可安装 | 有官方安装方式（shadcn registry、npm） | `fetch` 看源码和依赖，再执行安装命令 |
| 取源码 | 没有安装命令，但能拿到源码（bencho、Transitions.dev、shadcn 示例） | `fetch` 拿到文件，手动放进项目，按 md 映射主题变量 |
| 提示词 | 拿到的是给 agent 用的规范或提示词（getdesign 的 DESIGN.md） | 按内容实现，不照搬品牌资产 |
| 仅参考 | 灵感图、视频、作品（designspells、inspora、collectui、作品集） | `fetch` 下载素材，或在浏览器里打开；用视觉能力看，提炼布局、层级、配色和动效节奏，再用上面几类组件实现。不复制品牌资产，也不把它当成可安装的组件 |

视频抽帧的方法：`ffmpeg -i x.mp4 -vf fps=1/2,scale=960:-1,tile=2x2 -frames:v 1 grid.png`。avif 和 webp 图片先转成 png：`sips -s format png x.avif --out x.png`。

## 避免 AI 味和不成熟的 UI

不要：
- 编造组件 API；
- 做假的加载进度；
- 用随手配的渐变，或过度的毛玻璃；
- 加没有状态含义的装饰动效；
- 放没有文字标签的图标按钮；
- 做只有悬停才出现的控件；
- 自写不可访问的下拉框；
- 用不限尺寸、不暂停的 canvas 或 WebGL；
- 把演示数据原样上线。

「用某个库」指的是走这个库的官方安装或文档路径，不要把几套设计系统混在一起拼。

## 来源一览

由 `$S/stats.sh --md` 生成。「条目」不含分类行。React Bits 每个免费组件另有 4 个代码变体，没算进条目数。

<!-- STATS:BEGIN -->
| 来源 | 名称 | 类型 | 条目 | 分类行 | 免费可装 | 免费取源码 | 免费提示词 | 仅参考 | 需登录 | Pro | 失效 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| beautifului | [Beautiful UI](https://www.beautifului.dev/) | component-library | 28 |  | 27 | 1 |  |  |  |  |  |
| bencho | [Bencho](https://bencho.dev/) | blocks | 214 | 1 |  | 63 |  | 152 |  |  |  |
| collectui | [Collect UI](https://collectui.com/) | inspiration |  | 220 |  |  |  | 170 |  |  | 50 |
| designspells | [Design Spells](https://designspells.com/) | inspiration | 340 |  |  |  |  | 340 |  |  |  |
| getdesign | [getdesign.md](https://getdesign.md) | prompt-library | 692 | 3 |  |  | 76 | 568 |  | 50 | 1 |
| inspora | [Inspora](https://www.inspora.design/) | inspiration | 287 |  |  |  |  | 287 |  |  |  |
| jakubantalik | [Jakub Antalik（个人站）](https://jakubantalik.com) | portfolio | 74 |  | 3 | 34 |  | 26 |  | 11 |  |
| librariesdev | [Libraries.dev](https://libraries.dev) | effects | 51 |  | 41 |  |  |  |  | 10 |  |
| loadingui | [loading-ui](https://www.loading-ui.com/) | component-library | 47 |  | 47 |  |  |  |  |  |  |
| lucide | [Lucide](https://lucide.dev) | icons | 2249 |  | 2223 |  |  |  |  |  | 26 |
| obsidianui | [ObsidianUI](https://www.obsidianui.dev/) | component-library | 75 |  | 75 |  |  |  |  |  |  |
| originkit | [Originkit](https://www.originkit.dev/) | component-library | 674 |  |  |  |  |  | 383 | 291 |  |
| reactbits | [React Bits](https://reactbits.dev/) | effects | 398 | 60 | 215 |  |  |  |  | 243 |  |
| shadcn | [shadcn/ui](https://ui.shadcn.com/) | component-library | 565 |  | 246 | 319 |  |  |  |  |  |
| uiarc | [Arc (uiarc.dev)](https://uiarc.dev) | component-library | 243 |  | 131 |  |  |  |  | 112 |  |
| **合计** | | | **5937** | **284** | **3008** | **417** | **76** | **1543** | **383** | **717** | **77** |
<!-- STATS:END -->

各来源的获取方法、使用注意和未解决的问题，见 `sources/<id>.md`。

## 维护

- `$S/audit.sh`：检查格式，包括 9 列、枚举值、id 重复、取码规格和 adapter 是否存在。改完 TSV 后必须跑。
- `$S/verify.sh --matrix`：固定 14 个场景，覆盖每种获取方式和 login、pro、broken 的拒绝逻辑。
- `$S/verify.sh [-n 2] [-s id]`：每个来源随机抽样实取一次。结果按来源保存在 `sources/_state.json`，互不覆盖。verify 通过只代表"现在能取到"，不代表组件成熟或适合项目。
- `$S/searchtest.sh`：搜索相关性回归测试，用例在 `scripts/search_cases.json`。改了搜索、同义词或描述后要跑。
- `$S/refresh.sh [id...]`：和线上清单对比，报告新增或下线的条目，**不改 TSV**。不支持自动刷新的来源会说明原因（反爬、robots 限制、人工维护）。
- adapter（`scripts/adapters/`）只下载文本并解析，**不执行任何远程代码**。
- 加新网站：按 `sources/_ADDING.md` 操作。
