# .vault-meta（知识库状态文件）

> 目的：让 Agent **不扫描几千篇 Markdown** 就能知道知识库全貌。状态文件是知识库的"数据库"，Agent 每次任务先读它，操作后同步它。

## 位置与结构

```
Vault/.vault-meta/
├── index.json        # 笔记索引：路径/分类/等级/状态
├── taxonomy.yaml     # 分类体系（唯一登记处）
├── relations.json    # 笔记关系：前置/相关/后续
└── changelog.md      # 变更日志（追加式）
```

## 1. index.json（笔记索引）

```json
{
  "notes": {
    "CompletableFuture": {
      "path": "数据结构/5-并发多线程/CompletableFuture.md",
      "category": "Java",
      "subcategory": "Concurrent",
      "level": "L2",
      "status": "learning",
      "tags": ["Java", "并发", "异步编程"],
      "related": ["Future", "ThreadPool"],
      "created": "2026-07-31",
      "updated": "2026-07-31",
      "review_date": "2026-08-03"
    }
  },
  "updated": "2026-07-31"
}
```

- key 用笔记名（无扩展名），与 `[[ ]]` 链接名一致。
- `tags` 和 `related` 用于冲突检测的预筛（`features/conflict-detection.md`），加速候选集定位。
- 文件移动/删除/状态变更 → 同步更新本条。

## 2. taxonomy.yaml（分类体系登记处）

```yaml
taxonomy:
  ComputerScience:
    Java:
      Concurrent:
        - CompletableFuture
        - CountDownLatch
        - CyclicBarrier
    Database:
      MySQL: []
  Architecture:
    DesignPatterns: []
```

**规则：**
- **唯一登记处**：新分类必须先在此登记，才能创建目录（见 `workflow/classify.md`）。
- 叶子节点列出该分类下的笔记名。
- 分类改名：先更新此处，再更新 `relations.json` 与受影响笔记 frontmatter。

## 3. relations.json（关系记录）

```json
{
  "relations": {
    "CompletableFuture": {
      "prerequisites": ["Future"],
      "related": ["CountDownLatch", "CyclicBarrier"],
      "next": ["ForkJoinPool"]
    }
  }
}
```

- 与笔记内"关联笔记"小节一一对应：**先写笔记内链接，再同步到这里**。
- 双向关系（A 是 B 的前置 ⇔ B 是 A 的后续）由维护流程保证（`workflow/maintain.md`）。

## 4. changelog.md（变更日志）

```markdown
# 知识库变更日志

## 2026-07-31
- 新建：数据结构/5-并发多线程/CompletableFuture.md（L2）
- 更新：MOC-Java并发.md（新增异步编程节点）
- 更新：index.json、relations.json
```

- **追加式**，不覆盖历史。
- 每次创建/修改/归档/移动文件都要记一笔。

## Agent 操作规范

| 场景 | 动作 |
|------|------|
| 任务开始 | 读 `index.json` + `taxonomy.yaml`，了解现状（不扫描全库） |
| 新建笔记 | 写文件 → 更新 index.json → 追加 changelog.md |
| 更新笔记 | 写文件 → 更新 index.json 的 updated → 追加 changelog.md |
| 归档/移动 | 移动文件 → 更新 index.json 路径/状态 → 追加 changelog.md |
| 新建分类 | 先登记 taxonomy.yaml → 再建目录（或先提建议经确认） |
| 变更关系 | 更新 relations.json + 双向补链 |

**红线：**
- `index.json` 与实际文件必须一致，不留幽灵条目。
- 状态文件被用户手动改动时，以用户改动为准，重建索引前先询问。
- `.vault-meta/` 本身不纳入笔记索引，可加入 Obsidian 忽略列表。
