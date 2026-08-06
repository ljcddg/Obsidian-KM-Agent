# Obsidian 使用规范细则

> Obsidian 生态操作规范：frontmatter、链接、MOC、文件夹、整合。与学科无关，任何 vault 通用。

## 0. 三层管理（目录 + 元数据 + 知识关系）

知识库组织不依赖单一维度。三层协同：

| 层 | 工具 | 作用 | 稳定性 |
|---|------|------|--------|
| **物理层** | 目录 + 文件名 | 快速定位，文件浏览器可见 | 受架构锁定保护（stable 下禁止随意重构，见 `features/architecture.md`） |
| **元数据层** | frontmatter（tags/category/subcategory/domain/level）| 多维度检索、Dataview 面板 | 不受锁定，可随时调整 |
| **关系层** | [[ ]] 双向链接 + MOC + 可选 .vault-meta 索引 | 知识网络，Agent 可达 | 不受锁定，随时维护 |

**目录层以项目为根，不强制固定结构。** 分类策略由自适应引擎（`workflow/classify.md`）根据项目现状决定：复用已有 / 优化 / 新建。推荐 `编号-分类名/` 命名，MOC 放项目根或就近。可选 0-Inbox / 9-Archive 骨架增强。

## 1. frontmatter 规范（KMA 标准）

```yaml
---
title: 笔记标题
category: 一级分类
subcategory: 二级分类
domain: 领域
level: L1 | L2 | L3
tags: [分类, 主题, 细分]
status: learning            # learning / mastered / review / archived
language: Java              # 技术笔记必填
version: JDK 21             # 技术笔记必填
created: YYYY-MM-DD
updated: YYYY-MM-DD
review_date: YYYY-MM-DD
related: [相关笔记名]
prerequisites: [前置笔记名]
---
```

- `tags` **从大到小**排列（一级分类 → 主题 → 细分），便于标签视图分层筛选。
- `category`/`subcategory`/`domain`/`level` 与分类引擎结果一致（`workflow/classify.md`）。
- `status`/`review_date` 是生命周期字段，规范见 `learning-system.md`。
- `related`/`prerequisites` 是关系字段，与笔记内"关联笔记"小节一致（`features/knowledge-map.md`）。
- 日期格式统一 `YYYY-MM-DD`。

## 2. 链接规范

- 笔记间引用一律用 `[[文件名]]`（Obsidian 按文件名解析）。
- 链接带**具体关联理由**：`[[X]] —— 同样是 XX 场景的落地`，不要裸链。
- 反链原则：A 链接到 B 后，在 B 末尾补一条指向 A 的链接，保证"任何一篇都能回到来源"。
- 引用了不存在的笔记（死链）时，改为普通文字，避免 Obsidian 渲染断链。

### 2.1 关系分类（知识图谱的核心）

"关联笔记"小节按**三种关系**组织，让图谱有层次而非乱麻：

```markdown
## 关联笔记
- **前置知识**：[[X]] —— 学本篇之前应掌握
- **相关知识**：[[Y]] —— 平行/对比/同体系
- **后续学习**：[[Z]] —— 学完本篇可进阶的方向
```

- **前置知识**：本笔记依赖的内容，读者缺它就读不懂。
- **相关知识**：可对比学习的平行概念（如 `CountDownLatch` ↔ `CyclicBarrier`）。
- **后续学习**：进阶方向（如 `CompletableFuture` → `ForkJoinPool`）。
- 完整维护流程见 `features/knowledge-map.md`。

## 3. 关于"移动文件是否断链"的准确说明

**移动文件前，先确认 Obsidian 设置：**

```
Settings → Files & Links → Automatically update internal links ✅（默认开启）
```

- **开启**（默认）：移动/重命名笔记时，Obsidian 自动更新所有指向它的 `[[ ]]` 链接，**不会断链**。
- **关闭**：移动后旧链接会失效，需要手动修复。

**结论**：批量归档文件夹前，先检查此开关；开启后 `mv` 移动文件是安全的。跨设备同步（如 Git）移动文件时，仍建议归档后做一次"未解析链接"检查（Obsidian 左侧"链接"面板可查）。

## 4. MOC（笔记地图）结构

MOC 放项目根或就近目录，命名 `MOC-{{主题}}.md`：

```markdown
---
title: MOC - {{主题}}总地图
tags: [MOC, {{主题}}, 索引]
created: ...
updated: ...
---
# {{主题}} · 笔记总地图

## 一、笔记图谱（mermaid）
graph：每个节点一篇笔记，MOC 连所有节点，相关节点间连线

## 二、按分类分组
### 📏 {{分类1}} `{{文件夹1}}/`
- [[笔记A]] —— 一句话说明
### 🌳 {{分类2}} `{{文件夹2}}/`
...

## 三、学习路线建议
1. 先读 ... → 再读 ... → 最后读 ...

## 四、整合说明 / 归档说明
```

- 分类标题后标注物理文件夹路径（`` `{{文件夹}}/` ``），地图与文件结构对应。
- mermaid 节点用中文短名，连线表示知识关联。
- **mermaid 只用于小图（≤8 节点）**：架构总览/分类对比类内容一律用表格（Obsidian 大 mermaid 会超出屏幕、连线交错，用户实测反馈）。
- 新增笔记时 MOC 的自动更新流程见 `workflow/maintain.md`。

## 5. 文件夹与分类

- 目录层以项目为根，不强制固定结构。分类策略由 `workflow/classify.md` 自适应决定。
- 命名建议：`数字-分类名/`（如 `1-线性结构/`、`2-树形结构/`），数字前缀保证按类排序。
- 分类粒度：每文件夹 1~8 篇为宜；超 10 篇考虑二级分类。
- MOC 放项目根或就近，不强制集中。
- 归档前确认链接跟随设置开启（见第三节）。分类结构受架构锁定保护（`features/architecture.md`）——stable 状态禁止随意重构。

## 6. 整合多篇笔记的原则

- **盘点先行**：先通读全部相关笔记，列出重复点清单。
- **主从确立**：内容重叠时选一篇作主篇吸收全部独有内容，其余降级为导航页（内容无损）。
- **约定分工**：如"总览留在 A 篇，细节留在 B 篇"，两篇末尾互相说明分工。
- **更新 MOC**：整合后更新图谱、分类索引与学习路线。
- **核对不丢失**：合并后逐条确认原笔记内容都在主篇中。

## 7. callout 与标记

```markdown
> [!abstract] 总览
> [!tip] 记忆口诀
> [!warning] 高频坑
> [!example] 示例
```

- 重点提示用 callout，不用普通加粗段落。
