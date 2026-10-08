# 落地页区块（marketing-section）

## 什么时候需要
做落地页、产品介绍页、活动页时，用来搭 hero、功能介绍、CTA、页脚、logo 墙、用户评价这些区块。这类页面是 Persuade 模式：访客要被说服然后行动，所以区块的任务是把一个论点讲清楚，不是把组件摆满。

不需要的情况：后台、设置页、文档页不要套营销区块；只有一句话加一个按钮的页面，用主底座的排版和 `button` 就够了。

先确认一件事：**shadcn 官方没有营销区块。** 它的 blocks 只有 sidebar、login、signup、dashboard 预览（`block/sidebar`、`block/login`、`block/signup`、`block/preview`）。shadcn 底座的落地页要么用 shadcn 基础组件自己排，要么从 obsidianui、originkit 拿区块再映射 token。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | 自己用 `shadcn:button`、`shadcn:navigation-menu`、`shadcn:accordion`（FAQ）、`shadcn:carousel` 排版，主导效果从 `reactbits` 免费背景或文字动效里挑一个 | 官方没有营销 block；基础件 + 一个效果是最不容易出 AI 味的组合，token 不用映射。reactbits 颜色走 props，按 `_styles.md` 的 shadcn + reactbits 条件传主题色 |
| uiarc | `uiarc:hero-section` + `uiarc:cta-section` + `uiarc:site-footer` + `uiarc:site-header` + `uiarc:faq-section` | 全部免费，同一套 token 和动效预设。hero-section 传 `title` 就渲染自己的内容（centered / split / minimal 三种布局），不传才显示演示；背景 mesh 是 WebGL，离屏和标签页隐藏时停，减弱动效只画一帧，没有 WebGL 时回落到 CSS 静态版（源码已看）。uiarc 风格规范本身就禁止眉标和装饰渐变 |
| 没有底座或其他 | `obsidianui:split-showcase`、`obsidianui:draggable-marquee` 这类 obsidianui block，放在 shadcn 底座上 | obsidianui 的 primitive 和 shadcn 同构，block 可以直接进 shadcn 项目；split-showcase 用 `useReducedMotion`，draggable-marquee 用 gsap `matchMedia` 处理减弱动效。装 block 时 CLI 提示覆盖 `ui/button.tsx` 一律跳过 |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| logo 墙 / 客户墙 | `uiarc:logo-marquee` | 免费里实现最完整：有暂停 / 播放按钮（带 `aria-label` 和 `aria-live` 提示）、精细指针悬停暂停、`prefers-reduced-motion` 停止、复制的一组 `aria-hidden`。跑马灯是第 3 级风险，这几条正好是它过关的条件 |
| logo 墙，shadcn 底座 | `obsidianui:draggable-marquee` | 可拖拽，gsap 驱动，减弱动效时不滚。默认 `pauseOnHover = false`，要打开，并补一个可见的暂停按钮 |
| 首屏需要一个"有记忆点"的主导效果 | `originkit:hero-26`（点阵背景）、`originkit:hero-14`（需登录） | originkit 免费 hero 里视觉完成度高的两个。需登录：由用户自己 `npx originkit add`。免费替代：uiarc `hero-section` 的 mesh 背景，或 shadcn 布局 + reactbits 一个背景 |
| 功能介绍，想用交互代替一排卡片 | `originkit:features-01`（需登录） | 竖向 tabs 切换功能和截图，registry 标签写了 keyboard-navigation。免费替代：`shadcn:tabs` 竖排 + 截图，自己做 |
| 移动 app 落地页 | `originkit:hero-02`、`originkit:footer-01`（需登录） | 手机 mockup、商店下载按钮、社交链接；hero-02 依赖 motion |
| 产品发布前的预约 | `originkit:hero-07`（需登录） | waitlist 首屏带邮箱表单。免费替代：`uiarc:newsletter-signup`，或 shadcn `input-group` + `button` |
| AI 产品首屏 | `originkit:hero-42`（需登录） | 产品 mockup + 对话预览。免费替代：shadcn `message` + `bubble` 编一段真实感的对话放在 hero 右侧 |
| FAQ | `uiarc:faq-section` 或 `shadcn:accordion` | uiarc 版有手风琴、主题栏、可搜索三种；shadcn 只要 accordion |
| 页脚 | `uiarc:site-footer` | 链接列 + 订阅，token 统一。shadcn 底座自己用 `separator` + 链接列排，比引入带硬编码黑底的页脚更省事 |
| 用户评价 | 自己写：一段大号引文 + 姓名职位 + 真实头像，最多 2–3 条 | 免费来源里没有成熟的评价区块（`uiarc:testimonial-stage` 是 Pro，reactbits 的 social-proof 是 Pro）。不要用等大卡片网格堆评价 |

