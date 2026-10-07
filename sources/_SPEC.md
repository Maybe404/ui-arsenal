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

## 2. sources/<id>.tsv
无表头，制表符分隔，每个组件一行，9 列：
`source_id	item_id	name	category	description	fetch_human	access	usage	spec`

- description：中文一句话，写进便于搜索的关键词（中英文都写，比如"磁吸标签选择 magnetic chip select"）。
- fetch_human：给人看的获取命令或 URL。
- access：只能是 `free` | `login`（需要用户账号）| `pro`（付费）| `broken`（失效或为空）中的一个。
- usage：只能是 `install`（有官方安装方式）| `source`（能拿到源码，但要手动放进项目）| `prompt`（拿到的是提示词或规范）| `reference`（只能看）中的一个。
- spec：给 `fetch.sh` 用的取码规格，多个之间用空格分隔：
  - `registry:<json url>`：shadcn 风格的 registry 条目，要求返回的 files 里带 content
  - `url:<url>`：直接下载的文件，比如 GitHub raw、SVG、DESIGN.md、mp4
  - `doc:<url>`：文档（Markdown），不能是 HTML 回落页
  - `prompt:<page url>`：从页面的 `<pre id="agent-prompt">` 里抽出提示词
  - `script:<adapter> <arg>`：调用 `scripts/adapters/<adapter>.sh <arg>`，用于需要专门处理的站点
  - `browser:<url>`：需要在浏览器里打开
  - `manual`：按 md 的「按需获取方法」手动操作
  - `none`：不获取；`pro` 条目必须写 none
条目极多时，可以每个分类一行，item_id 写 `category:<分类>`，用 `script:` 或 md 写清楚运行时怎么列出该分类的全部条目。

## 通用要求
- 先找机器可读入口：/sitemap.xml、/llms.txt、/llms-full.txt、/r/registry.json、/registry.json、/api/*、GitHub 仓库。用 curl（带浏览器 UA）和 WebFetch。站点是 SPA 抓不到时，看页面 JS bundle、__NEXT_DATA__、GitHub 仓库。
- 不登录、不注册、不付费、不提交任何表单。
- description 用中文，组件名/命令保持英文。
- 只写入你负责的 sources/<id>.md 和 sources/<id>.tsv（站点需要专门处理时，另加 scripts/adapters/<id>.sh），不碰其他文件。
- 写完跑 `scripts/audit.sh`，再用 `scripts/fetch.sh <id>:<某条>` 实测。
