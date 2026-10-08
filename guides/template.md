# 整站模板（template）

## 什么时候需要
模板是一整套已经排好的多页站点或应用骨架。适合的情况只有三种：
- 要在很短时间里上线一个**和模板定位基本一致**的站点（作品集、工作室官网、单产品落地页），愿意接受它的版式和视觉语言；
- 想看一个完整站点的信息架构和页面清单，作为自己设计的起点（当参考用）；
- 新开一个 React 项目，需要一个配好框架、Tailwind 和主底座的空骨架。

不适合的情况：已经有项目和主底座；需求和模板定位不同（拿作品集模板改 SaaS 官网）；需要的只是一两个区块（去看 `guides/marketing-section.md`）。改一个视觉语言很强的模板，往往比用主底座从头排更慢，而且容易留下模板自带的演示文案、图片、第二套图标库。

这个任务下免费可用的不多：56 个 template 条目里 46 个是 Pro（originkit 16、reactbits 14、getdesign 13、uiarc 3），按原则不推荐。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:templates`（`npx shadcn@latest init -t next`） | 官方项目骨架，next / vite / start / react-router / astro，单仓和 monorepo 各一份（GitHub `apps/v4/public/r/templates/` 实际列出 10 个 tar.gz）。它只给工程骨架和主题，不给页面设计，正好避免"改模板"的成本。Operate 类应用再加 `shadcn:dashboard-01` 当后台整页起点 |
| uiarc | 无免费模板 | `uiarc:template:arc-saas`、`arc-ai`、`arc-startup` 都是 Pro。用免费 block（`hero-section`、`site-header`、`site-footer`、`cta-section`、`faq-section`）自己拼 |
| 没有底座或其他 | `obsidianui:template:project-one` | MIT，Next.js 16 + React 19 + Tailwind v4 + motion + gsap，shadcn 风格（有 `components.json`、Radix primitive）。同时带营销页和登录后的产品页，是免费里唯一的完整站点（仓库已看） |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| 个人作品集 | `reactbits:pro-template-portfolio-template` | React Bits Pro 里唯一免费的模板，官方页写明可用于个人和商业项目。Next.js 16 + Tailwind v4 + motion + Lenis + Matter.js + next-themes，WebGL 流体 shader 背景 + 磁吸人像，黑白配色。获取方式：文档页没有直接的仓库链接，可能要登录 React Bits Pro 账号下载，未验证 |
| 后台 / 管理端起点 | `shadcn:dashboard-01` | 侧栏 + 指标卡 + 交互面积图 + 可拖拽数据表，全部是 shadcn 组件，依赖 `@tanstack/react-table`、`@dnd-kit/*`、`zod`（registry 已看）。演示数据在 `data.json`，要换 |
| 后台外壳，想要更强的交互 | `obsidianui:dashboard-shell` | 可拖拽缩放侧栏、窄屏变抽屉。`--obsidian-*` 色板要改成 shadcn 变量（见 `_styles.md`） |
| 工作室 / agency 官网 | uiarc 免费 block 自己拼 | 现在就能取码。登录后可换：`originkit:loaded`、`originkit:gency`，作品、评价、流程、FAQ 齐全；免费账号每天只能取 1 个模板；gency 在索引里标的是"Framer 制作"，能不能拿到可维护的 React 源码未验证 |
| SaaS / 多页营销站 | `shadcn:templates` 骨架 + `guides/marketing-section.md` 的区块 | 现在就能取码。登录后可换：`originkit:clever`、`originkit:landfree`，多页营销站模板，未看到源码（取码要登录，条款禁止抓取） |
| 深色个人作品集 | `reactbits:pro-template-portfolio-template`（免费，获取方式见上一行） | 换成深色主题即可。登录后可换：`originkit:darkmate`，索引标注"Framer 静态导出"，源码形态未验证 |

## 慎用
- `obsidianui:template:project-one`：不只是落地页，是一个"创作者经济"产品的完整应用：Prisma + Neon 数据库、`@opennextjs/cloudflare` 部署、reCAPTCHA v3、`/api/waitlist` 和 `/api/newsletter` 接口、登录后的 dashboard / ipos / market / portfolio 页面。`build` 脚本先跑 `prisma generate`，没有数据库配置会失败。另外同时装了 `lucide-react` 和 `react-icons`，违反"一页一套图标"。只想要营销页，就只拷 `components/landing-page/` 并把图标统一成 lucide；features 下有 `feature-card`、`mini-card` 网格，注意等大卡片堆结构的问题。
- originkit 所有模板：需登录，免费账号每天限 1 个；条款禁止把模板再分发或做成付费模板；预览里的字体和图片不在授权范围内，上线前必须换。`styling` 和 `dark_mode` 在 `_styles.md` 里都是 unknown。
- originkit Pro 模板（`operun`、`fintra`、`prismo`、`closor`、`waitlisty` 等 16 个）、reactbits Pro 模板（14 个）、`uiarc:template:*`（3 个）、`getdesign:template-*` 和 `getdesign:product-*`：Pro，不推荐。可以打开它们的公开预览看信息架构，再用免费组件实现。
- `shadcn:preview`、`preview-02`、`preview-03`：这是 shadcn/create 用来展示一整套预设风格的组件拼盘页，不是站点模板，不要当首页用。
- 任何模板都别"整份照搬再改文字"：模板的演示文案、头像、logo、数字、第二套动效库（gsap + motion + lenis 同时在）都会跟着进来。

## 页面模式约束
- Persuade：模板首屏的主导效果数量要先数一遍。React Bits Portfolio 是"整站 shader 背景 + 首屏 shader + 磁吸人像 + 物理 chips"，按预算首屏最多 1 个、整页最多 2 个，用之前要砍。
- Operate：只用 `shadcn:dashboard-01` 这类克制骨架；带 WebGL、平滑滚动、光标特效的营销模板不能拿来做后台。
- Experience：作品集模板可以保留一个为作品服务的主导效果，其余（平滑滚动、物理 chips）视作品量决定，作品图永远是主角。
- Read：不用营销模板；文档站另选文档框架。

## 接入要点
- **先拆再用**：拿到模板先列清单：依赖（动效库、图标库、数据库、第三方服务）、全局 CSS、字体、图片资源、环境变量、接口路由。把不需要的整块删掉，再开始改样式。
- **统一底座**：模板自带的 token 要和项目底座合并成一套（shadcn 项目就落到 shadcn 变量上）；`.dark` 与 `data-theme` 只留一个开关。
- **统一动效库和图标**：motion / framer-motion 只留一个；gsap、three、lenis 只在真正用到的页面引入；图标统一成一套（项目已有的优先，没有就用 lucide）。
- **替换所有演示资源**：文案、头像、logo、统计数字、图片 CDN 地址（如 obsidianui 的 `cdn-new.obsidianui.dev`）。
- **可访问性回归**：模板的平滑滚动（Lenis）会影响键盘翻页和锚点跳转，要测；所有自动动画要遵守 `prefers-reduced-motion`。
- **许可证**：originkit 和 reactbits 都禁止把组件或模板本身再分发；不要把改过的模板公开成"自己的模板"。

## 候选清单
- `shadcn:templates` — 官方项目骨架，默认首选
- `shadcn:dashboard-01` — 后台整页起点
- `obsidianui:template:project-one` — 免费完整站点（营销页 + 应用），依赖重
- `obsidianui:dashboard-shell` — 交互更强的后台外壳
- `reactbits:pro-template-portfolio-template` — 免费作品集模板，获取方式未验证
- `originkit:loaded` — 工作室作品集（需登录）
- `originkit:gency` — agency 多页站（需登录，源码形态未验证）
- `originkit:clever` — agency / SaaS 多页营销站（需登录）
- `originkit:landfree` — 多页营销站（需登录）
- `originkit:outstand` — 设计服务展示（需登录）
- `originkit:capable` — 社区 / 交友产品营销（需登录）
- `originkit:darkmate` — 深色作品集（需登录，Framer 导出未验证）
- 仅参考（Pro，只看公开预览）：`reactbits:pro-template-saas-landing`、`reactbits:pro-template-minimal-landing`、`uiarc:template:arc-startup`