## 慎用
- 等大卡片堆结构：用 `card` 排出"图标 + 标题 + 一段话"的三列或六格网格，是 `_scenes.md` 第 6 节点名的 AI 味做法（几项功能真的平行、同等重要时例外）。功能介绍改用：一个主功能大图 + 两三个次要功能文字说明；或交互 tabs；或真实截图配一句话。`uiarc:feature-bento` 是 Pro，也不必追。
- 眉标（kicker）：标题上方的小号大写标签。`obsidianui:footer` 就有一个 `uppercase tracking-[0.2em]` 的胶囊标签和全大写列标题；用时删掉。uiarc 的规范明确不用 eyebrow，`hero-section` 的 `announcement` 是一个可点的公告链接，只在真有发布消息时用。
- 英雄数据模板：大数字配小标签的统计带。`uiarc:stats-band` 就是这个模式（进入视口从 0 数到目标值）。只有数字真实、可核实、并且是论点本身时才用，而且一页一次；不要拿来填空。数字从 0 动画计数时，未进入视口前要显示最终值或保留宽度，不能出现"数字没跑完就看不清"。
- `obsidianui:footer`：`bg-black text-white` 写死、不跟随主题；用嵌套的 `<section id="light-one">` 做装饰光效（语义错误，屏幕阅读器会读到一串空 section），光效所需的 CSS 不在这个文件里；文案也是 ObsidianUI 自己的宣传语。要用只借布局。
- `obsidianui:v-prism`：three + postprocessing 的 WebGL 背景，带毛玻璃（`glass`），演示图片走 obsidianui CDN。只做首屏唯一主导效果，上线前换图。
- `obsidianui:flip-text`：registry 只给了 `flip-text.tsx` 和 `utils.ts`，`.flip-char` 用到的 keyframes 没有随包分发，装上不会动；还把标题拆成逐字 `<span>` 且没有 `aria-label`，默认无限循环、没有减弱动效分支。要做标题文字动效，用 `find.sh --task text-effect` 另挑。
- `uiarc:cta-section`、`uiarc:hero-section` 的按钮（2026-10-08 核对源码）：cta-section 的 `action` 既没有 `href` 也没有 `onClick` 时，点击只在原地切换成 `confirmedLabel`，什么也没发生（演示用）；hero-section 只要传了 `doneLabel`，点击就立刻显示完成态、2.4 秒后复原，不等 `onClick` 的真实结果。上线时一律传 `href`；要显示完成态就自己在真实请求成功后切换，不要依赖 `doneLabel`，否则是第 1 级的状态虚假。
- `uiarc:hero-section` 的 `centered` 演示：图片来自 `media.ts` 的 `/media/people/*.jpg` 等路径，registry 不附带这些文件，直接用演示会坏图。传 `title` 走自己的内容。
- originkit 免费 hero 的 `hero-01`、`hero-17`、`hero-24`、`hero-32`：registry 描述只是占位文字（"Hero 01 component."），没有依赖、标签只有 next.js / tailwind，看不出差异，未验证。选之前在官网看预览视频。
- originkit 背景类 component（`ribbon-glow`、`fibre-arc`、`glowing-sphere` 等，多数带 `glow`）：大量 three.js 全屏背景，一页只能一个；Pro 的 hero（hero-03、05、08… 共 36 个）和 `cta-01`、`cta-02`、`footer-02` 不推荐。
- `reactbits:category:pro-blocks/*`：Pro，不推荐。
- 渐变按钮、彩色光晕按钮（`originkit:moving-gradient-button`、`originkit:crystal-glow`、`librariesdev:border-beam-pulse-inner`）：主 CTA 已经在首屏有主导效果时不要再叠一个会动的按钮。

