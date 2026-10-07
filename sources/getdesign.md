---
id: getdesign
name: getdesign.md
url: https://getdesign.md
kind: prompt-library
stack: 任意（DESIGN.md 是给 AI 编码 agent 读的 Markdown 设计规范；付费背景包是 React canvas/WebGL 组件）
license: 76 个免费 DESIGN.md 来自 GitHub VoltAgent/awesome-design-md（MIT，内容声明为对公开设计的独立分析）；付费产品为自定义授权
pro: partial（76 个品牌 DESIGN.md 免费；566 条网站目录的截图、标签、简介免费可看，但对应的 DESIGN.md 原文要付费；Animated Backgrounds 36 个效果、Catalog Pass、Private DESIGN.md、Starter Kit、落地页模板、视频模板都要付费）
fetch: github-raw
verified: 2026-10-07
---
## 是什么 / 什么时候用
VoltAgent 团队维护的 DESIGN.md 合集。DESIGN.md 是一份 Markdown 设计规范，写的是某个知名品牌的视觉语言：YAML front-matter 里放颜色 token 和字号阶梯，正文写间距、组件和动效。把它放在项目根目录，让 agent 先读再写 UI，产出就不会千篇一律。
适合的场景：要"做成 Stripe/Linear/Vercel/Apple 那种感觉"的落地页或 SaaS 界面，或者需要一套现成的配色、字体和组件规则作为起点。免费部分只有 76 个品牌 DESIGN.md。动画背景（包括 shutter-fade）和 550+ 网站目录都是付费内容，只能在线预览、按描述挑效果，拿不到代码。

## 按需获取方法
**A. 免费 DESIGN.md（76 个，全部已实测返回 200 text/markdown）**
- 直接拉原文：`curl -s https://getdesign.md/design-md/{slug}/DESIGN.md -o DESIGN.md`
- CLI：`npx getdesign@latest add {slug}`（写入 ./DESIGN.md，已存在则写到 `{slug}/DESIGN.md`，`--force` 覆盖，`--out <path>` 指定路径）；`npx getdesign list` 列出全部。CLI 自带 76 个模板（npm 包 `templates/*.md` + `manifest.json`），离线即可用。注意 add 会向 `https://getdesign.md/api/cli/downloads` 上报一次下载统计。
- GitHub 镜像：`https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/{slug}/DESIGN.md`。镜像只有 74 个，缺 `discord` 和 `mobbin`，以站点和 npm 为准。
- 渲染预览 HTML：`https://getdesign.md/design-md/{slug}/preview`（浅色）、`/preview-dark`（深色）。旧路径 `preview.html` 会 307 跳转到这里。
- 运行时列出全部免费 slug（实测 76 个）：
  ```bash
  curl -s https://getdesign.md/sitemap.xml | grep -oE 'https://getdesign.md/[^/<]+/design-md<' | sed -E 's#https://getdesign.md/##; s#/design-md<##'
  ```
  也可以读 npm 包里的清单：`npm pack getdesign@latest && tar xzf getdesign-*.tgz && cat package/templates/manifest.json`，每项含 brand、description、templateHash。
- 用法：在 prompt 里写 "Read DESIGN.md before writing any UI. Match the tokens, type scale, and component patterns defined there."
- 实测：`curl -s https://getdesign.md/design-md/stripe/DESIGN.md` 返回 24.6 KB 的 markdown，front-matter 里有 `colors.primary: "#533afd"` 和 Sohne 300 字重的字号阶梯。品牌名做了变形处理（如 "Stripi"），以避开商标。

**B. Animated Backgrounds（36 个，全部付费）**
- 预览：`https://getdesign.md/backgrounds?fx={slug}`，slug 就是效果名转小写、空格换成连字符，36 个都实测过。页面服务端渲染了名称、编号、技术（webgl / canvas-2d）、描述和可调参数（颜色、背景、速度等）。
- 代码只在 $49 的 ZIP 包里（同时附送 Product Demo Video Template），购买 Website Starter Kit 也会送。包里的组件路径是 `app/components/backgrounds/effects/{slug}.tsx`，并附带一个 agent skill。页面上的 "Ask your AI" 示例 prompt 是 "Put Shutter Fade (app/components/backgrounds/effects/shutter-fade.tsx) behind the landing hero in our brand colors"，前提是已经买了包。
- 没有免费代码，也没有 Copy prompt。在线预览的实现在客户端 JS 里，属于付费内容，**没有提取**。需要类似效果时，可以按描述自己实现，或者换用其他免费库。

**C. 网站目录（566 条，付费）**
- 列出：`curl -s https://getdesign.md/sitemap.xml | grep -o 'https://getdesign.md/design-md/[^<]*'`（实测 566 条，页面上显示 "551"）。
- 单条元数据：`curl -s https://getdesign.md/design-md/{slug}`，解析内嵌的 `{item:{slug,title,category,tags,tagline,website,highDemand,...}}`。截图位于 `https://cdn.getdesign.md/catalog/{slug}/thumb.webp` 等路径。`highDemand:!0` 表示属于 Catalog Pass（共 40 条）。
- 目录条目对应的 `/design-md/{slug}/DESIGN.md` 返回 404，页面只有 "Request a DESIGN.md analysis"。这部分的价值仅限于看截图找灵感。

站点没有 llms.txt / registry.json / 公开 JSON API：这些路径都返回 200 的 HTML 回落页，要小心误判。robots.txt 只禁止 `/vibecoder-kit-docs/`。

