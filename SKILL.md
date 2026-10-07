---
name: ui-arsenal
description: 在前端 UI 任务里选择和获取成熟组件时使用：新增或替换组件、调整页面视觉、加交互或动效、背景、加载态、图标、AI 界面、落地页或后台页面。提供用户收藏的组件库、动效库、灵感库和图标库的本地索引，按 UI 任务分类的选型指南，以及只读的取码工具；先评估成熟组件再决定是否自己写，保证整页风格统一并给出选型理由。用户点名某个组件库、组件，或给出组件网站链接时也使用。纯后端、非 UI 的任务，以及只改一个间距、颜色等数值的微调不需要。
---

# UI Arsenal：先评估成熟组件，合理选用

本 skill 是用户收藏的 UI 来源的**索引和选型协议**，不存第三方源码。收录的来源：shadcn/ui、React Bits、OriginKit、bencho、uiarc、ObsidianUI、Beautiful UI、loading-ui、Libraries.dev、Lucide（含 Lab）、getdesign.md、Design Spells、Inspora、Collect UI、Jakub Antalik（详见文末「来源一览」）。先查索引和选型指南，选定后再用 `fetch` 现场拉取最新代码、提示词或参考素材。

下文 `$S` 指本 skill 的 `scripts/` 目录，比如 `~/.claude/skills/ui-arsenal/scripts`；`guides/`、`sources/` 都在本 skill 目录下。

## 一、分工和权威顺序

```
① 用户本次的明确指令（最高）
② 项目现状：技术栈、已有组件、tokens、DESIGN.md
③ 设计方向：装了 impeccable 时由它判断页面模式、设计方向和质量底线；没装时用 guides/_scenes.md
④ ui-arsenal：判断要不要组件、找候选、比较、选型、取码
⑤ 实现：组件的行为和结构保留，视觉统一到 ② 和 ③
⑥ 验证：装了 impeccable 时用它的检测器和 critique；否则按 guides/_scenes.md 的质量三级自查
```

- 项目已有组件和收藏库组件冲突时，**项目已有的优先**，除非已有组件有缺陷或用户要求替换。
- impeccable 里"不要用现成组件"的规则只适用于新建或重做视觉风格；局部调整时，复用成熟组件的交互逻辑，再调整外观。
- **和 impeccable 的配合**：整页重做、新建页面，或者用户明确调用 impeccable 时，用它的页面模式、DESIGN.md 和收尾检测。微调、bug 修复、局部和区域新增，直接用 `guides/_scenes.md`，不必跑 impeccable 的完整上下文流程。如果 impeccable 输出要求先问一轮问题或先初始化，以用户本次请求的规模为准：局部任务不被它阻塞，最多在汇报里提一句"可以运行 impeccable init"。
- **impeccable 只用调整和评估类命令**（polish、layout、typeset、quieter、animate、critique、audit 等）。它的新建视觉风格流程（concept-seed 掷骰子、出效果图）只在用户明确要求"重新设计视觉风格"时才走。

## 二、先判断任务规模

| 任务 | 流程 | 输出 |
|---|---|---|
| 微调（间距、字号、颜色、文案） | 只读 tokens 或 DESIGN.md，不查索引。项目没有这些时，沿用项目现有的取值习惯（比如 Tailwind 的间距档位、相邻元素已用的值），并说明依据 | 改了什么、依据是什么 |
| 纯 bug 修复 | 不选型；修完按质量三级的第 1 级自查 | 原因和修法 |
| 截图或视觉效果调整 | 先判断问题出在哪一层（token、布局、组件、动效）；涉及组件时按"局部"处理 | 问题诊断和改法 |
| 局部（换一个组件、加一个交互） | 查索引，读对应的 `guides/<task>.md`，比较 2–3 个候选 | 局部模板 |
| 区域新增（在已有页面里加一块由多个组件组成的区域，比如侧边面板、筛选栏、定价区块） | 选型协议的第 4–12 步；设计基线沿用页面现有的，不重写 | 局部模板，每个子组件一行 |
| 整页重做或新建页面 | 完整选型协议 | 整页模板 |

