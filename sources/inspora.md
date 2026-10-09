---
id: inspora
name: Inspora
url: https://www.inspora.design/
kind: inspiration
stack: 任意（纯参考图/视频，无代码）
license: 未声明（作品版权归原作者，多数转自 X/Twitter）
pro: none
fetch: browse-only
coverage: 人工快照：每个分类首屏的条目；robots.txt 禁止 /api/，不自动刷新，不保证全站完整
catalog_checked: 2026-10-07
source_status: active
visual_style: trend-driven motion and product ui references
foundation: n/a
styling: n/a
motion_lib: none
dark_mode: n/a
mixing_notes: 只借鉴布局和动效节奏，液态玻璃、shader 卡片这类强风格只在主底座能表达时才用，颜色字体按主底座实现
---
## 是什么 / 什么时候用
Inspora 是一个"每小时更新"的视觉设计灵感策展站，收录近期 X/Twitter 上的 UI、动效、品牌、插画作品，绝大多数是短视频（258/287 条为 mp4，29 条为静态图）。强项是**微交互与动效**（Motion 129 条）、**产品界面卡片/组件**（Product 65 条）、**网页区块**（Web 42 条：footer、hero、portfolio、bento、FAQ）。没有代码、没有提示词、没有模板下载，只能当视觉参考。
适用场景：要做一个"有质感"的组件/交互（液态玻璃、shader 卡片、AI agent 卡片、日期选择器、进度条、footer 等），先在这里按分类或关键词找 2-3 个参考，用视觉能力看帧，提炼布局/配色/动效节奏后自己实现（实现时优先去 shadcn / React Bits 等代码库找底座）。

## 按需获取方法
站点是 Next.js（App Router）+ Vercel，**有 Vercel 反爬挑战**：
- curl 可直接拿到：首页 `/`、分类页 `/?category={Category}`、精选 `/?view=featured`（HTML 内嵌 RSC 数据，只含**第一页 16 条**）；媒体 CDN `https://media.inspora.design/...`（webp/mp4，无限制）。
- curl 拿不到（429 + `x-vercel-mitigated: challenge`）：`/posts/{slug}` 详情页、`/sitemap.xml`、`/api/posts` 分页接口。需用真实浏览器（Claude Browser / Chrome）打开。
- robots.txt 写了 `Disallow: /api/`：不调用分页接口。
- sitemap.xml 已过期（只有 142 篇旧帖，缺 2026-08-30 之后的新帖），不要用它当全集。

分类（`category` 参数，大小写敏感）：`Web` `Branding` `Product` `Motion` `Illustration` `3D` `Print`；排序 `view=latest|featured`。

**步骤 1：curl 拿某分类最新 16 条（实测 2026-10-07，`?category=Web` 返回 16 条，首条 footer-section）**
```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
curl -sL -A "$UA" "https://www.inspora.design/?category={Category}" -o page.html
python3 - <<'PY'
import re,json
h=open('page.html').read()
s=''.join(json.loads('"'+c+'"') for c in re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)',h,flags=re.S))
i=s.index('"initialPage":')+len('"initialPage":');d=0
for k in range(i,len(s)):
    d+= s[k]=='{'; d-= s[k]=='}'
    if d==0: break
o=json.loads(s[i:k+1])
for it in o['items']:
    m=it['media'][0]
    print(it['slug'],'|',it['title'],'|',m['type'],'|',m.get('posterUrl') or m['url'],'|',m['url'])
print('nextCursor=',o['nextCursor'])
PY
```
每条字段：`slug, title, creator{name}, createdAt, media[{type:image|video, url, posterUrl(视频封面 webp), videoPreview{url 1080p 预览 mp4}, width, height}], mediaCount`。

**步骤 2：不要翻页**
robots.txt 禁止访问 `/api/`，所以**不调用 `/api/posts`**。运行时只用步骤 1 拿各分类首页的 16 条。想要更早的条目，从下方清单里挑 slug，把 `https://www.inspora.design/posts/{slug}` 给用户，让用户自己打开看。 注意：清单（inspora.tsv）里只有帖子页地址，没有媒体直链；媒体直链只能从分类首页（步骤 1）拿到。

**步骤 3：详情页（描述 + 行业/配色/风格标签 + 原帖链接）**
浏览器打开 `https://www.inspora.design/posts/{slug}`，用 get_page_text 读取。实测 `footer-section`：一段英文描述（"website footer with navigation links and a newsletter signup above a blue-and-cream desert illustration..."）、`Industries: Tableware`、`Colors: Blue, Cream`、`Styles: Editorial`、`View original` → X 原帖。这些标签只在详情页有，列表 JSON 里没有。

**步骤 4：把参考图喂给视觉能力**
```bash
# 图片 / 视频封面（webp → png，便于 Read 工具查看）
curl -s "{posterUrl}" -o ref.webp && sips -s format png ref.webp --out ref.png
# 视频：优先下载 videoPreview.url（1080p，几百 KB），抽 4 帧拼成 2x2 网格一次看完
curl -s "{videoPreview.url 或 media.url}" -o ref.mp4
ffmpeg -loglevel error -y -i ref.mp4 -vf "fps=1/2,scale=960:-1,tile=2x2" -frames:v 1 ref_grid.png
```
实测：`https://media.inspora.design/posts/889b9627-...webp`（footer-section 封面）200，转 png 成功；`.../a204b3d4-...mp4` 预览视频 358 KB 下载成功。

**开发 agent 使用流程**：按要做的东西选分类（页面区块→Web；App 界面/卡片/表单→Product；交互动效→Motion；图标/Logo→Branding）→ 在下方清单用标题关键词筛 2-3 条 → 取 posterUrl / 抽帧 → 用视觉能力描述布局结构、间距、配色（可配合详情页 Colors/Styles 标签）、动效时序 → 用现有组件库实现，不照抄原作品。

## 使用注意
- 无代码、无提示词、无模板、无下载按钮；只有"View original"跳 X 原帖。没有 Pro/付费内容，唯一表单是邮件订阅（不要提交）。
- 内容 90% 是视频，静态截图只看封面会漏掉动效，涉及交互时必须抽帧。
- 列表 JSON 不含分类字段，分类只能通过 `category` 参数反推；不含描述/配色标签，需要详情页。
- slug 不稳定且有怪名（`1-61`、`9-8`、`iquid-metal`），按标题检索更可靠。
- 作品版权属于原作者，只能借鉴，不能直接搬图或复刻品牌。
- 站点更新频繁（每天数条），下面清单是 2026-10-07 快照，最新内容用步骤 1/2 现取。

## 组件清单
2026-10-07 快照共 **287** 条：Motion 129、Product 65、Web 42、Illustration 25、Branding 17、3D 5、Print 4；Featured 9 条（备注 featured）。全部免费可看。获取列一律是详情页 URL；媒体直链用步骤 1/2 现取。

