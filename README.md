# ui-arsenal

给 AI 编程 agent（Claude Code、Codex 等）用的 UI 组件索引 skill。做页面、组件、交互、动效时，agent 先在这里查成熟的组件，再按需拉取最新的代码或提示词，尽量少写不成熟、带 AI 味的 UI。

它是**索引**，不存第三方源码：本地只保存组件清单、中文描述、访问状态和获取方式，代码和提示词每次都从原站现场获取。

## 收录来源

shadcn/ui、React Bits、OriginKit、Bencho、uiarc、ObsidianUI、Beautiful UI、loading-ui、Libraries.dev、Lucide（含 Lucide Lab）、getdesign.md、Design Spells、Inspora、Collect UI、Jakub Antalik。

每个来源的条目数和访问状态见 [SKILL.md](SKILL.md) 的「来源一览」，获取方法和注意事项见 `sources/<id>.md`。

## 安装

```bash
git clone https://github.com/Maybe404/ui-arsenal.git ~/code/github.com/Maybe404/ui-arsenal
ln -s ~/code/github.com/Maybe404/ui-arsenal ~/.claude/skills/ui-arsenal   # Claude Code
ln -s ~/code/github.com/Maybe404/ui-arsenal ~/.codex/skills/ui-arsenal    # Codex
```

依赖：Python 3（只用标准库）、curl。

## 常用命令

```bash
scripts/find.sh 磁吸 选择                  # 搜索，中英文都可以，自动展开同义词
scripts/find.sh 背景 --code                # 只要现在就能直接拿到代码的
scripts/fetch.sh bencho:magnet-select      # 只读拉取到临时目录，打印依赖和安装命令
scripts/stats.sh                           # 各来源统计
scripts/audit.sh                           # 格式检查
scripts/verify.sh --matrix                 # 获取链路固定场景测试
scripts/searchtest.sh                      # 搜索相关性回归测试
scripts/refresh.sh                         # 和线上清单比对，只报告差异
```

## 边界

- **不获取付费内容**：标为 Pro 的条目只记录名称，`fetch` 拒绝获取。
- **不代替用户登录**：需要账号的条目只给出官方获取方式，由用户决定是否登录。
- **不执行远程代码**：所有 adapter 只下载文本并解析。
- **选型有依据**：`guides/` 下每类 UI 任务都有指南，推荐和慎用都基于实际读过的源码。
- **遵守站点规则**：比如 inspora 的 robots.txt 禁止 `/api/`，这里就不调用该接口。
- **内容归属**：组件、截图、视频、品牌和商标都归各自网站和作者所有，使用前请遵守原站的许可证和条款。本仓库的中文描述是对原站内容的概括，用于检索。

## 目录结构

```
SKILL.md              agent 读的入口：原则、工作流、来源一览
guides/_scenes.md     页面模式、效果预算、质量三级、动效规范（所有指南共用）
guides/<task>.md      按 UI 任务分的选型指南：默认推荐、按场景换、慎用、接入要点
scripts/ua.py         所有命令的实现（find / fetch / verify / refresh / stats / audit / searchtest）
scripts/adapters/     需要专门处理的站点的取码脚本（只解析，不执行）
scripts/aliases.json  中英文同义词组
sources/<id>.md       每个来源的说明：获取方法、使用注意、未解决问题
sources/<id>.tsv      每个来源的条目清单，机器维护的字段（15 列，无表头）
sources/<id>.notes.tsv  人工维护的字段：中文描述、UI 任务、层级、标签、风险（刷新不会覆盖）
sources/_SPEC.md      来源文件格式规范
sources/_ADDING.md    新增来源的流程
```
