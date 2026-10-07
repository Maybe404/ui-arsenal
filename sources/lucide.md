---
id: lucide
name: Lucide
url: https://lucide.dev
kind: icons
stack: 任意（Vanilla JS / React / React Native / Vue / Svelte / Solid / Preact / Angular / Astro / 静态 SVG / 图标字体）
license: ISC（图标与各包；部分源自 Feather 的图标为 MIT）
pro: none
fetch: npm
verified: 2026-10-07
---
## 是什么 / 什么时候用
Lucide 是社区维护的开源线性图标库（Feather 的继承者），当前 1866 个图标（lucide-static 1.52.0），24×24 网格、2px 描边、`currentColor`，风格统一。shadcn/ui 默认图标库就是它，做任何 UI 需要通用图标时首选；需要填充风格、品牌 logo（Lucide 已不再收录品牌图标）或插画式图标时换别的库（品牌用 simple-icons）。

## 按需获取方法
### 1. 运行时搜索全部图标（机器可读，均实测 200）
- 名称 → tags：`https://lucide.dev/api/tags`（JSON 对象 `{ "a-arrow-down": ["letter","font size",...] }`，1866 项）
- 名称 → 分类：`https://lucide.dev/api/categories`（`{ "house": ["buildings","home","navigation"] }`）
- 图标 SVG 节点数据：`https://lucide.dev/api/icon-nodes`
- 单图标 SVG：`https://lucide.dev/api/icons/{name}`
- CDN 版本固定的同等数据：`https://unpkg.com/lucide-static@latest/tags.json`、`https://unpkg.com/lucide-static@latest/icon-nodes.json`、`https://unpkg.com/lucide-static@latest/icons/{name}.svg`（jsDelivr 也可：`https://cdn.jsdelivr.net/npm/lucide-static@latest/tags.json`）
- 单图标元数据（tags/categories/aliases/deprecated）：`https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/{name}.json`
- 文档 llms：`https://lucide.dev/llms.txt`，每个文档页加 `.md` 可直接拿 markdown（如 `https://lucide.dev/guide/react/getting-started.md`）
- 图标页面：`https://lucide.dev/icons/{name}`

搜索命令（按名或 tag 关键词）：
```bash
curl -s https://lucide.dev/api/tags | jq -r --arg q "{keyword}" 'to_entries[] | select((.key|contains($q)) or (.value|any(contains($q)))) | .key'
```
实测 `{keyword}=calendar` 返回 calendar-1、calendar-arrow-down、calendar-check 等。

名称换算：kebab-case → 组件名 PascalCase，数字段直接拼接：`house` → `House`，`a-arrow-down` → `AArrowDown`，`arrow-down-0-1` → `ArrowDown01`（已在 lucide-react 的 d.ts 中核对）。lucide-react 同时导出 `HouseIcon`、`LucideHouse` 别名（见 aliased-names 文档），可避免与自有组件重名。

### 2. 各框架包（版本均 1.52.0，ISC）
| 框架 | 安装 | 用法 |
|---|---|---|
| React | `npm i lucide-react` | `import { House } from "lucide-react"; <House size={20} strokeWidth={1.5} />`；按名动态：`import { DynamicIcon } from "lucide-react/dynamic"; <DynamicIcon name="camera" />`（会把全部图标打进构建，慎用） |
| React Native | `npm i lucide-react-native`（需 `react-native-svg`） | 同 React |
| Vue 3 | `npm i @lucide/vue` | `import { House } from "@lucide/vue"` |
| Svelte 5 | `npm i @lucide/svelte`（Svelte 4 用 `lucide-svelte`） | `import { House } from "@lucide/svelte"` |
| Solid | `npm i lucide-solid`（Solid 2 用 `@lucide/solid`） | `import { House } from "lucide-solid"` |
| Preact | `npm i lucide-preact` | 同 React |
| Angular | `npm i @lucide/angular` | 见 https://lucide.dev/guide/angular.md |
| Astro | `npm i @lucide/astro` | `import { House } from "@lucide/astro"` |
| Vanilla JS | `npm i lucide` | `import { createIcons, House } from "lucide"; createIcons({ icons: { House } })`，HTML 写 `<i data-lucide="house"></i>` |
| 静态 SVG/字体/sprite | `npm i lucide-static` | `lucide-static/icons/{name}.svg`、`lucide-static/font/lucide.css`(+woff2)、`lucide-static/sprite.svg`（unpkg 均实测 200） |
| 仅图标数据 | `npm i @lucide/icons` | 导出 `{ name, node }` 数据，给不支持的框架自建集成 |
| Lucide Lab（实验图标） | `npm i @lucide/lab`（0.7.0） | React：`import { Icon } from "lucide-react"; import { burger } from "@lucide/lab"; <Icon iconNode={burger} />` |