| id | 名称 | 分类 | 一句话用途 | 获取（具体命令或URL） | 备注 |
|---|---|---|---|---|---|
| fluid-illumination | fluid illumination | Motion | 动效/微交互灵感视频：fluid illumination | https://www.inspora.design/posts/fluid-illumination |  |
| downloading-an-invoice | downloading an invoice | Product | 产品界面/应用 UI灵感视频：downloading an invoice | https://www.inspora.design/posts/downloading-an-invoice |  |
| color-text-in-notes | color text in Notes | Motion | 动效/微交互灵感视频：color text in Notes | https://www.inspora.design/posts/color-text-in-notes |  |
| model-router | Model router | Product | 产品界面/应用 UI灵感视频：Model router | https://www.inspora.design/posts/model-router |  |
| glass-circle-with-a-gradient | glass circle with a gradient | Product | 产品界面/应用 UI灵感图片：glass circle with a gradient | https://www.inspora.design/posts/glass-circle-with-a-gradient |  |
| airport-matrix-time | Airport matrix time | Motion | 动效/微交互灵感视频：Airport matrix time | https://www.inspora.design/posts/airport-matrix-time |  |
| hairlines-v2 | hairlines v0.2 | Illustration | 插画/拟物视觉灵感视频：hairlines v0.2 | https://www.inspora.design/posts/hairlines-v2 |  |
| isometric-ai-computer | isometric AI computer | Illustration | 插画/拟物视觉灵感视频：isometric AI computer | https://www.inspora.design/posts/isometric-ai-computer |  |
| run-to-the-hills | run to the hills | Illustration | 插画/拟物视觉灵感视频：run to the hills | https://www.inspora.design/posts/run-to-the-hills |  |
| agent-cards | Agent cards | Product | 产品界面/应用 UI灵感图片：Agent cards | https://www.inspora.design/posts/agent-cards |  |
| ai-ends-motion-hiring | AI ends motion hiring. | Motion | 动效/微交互灵感视频：AI ends motion hiring. | https://www.inspora.design/posts/ai-ends-motion-hiring |  |
| footer-section | footer section | Web | 网页/落地页区块灵感图片：footer section | https://www.inspora.design/posts/footer-section |  |
| dither-and-ascii-card | Dither and Ascii card | Motion | 动效/微交互灵感视频：Dither and Ascii card | https://www.inspora.design/posts/dither-and-ascii-card |  |
| anthropomorphic-brand-character | anthropomorphic brand character. | Branding | 品牌/图标/Logo灵感视频：anthropomorphic brand character. | https://www.inspora.design/posts/anthropomorphic-brand-character |  |
| iquid-metal | liquid metal | Motion | 动效/微交互灵感视频：liquid metal | https://www.inspora.design/posts/iquid-metal |  |
| i-will-survive | I will survive | Illustration | 插画/拟物视觉灵感视频：I will survive | https://www.inspora.design/posts/i-will-survive |  |
| a-lightweight-portfolio | A lightweight portfolio | Web | 网页/落地页区块灵感视频：A lightweight portfolio | https://www.inspora.design/posts/a-lightweight-portfolio |  |
| melon-jelly | Melon Jelly | Web | 网页/落地页区块灵感视频：Melon Jelly | https://www.inspora.design/posts/melon-jelly |  |
| voice-model | voice model | Motion | 动效/微交互灵感视频：voice model | https://www.inspora.design/posts/voice-model |  |
| personal-site | personal site | Web | 网页/落地页区块灵感视频：personal site | https://www.inspora.design/posts/personal-site |  |
| fluid-liquid-card-carousel | Fluid liquid card carousel. | Motion | 动效/微交互灵感视频：Fluid liquid card carousel. | https://www.inspora.design/posts/fluid-liquid-card-carousel |  |
| ai-keychain | AI keychain. | Motion | 动效/微交互灵感视频：AI keychain. | https://www.inspora.design/posts/ai-keychain |  |
| thanos-snap-ticket | Thanos snap ticket | Motion | 动效/微交互灵感视频：Thanos snap ticket | https://www.inspora.design/posts/thanos-snap-ticket |  |
| apple-style-level-components | apple style level components | Motion | 动效/微交互灵感视频：apple style level components | https://www.inspora.design/posts/apple-style-level-components |  |
| progress-bar-animation | progress bar animation | Motion | 动效/微交互灵感视频：progress bar animation | https://www.inspora.design/posts/progress-bar-animation |  |
| quiet-overlapping-clocks | Quiet overlapping clocks | Product | 产品界面/应用 UI灵感图片：Quiet overlapping clocks | https://www.inspora.design/posts/quiet-overlapping-clocks |  |
| a-calendar-booking-page | a calendar booking page | Product | 产品界面/应用 UI灵感视频：a calendar booking page | https://www.inspora.design/posts/a-calendar-booking-page |  |
| tiny-animated-svg | Tiny animated SVG | Motion | 动效/微交互灵感视频：Tiny animated SVG | https://www.inspora.design/posts/tiny-animated-svg |  |
| blurry-pioneer-interfaces | Blurry Pioneer interfaces | Product | 产品界面/应用 UI灵感图片：Blurry Pioneer interfaces | https://www.inspora.design/posts/blurry-pioneer-interfaces |  |
| wos-island-animations | WOS Island Animations | Motion | 动效/微交互灵感视频：WOS Island Animations | https://www.inspora.design/posts/wos-island-animations |  |
| i-want-to-run-again | I want to run again | Illustration | 插画/拟物视觉灵感视频：I want to run again | https://www.inspora.design/posts/i-want-to-run-again |  |
| look-away-preview | Look Away preview | Product | 产品界面/应用 UI灵感视频：Look Away preview | https://www.inspora.design/posts/look-away-preview |  |
| lookaway-ios | LookAway iOS | Motion | 动效/微交互灵感视频：LookAway iOS | https://www.inspora.design/posts/lookaway-ios |  |
| ai-scheduler | AI scheduler | Product | 产品界面/应用 UI灵感视频：AI scheduler | https://www.inspora.design/posts/ai-scheduler |  |
| eleven-v4 | Eleven v4 | Motion | 动效/微交互灵感视频：Eleven v4 | https://www.inspora.design/posts/eleven-v4 |  |
| vintage-stamp-collage | Vintage stamp collage | Print | 印刷/海报灵感视频：Vintage stamp collage | https://www.inspora.design/posts/vintage-stamp-collage |  |
| glowing-loader | glowing loader | Motion | 动效/微交互灵感视频：glowing loader | https://www.inspora.design/posts/glowing-loader |  |
| artistic-fintech | Artistic fintech UI | Product | 产品界面/应用 UI灵感视频：Artistic fintech UI | https://www.inspora.design/posts/artistic-fintech |  |
| sticky-note-app | Sticky-note app | Product | 产品界面/应用 UI灵感视频：Sticky-note app | https://www.inspora.design/posts/sticky-note-app |  |
| order-status-card | order-status card | Motion | 动效/微交互灵感视频：order-status card | https://www.inspora.design/posts/order-status-card |  |
| temperature-as-a-material | Temperature as a material. | Product | 产品界面/应用 UI灵感图片：Temperature as a material. | https://www.inspora.design/posts/temperature-as-a-material |  |
| bright-candy-icons | bright candy icons | Branding | 品牌/图标/Logo灵感图片：bright candy icons | https://www.inspora.design/posts/bright-candy-icons |  |
| audience-data | audience data | Product | 产品界面/应用 UI灵感视频：audience data | https://www.inspora.design/posts/audience-data |  |
| paperclip-interaction | Paperclip interaction | Product | 产品界面/应用 UI灵感视频：Paperclip interaction | https://www.inspora.design/posts/paperclip-interaction |  |
| dynamic-island-pixel-art-horse | Dynamic Island pixel-art horse | Motion | 动效/微交互灵感视频：Dynamic Island pixel-art horse | https://www.inspora.design/posts/dynamic-island-pixel-art-horse |  |
| medicine-to-my-soul | medicine to my soul | Illustration | 插画/拟物视觉灵感视频：medicine to my soul | https://www.inspora.design/posts/medicine-to-my-soul |  |
| club-playing-cards | club playing cards | Motion | 动效/微交互灵感视频：club playing cards | https://www.inspora.design/posts/club-playing-cards |  |
| 3d-interactive-cassette-tape | 3D interactive cassette-tape | Motion | 动效/微交互灵感视频：3D interactive cassette-tape | https://www.inspora.design/posts/3d-interactive-cassette-tape |  |
| the-lord-of-horses | The Lord of Horses. | Motion | 动效/微交互灵感视频：The Lord of Horses. | https://www.inspora.design/posts/the-lord-of-horses |  |
| handmade-icons | Handmade icons | Branding | 品牌/图标/Logo灵感视频：Handmade icons | https://www.inspora.design/posts/handmade-icons |  |
| invite-code-interaction | invite code interaction | Motion | 动效/微交互灵感视频：invite code interaction | https://www.inspora.design/posts/invite-code-interaction |  |
| portfolio | portfolio | Web | 网页/落地页区块灵感视频：portfolio | https://www.inspora.design/posts/portfolio |  |
| chat-component-interaction | Chat component interaction | Product | 产品界面/应用 UI灵感视频：Chat component interaction | https://www.inspora.design/posts/chat-component-interaction |  |
| onboarding | Onboarding | Motion | 动效/微交互灵感视频：Onboarding | https://www.inspora.design/posts/onboarding |  |
| folder-icon-timeline | macOS Folder Icon Timeline | Motion | 动效/微交互灵感视频：macOS Folder Icon Timeline | https://www.inspora.design/posts/folder-icon-timeline |  |
| ticket-stub | ticket stub | Motion | 动效/微交互灵感视频：ticket stub | https://www.inspora.design/posts/ticket-stub |  |
| composer-mockup | composer mockup | Motion | 动效/微交互灵感视频：composer mockup | https://www.inspora.design/posts/composer-mockup |  |
| folder-interaction | folder interaction | Motion | 动效/微交互灵感视频：folder interaction | https://www.inspora.design/posts/folder-interaction |  |
| tap-get-invoice | Tap Get Invoice | Motion | 动效/微交互灵感视频：Tap Get Invoice | https://www.inspora.design/posts/tap-get-invoice |  |
| dessn-welcome-envelope | DESSN welcome envelope | Motion | 动效/微交互灵感视频：DESSN welcome envelope | https://www.inspora.design/posts/dessn-welcome-envelope |  |
| scenic-footer-section | Scenic Footer Section | Web | 网页/落地页区块灵感视频：Scenic Footer Section | https://www.inspora.design/posts/scenic-footer-section |  |
| payment-links | payment links | Product | 产品界面/应用 UI灵感视频：payment links | https://www.inspora.design/posts/payment-links |  |
| hypnotizing-ui | hypnotizing UI | Motion | 动效/微交互灵感视频：hypnotizing UI | https://www.inspora.design/posts/hypnotizing-ui |  |
| liquid-metal | Liquid metal | Illustration | 插画/拟物视觉灵感视频：Liquid metal | https://www.inspora.design/posts/liquid-metal |  |
| enter-the-unknown | Enter the Unknown | Illustration | 插画/拟物视觉灵感视频：Enter the Unknown | https://www.inspora.design/posts/enter-the-unknown |  |
| session-progress-and-recovery-timeline | Session progress and recovery timeline | Product | 产品界面/应用 UI灵感图片：Session progress and recovery timeline | https://www.inspora.design/posts/session-progress-and-recovery-timeline |  |
| interactive-cards | Interactive cards. | Web | 网页/落地页区块灵感视频：Interactive cards. | https://www.inspora.design/posts/interactive-cards |  |
| holographic-card | holographic card | Illustration | 插画/拟物视觉灵感视频：holographic card | https://www.inspora.design/posts/holographic-card |  |
| infinite-faq | infinite faq | Web | 网页/落地页区块灵感视频：infinite faq | https://www.inspora.design/posts/infinite-faq |  |
| grok-bot-can-talk-now | Grok Bot can talk now | Motion | 动效/微交互灵感视频：Grok Bot can talk now | https://www.inspora.design/posts/grok-bot-can-talk-now |  |
| pick-your-plan | Pick your Plan | Product | 产品界面/应用 UI灵感视频：Pick your Plan | https://www.inspora.design/posts/pick-your-plan |  |
| glowing-blue-orb | glowing blue orb | Motion | 动效/微交互灵感视频：glowing blue orb | https://www.inspora.design/posts/glowing-blue-orb |  |
| collection-layout | interaction collection layout | Motion | 动效/微交互灵感视频：interaction collection layout | https://www.inspora.design/posts/collection-layout |  |
| pill-buttons | pill buttons | Product | 产品界面/应用 UI灵感视频：pill buttons | https://www.inspora.design/posts/pill-buttons |  |
| voice-effect | Voice effect | Motion | 动效/微交互灵感视频：Voice effect | https://www.inspora.design/posts/voice-effect |  |
| coding-agent | Coding agent | Product | 产品界面/应用 UI灵感视频：Coding agent | https://www.inspora.design/posts/coding-agent |  |
| 3d-gradient-cards | 3D gradient cards | Motion | 动效/微交互灵感视频：3D gradient cards | https://www.inspora.design/posts/3d-gradient-cards |  |
| app-review | App review | Motion | 动效/微交互灵感视频：App review | https://www.inspora.design/posts/app-review |  |
| angry-sliders | angry sliders | Motion | 动效/微交互灵感视频：angry sliders | https://www.inspora.design/posts/angry-sliders |  |
| stamp-shader | Stamp Shader | Motion | 动效/微交互灵感视频：Stamp Shader | https://www.inspora.design/posts/stamp-shader |  |
| paid-stamp | 3D paid stamp | Motion | 动效/微交互灵感视频：3D paid stamp | https://www.inspora.design/posts/paid-stamp |  |
| travel-app | travel app | Product | 产品界面/应用 UI灵感视频：travel app | https://www.inspora.design/posts/travel-app |  |
| bencho-logo | Bencho logo | Branding | 品牌/图标/Logo灵感视频：Bencho logo | https://www.inspora.design/posts/bencho-logo |  |
| support-analytics | Support analytics | Product | 产品界面/应用 UI灵感视频：Support analytics | https://www.inspora.design/posts/support-analytics |  |
| onboarding-flow | onboarding flow | Product | 产品界面/应用 UI灵感视频：onboarding flow | https://www.inspora.design/posts/onboarding-flow |  |
| dynamic-island-streak | Dynamic Island Streak | Motion | 动效/微交互灵感视频：Dynamic Island Streak | https://www.inspora.design/posts/dynamic-island-streak |  |
| file-upload-card | File upload card | Motion | 动效/微交互灵感视频：File upload card | https://www.inspora.design/posts/file-upload-card |  |
| sidebar-active-state | Sidebar Active State | Product | 产品界面/应用 UI灵感视频：Sidebar Active State | https://www.inspora.design/posts/sidebar-active-state |  |
| unlocking-keypad | Unlocking keypad | 3D | 3D灵感视频：Unlocking keypad | https://www.inspora.design/posts/unlocking-keypad |  |
| pigeon-online | pigeon online | Illustration | 插画/拟物视觉灵感视频：pigeon online | https://www.inspora.design/posts/pigeon-online |  |
| motion-exploration | Personal brand — motion exploration | Branding | 品牌/图标/Logo灵感视频：Personal brand — motion exploration | https://www.inspora.design/posts/motion-exploration |  |
| stamp-style-cards | stamp-style cards | Branding | 品牌/图标/Logo灵感图片：stamp-style cards | https://www.inspora.design/posts/stamp-style-cards |  |
| tracking-cards | Tracking cards | Product | 产品界面/应用 UI灵感图片：Tracking cards | https://www.inspora.design/posts/tracking-cards |  |
| ghost-pass | ghost pass | Motion | 动效/微交互灵感视频：ghost pass | https://www.inspora.design/posts/ghost-pass |  |
| component-anatomy | Component Anatomy | Motion | 动效/微交互灵感视频：Component Anatomy | https://www.inspora.design/posts/component-anatomy |  |
| beveled-cards | beveled cards | Web | 网页/落地页区块灵感视频：beveled cards | https://www.inspora.design/posts/beveled-cards |  |
| cartridge-portfolio | Cartridge portfolio | Motion | 动效/微交互灵感视频：Cartridge portfolio | https://www.inspora.design/posts/cartridge-portfolio |  |
| feature-menu | feature menu | Web | 网页/落地页区块灵感视频：feature menu | https://www.inspora.design/posts/feature-menu |  |
| ai-prompt-bar | AI prompt bar | Product | 产品界面/应用 UI灵感视频：AI prompt bar | https://www.inspora.design/posts/ai-prompt-bar |  |
| data-collect | Data Collect | Motion | 动效/微交互灵感视频：Data Collect | https://www.inspora.design/posts/data-collect |  |
| morph-shap | Morph. | Motion | 动效/微交互灵感视频：Morph. | https://www.inspora.design/posts/morph-shap |  |
| task-card | Task Card | Product | 产品界面/应用 UI灵感视频：Task Card | https://www.inspora.design/posts/task-card |  |
| agent-plan | Agent Plan | Product | 产品界面/应用 UI灵感视频：Agent Plan | https://www.inspora.design/posts/agent-plan |  |
| brand-work | Brand work | Branding | 品牌/图标/Logo灵感图片：Brand work | https://www.inspora.design/posts/brand-work |  |
| glassmorphism-animation | glassmorphism animation | Web | 网页/落地页区块灵感视频：glassmorphism animation | https://www.inspora.design/posts/glassmorphism-animation |  |
| icons-for-iphone-duo | icons for iPhone Duo | Motion | 动效/微交互灵感视频：icons for iPhone Duo | https://www.inspora.design/posts/icons-for-iphone-duo |  |
| iphone-duo-bar-icons | iPhone Duo | Illustration | 插画/拟物视觉灵感图片：iPhone Duo | https://www.inspora.design/posts/iphone-duo-bar-icons |  |
| iphone-duo | This iPhone Duo animation | Motion | 动效/微交互灵感视频：This iPhone Duo animation | https://www.inspora.design/posts/iphone-duo |  |
| orb-loom | orbloom | Product | 产品界面/应用 UI灵感视频：orbloom | https://www.inspora.design/posts/orb-loom |  |
| gooey-navbar-component | navbar component | Motion | 动效/微交互灵感视频：navbar component | https://www.inspora.design/posts/gooey-navbar-component |  |
| train-animation | footer train animation | Web | 网页/落地页区块灵感视频：footer train animation | https://www.inspora.design/posts/train-animation |  |
| tensorlake-brand | tensorlake brand | Web | 网页/落地页区块灵感视频：tensorlake brand | https://www.inspora.design/posts/tensorlake-brand |  |
| morphing-nav | morphing nav bar | Product | 产品界面/应用 UI灵感视频：morphing nav bar | https://www.inspora.design/posts/morphing-nav |  |
| 3d-animated-cards | 3D animated cards | Web | 网页/落地页区块灵感视频：3D animated cards | https://www.inspora.design/posts/3d-animated-cards |  |
| shader-dial | Shader Dial | Motion | 动效/微交互灵感视频：Shader Dial | https://www.inspora.design/posts/shader-dial |  |
| interactive-footer | interactive footer | Web | 网页/落地页区块灵感视频：interactive footer | https://www.inspora.design/posts/interactive-footer |  |
| liquid-glass | Liquid glass | Web | 网页/落地页区块灵感视频：Liquid glass | https://www.inspora.design/posts/liquid-glass |  |
| sticker-footer | Footer | Web | 网页/落地页区块灵感视频：Footer | https://www.inspora.design/posts/sticker-footer |  |
| progress-bars | progress bars | Motion | 动效/微交互灵感视频：progress bars | https://www.inspora.design/posts/progress-bars |  |
| onboarding-screen | onboarding screen | Product | 产品界面/应用 UI灵感视频：onboarding screen | https://www.inspora.design/posts/onboarding-screen |  |
| realistic-button | realistic button | Illustration | 插画/拟物视觉灵感视频：realistic button | https://www.inspora.design/posts/realistic-button |  |
| ascii-cards | ASCII cards | Motion | 动效/微交互灵感视频：ASCII cards | https://www.inspora.design/posts/ascii-cards |  |
| heic-file-upload | HEIC File Upload | Motion | 动效/微交互灵感视频：HEIC File Upload | https://www.inspora.design/posts/heic-file-upload |  |
| rag-pipeline | RAG Pipeline | Product | 产品界面/应用 UI灵感视频：RAG Pipeline | https://www.inspora.design/posts/rag-pipeline |  |
| bleep-app | Bleep App | Motion | 动效/微交互灵感视频：Bleep App | https://www.inspora.design/posts/bleep-app |  |
| portfolio-gameboy | Portfolio Gameboy | Web | 网页/落地页区块灵感视频：Portfolio Gameboy | https://www.inspora.design/posts/portfolio-gameboy |  |
| mobile-gradient | Mobile Gradient UI | Motion | 动效/微交互灵感视频：Mobile Gradient UI | https://www.inspora.design/posts/mobile-gradient |  |
| gpt-6-astra | generating UI using GPT-6 Astra | Motion | 动效/微交互灵感视频：generating UI using GPT-6 Astra | https://www.inspora.design/posts/gpt-6-astra |  |
| dropdown-component | Dropdown Component | Product | 产品界面/应用 UI灵感视频：Dropdown Component | https://www.inspora.design/posts/dropdown-component |  |
| document-signature | document signature | Product | 产品界面/应用 UI灵感视频：document signature | https://www.inspora.design/posts/document-signature |  |
| mechanical-macropad | mechanical macropad | 3D | 3D灵感视频：mechanical macropad | https://www.inspora.design/posts/mechanical-macropad |  |
| photo-folders | photos folders | Motion | 动效/微交互灵感视频：photos folders | https://www.inspora.design/posts/photo-folders |  |
| portfolio-page | portfolio page | Web | 网页/落地页区块灵感视频：portfolio page | https://www.inspora.design/posts/portfolio-page |  |
| multi-action-button | multi-action button | Motion | 动效/微交互灵感视频：multi-action button | https://www.inspora.design/posts/multi-action-button |  |
| bento-cards | Bento cards. | Web | 网页/落地页区块灵感视频：Bento cards. | https://www.inspora.design/posts/bento-cards |  |
| follower-count | Follower Count | Motion | 动效/微交互灵感视频：Follower Count | https://www.inspora.design/posts/follower-count |  |
| time-zones | Time for different time zones | Product | 产品界面/应用 UI灵感视频：Time for different time zones | https://www.inspora.design/posts/time-zones |  |
| boarding-pass-printer | boarding pass printer | Motion | 动效/微交互灵感视频：boarding pass printer | https://www.inspora.design/posts/boarding-pass-printer |  |
| deploy-pipeline | Deploy Pipeline | Product | 产品界面/应用 UI灵感视频：Deploy Pipeline | https://www.inspora.design/posts/deploy-pipeline |  |
| product-comps | Product comps | Product | 产品界面/应用 UI灵感图片：Product comps | https://www.inspora.design/posts/product-comps |  |
| wafer-page | Wafer page | Web | 网页/落地页区块灵感视频：Wafer page | https://www.inspora.design/posts/wafer-page |  |
| dither-cards | Dither Cards | Motion | 动效/微交互灵感视频：Dither Cards | https://www.inspora.design/posts/dither-cards |  |
| bankito-frozen-card | bankito® frozen card | Motion | 动效/微交互灵感视频：bankito® frozen card | https://www.inspora.design/posts/bankito-frozen-card |  |
| hook-sidebar | Hook sidebar | Product | 产品界面/应用 UI灵感视频：Hook sidebar | https://www.inspora.design/posts/hook-sidebar |  |
| sandbox-boot-sequence | Sandbox Boot Sequence | Product | 产品界面/应用 UI灵感视频：Sandbox Boot Sequence | https://www.inspora.design/posts/sandbox-boot-sequence |  |
| maple-research-cards | Maple Research cards | Branding | 品牌/图标/Logo灵感视频：Maple Research cards | https://www.inspora.design/posts/maple-research-cards |  |
| hero-section | Hero section | Web | 网页/落地页区块灵感视频：Hero section | https://www.inspora.design/posts/hero-section |  |
| components-n3xt | Components N3XT | Motion | 动效/微交互灵感视频：Components N3XT | https://www.inspora.design/posts/components-n3xt |  |
| file-management-dashboard | a file-management dashboard | Product | 产品界面/应用 UI灵感图片：a file-management dashboard | https://www.inspora.design/posts/file-management-dashboard |  |
| soft-fluid-systems | soft + fluid systems | Branding | 品牌/图标/Logo灵感图片：soft + fluid systems | https://www.inspora.design/posts/soft-fluid-systems |  |
| mega-menu | Mega Menu Animation | Web | 网页/落地页区块灵感视频：Mega Menu Animation | https://www.inspora.design/posts/mega-menu |  |
| genres-filter | Genres filter | Motion | 动效/微交互灵感视频：Genres filter | https://www.inspora.design/posts/genres-filter |  |
| orb-interation | Orb interaction | Motion | 动效/微交互灵感视频：Orb interaction | https://www.inspora.design/posts/orb-interation |  |
| 1-61 | Window controlled Dark mode | Motion | 动效/微交互灵感视频：Window controlled Dark mode（Featured 精选） | https://www.inspora.design/posts/1-61 | featured |
| 1-60 | Ringwriter | Motion | 动效/微交互灵感视频：Ringwriter | https://www.inspora.design/posts/1-60 |  |
| 1-58 | Mini calendar | Product | 产品界面/应用 UI灵感视频：Mini calendar | https://www.inspora.design/posts/1-58 |  |
| 1-57 | 404 page | Web | 网页/落地页区块灵感视频：404 page | https://www.inspora.design/posts/1-57 |  |
| 1-55 | Portfolio Boarding Pass | Motion | 动效/微交互灵感视频：Portfolio Boarding Pass | https://www.inspora.design/posts/1-55 |  |
| 1-56 | Spiderman icon | Branding | 品牌/图标/Logo灵感图片：Spiderman icon | https://www.inspora.design/posts/1-56 |  |
| 1-54 | dropdown interaction | Motion | 动效/微交互灵感视频：dropdown interaction | https://www.inspora.design/posts/1-54 |  |
| 1-53 | glossy orb animation | Web | 网页/落地页区块灵感视频：glossy orb animation | https://www.inspora.design/posts/1-53 |  |
| 1-52 | curved browser tabs | Illustration | 插画/拟物视觉灵感视频：curved browser tabs | https://www.inspora.design/posts/1-52 |  |
| 1-51 | Payment plans | Motion | 动效/微交互灵感视频：Payment plans | https://www.inspora.design/posts/1-51 |  |
| 1-50 | onboarding modal | Web | 网页/落地页区块灵感视频：onboarding modal | https://www.inspora.design/posts/1-50 |  |
| 1-49 | App icon concepts | Branding | 品牌/图标/Logo灵感视频：App icon concepts | https://www.inspora.design/posts/1-49 |  |
| 1-48 | Agent Handoff | Product | 产品界面/应用 UI灵感视频：Agent Handoff | https://www.inspora.design/posts/1-48 |  |
| 1-47 | voice note / interaction | Motion | 动效/微交互灵感视频：voice note / interaction | https://www.inspora.design/posts/1-47 |  |
| 1-46 | Grid Reveal animation | Motion | 动效/微交互灵感视频：Grid Reveal animation | https://www.inspora.design/posts/1-46 |  |
| 1-45 | Event Swatch | Motion | 动效/微交互灵感视频：Event Swatch | https://www.inspora.design/posts/1-45 |  |
| 1-44 | Meeting Finder | Product | 产品界面/应用 UI灵感视频：Meeting Finder | https://www.inspora.design/posts/1-44 |  |
| 1-43 | Emotion Shader | Motion | 动效/微交互灵感视频：Emotion Shader | https://www.inspora.design/posts/1-43 |  |
| 1-42 | Morphing braille loader | Product | 产品界面/应用 UI灵感视频：Morphing braille loader | https://www.inspora.design/posts/1-42 |  |
| 1-41 | A country picker | Motion | 动效/微交互灵感视频：A country picker | https://www.inspora.design/posts/1-41 |  |
| 1-40 | A bento card | Web | 网页/落地页区块灵感视频：A bento card | https://www.inspora.design/posts/1-40 |  |
| 1-39 | Watch face | Motion | 动效/微交互灵感视频：Watch face | https://www.inspora.design/posts/1-39 |  |
| 1-38 | Sidebar sub menu | Motion | 动效/微交互灵感视频：Sidebar sub menu | https://www.inspora.design/posts/1-38 |  |
| 1-37 | AI Agent Approval Cards | Product | 产品界面/应用 UI灵感视频：AI Agent Approval Cards | https://www.inspora.design/posts/1-37 |  |
| 1-36 | Liquid metal button | Motion | 动效/微交互灵感视频：Liquid metal button | https://www.inspora.design/posts/1-36 |  |
| 1-35 | Print Receipt | Motion | 动效/微交互灵感视频：Print Receipt | https://www.inspora.design/posts/1-35 |  |
| 1-34 | card details microinteraction | Product | 产品界面/应用 UI灵感视频：card details microinteraction | https://www.inspora.design/posts/1-34 |  |
| 1-33 | Hero section | Web | 网页/落地页区块灵感视频：Hero section | https://www.inspora.design/posts/1-33 |  |
| 1-32 | Mechanical keyboard for iphone | Illustration | 插画/拟物视觉灵感图片：Mechanical keyboard for iphone | https://www.inspora.design/posts/1-32 |  |
| 1-31 | Liquid metal button | Motion | 动效/微交互灵感视频：Liquid metal button | https://www.inspora.design/posts/1-31 |  |
| 1-30 | Date Range Picker | Product | 产品界面/应用 UI灵感视频：Date Range Picker（Featured 精选） | https://www.inspora.design/posts/1-30 | featured |
| 1-29 | Speed Slider | Motion | 动效/微交互灵感视频：Speed Slider | https://www.inspora.design/posts/1-29 |  |
| 1-28 | Liquid Glass | Illustration | 插画/拟物视觉灵感图片：Liquid Glass | https://www.inspora.design/posts/1-28 |  |
| 1-27 | Smooth scroll with lens refraction. | Motion | 动效/微交互灵感视频：Smooth scroll with lens refraction. | https://www.inspora.design/posts/1-27 |  |
| 1-26 | Wave thinking animations | 3D | 3D灵感视频：Wave thinking animations | https://www.inspora.design/posts/1-26 |  |
| 1-25 | Team section | Web | 网页/落地页区块灵感视频：Team section | https://www.inspora.design/posts/1-25 |  |
| 1-24 | Spider-Man web dropdown | Motion | 动效/微交互灵感视频：Spider-Man web dropdown | https://www.inspora.design/posts/1-24 |  |
| 1-23 | We're making Grok Bot more widely available. | Motion | 动效/微交互灵感视频：We're making Grok Bot more widely available. | https://www.inspora.design/posts/1-23 |  |
| 1-22 | wavy carousel | Motion | 动效/微交互灵感视频：wavy carousel（Featured 精选） | https://www.inspora.design/posts/1-22 | featured |
| 1-21 | Brand story cards | Web | 网页/落地页区块灵感视频：Brand story cards | https://www.inspora.design/posts/1-21 |  |
| 1-20 | Toggle to premium plans | Motion | 动效/微交互灵感视频：Toggle to premium plans | https://www.inspora.design/posts/1-20 |  |
| 1-19 | Sign-Up page | Web | 网页/落地页区块灵感视频：Sign-Up page | https://www.inspora.design/posts/1-19 |  |
| 1-18 | waitlist screen | Web | 网页/落地页区块灵感图片：waitlist screen | https://www.inspora.design/posts/1-18 |  |
| 1-17 | analytics dashboard | Product | 产品界面/应用 UI灵感图片：analytics dashboard | https://www.inspora.design/posts/1-17 |  |
| 1-16 | Dark mode toggle | Illustration | 插画/拟物视觉灵感视频：Dark mode toggle（Featured 精选） | https://www.inspora.design/posts/1-16 | featured |
| 1-15 | New Calendly logo | Branding | 品牌/图标/Logo灵感视频：New Calendly logo | https://www.inspora.design/posts/1-15 |  |
| 1-14 | Shader Stamps | Motion | 动效/微交互灵感视频：Shader Stamps | https://www.inspora.design/posts/1-14 |  |
| 1-13 | folder component | Web | 网页/落地页区块灵感视频：folder component | https://www.inspora.design/posts/1-13 |  |
| 1-12 | Glass shader | Motion | 动效/微交互灵感视频：Glass shader | https://www.inspora.design/posts/1-12 |  |
| 1-11 | A highlighter marker | 3D | 3D灵感视频：A highlighter marker | https://www.inspora.design/posts/1-11 |  |
| 9-8 | html-in-canvas | Web | 网页/落地页区块灵感视频：html-in-canvas | https://www.inspora.design/posts/9-8 |  |
| 9-7 | OTP | Product | 产品界面/应用 UI灵感视频：OTP | https://www.inspora.design/posts/9-7 |  |
| 9-6 | tabs animation | Motion | 动效/微交互灵感视频：tabs animation | https://www.inspora.design/posts/9-6 |  |
| 9-5 | Opt-in-performance | Product | 产品界面/应用 UI灵感视频：Opt-in-performance | https://www.inspora.design/posts/9-5 |  |
| 9-4 | toss your note to the bin | Motion | 动效/微交互灵感视频：toss your note to the bin | https://www.inspora.design/posts/9-4 |  |
| 9-3 | Retro CRT | Illustration | 插画/拟物视觉灵感视频：Retro CRT | https://www.inspora.design/posts/9-3 |  |
| 9-2 | status tags with glass bubble | Motion | 动效/微交互灵感视频：status tags with glass bubble | https://www.inspora.design/posts/9-2 |  |
| 8-0 | Timeline concept | Product | 产品界面/应用 UI灵感视频：Timeline concept | https://www.inspora.design/posts/8-0 |  |
| 9-1 | App icon | Branding | 品牌/图标/Logo灵感图片：App icon（Featured 精选） | https://www.inspora.design/posts/9-1 | featured |
| 8-9 | A calendar of your life | Product | 产品界面/应用 UI灵感视频：A calendar of your life | https://www.inspora.design/posts/8-9 |  |
| 8-8 | ipod AI agent | Illustration | 插画/拟物视觉灵感视频：ipod AI agent | https://www.inspora.design/posts/8-8 |  |
| 8-7 | Apple's new macOS window controls | Product | 产品界面/应用 UI灵感图片：Apple's new macOS window controls | https://www.inspora.design/posts/8-7 |  |
| 8-1 | File cabinet slide | Motion | 动效/微交互灵感视频：File cabinet slide | https://www.inspora.design/posts/8-1 |  |
| 7-8 | Shader Credit Card | Motion | 动效/微交互灵感视频：Shader Credit Card | https://www.inspora.design/posts/7-8 |  |
| 8-6 | Invoices style | Product | 产品界面/应用 UI灵感视频：Invoices style | https://www.inspora.design/posts/8-6 |  |
| 8-5 | Liquid glass buttons | Motion | 动效/微交互灵感视频：Liquid glass buttons | https://www.inspora.design/posts/8-5 |  |
| 8-4 | Same element, new position. | Motion | 动效/微交互灵感视频：Same element, new position. | https://www.inspora.design/posts/8-4 |  |
| 8-3 | Weather scrubber | Motion | 动效/微交互灵感视频：Weather scrubber | https://www.inspora.design/posts/8-3 |  |
| 7-9 | Notification Cards | Motion | 动效/微交互灵感视频：Notification Cards | https://www.inspora.design/posts/7-9 |  |
| 7-7 | Stamp designs | Print | 印刷/海报灵感视频：Stamp designs | https://www.inspora.design/posts/7-7 |  |
| 7-6 | Delete this file | Motion | 动效/微交互灵感视频：Delete this file | https://www.inspora.design/posts/7-6 |  |
| 7-5 | Folder interaction | Motion | 动效/微交互灵感视频：Folder interaction | https://www.inspora.design/posts/7-5 |  |
| 7-4 | Carousel animation | Motion | 动效/微交互灵感视频：Carousel animation | https://www.inspora.design/posts/7-4 |  |
| 7-3 | Assets overview carousel | Product | 产品界面/应用 UI灵感视频：Assets overview carousel | https://www.inspora.design/posts/7-3 |  |
| 7-2 | Sketch logo | Illustration | 插画/拟物视觉灵感图片：Sketch logo | https://www.inspora.design/posts/7-2 |  |
| 8-2 | Liquid Glow Button | Motion | 动效/微交互灵感视频：Liquid Glow Button | https://www.inspora.design/posts/8-2 |  |
| 7-1 | Button motion | Motion | 动效/微交互灵感视频：Button motion | https://www.inspora.design/posts/7-1 |  |
| 6-9 | Thinking states | Motion | 动效/微交互灵感视频：Thinking states | https://www.inspora.design/posts/6-9 |  |
| 6-8 | A sending animation | Motion | 动效/微交互灵感视频：A sending animation | https://www.inspora.design/posts/6-8 |  |
| 6-7 | 3D Rolling transition | Illustration | 插画/拟物视觉灵感视频：3D Rolling transition（Featured 精选） | https://www.inspora.design/posts/6-7 | featured |
| 6-6 | Isometric animation | Illustration | 插画/拟物视觉灵感视频：Isometric animation | https://www.inspora.design/posts/6-6 |  |
| 6-5 | Liquid metal | Illustration | 插画/拟物视觉灵感视频：Liquid metal | https://www.inspora.design/posts/6-5 |  |
| 6-4 | hero concepts for a hiring platform | Web | 网页/落地页区块灵感图片：hero concepts for a hiring platform | https://www.inspora.design/posts/6-4 |  |
| 6-3 | Shader Mixer | Motion | 动效/微交互灵感视频：Shader Mixer | https://www.inspora.design/posts/6-3 |  |
| 6-2 | Camera transitions | Motion | 动效/微交互灵感视频：Camera transitions | https://www.inspora.design/posts/6-2 |  |
| 6-1 | Light work | Motion | 动效/微交互灵感视频：Light work | https://www.inspora.design/posts/6-1 |  |
| 5-9 | Motion blur | Motion | 动效/微交互灵感视频：Motion blur | https://www.inspora.design/posts/5-9 |  |
| 5-8 | Animated thinking orb | Motion | 动效/微交互灵感视频：Animated thinking orb | https://www.inspora.design/posts/5-8 |  |
| 5-7 | Shader Slider | Motion | 动效/微交互灵感视频：Shader Slider | https://www.inspora.design/posts/5-7 |  |
| 5-6 | Clucky Landing page | Web | 网页/落地页区块灵感视频：Clucky Landing page | https://www.inspora.design/posts/5-6 |  |
| 5-5 | Book animation | Motion | 动效/微交互灵感视频：Book animation | https://www.inspora.design/posts/5-5 |  |
| 5-4 | Floating cards | Motion | 动效/微交互灵感视频：Floating cards | https://www.inspora.design/posts/5-4 |  |
| 5-3 | Personal portfolio | Web | 网页/落地页区块灵感视频：Personal portfolio | https://www.inspora.design/posts/5-3 |  |
| 5-2 | Balance details | Product | 产品界面/应用 UI灵感视频：Balance details | https://www.inspora.design/posts/5-2 |  |
| 5-1 | subscription tracker calendar | Product | 产品界面/应用 UI灵感图片：subscription tracker calendar | https://www.inspora.design/posts/5-1 |  |
| 4-9 | Expandable Tab Bar | Product | 产品界面/应用 UI灵感视频：Expandable Tab Bar | https://www.inspora.design/posts/4-9 |  |
| 4-8 | Brand work | Branding | 品牌/图标/Logo灵感图片：Brand work | https://www.inspora.design/posts/4-8 |  |
| 4-7 | Receipt Printer | Motion | 动效/微交互灵感视频：Receipt Printer | https://www.inspora.design/posts/4-7 |  |
| 4-6 | Hero Section | Web | 网页/落地页区块灵感视频：Hero Section | https://www.inspora.design/posts/4-6 |  |
| 4-5 | Gooey liquid effect | Motion | 动效/微交互灵感视频：Gooey liquid effect | https://www.inspora.design/posts/4-5 |  |
| 4-4 | Earnings posters | Print | 印刷/海报灵感视频：Earnings posters | https://www.inspora.design/posts/4-4 |  |
| 4-3 | Weather Widget | Product | 产品界面/应用 UI灵感视频：Weather Widget | https://www.inspora.design/posts/4-3 |  |
| 4-2 | A soft-UI app icon | Branding | 品牌/图标/Logo灵感图片：A soft-UI app icon | https://www.inspora.design/posts/4-2 |  |
| 4-1 | Age Progression slider | Motion | 动效/微交互灵感视频：Age Progression slider | https://www.inspora.design/posts/4-1 |  |
| 3-9 | A brick button | Motion | 动效/微交互灵感视频：A brick button | https://www.inspora.design/posts/3-9 |  |
| 3-7 | Flight Card | Product | 产品界面/应用 UI灵感视频：Flight Card | https://www.inspora.design/posts/3-7 |  |
| 3-6 | Liquid glass | Product | 产品界面/应用 UI灵感图片：Liquid glass | https://www.inspora.design/posts/3-6 |  |
| 3-5 | Notification Cards | Motion | 动效/微交互灵感视频：Notification Cards | https://www.inspora.design/posts/3-5 |  |
| 3-4 | Two-Step Dock Menu | Product | 产品界面/应用 UI灵感视频：Two-Step Dock Menu | https://www.inspora.design/posts/3-4 |  |
| 3-3 | Testimonials puzzle | Web | 网页/落地页区块灵感视频：Testimonials puzzle | https://www.inspora.design/posts/3-3 |  |
| 3-2 | Take your wallet everywhere. | Product | 产品界面/应用 UI灵感视频：Take your wallet everywhere. | https://www.inspora.design/posts/3-2 |  |
| 3-1 | Boat loader | 3D | 3D灵感视频：Boat loader | https://www.inspora.design/posts/3-1 |  |
| 2-9 | Jelly Switch | Motion | 动效/微交互灵感视频：Jelly Switch | https://www.inspora.design/posts/2-9 |  |
| 2-8 | AI Motion | Motion | 动效/微交互灵感视频：AI Motion | https://www.inspora.design/posts/2-8 |  |
| 2-7 | Stamp Folder animation | Motion | 动效/微交互灵感视频：Stamp Folder animation | https://www.inspora.design/posts/2-7 |  |
| 2-6 | e-signature field | Illustration | 插画/拟物视觉灵感视频：e-signature field（Featured 精选） | https://www.inspora.design/posts/2-6 | featured |
| 2-5 | Glowing particle burst | Motion | 动效/微交互灵感视频：Glowing particle burst | https://www.inspora.design/posts/2-5 |  |
| 2-4 | Dynamic island lego | Illustration | 插画/拟物视觉灵感视频：Dynamic island lego | https://www.inspora.design/posts/2-4 |  |
| 2-3 | Abstract gradient | Motion | 动效/微交互灵感视频：Abstract gradient | https://www.inspora.design/posts/2-3 |  |
| 2-2 | MacOS | Illustration | 插画/拟物视觉灵感图片：MacOS | https://www.inspora.design/posts/2-2 |  |
| 2-1 | Confidential file animation | Motion | 动效/微交互灵感视频：Confidential file animation | https://www.inspora.design/posts/2-1 |  |
| 1-9 | Footer.mp4 | Web | 网页/落地页区块灵感视频：Footer.mp4 | https://www.inspora.design/posts/1-9 |  |
| 1-8 | Nsight Studio | Branding | 品牌/图标/Logo灵感视频：Nsight Studio | https://www.inspora.design/posts/1-8 |  |
| 1-7 | X money | Product | 产品界面/应用 UI灵感视频：X money | https://www.inspora.design/posts/1-7 |  |
| 1-6 | Liquid Glass | Motion | 动效/微交互灵感视频：Liquid Glass（Featured 精选） | https://www.inspora.design/posts/1-6 | featured |
| 1-5 | Date picker | Product | 产品界面/应用 UI灵感视频：Date picker | https://www.inspora.design/posts/1-5 |  |
| 1-4 | Liquid gold | Motion | 动效/微交互灵感视频：Liquid gold | https://www.inspora.design/posts/1-4 |  |
| 1-3 | Dither Motion | Motion | 动效/微交互灵感视频：Dither Motion | https://www.inspora.design/posts/1-3 |  |
| 1-2 | Jelly Slider | Motion | 动效/微交互灵感视频：Jelly Slider（Featured 精选） | https://www.inspora.design/posts/1-2 | featured |
| 1-1 | Brightness & volume controller | Motion | 动效/微交互灵感视频：Brightness & volume controller | https://www.inspora.design/posts/1-1 |  |
| 1-visualexploration | Visual Exploration | Branding | 品牌/图标/Logo灵感视频：Visual Exploration | https://www.inspora.design/posts/1-visualexploration |  |
| quartr-meta | Quartr x Meta Earnings | Print | 印刷/海报灵感视频：Quartr x Meta Earnings | https://www.inspora.design/posts/quartr-meta |  |
| 404-page-2 | 404 page | Web | 网页/落地页区块灵感视频：404 page | https://www.inspora.design/posts/404-page-2 |  |
| 404-page | 404 page | Web | 网页/落地页区块灵感视频：404 page | https://www.inspora.design/posts/404-page |  |
## 未解决
- `/posts/{slug}`、`/sitemap.xml`、`/api/posts` 对 curl 返回 429（Vercel Security Checkpoint 挑战），只能用真实浏览器访问；无头 curl 只能拿各分类首屏 16 条。
- robots.txt 禁止 `/api/`。本清单是 2026-10-07 的快照，运行时不调用该接口，只用分类首页的 16 条。
- 详情页的 Industries / Colors / Styles 标签没有批量接口，清单里没有这些字段。
- sitemap.xml 过期（142 条、缺新帖），不能用来列全集。
- 不提供任何代码、提示词或模板下载。
