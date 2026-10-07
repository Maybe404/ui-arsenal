---
id: originkit
name: Originkit
url: https://www.originkit.dev/
kind: component-library
stack: React / Next.js / Vite（TSX，"use client"；依赖视组件而定：framer-motion、three、motion、gsap、ogl 等），同一份源码也可导出为 Framer code component
license: 自定义（Originkit Licensing & Usage：可用于自有/客户项目，禁止把组件本身再分发/做成模板或组件市场出售）
pro: partial（236/593 个 component、39/58 个 section、16/23 个 template 需 Pro/Ultimate 订阅；免费账号每天 10 个 component / 10 个 section / 1 个 template）
fetch: npm
verified: 2026-10-07
source_status: active
visual_style: flashy webgl/3d showcase effects
foundation: none
styling: unknown
motion_lib: mixed(framer-motion,three,motion,gsap,ogl)
dark_mode: unknown
mixing_notes: 取码要用户登录；同一项目里 framer-motion 和 motion 只留一种写法，颜色按主底座传参，一页最多一个重 WebGL 背景
---
## 是什么 / 什么时候用
Originkit 自称最大的免费动效组件库：593 个 component（其中约 200 个是 WebGL/shader/Canvas 背景动画）、58 个页面区块 section（hero 47、features 4、pricing 3、cta 2、footer 2）和 23 套整站模板。风格偏"炫"：3D、粒子、液态、光带、动态文字、画廊、preloader、自定义光标、网页小游戏。
适合：落地页 / 作品集需要一个抓眼球的 hero 背景、文字入场、图片画廊或 loading 动画。不适合：常规业务 UI（表单、表格、对话框，去 shadcn）；对包体积敏感、不能引入 three.js 的页面。
所有正式取码途径（CLI / MCP / 网页 Copy）都需要登录 Originkit 账号；标 pro 的条目还需要付费订阅。

## 按需获取方法
**1. 列出 / 搜索全部条目（无需登录，已实测）**
```sh
curl -s https://mcp.originkit.dev/v1/registry | jq '.count, .components[0]'   # 651 条：name, displayName, category, kind(component|section), description, tags, dependencies
npx -y originkit list --json                          # 同上，CLI 封装
npx -y originkit list --category loader               # 按分类；--kind component|section
npx -y originkit search "text reveal"                 # 关键词搜索
```
registry 不返回 Pro 标记。要判断 Pro，看本目录 originkit.tsv 的 access 列（`pro` 或 `login`）；不确定时请用户在浏览器里打开组件页确认，不从页面数据里抓取。

**2. 官方取码：CLI（类似 shadcn，需要登录）**
```sh
npx originkit login                   # 浏览器登录（必须由用户本人完成，agent 不代为登录）
# 或 export ORIGINKIT_API_KEY=<key>   # 在 Originkit → Profile → API Keys 创建
npx originkit init                    # 生成 components.json（安装目录、alias、TS）
npx originkit add {name}              # 写入 ui/{name}.tsx 并 npm 安装依赖
npx originkit add {name} --dark       # 指定 preset，输出到 ui/{name}-dark.tsx
npx originkit add {name} --dry-run    # 只打印要写的文件
npx originkit whoami                  # 查看当前凭据，不耗额度
```
实测（2026-10-07）：未登录时 `list` / `search` 正常；`npx originkit add tiles-loader --dry-run` 报 "You're not signed in"。登录后的 add 未测，因为规范不允许登录。
额度：`add`、网页复制代码、MCP `get_component` / `fetch` 都计入每日额度（Free 10、Pro 25、Ultimate 不限，均为 IST 日）；另有 fair use：1 小时内超过 15 个会暂停 4 小时。复制 CLI 命令或 AI prompt、浏览、预览不计额度。