通用 props：`size`(24)、`color`(currentColor)、`strokeWidth`(2)、`nonScalingStroke`(false，描边不随 size 缩放；旧版本 0.x 中同类功能叫 `absoluteStrokeWidth`，升级时注意)，以及任意 SVG 属性。

### 3. 实测例子（house）
- `curl -s https://unpkg.com/lucide-static@latest/icons/house.svg` → 带 `@license lucide-static v1.52.0 - ISC` 注释的 SVG（两个 path）
- `curl -s https://lucide.dev/api/icons/house` → 同一 SVG 单行版，含 `aria-hidden="true"`
- GitHub 元数据显示 `home` 是 `house` 的已废弃别名

## 使用注意
- 永远按具名 import（tree-shaking），不要 `import * as icons`，也别在生产中滥用 `DynamicIcon`。
- 有些旧名改成了别名（如 `home`→`house`），看到旧代码 import 报错时查 `icons/{name}.json` 的 `aliases`。
- 图标默认 24px、描边 2；小尺寸（16px）界面常配 `strokeWidth={1.5}` 或 `nonScalingStroke`。
- 品牌图标已移除：实测 /api/tags 中没有 github、twitter、figma、chrome。
- 填充风格不受官方支持，`fill` 只对部分图标有效果。
- 无障碍：装饰性图标默认 `aria-hidden`；独立图标按钮需 `aria-label`。
- 与 uiarc 等库并存没问题（uiarc 也依赖 lucide-react）。

## 组件清单
条目 1866 个（>500），按规范只列分类级（42 类，一个图标可属多个分类，例子取主分类为该类的图标）。全部图标逐行写在 `lucide.tsv`（name 列为 React 组件名，description 含分类与 tags，fetch 为 unpkg SVG）。运行时列全部请用上面的 `/api/tags`、`/api/categories`。

