# 添加新来源

用户说"把 <URL> 加进 ui-arsenal"时，照下面的步骤做。

1. **定 id**：小写短横线，例如 `magicui`，不能和已有的 `sources/*.md` 重名。
2. **调研**（遵守 `_SPEC.md`）：
   - 先找机器可读入口：`/r/registry.json`、`/llms.txt`、`/sitemap.xml`、GitHub 仓库、npm 包。小心有的站点对不存在的路径也返回 200，内容其实是 HTML 回落页。
   - 弄清获取方式和访问边界：free、login、pro。"页面上能看到"不等于"源码免费"。
   - 挑一个真实条目实测获取。
   - 列全部条目，Pro 条目也列。
3. **写文件**：`sources/<id>.md`（frontmatter 必填）和 `sources/<id>.tsv`（9 列）。站点需要专门处理才能取代码时，写 `scripts/adapters/<id>.py`（或 `.sh`），要求：只读，结果输出到 stdout；**只下载文本并解析，不执行任何远程代码**（不用 `node import`、`eval`，也不运行下载来的脚本）；解析不了时报错退出。spec 写成 `script:<id> <item>`。
4. **接入 refresh（可选）**：站点有公开的清单接口时，在 `scripts/ua.py` 的 `REFRESH` 里加一个函数，返回线上清单、本地清单和 hash；没有接口的，在 `NO_REFRESH` 里写明原因。
5. **校验**：
   - `scripts/audit.sh` 0 问题；
   - `scripts/verify.sh -s <id>` 全部 ok；
   - `scripts/find.sh -s <id> <关键词>` 能搜到；
   - `scripts/fetch.sh <id>:<item>` 能取到；
   - `scripts/searchtest.sh` 全部通过，可以给新来源加一两条用例到 `scripts/search_cases.json`；
   - 新增了获取方式或 adapter 时，在 `scripts/ua.py` 的 `MATRIX` 里加一个场景，`scripts/verify.sh --matrix` 全部 ok。
6. **登记**：
   - 运行 `scripts/stats.sh --write-skill`，更新 SKILL.md 的来源表；
   - 新来源的名字加进 SKILL.md frontmatter description 的括号里；
   - 有新的常用中文说法时，补进 `scripts/aliases.json`。
7. **汇报**：告诉用户条目数、获取方式、哪些拿不到以及原因。

已有来源改版或失效时（verify 报 FAIL，或 refresh 报出新增、下线），重新调研，覆盖这两个文件，并更新 `verified` 日期。