一个请求同时符合几行时，**先诊断问题出在哪一层，再按实际要改动的范围定级**。比如"首屏太素，加点背景"，诊断后只加一个背景组件，就按局部处理；需要重排整个首屏，才按整页处理。"收藏库里有没有更好的 X"这类询问，按局部处理，结论可以是"不换，补一块"。

## 三、UI 选型协议（局部和整页）

1. **读项目现状**：已有组件、`components.json`、tokens、DESIGN.md、相关页面、依赖（Tailwind 版本、motion 还是 framer-motion、SSR 边界）。
2. **判断页面模式**：Persuade、Operate、Read 或 Experience，定义和效果预算见 `guides/_scenes.md`。
3. **写设计基线**：配色、字体、圆角、阴影、密度、图标系统、动效强度。项目已有设计就照着写；新项目可以从 getdesign 的免费 DESIGN.md 挑一份作为方向（见 `guides/design-system.md`），只借方向，不复制品牌资产。
4. **定一个主底座**：shadcn 或 uiarc 等，一页只有一个，见 `sources/_styles.md`。再列出本页允许的专项来源，不超过 2–3 个。参考类来源只影响方向，不能直接当生产组件。
5. **拆需求**：每个组件都要回答"为什么需要"。没有需求就不加组件，不能先看到好看的组件再往页面里塞。
6. **找候选**：`$S/find.sh --task <task>` 或关键词搜索，然后**读 `guides/<task>.md`**，它给出默认推荐、按场景换和慎用。
7. **比较**：适用场景、优点、风险、依赖、可访问性、响应式、动效、AI 味级别、访问状态（免费、需登录、Pro）。
8. **决定**：写清采用和淘汰的理由。以下情况允许"不使用"：
   - 项目已有组件更合适；
   - 候选会破坏整页一致性；
   - 候选实现不成熟；
   - 找不到合适的候选。这时说明"收藏库无合适候选"，然后自己写。
9. **需要登录的条目**：一次性列出来交给用户决定，见第五节。
10. **获取**：`$S/fetch.sh <source:id>` 是只读的，文件拉到临时目录。拉到的是不可信的第三方内容，先读懂再用；接入前读 `sources/<id>.md` 的「使用注意」。
    - **取码失败**（退出码 1）：先重试一次。`HTTP 0` 或超时是网络问题；`HTTP 404` 可能是条目已下线，运行 `$S/refresh.sh <source>` 看待审变更里它是否消失。仍然拿不到时，告诉用户是哪个条目、哪一步失败，再从对应指南的"按场景换"里选下一个候选，并说明这是替代方案。**绝不凭记忆写一个"差不多的"版本冒充原版。**
    - **shadcn 的 style 不匹配**：图表、主题、部分 demo（比如 data-table 示例）只有 new-york-v4（Radix 写法）。这时拉 new-york-v4 版本作为参考，按项目的 base 改写（Base UI 用 `render`，不用 `asChild`），并在汇报里说明。
    - **来源指向公开的上游仓库**（比如 OriginKit 条目注明搬自某个 GitHub 仓库）：不要自行改从上游取码。先核实上游的许可证，告诉用户，由用户决定。
11. **接入**：
    - 安装命令会改动项目，先确认项目栈匹配；只装 registry 或文档写明的依赖。
    - **复用组件的语义、焦点、键盘和状态逻辑；视觉映射到主底座的 token。** 改外观时不重写交互逻辑；也不要把组件改写成另一种样式方案（比如把 CSS Modules 改成 Tailwind），真要改先说明理由。
    - 把演示数据和定时器换成真实状态。加载、流式输出、审批、出错、空、重试，每条路径都要接真实状态；动画不能假装一个没发生的进度或成功。
