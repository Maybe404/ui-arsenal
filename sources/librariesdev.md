---
id: librariesdev
name: Libraries.dev
url: https://libraries.dev
kind: effects
stack: React 18+（零运行时依赖；img-fx 需 three），部分库有 React Native / SwiftUI 端口（未上 npm）
license: MIT（npm 包与 GitHub 仓库）；Studio 导出、Pro 预设/配方为商业授权
pro: partial（7 个库本身全部免费；Studio、Pro 预设/配色/额外形状与状态、Pro skill 付费：Pro 月付 / Lifetime $149 / Business $59/mo）
fetch: npm
verified: 2026-10-07
source_status: active
visual_style: ai-state glow and canvas/webgl effects
foundation: none
styling: inline
motion_lib: mixed(none,three)
dark_mode: prop
mixing_notes: 颜色和明暗走 props 不读主底座 token；border-beam 默认 theme="dark" 且 auto 只看 prefers-color-scheme，站内手动切暗色时要显式传 theme；同一元素或相邻元素不要叠两个特效
---
## 是什么 / 什么时候用
Jakub Antalik 做的 7 个"AI 时代"React 动效库，每个库都是独立 npm 包和一个组件，包住你已有的元素即可：Border beam（边框光束）、Thinking orbs（AI 思考点阵球）、Gooey（液态融合）、Voice（语音光晕）、Bot avatars（agent 动画头像）、Liquid metal（液态金属按钮/徽章/文字）、Image（图片生成占位 loader）。
做 AI 产品的等待态（thinking / searching / 生成图片）、聊天输入框高亮、语音输入、agent 头像、付费 CTA/徽章时优先考虑。作者给出的放置规则：等待不足 2 秒不加任何效果；2 秒以上用 Thinking orbs；超过 3 秒再给工作中的元素加 Border beam；同一元素或相邻元素不要叠加两个效果。

## 按需获取方法
机器可读入口（均已实测）：
1. **官方 agent skill（最推荐，含每个库全部免费 props、配方、常见坑）**
   - 总览：`curl -s https://raw.githubusercontent.com/Jakubantalik/Libraries.dev/main/skills/libraries-dev/SKILL.md`
   - 单库参考：`curl -s https://raw.githubusercontent.com/Jakubantalik/Libraries.dev/main/skills/libraries-dev/references/{ref}.md`
     ref 取值：`01-border-beam` `02-thinking-orbs` `03-liquid-gooey` `04-voice-glow` `05-bot-avatars` `06-metal-fx` `07-img-fx`
   - 安装成 skill：`npx libraries-dev skill`（装到 ~/.claude/skills/libraries-dev）或 `npx skills add Jakubantalik/Libraries.dev`
2. **Copy prompt 原文**：每个库页面的"Copy prompt"按钮复制的是静态 HTML 里的 `<pre id="agent-prompt" hidden>`，curl 即可拿到，不需要渲染：
   ```bash
   curl -sL https://libraries.dev/{page} | python3 -c "import sys,re,html;print(html.unescape(re.search(r'<pre id=\"agent-prompt\" hidden>(.*?)</pre>',sys.stdin.read(),re.S).group(1)))"
   ```
   page 取值：`beam` `orbs` `gooey` `voice` `bots`（`avatars` 同一页）`metal` `image`
3. **安装**：`npm install {pkg}`，pkg = `border-beam` `thinking-orbs` `liquid-gooey` `voice-glow` `bot-avatars` `metal-fx` `img-fx`（img-fx 另装 `three`）。当前版本：border-beam 1.4.1、thinking-orbs 0.3.2、liquid-gooey 0.2.2、voice-glow 0.3.0、bot-avatars 0.2.2、metal-fx 2.0.11、img-fx 0.5.1。
4. **源码**：GitHub `Jakubantalik/Libraries.dev`（MIT），`packages/{pkg}/src/`，raw 前缀 `https://raw.githubusercontent.com/Jakubantalik/Libraries.dev/main/`。RN/SwiftUI 端口在 `packages/{pkg}/ports/`（metal-fx 的在 `packages/metal-fx/ports/`）。