## 页面模式约束
- Persuade（本任务的主场景）：首屏最多 1 个主导效果，整页最多 2 个且不在同一屏；装饰动效每屏最多 1 处并且要有含义；动效强度 4–7，密度 3–5。常见合格组合：首屏一个背景或一段文字动效 + 静态排版的其余区块；或首屏静态 + 中段一个交互演示。
- Experience（作品集首页）：效果服务于作品，hero 让位给作品图；logo 墙、统计带一般不需要。
- Operate、Read：不用营销区块。产品内的升级提示用主底座的 `alert` 或 `card`。

## 接入要点
- **一个底座**：uiarc 区块和 shadcn 基础件不要混在一页。shadcn 底座拿 obsidianui / originkit 区块时，把硬编码颜色（`bg-black`、`text-zinc-*`、`--obsidian-*`）改成 `--background`、`--foreground`、`--muted-foreground`、`--primary`。
- **动效库**：originkit 区块可能用 framer-motion，项目里已有 `motion/react` 时统一成一个（改 import）。three / gsap 只在用到的区块里懒加载，Next.js 里 WebGL 区块用 `dynamic(..., { ssr: false })`。
- **内容默认可见**：区块入场动画失败时内容也要在。不要每个区块都用同一个"淡入上移"；入场只给首屏一处，其余区块直接显示或只做有含义的揭示。
- **跑马灯**：必须能暂停（WCAG 2.2.2，超过 5 秒自动移动的内容要有暂停机制），遵守减弱动效，复制出来的那组 `aria-hidden`。
- **logo 与评价素材**：logo 用真实客户的、已获授权的；评价要有真实姓名和来源。演示 logo、演示头像、演示数字上线前全部替换。
- **CTA**：一页一个主行动，按钮文字说清结果（"开始免费试用"而不是"了解更多"）；主次按钮视觉差异明显。
- **移动端**：hero 在 375px 宽下标题不溢出、按钮不小于 44px；WebGL 背景在移动端降级或换静态图。
- **性能**：首屏的 WebGL 不阻塞 LCP；hero 图片给尺寸、用合适格式；视频背景要有海报帧并在减弱动效下不自动播放。

## 候选清单
- `uiarc:hero-section` — uiarc 底座首屏，三种布局，传 `title` 用自己的内容
- `uiarc:cta-section` — uiarc 底座行动号召
- `uiarc:site-header` — 滚动变实心、mega menu、移动端菜单
- `uiarc:site-footer` — 链接列 + 订阅
- `uiarc:faq-section` — 手风琴 / 主题栏 / 可搜索 FAQ
- `uiarc:logo-marquee` — 可暂停的 logo 墙
- `shadcn:accordion` — shadcn 底座 FAQ
- `shadcn:navigation-menu` — shadcn 底座顶栏
- `shadcn:carousel` — 截图轮播（评价不建议轮播）
- `obsidianui:split-showcase` — shadcn 底座的左右分栏展示块
- `obsidianui:draggable-marquee` — shadcn 底座可拖拽 logo 墙
- `originkit:hero-26` — 点阵背景 hero（需登录；免费替代 uiarc hero-section mesh）
- `originkit:hero-14` — 浮动标签 + 光束 hero（需登录，带光束渐变）
- `originkit:features-01` — 竖向 tabs 功能展示（需登录；免费替代 shadcn tabs）
- `originkit:features-02` — 可拖拽地球 + 指标（需登录；含英雄数据，慎用）
- `originkit:hero-02`、`originkit:footer-01` — app 落地页首屏与页脚（需登录）
- `originkit:hero-07` — waitlist 首屏（需登录；免费替代 uiarc newsletter-signup）
- `originkit:hero-42` — AI 产品首屏（需登录；免费替代 shadcn message 编排）
- `uiarc:stats-band` — 统计带（只在数字真实且是论点时用）
- `uiarc:newsletter-signup` — 邮件订阅
- `uiarc:announcement-bar` — 顶部公告条
- `obsidianui:footer` — 只借布局，颜色和语义要改
- 仅参考：`collectui` 的落地页类分类、`inspora` 的 website 类条目、`getdesign` 网站目录里的品牌落地页（见 `guides/page-inspiration.md`）