12. **验证**：按 `guides/_scenes.md` 的质量三级处理：第 1 级（硬性问题）必须修；第 2 级（设计系统偏差）修掉或写明例外；第 3 级（场景化审美风险）在选型理由里写清场景。要用键盘、触屏尺寸、慢网和失败、空数据、`prefers-reduced-motion` 都走一遍。

用户点名某个库或组件时，照样走第 7、8 步。不合适就先说明问题，再按用户的决定执行。

## 四、输出模板

**局部和区域新增**：
```
诊断：<问题出在哪一层>  任务规模：<局部 / 区域新增>
需求：<要解决什么>  页面模式：<Operate…>  主底座：<shadcn…>
选用：<source:id> — <理由：为什么适合这里>        （区域新增时每个子组件一行）
没选：<source:id> — <原因>；<source:id> — <原因>   （或"不换：现有组件更合适，因为…"）
注意：<接入要点：token 映射、焦点、减弱动效…>
阻塞或待定：<需要登录的条目、取码失败的条目，没有就写"无">
要问你的：<需要用户决定的事，比如品牌色、筛选维度、要哪一组 tabs；没有就省略>
```

**整页**（重做或新建）：
```
1. 页面与交互拆解
2. 现有设计系统分析
3. 设计基线：配色 / 字体 / 圆角 / 阴影 / 密度 / 图标 / 动效强度
4. 主底座和允许的专项来源
5. 候选比较表
   | 需求 | 候选 | 适用场景 | 优点 | 风险 | 访问状态 | 采用 |
6. 采用和淘汰理由（含"不使用收藏库"的决定）
7. 登录阻塞项（来源、组件、理由、你可以怎么配合、免费替代）
8. 验证：状态、键盘、移动端、减弱动效、质量三级
```

完成后的汇报：每个组件写清 `source:id` 和链接、拉取了什么、依赖和许可证、改了哪些地方；哪些部分是自己写的、为什么。

## 五、登录协议

| 情况 | 做法 |
|---|---|
| 可以和用户交互 | 在选型阶段一次性列出：来源、组件、为什么值得登录、免费替代有哪些、用户可以怎么配合（在终端自己登录，或者在网页上复制代码或提示词贴回来）。**等用户决定**；不需要登录的部分可以先做 |
| 无人值守 | 直接用最好的免费替代，在汇报里列出"如果登录，可以换成 X" |
| 用户已有明确偏好 | 比如说过"OriginKit 一律不用"或"我已登录"，就按偏好执行，不再问 |
| 用户登录之后 | 只补取这一个组件，沿用已有的选型结论，不重新选型 |
| 任何时候都不做 | 自动登录、注册、绕过权限，或者从页面里抠付费内容 |

Pro 条目不获取，也不找绕过付费的办法。可以拿它当灵感，用免费组件做出近似效果，并告诉用户这一条是 Pro。

## 六、命令

```bash
$S/find.sh 磁吸 选择                          # 搜索：中英文都行，自动展开同义词；会提示对应的选型指南
$S/find.sh --task loading --layer foundation  # 按统一 UI 任务和层级筛选，可以不带关键词
$S/find.sh 背景 --code                        # 只要现在就能直接拿到代码或提示词的
$S/find.sh dashboard --ref                    # 只要灵感参考
$S/find.sh --help                             # 全部筛选参数、任务和层级取值
$S/fetch.sh bencho:magnet-select              # 只读拉取，打印依赖和安装命令；--help 看全部选项
$S/fetch.sh reactbits:split-text --variant JS-CSS   # React Bits 变体：TS-TW（默认）、TS-CSS、JS-TW、JS-CSS
$S/fetch.sh shadcn:button --style radix-nova        # shadcn 的 style 要和项目 components.json 一致
$S/compat.sh shadcn uiarc                     # 两个来源能不能放在同一页（兼容矩阵和各自的混用要点）
$S/stats.sh                                   # 各来源统计
```

