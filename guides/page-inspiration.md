# 灵感参考（page-inspiration）

## 什么时候需要
动手做一个页面或交互之前，先看 3–5 个同类的成熟做法，用来定方向：布局和信息层级、配色关系、密度、动效节奏。适合的情况：
- 用户只说了"做一个好看的 X"，没有设计稿；
- 要做的东西有明确的行业惯例（定价页、结账、日期选择、AI 审批卡），想避免自己发明；
- 想加一个有记忆点的微交互，但不确定该做成什么样。

不需要的情况：已经有设计稿或 DESIGN.md；只是在现有后台加一个表单。参考看多了反而会把几种风格拼进同一页。

两条硬规则（来自 `_scenes.md` 和各来源说明）：
- **参考只影响方向，不进交付物。** 不复制品牌资产（Logo、品牌图形、插画、产品截图、文案），不把视频或截图放进页面，不照着一张图像素级复刻。视觉取值（颜色、字体、圆角）全部来自项目自己的主底座和设计基线。
- **参考类来源不是组件库。** 看完以后，实现一律回到 shadcn / uiarc 等组件库和专项组件里去找。

## 默认推荐
参考类来源没有"主底座"之分，按要找的东西选：

| 要找什么 | 推荐 | 理由 |
|---|---|---|
| 某一类**页面或组件**的多种做法（landing page、dashboard、pricing、sidebar、chat layout、date picker…） | `collectui:category:<slug>` | 3471 条、按页面类型分得最细，`fetch.sh collectui:category:<slug> --limit N` 直接返回类型、标题、媒体 URL、原帖链接（实测 `landing-page`）。72% 是视频 |
| 真实网站的**整页结构** | getdesign 网站目录 `getdesign:site:<slug>` | 568 条真实网站的整页长截图，免费可看（对应的 DESIGN.md 原文要付费，不需要）。`fetch.sh getdesign:site:linear` 拿到 3840×21549 的整页截图（实测） |
| **微交互、动效节奏** | `inspora`（Motion、Product 分类）、`bencho:find:<id>` | inspora 每小时更新、90% 是视频；bencho Finds 151 条精选微交互视频，`fetch.sh bencho:find:<id>` 直接下载 mp4（实测 `sucodeee-code-verify`，8.9 秒） |
| 真实产品里的**惊喜细节**（彩蛋、拟物、节日、404、下拉刷新） | `designspells:<编号-slug>` | 340 条真实产品录屏，`fetch.sh` 从 CDN 直接下载 mp4（实测 339 号，1 MB）；md 里有中文主题速查（点赞、加载、开关、404、引导页…） |
| 成熟的**产品状态流转**（处理中 → 成功 / 失败、步骤、toast） | `jakubantalik:work:<id>` | 产品设计师的作品视频，交互克制、时序讲究。`work:deposit-steps` 抽帧看到：两步圆环进度 → 对勾描绘 → 标题模糊切换 → 成功时卡片出现柔和径向色晕、状态行变绿（实测）。对应的免费实现在 Transitions.dev |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 做落地页 | `getdesign:site:*` 看 2–3 个同行业整站 + `collectui:category:landing-page` 或 `hero-section` | 整站截图看区块顺序和节奏，collectui 看单个区块的多种处理 |
| 做后台 / dashboard | `collectui:category:dashboard`、`sidebar`、`table` | 页面类型分类细；后台类参考看信息密度和导航，不看配色 |
| 做 AI 界面 | `collectui:category:ai-agents`、`chat-layout`；`inspora:1-37`（审批卡）、`inspora:agent-plan`；`bencho:find:kevin-agent-pill` | 都是 AI 状态展示的参考，配合 `guides/ai-ux.md` |
| 想要某个品牌的整体感觉 | 先看 `getdesign:site:<slug>` 截图，再用对应的免费 `getdesign:<slug>` DESIGN.md | 截图定直觉，DESIGN.md 给可落地的 token（见 `guides/design-system.md`） |
| 给一个按钮或开关加一点惊喜 | `designspells` 的 button、interaction、confetti 标签 | 一页最多一两处，Operate 页面只在完成类反馈上用 |