| id | 名称 | 分类 | 一句话用途 | 获取（具体命令或URL） | 备注 |
|---|---|---|---|---|---|
| category:text | text | text | 文字排版，270 个图标，例：a-arrow-down, a-arrow-up, a-large-small, ampersand | `jq -r 'to_entries[]\|select(.value\|index("text"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:development | development | development | 开发/代码，269 个图标，例：bitcoin, blocks, book-copy, book-dashed | `jq -r 'to_entries[]\|select(.value\|index("development"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:arrows | arrows | arrows | 箭头，218 个图标，例：arrow-big-down-dash, arrow-big-down, arrow-big-left-dash, arrow-big-left | `jq -r 'to_entries[]\|select(.value\|index("arrows"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:devices | devices | devices | 设备，188 个图标，例：alarm-clock-check, alarm-clock-minus, alarm-clock-off, alarm-clock-plus | `jq -r 'to_entries[]\|select(.value\|index("devices"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:files | files | files | 文件，170 个图标，例：archive-restore, archive-x, archive, file-archive | `jq -r 'to_entries[]\|select(.value\|index("files"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:design | design | design | 设计工具，168 个图标，例：axis-3d, blend, bring-to-front, component | `jq -r 'to_entries[]\|select(.value\|index("design"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:gaming | gaming | gaming | 游戏，163 个图标，例：backpack, bow-arrow, chess-bishop, chess-king | `jq -r 'to_entries[]\|select(.value\|index("gaming"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:multimedia | multimedia | multimedia | 多媒体/播放，159 个图标，例：ad, airplay, audio-lines-off, audio-lines-x | `jq -r 'to_entries[]\|select(.value\|index("multimedia"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:account | account | account | 账号/用户，158 个图标，例：award, badge-alert, badge-info, badge | `jq -r 'to_entries[]\|select(.value\|index("account"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:layout | layout | layout | 布局，158 个图标，例：align-center-horizontal, align-center-vertical, align-end-horizontal, align-end-vertical | `jq -r 'to_entries[]\|select(.value\|index("layout"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:social | social | social | 社交，142 个图标，例：badge-check, badge-minus, badge-percent, badge-plus | `jq -r 'to_entries[]\|select(.value\|index("social"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:navigation | navigation | navigation | 导航/地图，101 个图标，例：binoculars, compass, dumbbell, earth | `jq -r 'to_entries[]\|select(.value\|index("navigation"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:connectivity | connectivity | connectivity | 连接/网络，97 个图标，例：battery-charging, battery-full, battery-low, battery-medium | `jq -r 'to_entries[]\|select(.value\|index("connectivity"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:travel | travel | travel | 旅行，84 个图标，例：bath, bridge, briefcase-conveyor-belt, cigarette-off | `jq -r 'to_entries[]\|select(.value\|index("travel"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:food-beverage | food-beverage | food-beverage | 食物饮料，83 个图标，例：amphora, apple, banana, barrel | `jq -r 'to_entries[]\|select(.value\|index("food-beverage"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:tools | tools | tools | 工具，83 个图标，例：axe, bolt, broom-sparkles, broom | `jq -r 'to_entries[]\|select(.value\|index("tools"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:math | math | math | 数学，81 个图标，例：angle, calculator, circle-divide, circle-equal | `jq -r 'to_entries[]\|select(.value\|index("math"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:photography | photography | photography | 摄影，79 个图标，例：aperture, book-image, camera-off, camera | `jq -r 'to_entries[]\|select(.value\|index("photography"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:home | home | home | 家居，78 个图标，例：air-vent, alarm-smoke, armchair, bed-double | `jq -r 'to_entries[]\|select(.value\|index("home"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:transportation | transportation | transportation | 交通，71 个图标，例：anchor, baggage-claim, bike, briefcase-business | `jq -r 'to_entries[]\|select(.value\|index("transportation"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:time | time | time | 时间/日历，68 个图标，例：calendar-1, calendar-arrow-down, calendar-arrow-up, calendar-check-2 | `jq -r 'to_entries[]\|select(.value\|index("time"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:security | security | security | 安全/锁，68 个图标，例：bomb, brick-wall-fire, brick-wall-shield, cctv-off | `jq -r 'to_entries[]\|select(.value\|index("security"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:finance | finance | finance | 金融/货币，67 个图标，例：armenian-dram, bangladeshi-taka, banknote-arrow-down, banknote-arrow-up | `jq -r 'to_entries[]\|select(.value\|index("finance"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:shapes | shapes | shapes | 形状，67 个图标，例：astroid, box, boxes, circle-dashed-check | `jq -r 'to_entries[]\|select(.value\|index("shapes"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:communication | communication | communication | 沟通/消息，66 个图标，例：chevrons-left-right-ellipsis, circle-fading-plus, ethernet-port, lectern | `jq -r 'to_entries[]\|select(.value\|index("communication"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:medical | medical | medical | 医疗，53 个图标，例：activity, ambulance, bandage, bone-fracture | `jq -r 'to_entries[]\|select(.value\|index("medical"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:weather | weather | weather | 天气，52 个图标，例：bubbles, cloud-drizzle, cloud-fog, cloud-hail | `jq -r 'to_entries[]\|select(.value\|index("weather"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:notifications | notifications | notifications | 通知/铃铛，48 个图标，例：bell-minus, bell-off, bell-plus, bell-ring | `jq -r 'to_entries[]\|select(.value\|index("notifications"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:science | science | science | 科学，45 个图标，例：atom, beaker, biohazard, brain-circuit | `jq -r 'to_entries[]\|select(.value\|index("science"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:emoji | emoji | emoji | 表情，45 个图标，例：balloon, biceps-flexed, face-angry, face-expressionless | `jq -r 'to_entries[]\|select(.value\|index("emoji"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:shopping | shopping | shopping | 购物，40 个图标，例：badge-cent, badge-dollar-sign, badge-euro, badge-indian-rupee | `jq -r 'to_entries[]\|select(.value\|index("shopping"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:accessibility | accessibility | accessibility | 无障碍，34 个图标，例：accessibility, baby, badge-question-mark, circle-question-mark | `jq -r 'to_entries[]\|select(.value\|index("accessibility"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:cursors | cursors | cursors | 光标/指针，34 个图标，例：hand-grab, hand, loader-circle, loader-pinwheel | `jq -r 'to_entries[]\|select(.value\|index("cursors"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:charts | charts | charts | 图表，32 个图标，例：chart-area, chart-bar-big, chart-bar-decreasing, chart-bar-increasing | `jq -r 'to_entries[]\|select(.value\|index("charts"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:buildings | buildings | buildings | 建筑，31 个图标，例：anvil, brick-wall, castle, church | `jq -r 'to_entries[]\|select(.value\|index("buildings"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:mail | mail | mail | 邮件，29 个图标，例：forward, mail-badge, mail-check, mail-minus | `jq -r 'to_entries[]\|select(.value\|index("mail"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:nature | nature | nature | 自然，26 个图标，例：birdhouse, cannabis-off, cannabis, feather | `jq -r 'to_entries[]\|select(.value\|index("nature"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:animals | animals | animals | 动物，26 个图标，例：bird, bone, cat, dog | `jq -r 'to_entries[]\|select(.value\|index("animals"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:sustainability | sustainability | sustainability | 环保，26 个图标，例：recycle | `jq -r 'to_entries[]\|select(.value\|index("sustainability"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:sports | sports | sports | 运动，18 个图标，例：circle-star, fishing-hook, fishing-rod, medal | `jq -r 'to_entries[]\|select(.value\|index("sports"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:people | people | people | 人物，8 个图标，例：baby, clock-arrow-right, hand-platter, person-standing | `jq -r 'to_entries[]\|select(.value\|index("people"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |
| category:seasons | seasons | seasons | 季节，6 个图标，例：flower-2, leaf, rose, snowflake | `jq -r 'to_entries[]\|select(.value\|index("seasons"))\|.key'` 作用于 https://lucide.dev/api/categories | 一个图标可属多个分类 |

## 未解决
- 无付费项。`https://lucide.dev/icons/{name}.md` 不存在（返回站点 404 页），图标页只能看 HTML；用 API 或 GitHub JSON 代替。
- `lucide.dev/api/*` 响应 `cache-control: no-cache` 且未声明为公开稳定 API，长期依赖建议用 unpkg 上 `lucide-static@<固定版本>` 的 tags.json。
- `use-cases` 字段在 GitHub 元数据中多为空，未写入。

## Lucide Lab（2026-10-07 补充）
Lucide Lab 已逐条写进 lucide.tsv：以 npm `@lucide/lab` 0.7.0 实际发布的 357 个为准（access=free），另有仓库 main 分支里 26 个还没发布的（access=broken，默认搜索不显示），id 为 `lab:{name}`，name 列是导出名（camelCase）。
- SVG：`https://raw.githubusercontent.com/lucide-icons/lucide-lab/main/icons/{name}.svg`；元数据（tags、categories）在同目录的 `{name}.json`。
- 用法：`npm i @lucide/lab`，然后 `import { Icon } from "lucide-react"; import { avocado } from "@lucide/lab"; <Icon iconNode={avocado} />`。
- npm 和仓库不完全一致：npm 里有 10 个在仓库里已改名或删除，它们的源码从 `https://unpkg.com/@lucide/lab@0.7.0/dist/esm/icons/{name}.js` 取；仓库里新增的 26 个要等 npm 发新版。
- 更新：对比 `https://unpkg.com/@lucide/lab@latest/?meta` 的 `dist/esm/icons/*.js` 和 tsv 里的 `lab:` 行。
