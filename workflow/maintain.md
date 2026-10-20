# Workflow · Maintain（知识库维护）

> 目标：每次创建/修改笔记后，同步更新知识库的**索引、关系与生命周期**，让知识库永远"自洽"。

## Step 0 · 架构状态检查（涉及目录变更时）

- 读取当前 `architecture_status`（`features/architecture.md`），无记录则默认 `stable`。
- **`stable` 状态下禁止随意重构目录**：改名/移动/新建一级分类前，先提方案并征得确认。
- **`experimental` 状态下允许调整**，但每次变更记 `changelog.md`。
- **`migration` 状态下不新建笔记**，完成迁移清单后再切回 `stable`。

## Step 1 · 更新 .vault-meta 状态文件（可选）

已有 `.vault-meta/` 时同步更新，没有则跳过：

- `index.json`：笔记 → 路径/分类/等级/状态的索引。
- `taxonomy.yaml`：分类体系（仅当新建分类时追加）。
- `relations.json`：笔记间的前置/相关/后续关系。
- `changelog.md`：追加一条变更记录（日期 + 动作 + 涉及文件）。

## Step 2 · 导航页自动维护（两种形态，一个 vault 只选一种）

**形态 A · MOC 地图**（多主题大型库）：每个领域维持一张 `MOC-{{领域}}.md`。

1. 定位该笔记所属领域的 MOC，不存在则创建。
2. 在对应分类小节追加一行：`- [[{{笔记名}}]] —— {{一句话说明}}`。
3. 同步更新 MOC 的 mermaid 图谱（新增节点与连线）。
4. 检查并补"学习路线"章节的节点。

**形态 B · 单页路线页**（以学习顺序为唯一导航，如 `学习路线.md`）：

1. 把新笔记插进路线里**语义正确的那一步**，不只追加到末尾。
2. 插入后**整段重排步号**并 `assert` 条数兜底。
3. 更新篇数标注——口径是「除导航页自身外」，原值 N → 新值 N+1。
4. 同步该篇正文的「📍 本篇位置」行（`N/M` 分母 + 链路文字），同章其他篇若分母变化也要一并重算。

示例（形态 A）：新增 `CompletableFuture.md` → `MOC-Java并发.md` 自动追加：

```markdown
## 异步编程
- [[Future]] —— 异步结果的占位符
- [[CompletableFuture]] —— 异步编排与组合（新增）
```

## Step 3 · 双向链接补全

- 对被链接笔记逐一补反链（已有则跳过）。
- 反链理由写具体，不写"相关"两字糊弄。

## Step 4 · 生命周期状态流转

按 `references/learning-system.md` 规则流转 `status`：

```
learning（新笔记默认） → mastered（能讲解） → review（进入复习排期）
  → archived（长期掌握，移入项目归档目录，如 _archive/）
```

- 状态变更时：更新 frontmatter `status` + `review_date`，必要时移动文件（如 archived）。
- 移动文件前确认 Obsidian 链接跟随设置开启（`references/obsidian.md` 第三节）。

## Step 5 · 输出维护摘要

每次任务结束时，向用户返回变更摘要：

```markdown
✅ 变更摘要
- 新建：数据结构/5-并发多线程/CompletableFuture.md（L2）
- 更新：MOC-Java并发.md（新增节点 + 学习路线）
- 更新：.vault-meta/index.json、relations.json、changelog.md
- 反链：CountDownLatch.md 已补 ← CompletableFuture
```

## 维护红线

- **索引与实际文件必须一致**：文件移动/删除后，`index.json` 同步更新，不得留幽灵条目。
- 不做未登记的目录创建：任何新目录先进 `taxonomy.yaml`。
- 不批量移动用户笔记：涉及历史笔记迁移时，先列清单征得确认。
