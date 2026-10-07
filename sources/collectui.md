---
id: collectui
name: Collect UI
url: https://collectui.com/
kind: inspiration
stack: 任意（纯参考图/视频，无代码）
license: 未声明（作品版权归原作者，内容转自 X/Twitter）
pro: none
fetch: browse-only
verified: 2026-10-07
source_status: active
visual_style: curated x/twitter ui references, mixed styles
foundation: n/a
styling: n/a
motion_lib: none
dark_mode: n/a
mixing_notes: 只借鉴布局、层级和动效节奏，配色、字体、圆角一律按主底座实现，不要把参考图的风格当成第二套设计系统
---
## 是什么 / 什么时候用
Collect UI 早期是 Dribbble "Daily UI" 挑战作品集（按 challenge 分类，如 Sign Up、Checkout、404 Page）；2026 年的现版本改成了 SvelteKit + Supabase，内容换成从 X/Twitter 策展的设计帖（视频 2486 条、图片 985 条，**共 3471 条已发布**），沿用了 challenge 风格的分类体系（分类表 215 行 / 212 个唯一 slug，其中 162 个有内容）。旧的 `/challenges/{slug}` 会 308 跳转到 `/designs/{slug}-ui-design-inspiration`。
适用场景：要做某类**页面或组件**（landing page、hero、dashboard、pricing、sidebar、modal、date picker、chat layout、onboarding……）时按分类找参考；量大、按页面类型分得细，适合"先看 5-10 个同类做法再动手"。没有代码、提示词或模板。

## 按需获取方法

站点是 SvelteKit 单页应用，HTML 里没有数据，条目由前端运行时从站点的数据接口读取（只读、已发布内容）。媒体 CDN `https://cdn.collectui.com/...` 可以直接下载。

**按分类取条目**：用 `scripts/fetch.sh collectui:category:<slug> [--limit N]`。adapter 会在运行时完成接口准备，输出每条的类型（image/video）、标题、媒体 URL 和原帖链接。实测 `dashboard` 返回的条目和站点页面一致（2026-10-07）。

**分类计数**：浏览器打开 `https://collectui.com/categories`，页面列出每个有内容分类的条目数；下方清单的条目数是 2026-10-07 的快照（总数 3471）。

**步骤 4：把参考图喂给视觉能力**
```bash
# 图片（avif → png）
curl -s "{media_url}" -o ref.avif && sips -s format png ref.avif --out ref.png
# 视频：抽 4 帧拼 2x2 网格，一次看完动效关键帧
curl -s "{media_url}" -o ref.mp4 && ffmpeg -loglevel error -y -i ref.mp4 -vf "fps=1/3,scale=960:-1,tile=2x2" -frames:v 1 ref_grid.png
```
实测：`https://cdn.collectui.com/media/HSexuGLWAAACpyz.avif`（AI Support Agent Dashboard，3000×2250）转 png 成功；dashboard 分类首条视频抽帧网格清晰可读（笔记/任务/收藏三栏 app 界面）。

**人工浏览 URL**：分类页 `https://collectui.com/designs/{slug}-ui-design-inspiration`（SPA，需浏览器渲染）；全部分类 `https://collectui.com/categories`；热门 `https://collectui.com/trending`；设计师 `https://collectui.com/designers/{username}`。帖子没有独立详情页（`/designs/{id}` 404），点击卡片是弹窗预览，原帖看 `source_url`。

**开发 agent 使用流程**：确定页面/组件类型 → 在下方清单找对应 slug（可同时查 2 个近义分类，如 `landing-page` + `hero-section`）→ 步骤 2 取最新 10-20 条，优先 `media_type=image` 看静态布局、视频看交互 → 下载并抽帧 → 用视觉能力归纳：信息架构/栅格、字号层级、配色（主色/中性色/强调色）、圆角阴影、动效节奏 → 用组件库实现，不照抄。

## 使用注意
- 只读用途：只用 GET 查询 `collectui_posts` / `collectui_categories`；bundle 里还有 likes、submissions、signups 等写操作，**不要调用**。
- 站点改版后 adapter 可能失效，`verify.sh --matrix` 会报出来；这时先用浏览器方式（见下）。
- 分类标注较粗：一帖常有 2-3 个分类，`ui-interaction`（723）、`motion`（302）、`landing-page`（256）、`card`（208）是大杂烩，建议用更细分类或叠加 `title=ilike`。
- 50 个分类当前 0 条（多为旧 Daily UI 挑战题目，如 calculator、hotel-booking、leaderboard、pitch-deck），清单中标 broken；另有 8 个标签只出现在帖子里、不在分类表（stat-card、photo-album 等），只能用 REST 查。
- 72% 是视频，只看首帧会漏掉交互；图片多为 avif，Read 工具前先转 png。
- 内容版权归原作者（X 帖子），只借鉴不搬运。
- 无 Pro/付费内容；`/favorites`（点赞收藏）需要登录，不需要用。