实测例子（orbs，2026-10-07）：
- `curl -sL https://libraries.dev/orbs | …` 拿到的 prompt 开头为 "Add the Orb effect from Libraries.dev to my React app. / npm install thinking-orbs / `<ThinkingOrb state="searching" size={64} />`"，并列出 9 个 state。
- 参考文档 `references/02-thinking-orbs.md` 正常返回（256 行）。
- 最小用法：
  ```tsx
  import { ThinkingOrb } from 'thinking-orbs';
  <ThinkingOrb state="searching" size={64} theme="auto" />
  ```

站点没有 sitemap.xml / llms.txt / registry.json（这些路径都回落到首页 HTML），robots.txt 允许全部抓取。

## 使用注意
- 所有包都需要 React ≥ 18；canvas/WebGL 组件在 Next.js App Router 里要放进 `"use client"` 文件（包本身没写这个指令）。
- **Copy prompt 有已知错误**：orbs 的 prompt 写了 `dark: boolean` 和 `speed`，实际不存在，主题要用 `theme="dark|light|auto"`（官方 skill 也特别说明了）。beam 的 prompt 里出现的 `sm`/`ocean`/`sunset` 是包里真实存在的值，只是页面调参器没露出来。所以**以 skill 参考文档为准，prompt 只作为快速粘贴**。
- Thinking orbs 只针对 64 / 20 两档尺寸调过，用 CSS 放大会糊；在浅色应用里的深色卡片上要固定 `theme`。
- Metal 和 Image 跑 WebGL，开销最大；同一页的金属元素共用一种颜色，两个金属按钮不要挨着放。metal-fx 2.x 是基于 Paper Shaders 的 v2 引擎，要 v1 就装 `metal-fx@1`。
- img-fx 需要 peer 依赖 `three >= 0.149`。
- bot-avatars 包里的类型定义有 18 种形状，但免费页面和 skill 只开放 8 种，另外 10 种和 `sleeping` 状态属于 Pro（类型是写在包里的，能不能直接传值使用没有实测，按授权视为 Pro）。
- React Native 端口（`*-native`）**没有发布到 npm**，只能从仓库目录本地引用；Expo 需要 `expo run:ios/android`。SwiftUI 包用本地 Swift Package，Metal shader 要通过 Xcode 构建。
- 多数库处理了 `prefers-reduced-motion`（降为静帧）并在离屏时暂停，不要覆盖这些行为。**例外**：border-beam 官方文档写明旋转类型（`md`、`sm`、`line`）不处理减弱动效，用这些类型时要自己在 `prefers-reduced-motion: reduce` 下关掉或换成静态边框（2026-10-07 核实）。

