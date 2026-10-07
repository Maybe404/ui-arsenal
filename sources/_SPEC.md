# 来源文件规范（每个站点产出两个文件）

## 1. sources/<id>.md
```
---
id: <id，小写短横线>
name: <站点名>
url: <主页>
kind: component-library | effects | blocks | inspiration | icons | template | prompt-library | portfolio
stack: <如 React + Tailwind + Motion / 纯 CSS / 任意>
license: <MIT / 自定义 / 未声明>
pro: none | partial | all   （partial 写明哪些付费）
fetch: <主获取方式：shadcn-registry | npm | github-raw | page-copy | prompt-copy | browse-only>
verified: 2026-10-07
---
## 是什么 / 什么时候用
（2-5 句，给开发 agent 判断"该不该用这个库"）

## 按需获取方法
（逐步、可直接执行的命令或 URL 模板，用占位符 {name}。必须用一个真实组件实测过，写出实测例子。
 若有 shadcn registry / llms.txt / sitemap / GitHub 原始文件 / JSON API，优先写这些机器可读途径。
 若站点提供"复制提示词 / Copy prompt"，写清楚提示词在哪个 URL、如何抓取（curl 能拿到？需要渲染？）。
 写出依赖安装方式。）

## 使用注意
（依赖、框架限制、常见坑、和其他库的冲突，例如 Tailwind v3/v4、motion vs framer-motion）

## 组件清单
| id | 名称 | 分类 | 一句话用途 | 获取（具体命令或URL） | 备注 |
（列出站点上的全部组件/条目，一个不落。Pro 条目也要列，备注写 pro。
 若条目极多（>500，例如图标、灵感截图），清单写到分类级，并给出能在运行时列出/搜索全部条目的方法（API/JSON/sitemap），实测可用。）

## 未解决
（拿不到的内容、需要登录、被反爬、仅 Pro 等，逐条写原因。没有就写"无"。）
```

## 2. 条目清单：两个文件，机器字段和人工字段分开

刷新脚本只会写 `<id>.tsv`，并且只在人工批准之后写；`<id>.notes.tsv` 永远由人维护，刷新不会覆盖中文描述和选型判断。两个文件都无表头，制表符分隔，用 item_id 对应。

### sources/<id>.tsv（机器维护，15 列）
| 列 | 含义 |
|---|---|
| source | 来源 id，等于文件名 |
| item_id | 条目 id，来源内唯一；改名时保留旧行并填 alias_of |
| title | 站点上的名称 |
| category | 站点自己的分类 |
| official_url | 给人看的官方页面 |
| fetch_human | 给人看的获取命令或说明 |
| spec | 给 fetch 用的取码规格，见下 |
| access | `free` \| `login`（需要用户账号）\| `pro`（付费）\| `broken`（失效或为空） |
| usage | `install`（有官方安装方式）\| `source`（能拿到源码，手动接入）\| `prompt`（提示词或规范）\| `reference`（只能看） |
| framework | react \| css \| multi \| any …，留空表示未知 |
| deps | 依赖，空格分隔，留空表示未采集 |
| item_status | `active` \| `needs-review` \| `removed`（下线但保留，默认不搜） |
| alias_of | 改名后指向的新 item_id |
| last_seen | 最后一次在线上清单里看到的日期 |
| fingerprint | 元数据指纹（名称、依赖、付费标记、文件路径等算出的短 hash），用来发现内容变化 |

spec 由空格分隔的若干项组成，每项是 `<adapter>:<arg>`：
- `registry:<json url>`：shadcn 风格的 registry 条目，要求返回的 files 里带 content
- `url:<url>`：直接下载的文件，比如 GitHub raw、SVG、DESIGN.md、mp4
- `doc:<url>`：文档（Markdown），不能是 HTML 回落页
- `prompt:<page url>`：从页面的 `<pre id="agent-prompt">` 里抽出提示词
- `script:<adapter> <arg>`：调用 `scripts/adapters/<adapter>.py|.sh <arg>`，只解析，不执行远程代码
- `browser:<url>`：需要在浏览器里打开
- `manual`：按 md 的「按需获取方法」手动操作
- `none`：不获取；`pro` 条目必须写 none

### sources/<id>.notes.tsv（人工维护，8 列）
| 列 | 含义 |
|---|---|
| item_id | 对应机器文件的 item_id |
| desc_zh | 中文一句话，写进便于搜索的中英文关键词（必填） |
| task | 统一的 UI 任务分类，最多两个，逗号分隔，第一个是主任务。取值见 `scripts/ua.py` 的 `TASKS` |
| layer | `foundation`（设计底座）\| `specialized`（专项组件或效果）\| `reference`（只作参考）\| `icons` \| `design-spec`（DESIGN.md 这类设计规范） |
| visual_tags | webgl、canvas、3d、pixel、gradient、glass、dark、illustration 等 |
| interaction_tags | hover、press、drag、scroll、cursor、swipe、keyboard、sound 等 |
| risk | 场景化审美风险：gradient-text、marquee、glow、grid-background、typewriter、bounce、glass、pulse-dot。不是禁止，用的时候要写理由 |
| notes | 人工选型备注 |

条目极多时，可以每个分类一行，item_id 写 `category:<分类>`，用 `script:` 或 md 写清楚运行时怎么列出该分类的全部条目。

## 通用要求
- 先找机器可读入口：/sitemap.xml、/llms.txt、/llms-full.txt、/r/registry.json、/registry.json、/api/*、GitHub 仓库。用 curl（带浏览器 UA）和 WebFetch。站点是 SPA 抓不到时，看页面 JS bundle、__NEXT_DATA__、GitHub 仓库。
- 不登录、不注册、不付费、不提交任何表单。
- description 用中文，组件名/命令保持英文。
- 只写入你负责的 sources/<id>.md 和 sources/<id>.tsv（站点需要专门处理时，另加 scripts/adapters/<id>.sh），不碰其他文件。
- 写完跑 `scripts/audit.sh`，再用 `scripts/fetch.sh <id>:<某条>` 实测。