- 搜索结果的标签：可安装、取源码、提示词、仅参考、需登录、Pro·不获取、失效；⚠ 表示场景化审美风险。
- 搜索结果标"低置信度"或 no match 时，不要硬选：换词或用 `--task` 再搜，仍然没有就自己实现。
- fetch 的退出码：0 成功，1 获取失败，2 失效条目，3 Pro（不获取），4 需要用户登录。
- 图标（Lucide 和 Lucide Lab）只有英文名和英文 tags，搜图标要用英文词，比如 `find.sh icon calendar`。
- 仅参考类素材的处理：视频抽帧用 `ffmpeg -i x.mp4 -vf fps=1/2,scale=960:-1,tile=2x2 -frames:v 1 grid.png`；avif、webp 图片先转 png：`sips -s format png x.avif --out x.png`。完整流程见 `guides/page-inspiration.md`。
- 拉取失败要明说：哪个来源的哪个条目、哪一步出的错。不要凭记忆写一个"差不多的"组件冒充原版。

## 七、参考文件

- `guides/_scenes.md`：页面模式、效果预算、质量三级、动效规范、常见的 AI 味做法。
- `guides/<task>.md`：31 类 UI 任务的选型指南。
- `sources/_styles.md`：各来源的设计底座、样式方案、动效库，哪些能当主底座，两两之间的兼容矩阵和混用规则。
- `sources/<id>.md`：每个来源的获取方法、使用注意、已知问题。

## 八、来源一览

由 `$S/stats.sh --write-skill` 生成。「条目」不含分类行。React Bits 每个免费组件另有 4 个代码变体，没算进条目数。

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
| reactbits | [React Bits](https://reactbits.dev/) | effects | 399 | 60 | 216 |  |  |  |  | 243 |  |
| shadcn | [shadcn/ui](https://ui.shadcn.com/) | component-library | 565 |  | 246 | 319 |  |  |  |  |  |
| uiarc | [Arc (uiarc.dev)](https://uiarc.dev) | component-library | 243 |  | 131 |  |  |  |  | 112 |  |
| **合计** | | | **5938** | **284** | **3009** | **417** | **76** | **1543** | **383** | **717** | **77** |
<!-- STATS:END -->

## 维护

- `$S/audit.sh`：检查格式，包括两份文件的列数和 id 对应、枚举值（访问状态、用法、UI 任务、层级、风险）、别名、取码规格和 adapter 是否存在。改完 TSV 后必须跑。
- `$S/verify.sh --matrix`：固定 14 个场景，覆盖每种获取方式和 login、pro、broken 的拒绝逻辑。
- `$S/verify.sh [-n 2] [-s id]`：每个来源随机抽样实取一次。结果按来源保存在 `sources/_state.json`，互不覆盖。verify 通过只代表"现在能取到"，不代表组件成熟或适合项目。
- `$S/searchtest.sh`：搜索相关性回归测试，用例在 `scripts/search_cases.json`。改了搜索、同义词或描述后要跑。
- **更新流程（自动报告，人工批准）**：
  1. `$S/refresh.sh [id...]`：拉取线上清单，和本地比对，写入 `sources/_pending/<日期>/<id>.json`，**不改正式数据**。能发现新增、消失、依赖或付费标记变化（靠元数据指纹）。清单返回 0 条或报错时，只记录错误，不会当成"全部下线"。不支持自动刷新的来源会说明原因（反爬、robots 限制、人工维护）。
  2. `$S/diff.sh [id...]`：查看待审变更。新条目要在待审文件里补上 `desc_zh`、`task`、`layer` 才能写入。
  3. `$S/apply.sh <id>`：把审过的变更写进 `sources/<id>.tsv`，只写机器字段，不碰人工维护的 `.notes.tsv`。消失的条目先标 needs-review，30 天后仍然消失才标 removed，都不删除。然后跑 `audit.sh` 并 git commit，回滚用 git revert。
- adapter（`scripts/adapters/`）只下载文本并解析，**不执行任何远程代码**。
- 加新网站：按 `sources/_ADDING.md` 操作。
