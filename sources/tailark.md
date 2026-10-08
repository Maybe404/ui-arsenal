---
id: tailark
name: Tailark
url: https://tailark.com/
kind: blocks
stack: React + shadcn/ui（Radix 或 Base UI 两套）+ Tailwind CSS v4；少数区块用 motion-primitives、recharts、dotted-map
license: 开源版 MIT（GitHub tailark/blocks）；tailark.com 上的完整区块和插画需要付费套餐
pro: partial（tailark.com registry 的 264 个区块和 123 个插画组件要登录付费套餐，返回 401；开源版 dusk / mist / veil 三套 144 个区块免费）
fetch: github-raw
coverage: 付费部分：tailark.com registry 全量（区块、插画组件），refresh 自动比对；开源部分：tailark/blocks 仓库 base 版三套 kit 的 144 个区块，人工快照（仓库 2026-07-29 的提交），不自动刷新
catalog_checked: 2026-10-08
source_status: active
visual_style: clean saas marketing sections
foundation: shadcn-compatible
styling: tailwind-v4
motion_lib: mixed(css,motion)
dark_mode: class
mixing_notes: 开源版每套 kit 自带一份 ui（button、card 等，按 kit 微调过样式），和项目的 shadcn ui 同名，取码后改成引用项目自己的 ui；logo 墙用的品牌 SVG 只是示意，上线前换成真实客户
---
## 是什么 / 什么时候用
shadcn 风格的营销页区块库：hero、功能、bento、定价、FAQ、团队、评价、统计、logo 墙、集成、联系、登录注册、页脚等。做落地页、官网时按区块拼。付费版（tailark.com）区块多、带插画组件；开源版（MIT）分 dusk、mist、veil 三套视觉，每套 40–60 个区块，可以直接取源码。

## 按需获取方法
开源版（免费，本库登记为 `tailark:oss-<kit>-<category>-<n>`）：
- 源码在 GitHub：`https://github.com/tailark/blocks/tree/main/registry/bases/base/<kit>/blocks/<category>`（`radix` 目录是 Radix 版，内容相同）
- 本库：`fetch.sh tailark:oss-dusk-hero-section-1`，按 spec 下载区块文件和它用到的局部组件、kit 内 ui、logo SVG、motion-primitives，原样保存（不改 import 路径）
- 官方 registry：README 写的是 `npx shadcn@latest add https://oss-tailark.com/r/<kit>-<category>-<n>`（Base UI）和 `/r/radix/...`；2026-10-08 在本机连不上 oss-tailark.com（TLS 握手失败），没有实测
- 区块用 `@/lib/utils` 的 `cn`；`@/components/ui/*` 指向 kit 自己的 ui 文件（spec 里已列出），import 路径要按项目结构改

付费版（Pro，只当灵感）：
- 目录：`curl -s https://tailark.com/r/registry.json`（476 项）；单项 `/r/{name}.json` 未登录返回 401 `{"reason":"unauthenticated","required":"blocks"}`
- 区块截图：`https://raw.githubusercontent.com/tailark/pro-images/main/{name}.png`（另有 `-dark.png`），264 个里 257 个有截图；插画只有 `https://tailark.com/illustrations` 总览页
- 免费的只有 motion-primitives-*（6 个）、core-prompt-input、core-suggestion，以及 core-* 品牌 logo 和 shadcn 同构 ui（这两类没有登记）

实测（2026-10-08）：`fetch.sh tailark:oss-dusk-hero-section-1` 取到区块和依赖文件；`curl -s https://tailark.com/r/team-3.json` 返回 401；`https://raw.githubusercontent.com/tailark/pro-images/main/team-3.png` 返回 200。

## 使用注意
- 开源版区块大多不含动画；少数用 motion-primitives（infinite-slider、text-effect、animated-group、progressive-blur）做 logo 滚动和入场，要自己补减弱动效。
- 区块里的文案、数字、客户 logo、头像都是示例，按 `guides/marketing-section.md` 换成真实内容或标为示例。
- 同一页只用一套 kit（dusk / mist / veil 的按钮和卡片样式不同）。

## 组件清单
- 开源版 144 个区块：dusk 39、mist 48、veil 57，分类有 hero-section、features、content、call-to-action、faqs、footer、logo-cloud、pricing、stats、team、testimonials、integrations、contact、login、sign-up 等。
- 付费版 264 个区块（bento、blog、call-to-action、code-demo、comparator、contact、content、description-list、expandable-features、faqs、features、features-carousel、footer、forgot-password、header、hero-section、how-it-works、integrations、login、logo-cloud、open-roles、pricing、secondary-hero、sign-up、stats、team、testimonials 等）和 123 个插画组件（document、flow、ai、calendar、mobile、workspace 等），另有 8 个免费组件。逐条见 `sources/tailark.tsv`。