## 组件清单
| id | 名称 | 分类 | 一句话用途 | 获取（具体命令或URL） | 备注 |
|---|---|---|---|---|---|
| border-beam | Border beam | border/glow | 沿卡片/按钮/输入框边框游走的彩虹光束 border beam glow，AI 输入框、激活卡片高亮；React，<BorderBeam> 包裹元素 | `npm i border-beam`；prompt 见 libraries.dev/beam |  |
| border-beam-md | BorderBeam size="md" | border/glow | 整圈边框游走光束（默认类型），卡片/面板高亮 animated border | `npm i border-beam`；prompt 见 libraries.dev/beam |  |
| border-beam-line | BorderBeam size="line" | border/glow | 底边游走发光线，提交后等待结果的搜索框/命令框 loading 状态 | `npm i border-beam`；prompt 见 libraries.dev/beam |  |
| border-beam-sm | BorderBeam size="sm" | border/glow | 按钮尺寸的紧凑边框光束 compact beam | `npm i border-beam`；prompt 见 libraries.dev/beam |  |
| border-beam-pulse-inner | BorderBeam size="pulse-inner" | border/glow | 边框内侧呼吸脉冲光，CTA 按钮高亮 pulse | `npm i border-beam`；prompt 见 libraries.dev/beam |  |
| border-beam-pulse-outside | BorderBeam size="pulse-outside" | border/glow | 边框向外扩散的脉冲光晕，prompt 输入框高亮 pulse bloom | `npm i border-beam`；prompt 见 libraries.dev/beam |  |
| border-beam-palettes | colorVariant colorful/mono/ocean/sunset | border/glow | 边框光束配色：彩虹/灰阶/海洋/日落 palette | `npm i border-beam`；prompt 见 libraries.dev/beam |  |
| border-beam-pro-palettes | Beam Pro palettes (Forest/Candy/Ice/Gold) + 细调 | border/glow | Pro 配色与时长、光晕、色相等细调，仅 Studio/Pro skill | https://libraries.dev/studio | pro |
| thinking-orbs | Thinking orbs | loader/ai-status | AI 思考中点阵 3D 小球 loading 指示器 thinking orb spinner 替代，9 种动画状态，2D canvas 无 WebGL | `npm i thinking-orbs`；prompt 见 libraries.dev/orbs |  |
| thinking-orbs-working | ThinkingOrb state="working" | loader/ai-status | 粒子沿倾斜轨道运动，通用 agent 工作中/工具调用中 loading | `npm i thinking-orbs`；prompt 见 libraries.dev/orbs |  |
| thinking-orbs-searching | ThinkingOrb state="searching" | loader/ai-status | 扫描子午线扫过点阵地球，联网搜索/检索/RAG 中 | `npm i thinking-orbs`；prompt 见 libraries.dev/orbs |  |
| thinking-orbs-solving | ThinkingOrb state="solving" | loader/ai-status | 条带四分之一转打乱再复位，代码执行/数学/调试中 | `npm i thinking-orbs`；prompt 见 libraries.dev/orbs |  |
| thinking-orbs-listening | ThinkingOrb state="listening" | loader/ai-status | 纬线环上滚动波形，麦克风录音/语音输入中 | `npm i thinking-orbs`；prompt 见 libraries.dev/orbs |  |
| thinking-orbs-connecting | ThinkingOrb state="connecting" | loader/ai-status | 星座连线+数据包流动，连接服务/MCP/数据源中 | `npm i thinking-orbs`；prompt 见 libraries.dev/orbs |  |
| thinking-orbs-weaving | ThinkingOrb state="weaving" | loader/ai-status | 三股线绕球编织，规划/planning/合并结果中 | `npm i thinking-orbs`；prompt 见 libraries.dev/orbs |  |
| thinking-orbs-composing | ThinkingOrb state="composing" | loader/ai-status | 起伏多带饰带，写作/生成文本/打字指示器替代 | `npm i thinking-orbs`；prompt 见 libraries.dev/orbs |  |
| thinking-orbs-breathing | ThinkingOrb state="breathing" | loader/ai-status | 正面圆环缓慢变形呼吸，空闲 Thinking…/推理中 | `npm i thinking-orbs`；prompt 见 libraries.dev/orbs |  |
| thinking-orbs-shaping | ThinkingOrb state="shaping" | loader/ai-status | 点阵轮廓在圆/三角/方之间变形，设计/构建布局中 | `npm i thinking-orbs`；prompt 见 libraries.dev/orbs |  |
| thinking-orbs-pro | Orbs Pro (32px、速度、墨色、点密度、每状态细调、几何重建) | loader/ai-status | Orb 的 Pro 细调选项，仅 Studio/Pro skill | https://libraries.dev/studio | pro |
| liquid-gooey | Gooey (Liquid) | liquid/morph | 液态融合 gooey 效果：元素靠近时像黏液合并、像果冻变形且文字保持清晰；SVG filter，<Liquid>/<Liquid.Item> | `npm i liquid-gooey`；prompt 见 libraries.dev/gooey |  |
| liquid-gooey-morph | Liquid.Item effect="morph" | liquid/morph | 元素合并/分裂，加号 FAB 菜单展开成多个按钮 gooey menu | `npm i liquid-gooey`；prompt 见 libraries.dev/gooey |  |
| liquid-gooey-move | Liquid.Item effect="move" | liquid/morph | 表面跟随移动元素拖出液滴尾巴，液态 tab 指示器/滑块 thumb | `npm i liquid-gooey`；prompt 见 libraries.dev/gooey |  |
| liquid-gooey-bend | Liquid.Item effect="bend" | liquid/morph | 拖拽时卡片随速度弯曲，可拖拽卡片 drag card | `npm i liquid-gooey`；prompt 见 libraries.dev/gooey |  |
| liquid-gooey-melt | Liquid.Item effect="melt" | liquid/morph | 两张图片熔化互相流入，image melt 过渡 | `npm i liquid-gooey`；prompt 见 libraries.dev/gooey |  |
| liquid-gooey-pro | Gooey Pro (波纹、编排时序、物理参数、滤镜链重建) | liquid/morph | Gooey 的 Pro 细调，仅 Studio/Pro skill | https://libraries.dev/studio | pro |
| voice-glow | Voice (VoiceBeam) | voice/audio | 随说话音量从聊天输入框/手机屏底部升起的彩色光晕 voice visualizer，处理中左右扫动；含 useMicrophone | `npm i voice-glow`；prompt 见 libraries.dev/voice |  |
| voice-glow-default | VoiceBeam type="default" | voice/audio | 约 350px 聊天输入框的语音光晕预设 | `npm i voice-glow`；prompt 见 libraries.dev/voice |  |
| voice-glow-mobile | VoiceBeam type="mobile" | voice/audio | 手机屏幕底部语音光晕预设，范围更宽更高 | `npm i voice-glow`；prompt 见 libraries.dev/voice |  |
| voice-glow-processing | VoiceBeam processing | voice/audio | 光晕聚成一束来回扫动，语音转写/回复思考中 | `npm i voice-glow`；prompt 见 libraries.dev/voice |  |
| voice-glow-usemicrophone | useMicrophone() | voice/audio | 麦克风权限与 MediaStream 管理 hook（start/stop/state） | `npm i voice-glow`；prompt 见 libraries.dev/voice |  |
| voice-glow-pro | Voice Pro (配色、输入链、形状、录音胶囊宿主) | voice/audio | Voice 的 Pro 细调，仅 Studio/Pro skill | https://libraries.dev/studio | pro |
| bot-avatars | Bot avatars | avatar | AI agent 动画头像：毛绒/塑料质感 3D 形状带表情，会四处看、跳、工作时蹦跳；canvas 无 WebGL | `npm i bot-avatars`；prompt 见 libraries.dev/bots |  |
| bot-avatars-free-types | BotAvatar type: clover/flower/star/ghost/mech/circle/hexagon/square | avatar | 8 种免费身体形状 bot 头像，state default/working，size 96/64/32，shading fabric/plastic | `npm i bot-avatars`；prompt 见 libraries.dev/bots |  |
| bot-avatars-pro-types | BotAvatar Pro types: triangle/blob/drop/droid/alien/cat/cloud/pill/pebble/puddle | avatar | 另外 10 种身体形状（包内类型已存在，页面/免费 skill 未开放） | https://libraries.dev/studio | pro |
| bot-avatars-pro-extras | Bot avatars Pro (sleeping 状态、帽子眼镜耳机领结、毛发灯光、自定义轮廓) | avatar | sleeping 睡眠态、配饰、毛发/光照细调、自定义 SVG 轮廓 | https://libraries.dev/studio | pro |
| metal-fx | Liquid metal (metal-fx) | metal/shader | 实时液态金属材质：按钮/图标/文字/徽章，游走光晕、邻近元素反射、光标弯折；WebGL（v2 基于 Paper Shaders） | `npm i metal-fx`；prompt 见 libraries.dev/metal |  |
| metal-fx-button | MetalFx variant="button" | metal/shader | 液态金属描边胶囊按钮，卖东西的 CTA（Get Pro/Upgrade） | `npm i metal-fx`；prompt 见 libraries.dev/metal |  |
| metal-fx-circle | MetalFx variant="circle" | metal/shader | 液态金属圆形图标按钮（如发送按钮） | `npm i metal-fx`；prompt 见 libraries.dev/metal |  |
| metal-fx-text | MetalText | metal/shader | 液态金属文字，大标题 h1 高亮 headline | `npm i metal-fx`；prompt 见 libraries.dev/metal |  |
| metal-fx-badge | MetalBadge | metal/shader | 液态金属徽章 New/Pro/Beta badge | `npm i metal-fx`；prompt 见 libraries.dev/metal |  |
| metal-fx-presets | preset chromatic/silver/gold + useMetalBend/useMetalTextReflection | metal/shader | 金属配色预设与光标弯折、文字反射 hook | `npm i metal-fx`；prompt 见 libraries.dev/metal |  |
| metal-fx-v1 | metal-fx@1 (v1 engine) | metal/shader | 旧版 v1 金属引擎 | npm i metal-fx@1 |  |
| metal-fx-pro | Metal Pro (Button/Badge 调优基线、着色器尺度、环宽、引擎调参) | metal/shader | Metal 的 Pro 细调，仅 Studio/Pro skill | https://libraries.dev/studio | pro |
| img-fx | Image generation (img-fx) | loader/image | 图片生成占位 loader：WebGL 像素马赛克 shader 翻涌后溶解出真实图片，AI 生图/上传/懒加载；需要 three | `npm i img-fx three`；prompt 见 libraries.dev/image |  |
| img-fx-pixels-organic | preset="pixels-organic" | loader/image | 柔和云状像素马赛克生成占位 | `npm i img-fx three`；prompt 见 libraries.dev/image |  |
| img-fx-pixels-mechanic | preset="pixels-mechanic" | loader/image | 锐利网格对齐像素马赛克生成占位 | `npm i img-fx three`；prompt 见 libraries.dev/image |  |
| img-fx-sweep-gradient | preset="sweep-gradient" | loader/image | 对角渐变带扫过+格子闪烁，可替代 skeleton 骨架屏 | `npm i img-fx three`；prompt 见 libraries.dev/image |  |
| img-fx-pro | Image Pro (速度、像素格大小、Ocean/Ember/Mono 配色、shader 重建) | loader/image | Image 的 Pro 细调，仅 Studio/Pro skill | https://libraries.dev/studio | pro |
| libraries-dev-skill | libraries-dev agent skill (free) | tooling | 官方免费 agent skill：7 个库的安装、用法、放置规则，含 libraries reveal/review/apply 命令 | npx libraries-dev skill  或  npx skills add Jakubantalik/Libraries.dev  或 GitHub skills/libraries-dev/SKILL.md |  |
| libraries-pro-skill | libraries-pro agent skill | tooling | Pro skill：Studio 全部参数、配色、cursor gravity、核心几何/shader 定制契约 | npx libraries-dev skill --pro（需浏览器登录 Pro） | pro |
| studio | Studio | tooling | 全部库的深度可视化调参台 + AI agent 调参，导出 React/RN/SwiftUI 配置 | https://libraries.dev/studio | pro |

## 未解决
- Pro 内容（Studio、Pro 预设和配色、bot 的另外 10 种形状和 sleeping 状态、Pro skill）需要登录并付费，没有抓取，只按官方 skill 的 "Go further (Pro)" 段落列出。
- Pro 月付的具体价格在静态 HTML 里显示为空的 "$"（应该是客户端渲染的），能确认的只有 Lifetime $149、Business $59/月（或 $590/年）。
- RN/SwiftUI 端口没上 npm，没有实测构建。

## 风格字段说明（2026-10-07）
- `dark_mode: prop`：明暗都由 `theme` prop 决定。`auto` 的解析在各包不一致：thinking-orbs 先看祖先的 `data-theme` / `.dark` / `.light`，再看 `prefers-color-scheme`；border-beam（`src/BorderBeam.tsx`）的 `auto` 只看 `prefers-color-scheme`，且默认值是 `theme="dark"`。站点自己切换明暗时，显式传 `theme`。
- `motion_lib: mixed(none,three)`：多数包是自写 canvas / WebGL 循环，不依赖动效库；img-fx 需要 peer 依赖 `three`。