## 使用注意
- DESIGN.md 只是设计参考，不含组件代码。把它和 shadcn/ui 等组件库搭配，让 agent 按文件里的 token 改主题。
- 一个项目只放一份根目录 DESIGN.md。CLI 遇到已有文件不会覆盖，而是写到子目录，要留意 agent 读的是哪一份。
- 内容按"独立分析、不隶属该品牌"发布，品牌名有变形（Stripi 等），Logo 和商标不能直接商用。
- 免费 slug 的写法与品牌显示名不一定相同：`linear.app`、`mistral.ai`、`x.ai`、`together.ai`、`opencode.ai`、`cal`、`bmw-m`、`dell-1996`、`nintendo-2001`、`theverge`、`runwayml`。另外，付费目录里也有一个独立的 `linear`，和免费的 `linear.app` 不是同一条。
- 背景包用的是 canvas-2d / WebGL，交付形式是"kit 代码里的组件"，具体框架和依赖要买了才能确认。

## 组件清单
免费 DESIGN.md 和 36 个背景逐条列出。566 条付费网站目录超过 500 条，按规范只写到分类级，上文 C 节给出了运行时列举方法（已实测）。
| id | 名称 | 分类 | 一句话用途 | 获取（具体命令或URL） | 备注 |
|---|---|---|---|---|---|
| airbnb | Airbnb | design-md/ecommerce-retail | DESIGN.md 设计规范：旅行民宿平台风格：暖珊瑚色强调、摄影驱动、圆角 UI（电商/零售） | `/design-md/airbnb/DESIGN.md` |  |
| airtable | Airtable | design-md/design-creative | DESIGN.md 设计规范：表格数据库风格：多彩友好、结构化数据美学（设计/创意） | `/design-md/airtable/DESIGN.md` |  |
| apple | Apple | design-md/media-consumer | DESIGN.md 设计规范：苹果消费电子风格：大量留白、SF Pro、电影感大图（媒体/消费） | `/design-md/apple/DESIGN.md` |  |
| binance | Binance | design-md/fintech | DESIGN.md 设计规范：币安交易所风格：黑白底+醒目黄色强调、交易大厅紧迫感（金融科技） | `/design-md/binance/DESIGN.md` |  |
| bmw | BMW | design-md/automotive | DESIGN.md 设计规范：宝马豪华汽车风格：深色高级表面、精密德系工程感（汽车） | `/design-md/bmw/DESIGN.md` |  |
| bmw-m | BMW M | design-md/automotive | DESIGN.md 设计规范：宝马 M 赛车风格：纯黑画布、M 三色条纹、满版摄影（汽车） | `/design-md/bmw-m/DESIGN.md` |  |
| bugatti | Bugatti | design-md/automotive | DESIGN.md 设计规范：布加迪超跑风格：影院黑、单色克制、巨型展示字体（汽车） | `/design-md/bugatti/DESIGN.md` |  |
| cal | Cal.com | design-md/productivity-saas | DESIGN.md 设计规范：Cal.com 开源日程风格：干净中性 UI、开发者向简洁（生产力/SaaS） | `/design-md/cal/DESIGN.md` |  |
| claude | Claude | design-md/ai-ml | DESIGN.md 设计规范：Claude/Anthropic 风格：暖赤陶色强调、干净编辑式排版（AI/机器学习） | `/design-md/claude/DESIGN.md` |  |
| clay | Clay | design-md/design-creative | DESIGN.md 设计规范：Clay 创意机构风格：有机形状、柔和渐变、艺术指导式布局（设计/创意） | `/design-md/clay/DESIGN.md` |  |
| clickhouse | ClickHouse | design-md/backend-devops | DESIGN.md 设计规范：ClickHouse 分析数据库风格：黄色强调、技术文档式（后端/DevOps） | `/design-md/clickhouse/DESIGN.md` |  |
| cohere | Cohere | design-md/ai-ml | DESIGN.md 设计规范：Cohere 企业 AI 风格：鲜艳渐变、数据密集 dashboard（AI/机器学习） | `/design-md/cohere/DESIGN.md` |  |
| coinbase | Coinbase | design-md/fintech | DESIGN.md 设计规范：Coinbase 交易所风格：干净蓝色、可信赖机构感（金融科技） | `/design-md/coinbase/DESIGN.md` |  |
| composio | Composio | design-md/backend-devops | DESIGN.md 设计规范：Composio 工具集成平台风格：现代深色+彩色集成图标（后端/DevOps） | `/design-md/composio/DESIGN.md` |  |
| cursor | Cursor | design-md/developer-tools | DESIGN.md 设计规范：Cursor AI 编辑器风格：利落深色界面、渐变强调（开发者工具） | `/design-md/cursor/DESIGN.md` |  |
| dell-1996 | Dell (1996) | design-md/media-consumer | DESIGN.md 设计规范：1996 年戴尔复古网页风格：黑色页框、扁平色块卡片、Helvetica Black+Times（媒体/消费） | `/design-md/dell-1996/DESIGN.md` |  |
| discord | Discord | design-md/productivity-saas | DESIGN.md 设计规范：Discord 社区聊天风格：深靛蓝画布、Blurple 渐变、粗体全大写标题（生产力/SaaS） | `/design-md/discord/DESIGN.md` |  |
| elevenlabs | ElevenLabs | design-md/ai-ml | DESIGN.md 设计规范：ElevenLabs AI 语音风格：深色电影感、音频波形美学（AI/机器学习） | `/design-md/elevenlabs/DESIGN.md` |  |
| expo | Expo | design-md/developer-tools | DESIGN.md 设计规范：Expo React Native 平台风格：深色主题、紧凑字距、代码为中心（开发者工具） | `/design-md/expo/DESIGN.md` |  |
| ferrari | Ferrari | design-md/automotive | DESIGN.md 设计规范：法拉利风格：明暗对比编辑式、法拉利红强调、电影黑（汽车） | `/design-md/ferrari/DESIGN.md` |  |
| figma | Figma | design-md/design-creative | DESIGN.md 设计规范：Figma 协作设计工具风格：鲜艳多彩、俏皮又专业（设计/创意） | `/design-md/figma/DESIGN.md` |  |
| framer | Framer | design-md/design-creative | DESIGN.md 设计规范：Framer 建站工具风格：黑蓝大胆、动效优先、设计前卫（设计/创意） | `/design-md/framer/DESIGN.md` |  |
| hashicorp | HashiCorp | design-md/backend-devops | DESIGN.md 设计规范：HashiCorp 基础设施风格：企业级干净黑白（后端/DevOps） | `/design-md/hashicorp/DESIGN.md` |  |
| hp | HP | design-md/media-consumer | DESIGN.md 设计规范：惠普电子产品目录风格：白底电光蓝强调、尖角 V 形图案（媒体/消费） | `/design-md/hp/DESIGN.md` |  |
| ibm | IBM | design-md/media-consumer | DESIGN.md 设计规范：IBM 企业科技风格：Carbon 设计系统、结构化蓝色调（媒体/消费） | `/design-md/ibm/DESIGN.md` |  |
| intercom | Intercom | design-md/productivity-saas | DESIGN.md 设计规范：Intercom 客服消息风格：友好蓝色、对话式 UI 模式（生产力/SaaS） | `/design-md/intercom/DESIGN.md` |  |
| kraken | Kraken | design-md/fintech | DESIGN.md 设计规范：Kraken 加密交易风格：紫色强调深色 UI、数据密集 dashboard（金融科技） | `/design-md/kraken/DESIGN.md` |  |
| lamborghini | Lamborghini | design-md/automotive | DESIGN.md 设计规范：兰博基尼超跑风格：纯黑表面、金色强调、戏剧化大写字体（汽车） | `/design-md/lamborghini/DESIGN.md` |  |
| linear.app | Linear | design-md/productivity-saas | DESIGN.md 设计规范：Linear 项目管理风格：极简精确、紫色强调（SaaS 常用参考）（生产力/SaaS） | `/design-md/linear.app/DESIGN.md` |  |
| lovable | Lovable | design-md/developer-tools | DESIGN.md 设计规范：Lovable AI 全栈构建器风格：俏皮渐变、友好开发者美学（开发者工具） | `/design-md/lovable/DESIGN.md` |  |
| mastercard | Mastercard | design-md/fintech | DESIGN.md 设计规范：万事达风格：暖奶油画布、轨道胶囊形状、编辑式温暖（金融科技） | `/design-md/mastercard/DESIGN.md` |  |
| meta | Meta | design-md/ecommerce-retail | DESIGN.md 设计规范：Meta 商店风格：摄影优先、明暗二元表面、Meta 蓝 CTA（电商/零售） | `/design-md/meta/DESIGN.md` |  |
| minimax | MiniMax | design-md/ai-ml | DESIGN.md 设计规范：MiniMax AI 模型风格：大胆深色界面+霓虹强调（AI/机器学习） | `/design-md/minimax/DESIGN.md` |  |
| mintlify | Mintlify | design-md/productivity-saas | DESIGN.md 设计规范：Mintlify 文档平台风格：干净、绿色强调、为阅读优化（文档站参考）（生产力/SaaS） | `/design-md/mintlify/DESIGN.md` |  |
| miro | Miro | design-md/design-creative | DESIGN.md 设计规范：Miro 白板协作风格：亮黄强调、无限画布美学（设计/创意） | `/design-md/miro/DESIGN.md` |  |
| mistral.ai | Mistral AI | design-md/ai-ml | DESIGN.md 设计规范：Mistral AI 风格：法式工程极简、紫色调（AI/机器学习） | `/design-md/mistral.ai/DESIGN.md` |  |
| mobbin | Mobbin | design-md/design-creative | DESIGN.md 设计规范：Mobbin UI 参考库风格：画廊白单色、体育场形胶囊、电光蓝强调（设计/创意） | `/design-md/mobbin/DESIGN.md` |  |
| mongodb | MongoDB | design-md/backend-devops | DESIGN.md 设计规范：MongoDB 文档数据库风格：绿叶品牌、开发者文档为主（后端/DevOps） | `/design-md/mongodb/DESIGN.md` |  |
| nike | Nike | design-md/ecommerce-retail | DESIGN.md 设计规范：耐克运动零售风格：单色 UI、巨型大写字体、满版摄影（电商/零售） | `/design-md/nike/DESIGN.md` |  |
| nintendo-2001 | Nintendo.com (2001) | design-md/media-consumer | DESIGN.md 设计规范：2001 年任天堂 Y2K 复古网页风格：拉丝长春花金属面板、琥珀色导航（媒体/消费） | `/design-md/nintendo-2001/DESIGN.md` |  |
| notion | Notion | design-md/productivity-saas | DESIGN.md 设计规范：Notion 工作区风格：温暖极简、衬线标题、柔和表面（生产力/SaaS） | `/design-md/notion/DESIGN.md` |  |
| nvidia | NVIDIA | design-md/media-consumer | DESIGN.md 设计规范：NVIDIA 风格：绿黑能量感、技术力量美学（媒体/消费） | `/design-md/nvidia/DESIGN.md` |  |
| ollama | Ollama | design-md/ai-ml | DESIGN.md 设计规范：Ollama 本地 LLM 风格：终端优先、单色简洁（AI/机器学习） | `/design-md/ollama/DESIGN.md` |  |
| opencode.ai | OpenCode | design-md/ai-ml | DESIGN.md 设计规范：OpenCode AI 编码平台风格：开发者向深色主题（AI/机器学习） | `/design-md/opencode.ai/DESIGN.md` |  |
| pinterest | Pinterest | design-md/media-consumer | DESIGN.md 设计规范：Pinterest 风格：红色强调、瀑布流 masonry 网格、图片优先（媒体/消费） | `/design-md/pinterest/DESIGN.md` |  |
| playstation | PlayStation | design-md/media-consumer | DESIGN.md 设计规范：PlayStation 风格：三层频道式布局、沉稳展示字体、青色 hover 放大（媒体/消费） | `/design-md/playstation/DESIGN.md` |  |
| posthog | PostHog | design-md/backend-devops | DESIGN.md 设计规范：PostHog 产品分析风格：俏皮刺猬品牌、开发者友好深色 UI（后端/DevOps） | `/design-md/posthog/DESIGN.md` |  |
| raycast | Raycast | design-md/developer-tools | DESIGN.md 设计规范：Raycast 启动器风格：利落深色外壳、鲜艳渐变强调（开发者工具） | `/design-md/raycast/DESIGN.md` |  |
| renault | Renault | design-md/automotive | DESIGN.md 设计规范：雷诺汽车风格：极光渐变、NouvelR 字体、大胆能量（汽车） | `/design-md/renault/DESIGN.md` |  |
| replicate | Replicate | design-md/ai-ml | DESIGN.md 设计规范：Replicate 模型 API 风格：干净白底、代码前置（AI/机器学习） | `/design-md/replicate/DESIGN.md` |  |
| resend | Resend | design-md/productivity-saas | DESIGN.md 设计规范：Resend 邮件 API 风格：极简深色、等宽字体点缀（生产力/SaaS） | `/design-md/resend/DESIGN.md` |  |
| revolut | Revolut | design-md/fintech | DESIGN.md 设计规范：Revolut 数字银行风格：利落深色、渐变卡片、金融精确感（金融科技） | `/design-md/revolut/DESIGN.md` |  |
| runwayml | Runway | design-md/ai-ml | DESIGN.md 设计规范：Runway AI 视频风格：电影感深色 UI、富媒体布局（AI/机器学习） | `/design-md/runwayml/DESIGN.md` |  |
| sanity | Sanity | design-md/backend-devops | DESIGN.md 设计规范：Sanity 无头 CMS 风格：红色强调、内容优先编辑式布局（后端/DevOps） | `/design-md/sanity/DESIGN.md` |  |
| sentry | Sentry | design-md/backend-devops | DESIGN.md 设计规范：Sentry 错误监控风格：深色 dashboard、数据密集、粉紫强调（后端/DevOps） | `/design-md/sentry/DESIGN.md` |  |
| shopify | Shopify | design-md/ecommerce-retail | DESIGN.md 设计规范：Shopify 电商平台风格：深色优先电影感、霓虹绿强调、超细字重（电商/零售） | `/design-md/shopify/DESIGN.md` |  |
| slack | Slack | design-md/productivity-saas | DESIGN.md 设计规范：Slack 风格：深茄紫主色、奶油薰衣草 hero 渐变、胶囊 CTA（生产力/SaaS） | `/design-md/slack/DESIGN.md` |  |
| spacex | SpaceX | design-md/media-consumer | DESIGN.md 设计规范：SpaceX 风格：黑白强烈对比、满版图片、未来感（媒体/消费） | `/design-md/spacex/DESIGN.md` |  |
| spotify | Spotify | design-md/media-consumer | DESIGN.md 设计规范：Spotify 风格：深色底鲜绿、粗字体、专辑封面驱动（媒体/消费） | `/design-md/spotify/DESIGN.md` |  |
| starbucks | Starbucks | design-md/ecommerce-retail | DESIGN.md 设计规范：星巴克风格：四级绿色体系、暖奶油画布、全胶囊按钮（电商/零售） | `/design-md/starbucks/DESIGN.md` |  |
| stripe | Stripe | design-md/fintech | DESIGN.md 设计规范：Stripe 支付风格：标志性紫色渐变、300 细字重优雅（金融 SaaS 落地页常用参考）（金融科技） | `/design-md/stripe/DESIGN.md` |  |
| supabase | Supabase | design-md/backend-devops | DESIGN.md 设计规范：Supabase 风格：深色翡翠绿主题、代码优先（后端/DevOps） | `/design-md/supabase/DESIGN.md` |  |
| superhuman | Superhuman | design-md/developer-tools | DESIGN.md 设计规范：Superhuman 邮件客户端风格：高级深色、键盘优先、紫色辉光（开发者工具） | `/design-md/superhuman/DESIGN.md` |  |
| tesla | Tesla | design-md/automotive | DESIGN.md 设计规范：特斯拉风格：极度减法、全屏摄影、近乎零 UI（汽车） | `/design-md/tesla/DESIGN.md` |  |
| theverge | The Verge | design-md/media-consumer | DESIGN.md 设计规范：The Verge 科技媒体风格：酸薄荷+紫外强调、Manuka 字体、锐舞海报式卡片（媒体/消费） | `/design-md/theverge/DESIGN.md` |  |
| together.ai | Together AI | design-md/ai-ml | DESIGN.md 设计规范：Together AI 风格：技术感蓝图式设计（AI/机器学习） | `/design-md/together.ai/DESIGN.md` |  |
| uber | Uber | design-md/media-consumer | DESIGN.md 设计规范：Uber 风格：黑白大胆、紧凑字体、都市能量（媒体/消费） | `/design-md/uber/DESIGN.md` |  |
| vercel | Vercel | design-md/developer-tools | DESIGN.md 设计规范：Vercel 风格：黑白精确、Geist 字体（开发者工具常用参考）（开发者工具） | `/design-md/vercel/DESIGN.md` |  |
| vodafone | Vodafone | design-md/media-consumer | DESIGN.md 设计规范：沃达丰电信风格：巨型大写展示字、沃达丰红章节色带（媒体/消费） | `/design-md/vodafone/DESIGN.md` |  |
| voltagent | VoltAgent | design-md/ai-ml | DESIGN.md 设计规范：VoltAgent AI agent 框架风格：虚空黑画布、翡翠绿强调、终端原生（AI/机器学习） | `/design-md/voltagent/DESIGN.md` |  |
| warp | Warp | design-md/developer-tools | DESIGN.md 设计规范：Warp 终端风格：类 IDE 深色界面、块状命令 UI（开发者工具） | `/design-md/warp/DESIGN.md` |  |
| webflow | Webflow | design-md/design-creative | DESIGN.md 设计规范：Webflow 可视化建站风格：蓝色强调、精致营销站美学（设计/创意） | `/design-md/webflow/DESIGN.md` |  |
| wired | WIRED | design-md/media-consumer | DESIGN.md 设计规范：WIRED 杂志风格：纸白大报密度、定制衬线展示字、等宽小标、墨蓝链接（媒体/消费） | `/design-md/wired/DESIGN.md` |  |
| wise | Wise | design-md/fintech | DESIGN.md 设计规范：Wise 跨境汇款风格：亮绿强调、友好清晰（金融科技） | `/design-md/wise/DESIGN.md` |  |
| x.ai | xAI | design-md/ai-ml | DESIGN.md 设计规范：xAI 风格：强烈单色、未来极简（AI/机器学习） | `/design-md/x.ai/DESIGN.md` |  |
| zapier | Zapier | design-md/productivity-saas | DESIGN.md 设计规范：Zapier 自动化平台风格：暖橙色、友好插画驱动（生产力/SaaS） | `/design-md/zapier/DESIGN.md` |  |
| bg-glow-threads | Glow Threads | background/webgl | 动画背景 一束束发光丝线在画面中漂移，扇形随距离弯曲并呼吸；hero 背景；webgl，可调 Color 1, Color 2, Color 3, Background, Speed, Threads | `/backgrounds?fx=glow-threads` | pro |
| bg-ink-halftone | Ink Halftone | background/canvas-2d | 动画背景 印刷风半调网点，点半径随行进波起伏；复古 halftone 背景；canvas-2d，可调 Color, Background, Speed | `/backgrounds?fx=ink-halftone` | pro |
| bg-comet-cascade | Comet Cascade | background/canvas-2d | 动画背景 彗星尾迹从中间倾泻而下，近底部向外偏转像喷泉撞玻璃；canvas-2d，可调 Color 1, Color 2, Color 3, Background, Speed, Trails | `/backgrounds?fx=comet-cascade` | pro |
| bg-velvet-sweep | Velvet Sweep | background/webgl | 动画背景 一条弯曲发光丝绸带横扫画面，其余保持暗色；webgl，可调 Color, Background, Speed | `/backgrounds?fx=velvet-sweep` | pro |
| bg-signal-grid | Signal Grid | background/canvas-2d | 动画背景 细密方格网静静闪烁，一侧密集向另一侧渐隐；科技网格背景；canvas-2d，可调 Color, Background, Speed, Anchor | `/backgrounds?fx=signal-grid` | pro |
| bg-nimbus-twist | Nimbus Twist | background/webgl | 动画背景 画面中央呼吸的光环，鼠标靠近会扭成触须并加速旋转；交互式；webgl，可调 Color 1, Color 2, Color 3, Background, Speed | `/backgrounds?fx=nimbus-twist` | pro |
| bg-dot-bloom | Dot Bloom | background/canvas-2d | 动画背景 半调点阵上漂移的光斑云团，形成、变形、滑过网格；canvas-2d，可调 Color, Background, Speed, Density | `/backgrounds?fx=dot-bloom` | pro |
| bg-silk-flow | Silk Flow | background/webgl | 动画背景 满版丝绸褶皱横向漂移，专为放在 hero 内容后面；webgl，可调 Color 1, Color 2, Color 3, Background, Speed | `/backgrounds?fx=silk-flow` | pro |
| bg-storm-bolt | Storm Bolt | background/webgl | 动画背景 一道闪电劈下画面，每隔几秒换路径重新劈击并频闪；webgl，可调 Color, Background, Speed | `/backgrounds?fx=storm-bolt` | pro |
| bg-glyph-tide | Glyph Tide | background/canvas-2d | 动画背景 终端字符阶梯随波场呼吸，纯文字 ASCII canvas 背景；canvas-2d，可调 Color, Background, Speed, Characters | `/backgrounds?fx=glyph-tide` | pro |
| bg-aurora-spire | Aurora Spire | background/webgl | 动画背景 缓慢上升的光柱，丝绸般的极光帷幕在其中缠绕；webgl，可调 Color 1, Color 2, Color 3, Background, Speed | `/backgrounds?fx=aurora-spire` | pro |
| bg-photon-rush | Photon Rush | background/canvas-2d | 动画背景 超空间跃迁：明亮光束从暗核径向飞出；星际穿越效果；canvas-2d，可调 Color 1, Color 2, Color 3, Background, Speed, Streaks | `/backgrounds?fx=photon-rush` | pro |
| bg-mist-orb | Mist Orb | background/webgl | 动画背景 缓慢旋转的雾气球体，雾丝层层包裹并溢出边缘；webgl，可调 Color, Background, Speed | `/backgrounds?fx=mist-orb` | pro |
| bg-dither-drift | Dither Drift | background/canvas-2d | 动画背景 平滑波带经 Bayer 矩阵量化成复古有序抖动 dither；canvas-2d，可调 Color, Background, Speed | `/backgrounds?fx=dither-drift` | pro |
| bg-laser-field | Laser Field | background/canvas-2d | 动画背景 发光激光基线，细光束从中呼吸升起，火花在暗处上飘；canvas-2d，可调 Color, Background, Speed, Beams | `/backgrounds?fx=laser-field` | pro |
| bg-mercury-veins | Mercury Veins | background/webgl | 动画背景 翻涌的液态金属池，白热脉络穿过暗铬，鼠标可搅动；webgl，可调 Color, Background, Speed | `/backgrounds?fx=mercury-veins` | pro |
| bg-horizon-grid | Horizon Grid | background/canvas-2d | 动画背景 无尽地面网格向观者滚动，地平线发光；合成波 synthwave 风；canvas-2d，可调 Color, Background, Speed | `/backgrounds?fx=horizon-grid` | pro |
| bg-echo-rings | Echo Rings | background/webgl | 动画背景 柔和彩色圆环从画面底部拱起，色相由内向外漂移并涟漪扩散；webgl，可调 Color 1, Color 2, Color 3, Background, Speed | `/backgrounds?fx=echo-rings` | pro |
| bg-satin-streaks | Satin Streaks | background/webgl | 动画背景 长对角光迹如缓慢摇移的缎面：宽柔光带+细闪线；webgl，可调 Color 1, Color 2, Color 3, Background, Speed | `/backgrounds?fx=satin-streaks` | pro |
| bg-star-surge | Star Surge | background/canvas-2d | 动画背景 星空从中心向外冲出：核心闪烁点、边缘运动模糊拖尾；canvas-2d，可调 Color, Background, Speed, Stars | `/backgrounds?fx=star-surge` | pro |
| bg-vapor-ribbons | Vapor Ribbons | background/webgl | 动画背景 几条宽大朦胧彩带蛇行穿过画面，无硬边；webgl，可调 Color 1, Color 2, Color 3, Background, Speed | `/backgrounds?fx=vapor-ribbons` | pro |
| bg-crest-columns | Crest Columns | background/canvas-2d | 动画背景 竖向渐变柱，每根顶端发光波峰线沿 V 形波滚动；canvas-2d，可调 Color, Background, Speed, Columns | `/backgrounds?fx=crest-columns` | pro |
| bg-light-strands | Light Strands | background/canvas-2d | 动画背景 数十条叠加光丝编织成丝滑渐变带，带胶片颗粒；canvas-2d，可调 Color 1, Color 2, Color 3, Background, Speed | `/backgrounds?fx=light-strands` | pro |
| bg-opal-film | Opal Film | background/webgl | 动画背景 明亮的薄膜虹彩，彩虹条纹沿揉动场流动；全套唯一浅色背景；webgl，可调 Color, Background, Speed | `/backgrounds?fx=opal-film` | pro |
| bg-pulse-beams | Pulse Beams | background/webgl | 动画背景 一面竖向光柱墙，每根以各自节奏闪烁，柔和泛光；webgl，可调 Color, Background, Speed, Beams | `/backgrounds?fx=pulse-beams` | pro |
| bg-marble-flux | Marble Flux | background/webgl | 动画背景 光泽流体褶皱慢动作自我揉捏，像影棚灯下浇注的釉面；webgl，可调 Color, Background, Speed | `/backgrounds?fx=marble-flux` | pro |
| bg-shutter-fade | Shutter Fade | background/webgl | 动画背景 三段渐变被切成倾斜百叶窗，平时暗，跟随鼠标的聚光灯照亮经过的叶片；交互式；webgl，可调 Color 1, Color 2, Color 3, Background, Speed, Blinds | `/backgrounds?fx=shutter-fade` | pro |
| bg-orbit-trails | Orbit Trails | background/canvas-2d | 动画背景 细光弧绕共同中心旋转如长曝光星轨，内圈快外圈慢；canvas-2d，可调 Color 1, Color 2, Color 3, Background, Speed, Trails | `/backgrounds?fx=orbit-trails` | pro |
| bg-gumball-drop | Gumball Drop | background/canvas-2d | 动画背景 光泽小球在真实 2D 物理下滚落进坑，鼠标可挤开球堆；交互式；canvas-2d，可调 Color 1, Color 2, Color 3, Background, Speed, Balls | `/backgrounds?fx=gumball-drop` | pro |
| bg-veil-rays | Veil Rays | background/webgl | 动画背景 柔和体积光自上方落下：有机光束、呼吸光锥、胶片颗粒；webgl，可调 Color, Background, Speed | `/backgrounds?fx=veil-rays` | pro |
| bg-neon-wash | Neon Wash | background/webgl | 动画背景 霓虹灯管像真的一样点亮：闪烁、光从上到下铺满墙面后稳定；webgl，可调 Color, Background, Speed | `/backgrounds?fx=neon-wash` | pro |
| bg-dusk-filaments | Dusk Filaments | background/webgl | 动画背景 层叠霓虹细丝沿同一条 S 曲线，暖色光带滑过并带色差边；webgl，可调 Color 1, Color 2, Color 3, Background, Speed | `/backgrounds?fx=dusk-filaments` | pro |
| bg-molten-panes | Molten Panes | background/webgl | 动画背景 竖向玻璃格内缓慢上升的液态铬，形成光泽褶皱；webgl，可调 Color 1, Color 2, Color 3, Background, Speed, Panes | `/backgrounds?fx=molten-panes` | pro |
| bg-helix-haze | Helix Haze | background/webgl | 动画背景 一股细纤维绳拧过画面，刻意暗淡，作为缓慢旋转的纹理；webgl，可调 Color, Background, Speed | `/backgrounds?fx=helix-haze` | pro |
| bg-dawn-current | Dawn Current | background/webgl | 动画背景 一股柔光在画面中部流过，色相滑动，全画面无硬边；webgl，可调 Color 1, Color 2, Color 3, Background, Speed | `/backgrounds?fx=dawn-current` | pro |
| bg-pixel-pulse | Pixel Pulse | background/canvas-2d | 动画背景 圆角方格 LED 墙从中心向外脉冲同心圆环；canvas-2d，可调 Color, Background, Speed, Density | `/backgrounds?fx=pixel-pulse` | pro |
| category:catalog-productivity-saas | Website catalog · productivity-saas | catalog/productivity-saas | 网站设计分析目录（生产力/SaaS）221 条：真实网站截图+标签，DESIGN.md 需购买/申请，无免费原文 | curl -s https://getdesign.md/sitemap.xml / grep -o 'https://getdesign.md/design-md/[^<]*' | pro |
| category:catalog-design-creative | Website catalog · design-creative | catalog/design-creative | 网站设计分析目录（设计/创意）74 条：真实网站截图+标签，DESIGN.md 需购买/申请，无免费原文 | curl -s https://getdesign.md/sitemap.xml / grep -o 'https://getdesign.md/design-md/[^<]*' | pro |
| category:catalog-ai-ml | Website catalog · ai-ml | catalog/ai-ml | 网站设计分析目录（AI/机器学习）72 条：真实网站截图+标签，DESIGN.md 需购买/申请，无免费原文 | curl -s https://getdesign.md/sitemap.xml / grep -o 'https://getdesign.md/design-md/[^<]*' | pro |
| category:catalog-fintech | Website catalog · fintech | catalog/fintech | 网站设计分析目录（金融科技）62 条：真实网站截图+标签，DESIGN.md 需购买/申请，无免费原文 | curl -s https://getdesign.md/sitemap.xml / grep -o 'https://getdesign.md/design-md/[^<]*' | pro |
| category:catalog-developer-tools | Website catalog · developer-tools | catalog/developer-tools | 网站设计分析目录（开发者工具）56 条：真实网站截图+标签，DESIGN.md 需购买/申请，无免费原文 | curl -s https://getdesign.md/sitemap.xml / grep -o 'https://getdesign.md/design-md/[^<]*' | pro |
| category:catalog-media-consumer | Website catalog · media-consumer | catalog/media-consumer | 网站设计分析目录（媒体/消费）52 条：真实网站截图+标签，DESIGN.md 需购买/申请，无免费原文 | curl -s https://getdesign.md/sitemap.xml / grep -o 'https://getdesign.md/design-md/[^<]*' | pro |
| category:catalog-backend-devops | Website catalog · backend-devops | catalog/backend-devops | 网站设计分析目录（后端/DevOps）17 条：真实网站截图+标签，DESIGN.md 需购买/申请，无免费原文 | curl -s https://getdesign.md/sitemap.xml / grep -o 'https://getdesign.md/design-md/[^<]*' | pro |
| category:catalog-ecommerce-retail | Website catalog · ecommerce-retail | catalog/ecommerce-retail | 网站设计分析目录（电商/零售）12 条：真实网站截图+标签，DESIGN.md 需购买/申请，无免费原文 | curl -s https://getdesign.md/sitemap.xml / grep -o 'https://getdesign.md/design-md/[^<]*' | pro |
| category:catalog-pass | Catalog Pass 精选集 | catalog/pass | Catalog Pass 包含的 40 个网站 DESIGN.md（目录中 highDemand=true 的条目），订阅后可下载 | https://getdesign.md/design-md-pass | pro |
| product-backgrounds-bundle | Animated Backgrounds 包 | product/backgrounds | 36 个 canvas/WebGL 动画背景组件 + agent skill，ZIP 交付，$49 一次性（附送 Product Demo Video Template） | https://getdesign.md/backgrounds | pro |
| product-video-template | Product Demo Video Template | product/video | 产品演示视频模板（可用 Claude Code 等编辑的工程文件），$49，与背景包同价捆绑 | https://getdesign.md/video-template | pro |
| product-private-design-md | Private DESIGN.md | product/design-md | 按你给的网站 URL 定制分析出 DESIGN.md（明暗两套+预览页），$39 一次性 | https://getdesign.md/request | pro |
| product-catalog-pass | Catalog Pass | product/design-md | 月度订阅 $99/mo，40 个精选网站 DESIGN.md，每月新增 5+ | https://getdesign.md/design-md-pass | pro |
| product-website-starter-kit | Website Starter Kit | product/starter-kit | 面向 AI 编码工具的全栈网站起步套件（React/TanStack/Vite/Tailwind/shadcn/Supabase/Stripe 等），含 DESIGN.md，附送背景包，$249 终身 | https://getdesign.md/website-starter-kit  | pro |
| product-mobile-starter-kit | Mobile App Starter Kit | product/starter-kit | Expo + React Native 移动 App 起步套件（登录、支付、通知、上架配置），$249 终身 | https://getdesign.md/mobile-starter-kit | pro |
| product-brand-kit | {slug} Website Starter Kit + DESIGN.md | product/starter-kit | 任一免费 DESIGN.md 品牌对应的"同风格网站起步套件"，$249 | https://getdesign.md/{slug}/design-md/kit | pro |
| template-custom-design-md | Custom DESIGN.md | product/landing-template | Pro 落地页模板「Custom DESIGN.md」：完整源码+DESIGN.md，基于 Website Starter Kit，$249 一次性 | https://getdesign.md/landing-page-templates/custom-design-md | pro |
| template-saas-landing-page | SaaS Landing Page | product/landing-template | Pro 落地页模板「SaaS Landing Page」：完整源码+DESIGN.md，基于 Website Starter Kit，$249 一次性 | https://getdesign.md/landing-page-templates/saas-landing-page | pro |
| template-personal-website | Personal Website | product/landing-template | Pro 落地页模板「Personal Website」：完整源码+DESIGN.md，基于 Website Starter Kit，$249 一次性 | https://getdesign.md/landing-page-templates/personal-website | pro |
| template-portfolio-website-template | Portfolio Website Template | product/landing-template | Pro 落地页模板「Portfolio Website Template」：完整源码+DESIGN.md，基于 Website Starter Kit，$249 一次性 | https://getdesign.md/landing-page-templates/portfolio-website-template | pro |
| template-startup-website-template | Startup Website Template | product/landing-template | Pro 落地页模板「Startup Website Template」：完整源码+DESIGN.md，基于 Website Starter Kit，$249 一次性 | https://getdesign.md/landing-page-templates/startup-website-template | pro |
| template-business-website-template | Business Website Template | product/landing-template | Pro 落地页模板「Business Website Template」：完整源码+DESIGN.md，基于 Website Starter Kit，$249 一次性 | https://getdesign.md/landing-page-templates/business-website-template | pro |
| category:collections | Collections（OpenClaw 技能集合 SEO 页） | misc/collections | 4 个集合页（best-openclaw/automation/developer-productivity/content-creation），内容是免费 DESIGN.md 的小子集 | https://getdesign.md/collections/{name} |  |
| category:integrations | Integrations（SEO 页） | misc/integrations | 17 个 "Designs for {工具}" 页，SSR 显示 No designs matched，无实质内容 | https://getdesign.md/integrations/{name} | broken |
| guide-what-is-design-md | What is DESIGN.md / State of DESIGN.md 2026 / Blog | misc/docs | DESIGN.md 格式说明、年度报告、5 篇博客（落地页模板、单页网站、个人网站、SaaS 点子、web design md） | https://getdesign.md/what-is-design-md  |  |