**3. 官方取码：MCP / Copy → AI prompt**
托管 MCP 服务：`https://mcp.originkit.dev`。聊天类客户端走 Originkit OAuth 登录；代码编辑器类客户端用 API key。文档列出的能力有：按分类列目录、取某组件源码（可按技术栈改写、可带 tweak 参数）、关键词搜索（返回带引用 URL 的结果）、`fetch` 取 Next.js 版源码。工具名在文档里出现过 `get_component` 和 `fetch`。
网页上调好参数后点 Copy → AI prompt，会得到形如 "Using originkit MCP, get me the {name} component, dark theme, accent #7C3AED…" 的提示词，交给已接入 MCP 的 agent 执行。这个按钮要在浏览器里点，curl 拿不到。

**4. 不从页面提取源码**
免费组件的页面里虽然嵌着源码，但 OriginKit 条款禁止自动化抓取，所以**不写脚本从页面提取**。拿代码只走第 2、3 种方式（CLI 或 MCP），登录由用户自己完成。用户没有账号或当天额度用完时，告诉用户，改用其他来源里功能相近的免费组件。

依赖：registry 条目的 `dependencies` 字段（如 `three`、`framer-motion`、`motion`、`gsap`、`ogl`），自行 `npm i`。

## 使用注意
- 组件是单文件 TSX、`export default`，props 就是网页控制面板里的参数；preset 版本把参数写死成默认值。
- 依赖分布：framer-motion 101、three 98、motion 43、gsap 13、ogl 2，另有 matter-js、d3-geo、threejs-components 各 1。framer-motion 和 motion 两种写法都有，同一项目里注意别重复引入两套。
- 大量 WebGL / three.js 全屏背景，注意移动端性能、SSR（必须 "use client"，Next.js 里可能要 dynamic import + ssr:false）和包体积。
- 变体命名：registry 名 `ribbon-glow-02`，对应页面 URL `/components/ribbon-glow/02`。
- Section 是多文件（区块加子组件），只能在 React/Next.js 里用，不能用于 Framer；Framer 只支持 component。
- 授权：可以用在自己或客户的网站和产品里；禁止转售或再分发组件本身，包括付费模板、starter kit、Figma 复刻和公开仓库转载。条款也禁止自动化抓取和批量提取，所以 agent 只能按需取单个组件，不要批量抓。
- 预览里的字体和图片仅供演示，不在授权范围内。

## 组件清单
条目共 674 个（593 component + 58 section + 23 template），超过 500，下表只列到分类级；逐条清单（含中文描述、Pro 标记、取码命令）见 `sources/originkit.tsv`。运行时可以用 `curl -s https://mcp.originkit.dev/v1/registry` 或 `npx originkit list --json` 拿到全部 component 和 section（模板除外）。