## 组件清单
条目 3471 条（>500），按约定写到分类级：212 个唯一分类 + 8 个仅标签存在的 tag，共 220 行（与 collectui.tsv 一致）。计数为 2026-10-07 快照。

| id | 名称 | 分类 | 一句话用途 | 获取（具体命令或URL） | 备注 |
|---|---|---|---|---|---|
| category:ui-interaction | UI Interaction | design | UI 交互/微交互，723 条 | https://collectui.com/designs/ui-interaction-ui-design-inspiration |  |
| category:landing-pages | Landing pages | website | 落地页（网站组），1 条 | https://collectui.com/designs/landing-pages-ui-design-inspiration |  |
| category:landing-page | Landing Page | design | 落地页，256 条 | https://collectui.com/designs/landing-page-ui-design-inspiration |  |
| category:framer | Framer | design | Framer 站点，151 条 | https://collectui.com/designs/framer-ui-design-inspiration |  |
| category:button | Button | design | 按钮，108 条 | https://collectui.com/designs/button-ui-design-inspiration |  |
| category:navigation | Navigation | design | 导航，27 条 | https://collectui.com/designs/navigation-ui-design-inspiration |  |
| category:hero-section | Hero Section | design | 首屏 Hero 区，134 条 | https://collectui.com/designs/hero-section-ui-design-inspiration |  |
| category:agency | Agency | website | 代理机构官网，0 条 | REST: collectui_posts?categories=cs.{agency} | 空分类 |
| category:cta | CTA | design | 行动号召 CTA，34 条 | https://collectui.com/designs/cta-ui-design-inspiration |  |
| category:ai-sites | AI Sites | website | AI 产品官网，0 条 | REST: collectui_posts?categories=cs.{ai-sites} | 空分类 |
| category:footer | Footer | design | 页脚，51 条 | https://collectui.com/designs/footer-ui-design-inspiration |  |
| category:2 | 2 | website | 未命名测试分类，0 条 | REST: collectui_posts?categories=cs.{2} | 空分类 |
| category:claude | Claude | design | Claude 生成/相关界面，5 条 | https://collectui.com/designs/claude-ui-design-inspiration |  |
| category:sign-up | Sign Up | design | 注册页，21 条 | https://collectui.com/designs/sign-up-ui-design-inspiration |  |
| category:dashboard | Dashboard | design | 仪表盘后台，96 条 | https://collectui.com/designs/dashboard-ui-design-inspiration |  |
| category:todo-list | Todo List | design | 待办清单，21 条 | https://collectui.com/designs/todo-list-ui-design-inspiration |  |
| category:checkout | Checkout | design | 结账支付页，3 条 | https://collectui.com/designs/checkout-ui-design-inspiration |  |
| category:404-page | 404 Page | design | 404 页面，13 条 | https://collectui.com/designs/404-page-ui-design-inspiration |  |
| category:onboarding | Onboarding | design | 新手引导，32 条 | https://collectui.com/designs/onboarding-ui-design-inspiration |  |
| category:pop-up | Pop Up | design | 弹窗，5 条 | https://collectui.com/designs/pop-up-ui-design-inspiration |  |
| category:settings-page | Settings Page | design | 设置页，22 条 | https://collectui.com/designs/settings-page-ui-design-inspiration |  |
| category:user-profile | User Profile | design | 用户资料页，11 条 | https://collectui.com/designs/user-profile-ui-design-inspiration |  |
| category:features | Features | design | 功能介绍区，51 条 | https://collectui.com/designs/features-ui-design-inspiration |  |
| category:pricing | Pricing | design | 定价页，30 条 | https://collectui.com/designs/pricing-ui-design-inspiration |  |
| category:hover-state | Hover State | design | 悬停状态，51 条 | https://collectui.com/designs/hover-state-ui-design-inspiration |  |
| category:newsfeed | Newsfeed | design | 信息流，3 条 | https://collectui.com/designs/newsfeed-ui-design-inspiration |  |
| category:inbox | Inbox | design | 收件箱，3 条 | https://collectui.com/designs/inbox-ui-design-inspiration |  |
| category:quote | Quote | design | 引用块，0 条 | REST: collectui_posts?categories=cs.{quote} | 空分类 |
| category:contact-list | Contact List | design | 联系人列表，1 条 | https://collectui.com/designs/contact-list-ui-design-inspiration |  |
| category:verification-code | Verification Code | design | 验证码输入，0 条 | REST: collectui_posts?categories=cs.{verification-code} | 空分类 |
| category:mockup | Mockup | design | 样机展示，1 条 | https://collectui.com/designs/mockup-ui-design-inspiration |  |
| category:redesign | Redesign | design | 改版重设计，1 条 | https://collectui.com/designs/redesign-ui-design-inspiration |  |
| category:desk-inspiration | Desk Inspiration | design | 桌面布置灵感，0 条 | REST: collectui_posts?categories=cs.{desk-inspiration} | 空分类 |
| category:ui-kit | UI Kit | design | UI 套件，25 条 | https://collectui.com/designs/ui-kit-ui-design-inspiration |  |
| category:email-application | Email Application | design | 邮件客户端，4 条 | https://collectui.com/designs/email-application-ui-design-inspiration |  |
| category:illustration | Illustration | design | 插画，59 条 | https://collectui.com/designs/illustration-ui-design-inspiration |  |
| category:dial-pad | Dial Pad | design | 拨号盘，0 条 | REST: collectui_posts?categories=cs.{dial-pad} | 空分类 |
| category:style-guide | Style Guide | design | 风格指南，5 条 | https://collectui.com/designs/style-guide-ui-design-inspiration |  |
| category:terms-of-service | Terms of Service | design | 服务条款页，1 条 | https://collectui.com/designs/terms-of-service-ui-design-inspiration |  |
| category:brutal-design | Brutal Design | design | 粗野主义设计，1 条 | https://collectui.com/designs/brutal-design-ui-design-inspiration |  |
| category:admin-panel | Admin Panel | design | 管理后台，7 条 | https://collectui.com/designs/admin-panel-ui-design-inspiration |  |
| category:e-wallet | E-Wallet | design | 电子钱包，15 条 | https://collectui.com/designs/e-wallet-ui-design-inspiration |  |
| category:low-poly | Low Poly | design | 低多边形，0 条 | REST: collectui_posts?categories=cs.{low-poly} | 空分类 |
| category:collect-ui-curation | Collect UI Curation | design | Collect UI 精选，7 条 | https://collectui.com/designs/collect-ui-curation-ui-design-inspiration |  |
| category:montserrat | Montserrat | design | Montserrat 字体，0 条 | REST: collectui_posts?categories=cs.{montserrat} | 空分类 |
| category:funny-animation | Funny Animation | design | 趣味动画，15 条 | https://collectui.com/designs/funny-animation-ui-design-inspiration |  |
| category:project-management | Project Management | design | 项目管理，1 条 | https://collectui.com/designs/project-management-ui-design-inspiration |  |
| category:geometrical | Geometrical | design | 几何图形，0 条 | REST: collectui_posts?categories=cs.{geometrical} | 空分类 |
| category:character-animation | Character Animation | design | 角色动画，17 条 | https://collectui.com/designs/character-animation-ui-design-inspiration |  |
| category:stamp | Stamp | design | 邮票/印章风格，19 条 | https://collectui.com/designs/stamp-ui-design-inspiration |  |
| category:code-editor | Code Editor | design | 代码编辑器，5 条 | https://collectui.com/designs/code-editor-ui-design-inspiration |  |
| category:about-us | About Us | design | 关于我们页，9 条 | https://collectui.com/designs/about-us-ui-design-inspiration |  |
| category:reminder-alarm | Reminder / Alarm | design | 提醒/闹钟，2 条 | https://collectui.com/designs/reminder-alarm-ui-design-inspiration |  |
| category:e-commerce | E-Commerce | design | 电商，9 条 | https://collectui.com/designs/e-commerce-ui-design-inspiration |  |
| category:gallery | Gallery | design | 图库画廊，13 条 | https://collectui.com/designs/gallery-ui-design-inspiration |  |
| category:album-cover | Album Cover | design | 专辑封面，0 条 | REST: collectui_posts?categories=cs.{album-cover} | 空分类 |
| category:app-screens | App Screens | design | App 页面合集，12 条 | https://collectui.com/designs/app-screens-ui-design-inspiration |  |
| category:shape-invasion | Shape Invasion | design | 形状入侵（Daily UI 旧题），0 条 | REST: collectui_posts?categories=cs.{shape-invasion} | 空分类 |
| category:portfolio | Portfolio | design | 作品集，126 条 | https://collectui.com/designs/portfolio-ui-design-inspiration |  |
| category:email-design | Email Design | design | 邮件设计，3 条 | https://collectui.com/designs/email-design-ui-design-inspiration |  |
| category:error-state | Error State | design | 错误状态，1 条 | https://collectui.com/designs/error-state-ui-design-inspiration |  |
| category:pitch-deck | Pitch Deck | design | 路演幻灯片，0 条 | REST: collectui_posts?categories=cs.{pitch-deck} | 空分类 |
| category:scroll-transition | Scroll Transition | design | 滚动过渡，15 条 | https://collectui.com/designs/scroll-transition-ui-design-inspiration |  |
| category:travel-destination | Travel Destination | design | 旅行目的地，0 条 | REST: collectui_posts?categories=cs.{travel-destination} | 空分类 |
| category:real-estate | Real Estate | design | 房产，0 条 | REST: collectui_posts?categories=cs.{real-estate} | 空分类 |
| category:welcome-screen | Welcome Screen | design | 欢迎页，0 条 | REST: collectui_posts?categories=cs.{welcome-screen} | 空分类 |
| category:online-course | Online Course | design | 在线课程，0 条 | REST: collectui_posts?categories=cs.{online-course} | 空分类 |
| category:comments | Comments | design | 评论区，1 条 | https://collectui.com/designs/comments-ui-design-inspiration |  |
| category:book-cover | Book Cover | design | 书籍封面，3 条 | https://collectui.com/designs/book-cover-ui-design-inspiration |  |
| category:packaging | Packaging | design | 包装设计，0 条 | REST: collectui_posts?categories=cs.{packaging} | 空分类 |
| category:calligraphy | Calligraphy | design | 书法字体，0 条 | REST: collectui_posts?categories=cs.{calligraphy} | 空分类 |
| category:stranger-things | Stranger Things | design | 怪奇物语主题，0 条 | REST: collectui_posts?categories=cs.{stranger-things} | 空分类 |
| category:movie-card | Movie Card | design | 电影卡片，0 条 | REST: collectui_posts?categories=cs.{movie-card} | 空分类 |
| category:playing-cards | Playing Cards | design | 扑克牌，1 条 | https://collectui.com/designs/playing-cards-ui-design-inspiration |  |
| category:business-card | Business Card | design | 名片，4 条 | https://collectui.com/designs/business-card-ui-design-inspiration |  |
| category:bot-interface | Bot Interface | design | 聊天机器人界面，0 条 | REST: collectui_posts?categories=cs.{bot-interface} | 空分类 |
| category:halloween | Halloween | design | 万圣节主题，0 条 | REST: collectui_posts?categories=cs.{halloween} | 空分类 |
| category:documentation | Documentation | design | 文档页，1 条 | https://collectui.com/designs/documentation-ui-design-inspiration |  |
| category:infographic | Infographic | design | 信息图，8 条 | https://collectui.com/designs/infographic-ui-design-inspiration |  |
| category:statistics | Statistics | design | 统计数据展示，45 条 | https://collectui.com/designs/statistics-ui-design-inspiration |  |
| category:menu | Menu | design | 菜单，80 条 | https://collectui.com/designs/menu-ui-design-inspiration |  |
| category:captcha | Captcha | design | 人机验证，1 条 | https://collectui.com/designs/captcha-ui-design-inspiration |  |
| category:orb | Orb | design | 光球/AI 球体，26 条 | https://collectui.com/designs/orb-ui-design-inspiration |  |
| category:icons | Icons | design | 图标，46 条 | https://collectui.com/designs/icons-ui-design-inspiration |  |
| category:tabs | Tabs | design | 标签页 Tabs，55 条 | https://collectui.com/designs/tabs-ui-design-inspiration |  |
| category:invoice | Invoice | design | 发票账单，16 条 | https://collectui.com/designs/invoice-ui-design-inspiration |  |
| category:grid | Grid | design | 网格布局，23 条 | https://collectui.com/designs/grid-ui-design-inspiration |  |
| category:testimonials | Testimonials | design | 用户评价，18 条 | https://collectui.com/designs/testimonials-ui-design-inspiration |  |
| category:app-icon | App Icon | design | App 图标，52 条 | https://collectui.com/designs/app-icon-ui-design-inspiration |  |
| category:loading | Loading | design | 加载状态，42 条 | https://collectui.com/designs/loading-ui-design-inspiration |  |
| category:sidebar | Sidebar | design | 侧边栏，112 条 | https://collectui.com/designs/sidebar-ui-design-inspiration |  |
| category:liquid-glass | Liquid Glass | design | 液态玻璃，60 条 | https://collectui.com/designs/liquid-glass-ui-design-inspiration |  |
| category:motion | Motion | design | 动效，302 条 | https://collectui.com/designs/motion-ui-design-inspiration |  |
| category:css | CSS | design | CSS 效果，26 条 | https://collectui.com/designs/css-ui-design-inspiration |  |
| category:ai-flow | AI Flow | design | AI 流程，27 条 | https://collectui.com/designs/ai-flow-ui-design-inspiration |  |
| category:card | Card | design | 卡片，208 条 | https://collectui.com/designs/card-ui-design-inspiration |  |
| category:dark-mode | Dark Mode | design | 暗色模式，111 条 | https://collectui.com/designs/dark-mode-ui-design-inspiration |  |
| category:modal | Modal | design | 模态框，70 条 | https://collectui.com/designs/modal-ui-design-inspiration |  |
| category:scroll-animation | Scroll Animation | design | 滚动动画，90 条 | https://collectui.com/designs/scroll-animation-ui-design-inspiration |  |
| category:webflow | Webflow | design | Webflow 站点，6 条 | https://collectui.com/designs/webflow-ui-design-inspiration |  |
| category:3d | 3D | design | 3D，65 条 | https://collectui.com/designs/3d-ui-design-inspiration |  |
| category:notification | Notification | design | 通知，26 条 | https://collectui.com/designs/notification-ui-design-inspiration |  |
| category:bento | Bento | design | Bento 网格，68 条 | https://collectui.com/designs/bento-ui-design-inspiration |  |
| category:landing-section | Landing Section | design | 落地页区块，93 条 | https://collectui.com/designs/landing-section-ui-design-inspiration |  |
| category:weather | Weather | design | 天气，0 条 | REST: collectui_posts?categories=cs.{weather} | 空分类 |
| category:mobile-app | Mobile App | design | 移动 App，108 条 | https://collectui.com/designs/mobile-app-ui-design-inspiration |  |
| category:chat-layout | Chat Layout | design | 聊天布局，70 条 | https://collectui.com/designs/chat-layout-ui-design-inspiration |  |
| category:calendar | Calendar | design | 日历，29 条 | https://collectui.com/designs/calendar-ui-design-inspiration |  |
| category:text-effect | Text Effect | design | 文字特效，30 条 | https://collectui.com/designs/text-effect-ui-design-inspiration |  |
| category:responsive | Responsive | design | 响应式，16 条 | https://collectui.com/designs/responsive-ui-design-inspiration |  |
| category:color-palette | Color Palette | design | 配色方案，30 条 | https://collectui.com/designs/color-palette-ui-design-inspiration |  |
| category:dropdown | Dropdown | design | 下拉菜单，84 条 | https://collectui.com/designs/dropdown-ui-design-inspiration |  |
| category:tags | Tags | design | 标签 Tag，19 条 | https://collectui.com/designs/tags-ui-design-inspiration |  |
| category:loading-animation | Loading Animation | design | 加载动画，93 条 | https://collectui.com/designs/loading-animation-ui-design-inspiration |  |
| category:switch-button | Switch Button | design | 开关切换，16 条 | https://collectui.com/designs/switch-button-ui-design-inspiration |  |
| category:image-slider | Image Slider | design | 图片轮播/滑块，61 条 | https://collectui.com/designs/image-slider-ui-design-inspiration |  |
| category:subscribe | Subscribe | design | 订阅表单，5 条 | https://collectui.com/designs/subscribe-ui-design-inspiration |  |
| category:widget | Widget | design | 小组件 Widget，72 条 | https://collectui.com/designs/widget-ui-design-inspiration |  |
| category:mac-app | Mac App | design | Mac 应用，46 条 | https://collectui.com/designs/mac-app-ui-design-inspiration |  |
| category:faq | FAQ | design | 常见问题 FAQ，3 条 | https://collectui.com/designs/faq-ui-design-inspiration |  |
| category:search | Search | design | 搜索，21 条 | https://collectui.com/designs/search-ui-design-inspiration |  |
| category:social-media | Social Media | design | 社交媒体，10 条 | https://collectui.com/designs/social-media-ui-design-inspiration |  |
| category:shader | Shader | design | 着色器 Shader，47 条 | https://collectui.com/designs/shader-ui-design-inspiration |  |
| category:file-tree | File Tree | design | 文件树，15 条 | https://collectui.com/designs/file-tree-ui-design-inspiration |  |
| category:terminal-aesthetic | Terminal Aesthetic | design | 终端风格，45 条 | https://collectui.com/designs/terminal-aesthetic-ui-design-inspiration |  |
| category:file-upload | File Upload | design | 文件上传，11 条 | https://collectui.com/designs/file-upload-ui-design-inspiration |  |
| category:invite | Invite | design | 邀请，10 条 | https://collectui.com/designs/invite-ui-design-inspiration |  |
| category:tooltip-popover | Tooltip / Popover | design | 提示气泡/浮层，30 条 | https://collectui.com/designs/tooltip-popover-ui-design-inspiration |  |
| category:webgl | WebGL | design | WebGL，17 条 | https://collectui.com/designs/webgl-ui-design-inspiration |  |
| category:ai | AI | design | AI 界面，91 条 | https://collectui.com/designs/ai-ui-design-inspiration |  |
| category:notepad | Notepad | design | 记事本，4 条 | https://collectui.com/designs/notepad-ui-design-inspiration |  |
| category:accordion | Accordion | design | 手风琴折叠，7 条 | https://collectui.com/designs/accordion-ui-design-inspiration |  |
| category:folder | Folder | design | 文件夹，26 条 | https://collectui.com/designs/folder-ui-design-inspiration |  |
| category:badge | Badge | design | 徽章，6 条 | https://collectui.com/designs/badge-ui-design-inspiration |  |
| category:command-bar | Command Bar | design | 命令面板，15 条 | https://collectui.com/designs/command-bar-ui-design-inspiration |  |
| category:progress | Progress | design | 进度，24 条 | https://collectui.com/designs/progress-ui-design-inspiration |  |
| category:pattern | Pattern | design | 图案纹理，7 条 | https://collectui.com/designs/pattern-ui-design-inspiration |  |
| category:blog | Blog | design | 博客，10 条 | https://collectui.com/designs/blog-ui-design-inspiration |  |
| category:table | Table | design | 表格，16 条 | https://collectui.com/designs/table-ui-design-inspiration |  |
| category:dynamic-island | Dynamic Island | design | 灵动岛，10 条 | https://collectui.com/designs/dynamic-island-ui-design-inspiration |  |
| category:calculator | Calculator | design | 计算器，0 条 | REST: collectui_posts?categories=cs.{calculator} | 空分类 |
| category:music-player | Music Player | design | 音乐播放器，20 条 | https://collectui.com/designs/music-player-ui-design-inspiration |  |
| category:flash-messages | Flash Messages | design | 闪现消息提示，0 条 | REST: collectui_posts?categories=cs.{flash-messages} | 空分类 |
| category:single-product | Single Product | design | 单品页，2 条 | https://collectui.com/designs/single-product-ui-design-inspiration |  |
| category:direct-messaging | Direct Messaging | design | 私信，2 条 | https://collectui.com/designs/direct-messaging-ui-design-inspiration |  |
| category:countdown-timer | Countdown Timer | design | 倒计时，4 条 | https://collectui.com/designs/countdown-timer-ui-design-inspiration |  |
| category:email-receipt | Email Receipt | design | 邮件收据，0 条 | REST: collectui_posts?categories=cs.{email-receipt} | 空分类 |
| category:analytics-chart | Analytics Chart | design | 数据分析图表，29 条 | https://collectui.com/designs/analytics-chart-ui-design-inspiration |  |
| category:leaderboard | Leaderboard | design | 排行榜，0 条 | REST: collectui_posts?categories=cs.{leaderboard} | 空分类 |
| category:location-tracker | Location Tracker | design | 位置追踪，0 条 | REST: collectui_posts?categories=cs.{location-tracker} | 空分类 |
| category:tv-app | TV App | design | 电视 App，0 条 | REST: collectui_posts?categories=cs.{tv-app} | 空分类 |
| category:contact-us | Contact Us | design | 联系我们，0 条 | REST: collectui_posts?categories=cs.{contact-us} | 空分类 |
| category:map | Map | design | 地图，10 条 | https://collectui.com/designs/map-ui-design-inspiration |  |
| category:recipe | Recipe | design | 菜谱，0 条 | REST: collectui_posts?categories=cs.{recipe} | 空分类 |
| category:workout-tracker | Workout Tracker | design | 健身记录，1 条 | https://collectui.com/designs/workout-tracker-ui-design-inspiration |  |
| category:food-drink-menu | Food/Drink Menu | design | 餐饮菜单，0 条 | REST: collectui_posts?categories=cs.{food-drink-menu} | 空分类 |
| category:favorites | Favorites | design | 收藏夹，0 条 | REST: collectui_posts?categories=cs.{favorites} | 空分类 |
| category:info-card | Info Card | design | 信息卡片，5 条 | https://collectui.com/designs/info-card-ui-design-inspiration |  |
| category:coming-soon | Coming Soon | design | 即将上线页，1 条 | https://collectui.com/designs/coming-soon-ui-design-inspiration |  |
| category:job-listing | Job Listing | design | 职位列表，2 条 | https://collectui.com/designs/job-listing-ui-design-inspiration |  |
| category:press-page | Press Page | design | 媒体报道页，0 条 | REST: collectui_posts?categories=cs.{press-page} | 空分类 |
| category:header-navigation | Header Navigation | design | 顶部导航，10 条 | https://collectui.com/designs/header-navigation-ui-design-inspiration |  |
| category:breadcrumbs | Breadcrumbs | design | 面包屑，0 条 | REST: collectui_posts?categories=cs.{breadcrumbs} | 空分类 |
| category:video-player | Video Player | design | 视频播放器，0 条 | REST: collectui_posts?categories=cs.{video-player} | 空分类 |
| category:shopping-cart | Shopping Cart | design | 购物车，0 条 | REST: collectui_posts?categories=cs.{shopping-cart} | 空分类 |
| category:background-pattern | Background Pattern | design | 背景图案，4 条 | https://collectui.com/designs/background-pattern-ui-design-inspiration |  |
| category:redeem-coupon | Redeem Coupon | design | 兑换优惠券，0 条 | REST: collectui_posts?categories=cs.{redeem-coupon} | 空分类 |
| category:workout-of-the-day | Workout of the Day | design | 每日训练，0 条 | REST: collectui_posts?categories=cs.{workout-of-the-day} | 空分类 |
| category:select-user-type | Select User Type | design | 选择用户类型，0 条 | REST: collectui_posts?categories=cs.{select-user-type} | 空分类 |
| category:hotel-booking | Hotel Booking | design | 酒店预订，0 条 | REST: collectui_posts?categories=cs.{hotel-booking} | 空分类 |
| category:flight-search | Flight Search | design | 航班搜索，1 条 | https://collectui.com/designs/flight-search-ui-design-inspiration |  |
| category:trending | Trending | design | 热门趋势，0 条 | REST: collectui_posts?categories=cs.{trending} | 空分类 |
| category:event-listing | Event Listing | design | 活动列表，2 条 | https://collectui.com/designs/event-listing-ui-design-inspiration |  |
| category:schedule | Schedule | design | 日程安排，2 条 | https://collectui.com/designs/schedule-ui-design-inspiration |  |
| category:download-app | Download App | design | 下载 App，0 条 | REST: collectui_posts?categories=cs.{download-app} | 空分类 |
| category:notes-widget | Notes Widget | design | 笔记小组件，4 条 | https://collectui.com/designs/notes-widget-ui-design-inspiration |  |
| category:pre-order | Pre-Order | design | 预订购，0 条 | REST: collectui_posts?categories=cs.{pre-order} | 空分类 |
| category:thank-you | Thank You | design | 感谢页，0 条 | REST: collectui_posts?categories=cs.{thank-you} | 空分类 |
| category:date-picker | Date Picker | design | 日期选择器，11 条 | https://collectui.com/designs/date-picker-ui-design-inspiration |  |
| category:form | Form | design | 表单，18 条 | https://collectui.com/designs/form-ui-design-inspiration |  |
| category:progress-bar | Progress Bar | design | 进度条，17 条 | https://collectui.com/designs/progress-bar-ui-design-inspiration |  |
| category:pagination | Pagination | design | 分页，1 条 | https://collectui.com/designs/pagination-ui-design-inspiration |  |
| category:product-tour | Product Tour | design | 产品导览，15 条 | https://collectui.com/designs/product-tour-ui-design-inspiration |  |
| category:in-stock | In Stock | design | 库存状态，0 条 | REST: collectui_posts?categories=cs.{in-stock} | 空分类 |
| category:mobile-menu | Mobile Menu | design | 移动端菜单，6 条 | https://collectui.com/designs/mobile-menu-ui-design-inspiration |  |
| category:giveaway | Giveaway | design | 抽奖赠品，0 条 | REST: collectui_posts?categories=cs.{giveaway} | 空分类 |
| category:avatar | Avatar | design | 头像，2 条 | https://collectui.com/designs/avatar-ui-design-inspiration |  |
| category:itinerary | Itinerary | design | 行程单，1 条 | https://collectui.com/designs/itinerary-ui-design-inspiration |  |
| category:status-update | Status Update | design | 状态更新，1 条 | https://collectui.com/designs/status-update-ui-design-inspiration |  |
| category:splash-screen | Splash Screen | design | 启动页，1 条 | https://collectui.com/designs/splash-screen-ui-design-inspiration |  |
| category:text-editor | Text Editor | design | 文本编辑器，15 条 | https://collectui.com/designs/text-editor-ui-design-inspiration |  |
| category:pending-invitation | Pending Invitation | design | 待处理邀请，0 条 | REST: collectui_posts?categories=cs.{pending-invitation} | 空分类 |
| category:list-items | List Items | design | 列表项，16 条 | https://collectui.com/designs/list-items-ui-design-inspiration |  |
| category:web-animation | Web Animation | design | 网页动画，113 条 | https://collectui.com/designs/web-animation-ui-design-inspiration |  |
| category:ai-agents | AI Agents | design | AI Agent 界面，21 条 | https://collectui.com/designs/ai-agents-ui-design-inspiration |  |
| category:creative-tools | Creative Tools | design | 创意工具，5 条 | https://collectui.com/designs/creative-tools-ui-design-inspiration |  |
| category:color-picker | Color Picker | design | 取色器，9 条 | https://collectui.com/designs/color-picker-ui-design-inspiration |  |
| category:poster | Poster | design | 海报，93 条 | https://collectui.com/designs/poster-ui-design-inspiration |  |
| category:crypto | Crypto | design | 加密货币，13 条 | https://collectui.com/designs/crypto-ui-design-inspiration |  |
| category:virtual-reality | Virtual Reality | design | 虚拟现实，0 条 | REST: collectui_posts?categories=cs.{virtual-reality} | 空分类 |
| category:typography | Typography | design | 字体排版，35 条 | https://collectui.com/designs/typography-ui-design-inspiration |  |
| category:logo | Logo | design | Logo，92 条 | https://collectui.com/designs/logo-ui-design-inspiration |  |
| category:range-slider | Range Slider | design | 范围滑块，29 条 | https://collectui.com/designs/range-slider-ui-design-inspiration |  |
| category:otp-code | OTP Code | design | OTP 验证码，4 条 | https://collectui.com/designs/otp-code-ui-design-inspiration |  |
| category:liquid-metal | Liquid Metal | design | 液态金属，18 条 | https://collectui.com/designs/liquid-metal-ui-design-inspiration |  |
| category:activity-feed | Activity Feed | design | 动态流，3 条 | https://collectui.com/designs/activity-feed-ui-design-inspiration |  |
| category:ui-tips | UI Tips | design | UI 技巧，33 条 | https://collectui.com/designs/ui-tips-ui-design-inspiration |  |
| category:animation | Animation | design | 动画，59 条 | https://collectui.com/designs/animation-ui-design-inspiration |  |
| category:empty-states | Empty States | design | 空状态，8 条 | https://collectui.com/designs/empty-states-ui-design-inspiration |  |
| category:wireframe | Wireframe | design | 线框图，8 条 | https://collectui.com/designs/wireframe-ui-design-inspiration |  |
| category:branding | Branding | design | 品牌设计，171 条 | https://collectui.com/designs/branding-ui-design-inspiration |  |
| category:filter-products | Filter Products | design | 商品筛选，4 条 | https://collectui.com/designs/filter-products-ui-design-inspiration |  |
| category:ai-chat | ai-chat | tag-only | AI 聊天，1 条 | REST: collectui_posts?categories=cs.{ai-chat} | tag-only |
| category:data-table | data-table | tag-only | 数据表格，1 条 | REST: collectui_posts?categories=cs.{data-table} | tag-only |
| category:dropdown-menu | dropdown-menu | tag-only | 下拉菜单，1 条 | REST: collectui_posts?categories=cs.{dropdown-menu} | tag-only |
| category:glassmorphism | glassmorphism | tag-only | 玻璃拟态，1 条 | REST: collectui_posts?categories=cs.{glassmorphism} | tag-only |
| category:gradient | gradient | tag-only | 渐变，1 条 | REST: collectui_posts?categories=cs.{gradient} | tag-only |
| category:metrics-card | metrics-card | tag-only | 指标卡片，1 条 | REST: collectui_posts?categories=cs.{metrics-card} | tag-only |
| category:photo-album | photo-album | tag-only | 相册，3 条 | REST: collectui_posts?categories=cs.{photo-album} | tag-only |
| category:stat-card | stat-card | tag-only | 统计卡片，1 条 | REST: collectui_posts?categories=cs.{stat-card} | tag-only |
## 未解决
- adapter 依赖站点当前的前端结构，站点改版后可能失效；失效时退回浏览器打开分类页 `/designs/{slug}-ui-design-inspiration`，用 read_page 取 `<video>/<img>` 的 src。
- 没有帖子级的公开详情页，也没有描述/配色等结构化标签（只有 title、categories、作者）。
- `/favorites` 和点赞功能需要登录，未测试。
- 旧版 Daily UI 挑战（Dribbble 作品、challenge 编号）已不在现站，旧 challenge 分类大多保留但为空。
- 不提供任何代码、提示词或模板下载。