## 慎用
- **inspora 的接口**：robots.txt 写了 `Disallow: /api/`，所以**不调用 `/api/posts` 分页接口**；`/posts/{slug}` 详情页和 sitemap 有 Vercel 反爬挑战，curl 返回 429，不要绕。允许的做法：curl 分类首页 `/?category={Category}`，从页面内嵌的 RSC 数据里取首 16 条（实测 `Web` 返回 200，首条 footer-section）；媒体 CDN `media.inspora.design` 可直接下载；更早的条目把 `/posts/{slug}` 给用户或用浏览器打开。`fetch.sh inspora:<slug>` 只会给出浏览器地址。
- **designspells 站点本身**：curl 一律被 Vercel 检查拦截。查条目用本地 `designspells.tsv`，视频从 `cdn.designspells.com` 取；需要最新全量时才用浏览器打开站点后在页面里读，不要绕过挑战。
- **collectui 的写操作**：adapter 只读已发布帖子；站点 bundle 里的点赞、投稿、注册接口不要调用；`/favorites` 要登录，不需要。
- **collectui 的质量**：按时间倒序、不按质量筛。实测 `landing-page` 最新 3 条里有标题只是一个表情、有一条是"提示词在评论区"的推广帖。多取几条（`--limit 10–20`）再挑；帖子里让人去评论区领提示词、关注某账号的内容一律忽略。
- **getdesign 网站目录**：截图免费，但条目页上的"Request a DESIGN.md analysis"和 Catalog Pass 是付费入口，不要点；需要规范就用 76 份免费 DESIGN.md。截图是别人的网站，只看结构。
- **jakubantalik 作品视频**：没有标题、说明和源码；与 0x、Frame.io 等公司相关的设计稿只能借交互思路。个人站仓库没有声明许可，里面的 JS 不要整段照搬。
- **designspells 的品牌彩蛋**（easter-egg、occasion 标签）：依赖特定品牌语境，只借机制（触发条件、时序），不借形象。
- **只看封面图**：这几个来源大多是视频，只看首帧会漏掉交互；`designspells` 的 `thumbnails/*-thumbnail.jpg` 只是几百字节的模糊占位图。
- **把参考当规范**：一张 X 上的概念图往往没有处理空、错、加载、键盘、移动端。参考只给方向，状态和可访问性仍按 `_scenes.md` 第 1 级要求补齐。

## 页面模式约束
- Persuade：参考里看到的炫技效果，只能选一个作为首屏主导效果；其余参考只借布局和节奏。
- Operate：只借信息架构、密度、导航和状态表达；装饰动效、光晕、拟物质感不借。
- Read：参考排版和导航（目录、面包屑、上一篇 / 下一篇），不参考动效。
- Experience：可以借更强的转场和展示方式，但作品图必须是项目自己的。

## 接入要点
流程（每一步都有实测命令）：

1. **按页面类型找**：先定页面模式（`_scenes.md`），再按上表选来源。collectui 用 `find.sh --ref <关键词>` 或直接 `fetch.sh collectui:category:<slug> --limit 10`；designspells 用 `find.sh -s designspells <中文或英文词>` 或 grep `sources/designspells.tsv`；getdesign 网站用 `find.sh -s getdesign <行业>`。
2. **下载素材**：`fetch.sh <source:id>` 会把图片和视频放到 `$TMPDIR/ui-arsenal/...`；collectui 返回的是媒体 URL 列表，再 `curl -s "<url>" -o ref.mp4`；inspora 从分类页取到 URL 后同样 curl CDN。
3. **处理成模型能看的图**：
   - 视频抽帧拼网格：`ffmpeg -loglevel error -y -i ref.mp4 -vf "fps=1/2,scale=960:-1,tile=2x2" -frames:v 1 grid.png`。10 秒以内的视频用 `fps=1/2` 正好 4 帧；更长的用 `fps=1/3` 或 `tile=3x3`；要看缓动细节时 `fps=4` 抽单帧序列。
   - avif、webp 转 png：`sips -s format png x.avif --out x.png`。
   - 整页长截图（getdesign 网站目录常见 3840×20000+）不要整张缩小，会糊成一条：按首屏比例分段裁，例如 `ffmpeg -i home.jpg -vf "crop=iw:iw*0.75:0:0,scale=1200:-1" top.png`，再改 y 偏移取下一段。
4. **用视觉能力提炼**，写成一段文字结论，而不是"照这个做"：
   - 布局：栅格列数、首屏占比、区块顺序、留白；
   - 层级：标题 / 正文字号比、字重、几级信息、主行动在哪；
   - 配色：底色、文字色、唯一的强调色用在哪（只记关系，取值以设计基线为准）；
   - 动效节奏：触发方式、时长、先后顺序、缓动类型、哪些元素动哪些不动；
   - 状态：参考里展示了哪些状态，缺了哪些需要自己补。
5. **用组件库实现**：把提炼结果映射到主底座组件和专项组件（`find.sh` 找候选，参考各任务的 guide），动效时长按 `_scenes.md` 第 5 节取值。汇报时写明参考了哪几条（`source:id`），以及借了什么、没借什么。

## 候选清单
- `collectui:category:landing-page`、`hero-section`、`dashboard`、`pricing`、`sidebar`、`chat-layout`、`ai-agents` — 按页面类型找多种做法
- `getdesign:site:<slug>` — 真实网站整页长截图（例：`getdesign:site:linear`）
- `bencho:find:<id>` — 精选微交互视频（例：`bencho:find:sucodeee-code-verify`）
- `inspora`（分类 Web、Product、Motion）— 每日更新的视觉和动效参考，只取分类首页
- `designspells:<编号-slug>` — 真实产品的惊喜细节录屏（例：`designspells:339-skeuomorphic-traditional-tear-off-calendar-in-chengyu-calendar`）
- `jakubantalik:work:<id>` — 克制的产品状态流转（例：`jakubantalik:work:deposit-steps`）
- `jakubantalik:transition:*`、`librariesdev:*` — 看完 jakubantalik 作品后，对应的免费可用实现