| id | 名称 | 分类 | 一句话用途 | 获取（具体命令或URL） | 备注 |
|---|---|---|---|---|---|
| category:background-animation | background-animation | component | 背景动画（WebGL/shader/Canvas 全屏背景，hero 背景）；共 202（免费 133 / Pro 69），例：cursor-ring-field, silk-waves, ribbon-glow-02, reflect-shader, stream-convergence | https://www.originkit.dev/category/background-animation；`npx originkit list --category background-animation` |  |
| category:interactive-elements | interactive-elements | component | 交互元素（3D 物体、粒子球、可拖拽装饰）；共 96（免费 57 / Pro 39），例：plasma-ring, particle-jupiter, harmonic-shell, bubble-burst, rubber-spheres | https://www.originkit.dev/category/interactive-elements；`npx originkit list --category interactive-elements` |  |
| category:text | text | component | 文字动效（标题入场、hover 文字、滚动文字）；共 75（免费 40 / Pro 35），例：spring-text, textmorph, video-text, infinite-text-passage, domino-text-fall | https://www.originkit.dev/category/text；`npx originkit list --category text` |  |
| category:animation | animation | component | 动画装饰（线条、粒子、动态图形）；共 53（免费 36 / Pro 17），例：reactive-lines, vortex-dust-fall, kinetic-text, wave-arcs, dither-globe | https://www.originkit.dev/category/animation；`npx originkit list --category animation` |  |
| category:hero | hero | section | 页面区块 section：hero；共 47（免费 11 / Pro 36），例：hero-05, hero-21, hero-13, hero-24, hero-29 | https://www.originkit.dev/sections/category/hero；`npx originkit add <name>` | pro 占多数 |
| category:image-gallery | image-gallery | component | 图片画廊/轮播（carousel、3D 画廊）；共 45（免费 15 / Pro 30），例：flip-gallery, roundcarousel, rotunda-carousel, infinitegallery, boxcarousel | https://www.originkit.dev/category/image-gallery；`npx originkit list --category image-gallery` | pro 占多数 |
| category:image | image | component | 图片效果（hover 揭示、扭曲、翻转）；共 43（免费 27 / Pro 16），例：image-flipper, liquid-distortion, sticker-peel, dry-brush-reveal, fluid-image-reveal | https://www.originkit.dev/category/image；`npx originkit list --category image` |  |
| category:loader | loader | component | 加载动画/全屏 preloader；共 24（免费 22 / Pro 2），例：metal-unfold, particle-tether, motion-orbit, particle-dome, particle-pulse | https://www.originkit.dev/category/loader；`npx originkit list --category loader` |  |
| category:cursor | cursor | component | 自定义光标效果；共 23（免费 5 / Pro 18），例：spin-cursor, glyph-burst, usercursor, text-button-cursor, inkbleed-cursor | https://www.originkit.dev/category/cursor；`npx originkit list --category cursor` | pro 占多数 |
| category:template | template | template | 整站模板 template（React/Next.js 多页）；共 23（免费 7 / Pro 16），例：operun, fintra, clever, prismo, closor | https://www.originkit.dev/templates/{slug}；`npx originkit add {slug}`（模板不在 registry 列表里） | pro 占多数 |
| category:button | button | component | 按钮；共 21（免费 13 / Pro 8），例：keycap-button, dotted-offset-button, liquid-carve-button, label-slide-button, slide-fill-button | https://www.originkit.dev/category/button；`npx originkit list --category button` |  |
| category:games | games | component | 网页小游戏；共 7（免费 5 / Pro 2），例：pixel-run-game, flap, slice-blade, stack-tower, deparkanoid | https://www.originkit.dev/category/games；`npx originkit list --category games` |  |
| category:border | border | component | 边框发光动效；共 4（免费 4 / Pro 0），例：neon-border, pulsating-border, electricborder, glow-border | https://www.originkit.dev/category/border；`npx originkit list --category border` |  |
| category:features | features | section | 页面区块 section：features；共 4（免费 4 / Pro 0），例：features-02, features-03, features-04, features-01 | https://www.originkit.dev/sections/category/features；`npx originkit add <name>` |  |
| category:pricing | pricing | section | 页面区块 section：pricing；共 3（免费 3 / Pro 0），例：pricing-02, pricing-03, pricing-01 | https://www.originkit.dev/sections/category/pricing；`npx originkit add <name>` |  |
| category:footer | footer | section | 页面区块 section：footer；共 2（免费 1 / Pro 1），例：footer-02, footer-01 | https://www.originkit.dev/sections/category/footer；`npx originkit add <name>` |  |
| category:cta | cta | section | 页面区块 section：cta；共 2（免费 0 / Pro 2），例：cta-02, cta-01 | https://www.originkit.dev/sections/category/cta；`npx originkit add <name>` | pro 占多数 |

## 未解决
- 所有正式取码途径（CLI add、MCP、网页 Copy code）都需要登录，按规范没有登录，所以 `add` 的成功路径没有实测，只验证了未登录时的报错。不从页面提取源码（见第 4 节）。
- Pro 条目（component 236、section 39、template 16）需要付费订阅，没有测试，也不提供绕过方法。
- MCP 的确切 URL 路径（是否带 `/mcp` 等后缀）和完整工具清单需要登录后在 Settings 里查看，文档里只能确认主机 `mcp.originkit.dev` 以及 `get_component`、`fetch` 两个工具名。
- 模板不在 registry 里，也不在 sitemap 里（`/templates/{slug}` 页面可以打开）；模板价格字段是 null，Pro 标记来自页面数据里的 `paid`。
- section 的 registry 描述大多只是 "Hero 05 component." 这样的占位文字，tsv 里的中文描述是按名称、标签推断的，区分度有限，选用前要看页面预览视频（galleryMedia，cdn.originkit.dev）。