## 未解决
- Animated Backgrounds 的 36 个效果（包括用户收藏的 shutter-fade）只有付费 ZIP 提供代码，按规范不购买、不提取客户端预览代码。目前只拿到名称、技术栈、描述、可调参数和组件路径。
- 566 条网站目录的 DESIGN.md 需要 Catalog Pass（$99/月，含 40 条）或单独购买/申请（Private DESIGN.md $39）。站点 SSR 里看不到单条的购买价格。
- integrations/* 的 17 个页面在 SSR 中显示 "No designs matched"，可能要靠客户端加载，也可能本来就是空的 SEO 页。没有深究。
- 目录总数：页面显示 551，sitemap 有 566 条，差额原因不明（可能包括下架或未分类的条目）。

## 网站目录（2026-10-07 补充）
566 条网站目录已逐条写进 getdesign.tsv，id 为 `site:{slug}`，用法是"仅参考"，访问状态 free。
- 免费可看：每个网站的整页截图 `https://cdn.getdesign.md/catalog/{slug}/{page}.webp|jpg`（1–7 页）、风格标签和简介。`fetch.sh getdesign:site:{slug}` 会下载首页截图。
- 要付费的：对应的 DESIGN.md 原文，包括 Catalog Pass 里的 40 条精选（描述里标了"Catalog Pass 精选"）。
- 例外：linear 有免费的 DESIGN.md，对应条目是 `getdesign:linear.app`。
- 元数据来源：页面内嵌的 `item:{slug,title,category,tags,tagline,website,pages,highDemand,designMdSlug}`。注意 `highDemand` 有时排在 `title` 前面，要逐字段解析。robots.txt 允许抓取 `/design-md/`。
