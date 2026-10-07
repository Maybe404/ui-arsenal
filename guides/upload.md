# 文件上传（upload）

## 什么时候需要
让用户选择本地文件并上传：头像、附件、导入数据、批量图片。只要一个文件、不需要拖放和进度时，原生 `<input type="file">` 就够了；聊天输入框里的附件属于 AI 场景，展示已附加文件用 attachment 一类的组件即可。

## 默认推荐
| 主底座 | 推荐 | 理由 |
|---|---|---|
| shadcn | `shadcn:input-file`（选择）+ `shadcn:attachment`（文件条目）+ `shadcn:progress`（进度） | shadcn 没有拖放区组件。`input-file` 就是 `Input type="file"`，键盘、读屏、移动端相册都由浏览器负责；`attachment` 是文件条目卡片，`state` 支持 idle / uploading / processing / error / done，上传中文件名用 shimmer，错误态红框，图片缩略图未完成时半透明（2026-10-07 拉取 base-nova 源码确认）。但 attachment 只做展示：没有 `role="progressbar"`、没有 live region，进度和播报要自己加。需要拖放时见「按场景换」 |
| uiarc | `uiarc:file-dropzone` | 拖放区本身是原生 button，隐藏的 file input 移出 tab 序列；每行上传进度是 `role="progressbar"` 带 `aria-valuenow`；拒绝原因 `role="alert"`，增删和完成用 `role="status"` 播报；删除一行后焦点移到相邻行；`onUpload(item, { onProgress, signal })` 由你的真实上传报告进度，删除会中止请求；支持 `accept`、`maxSize`、`maxFiles`、图片预览（catalog + 源码）。**焦点框被 arc-foundation 全局去掉**，必须补 |
| 没有底座或其他 | 原生 `<label>` + `<input type="file">` | 最稳；多文件用 `multiple`，限制类型用 `accept`；上传进度用原生 `<progress>` |

## 按场景换
| 场景 | 推荐 | 理由 |
|---|---|---|
| shadcn 底座但需要拖放 + 多文件进度 | 自己写一个薄拖放区：`shadcn:button` 触发隐藏的 file input，外层监听 dragover/drop；列表用 `shadcn:attachment` + `shadcn:progress` | 结构照 `uiarc:file-dropzone`：拖放目标是可聚焦按钮、隐藏 input `tabIndex={-1}`、进度条 `role="progressbar"`、增删用 live region。按兼容矩阵，shadcn 页面不建议直接引入 uiarc 组件；确实要借，按 `_styles.md` 的作用域映射做 |
| uiarc 底座、轻量单区域上传 | `uiarc:file-upload` | 同样有 `onUpload(file, { onProgress, signal })`、类型和大小校验、重试/删除按钮带文件名标签、删除后焦点回到相邻按钮或拖放区；但进度没有 `role="progressbar"`，只靠 `aria-live` 状态行（源码） |
| 聊天/AI 输入框里的附件条 | `shadcn:attachment` | 本来就是为消息附件设计的，配合 shadcn 聊天组件 |
| 导入 CSV 并映射列 | uiarc catalog 建议 `import-mapper`（不在本索引的免费条目里，未验证） | 上传之后的映射流程不是上传组件能解决的 |
| 头像 | `shadcn:input-file` + `shadcn:avatar` 预览 | 单文件不需要拖放区；裁剪另找方案 |

## 慎用
- `bencho:upload-dropzone`：**不是真的上传组件**。源码注释写明"NO REAL FILES"：三个文件是组件自带的道具，不读本地文件、不发请求，进度用 `Math.random()` 推进，5MB 限制写死，视频文件永远超限。直接上线就是第 1 级"状态虚假"。只能借它"拖入时盒子吸入文件"的动效节奏，套到真实组件上。
- `obsidianui:file-input`：依赖 `next/image`，只能在 Next.js 用；颜色写死成 zinc/黑色（`bg-black`、`text-zinc-200` 等，只有暗色）；没有上传回调和进度，只是选文件后显示预览；拖放区 `div` 只靠里面的按钮可聚焦。要用就把颜色换成底座变量并自己加进度，否则选上面的方案。
- `originkit:particle-simulation`（Pro）：是用上传的照片生成 WebGL 点云的展示效果，不是上传组件。
- Pro 条目 `reactbits:category:pro-app-ui/file-manager`：只当灵感。
- 动画进度条和真实进度脱节：任何上传组件都只能显示后端/XHR 报告的进度；拿不到进度时用不确定态（spinner 或 indeterminate），不要假装匀速前进。

## 页面模式约束
- **Operate**：主底座组件 + 真实进度。动效只用于状态：拖入高亮、进度、成功/失败。不加吸入、粒子之类的装饰。
- **Persuade**：落地页上的"试一试，拖张图进来"可以有一处表现（比如借 bencho 的吸入节奏），但处理流程必须真实，失败要有出路。
- **Read**：基本不需要上传。
- **Experience**：作品集投稿类页面保持底座样式。

## 接入要点
- **真实状态**：`onProgress` 来自 XHR 的 `upload.onprogress` 或分片上传的回执；`fetch` 拿不到上传进度时用不确定态。失败要可重试，删除要能中止请求（uiarc 已传 `AbortSignal`）。
- **校验**：前端用 `accept` 和大小限制先拦一遍，拒绝原因写清楚（"超过 10 MB""只支持 PNG、JPG"）并用 `role="alert"`；后端必须再校验一次。
- **键盘和读屏**：拖放只是增强，必须能用按钮选文件；每个文件的删除、重试按钮带文件名；进度条有 `aria-valuenow` 或用文字播报百分比。
- **移动端**：没有拖放，按钮文案写"选择文件"而不是"拖到这里"；`accept="image/*"` 会打开相册/相机。
- **uiarc 焦点（必须做）**：删掉 `arc-foundation.css` 末尾的 `:is(*:focus, *:focus-visible, *:focus-within) { outline: none !important; }`，把 `--focus-ring` 从 `transparent` 改成可见色，再补：
  ```css
  :root, :root[data-theme="dark"] { --focus-ring: color-mix(in oklch, var(--foreground) 35%, transparent); }
  :where(button, [role="button"], [tabindex]):focus-visible { outline: 2px solid var(--foreground); outline-offset: 2px; }
  ```
- **token**：shadcn attachment 用 `--card`、`--muted`、`--destructive`；上传中的 shimmer 来自 shadcn 的工具类，确认项目里有 `shadcn/tailwind.css`（未验证具体定义位置）。
- **减弱动效**：uiarc 两个组件都有 `useReducedMotion` 分支（进度直接跳到目标值、行进出不位移）；shimmer 在减弱动效下是否停止未验证，必要时加 `motion-reduce:` 关掉。
- **常见坑**：图片预览用 `URL.createObjectURL` 后要 `revokeObjectURL`（uiarc file-dropzone 已处理）；同名文件重复添加要去重或提示；大文件不要读进内存做预览。

## 候选清单
- `shadcn:input-file` — 原生文件选择，单文件够用
- `shadcn:attachment` — 文件条目卡片，多状态
- `shadcn:progress` — 进度条
- `uiarc:file-dropzone` — 完整拖放区 + 列表 + 真实进度（补焦点后用）
- `uiarc:file-upload` — 轻量拖放上传，进度靠状态播报
- `obsidianui:file-input` — 仅 Next.js、暗色写死，需改造
- `bencho:upload-dropzone` — 只借吸入动效，组件是演示道具
- `inspora:file-upload-card` — 仅参考：上传卡片布局
- `collectui:category:file-upload` — 仅参考：上传样式
