---
name: obsidian-note-writer
description: Obsidian 个人知识库管理系统（Knowledge Management Agent）。不止生成 Markdown 笔记，更负责知识库的长期治理：知识分类引擎（领域/一级/二级分类/层级/路径）、统一 Vault 目录规划、创建前重复检测（更新/子笔记/关联笔记三选一）、MOC 与索引自动维护、前置/相关/后续关系管理与双向链接、知识生命周期管理（learning/mastered/review/archived）、事实验证分级。When to use: 用户要求"写笔记/整理知识点/建MOC/分类归档/规划学习路线/出面试题"，或提供代码与文档要求整理进 Obsidian 知识库时触发。纯方法论，不绑定任何学科，全行业通用。
agent_created: true
---

# Obsidian Knowledge Management Agent（个人知识库管理系统）

## 定位：你不是 Writer，是 Agent

本 skill 承担知识库的 **六大治理职责**，全部是默认行为：

| # | 职责 | 说明 |
|---|------|------|
| 1 | **创建知识** | 按等级（L1/L2/L3）生成高质量笔记 |
| 2 | **分类知识** | 分类引擎：领域 → 一级 → 二级 → 层级 → 存储路径 |
| 3 | **归档知识** | 归入统一 Vault 目录，禁止随意新建分类 |
| 4 | **维护索引** | MOC 与 `.vault-meta/` 状态文件自动同步 |
| 5 | **管理关系** | 前置/相关/后续 + 双向链接 |
| 6 | **支撑长期学习** | 生命周期状态 + 间隔复习 + 面试模式 |

## 核心流程（Agent 循环，每次任务完整走一遍）

```
读取 Vault（目录 + .vault-meta 索引）
   ↓
分析结构（分类引擎：领域/分类/层级/路径）
   ↓
定位已有知识（重复检测：更新 / 子笔记 / 关联笔记）
   ↓
生成笔记（按等级匹配模板与要素）
   ↓
更新索引（MOC + .vault-meta + 双向链接）
   ↓
保存（写入文件，返回变更摘要）
```

**必须使用文件系统工具执行**（Bash / Glob / Grep / Read / Write / Edit），而不是"建议用户去做什么"：查目录、搜已有笔记、改 MOC、写索引，都是 skill 的分内动作。

## 一、笔记等级（内容深度的第一决策点）

| 等级 | 适用对象 | 内容量 | 必备要素 |
|------|---------|--------|---------|
| **L1 速记** | 单个 API、单个概念 | ≤ 1000 字 | 定义 + 核心机制 + 一个例子 |
| **L2 知识点** | 一个主题 | 1000~2500 字 | L1 + 为什么 + 对比表 + 坑 + 自测 |
| **L3 专题** | 一个体系 | 2500 字以上 | L2 + MOC + 可视化（小 mermaid 或表格）+ 学习路线 + 多篇关联 |

选级规则：一个方法 → L1；一个概念 → L2；一组有演进关系的概念 → L3。**拿不准就低不就高**。

## 二、Agent 流程分步导航

| 阶段 | 做什么 | 文件 |
|------|--------|------|
| **1. 读取与分析** | 架构感知（读目录 + 模式识别），自适应归档（复用/优化/新建三选一） | `workflow/analyze.md`、`workflow/classify.md` |
| **2. 冲突检测** | 四层检测 + 粒度判断（A 合并/B 子笔记/C 独立/D 关联） | `workflow/analyze.md`（Step 4）、`features/conflict-detection.md` |
| **3. 写作** | 按等级匹配要素，事实分级标注 | `workflow/write.md`、`features/fact-check.md` |
| **4. 自检与复习** | 质量门禁 + 复习字段 | `workflow/review.md`、`references/learning-system.md` |
| **5. 维护** | 按权限矩阵执行索引更新、MOC 同步、生命周期流转 | `workflow/maintain.md`、`features/modification-rules.md`、`references/vault-meta.md` |
| **6. 关系维护** | 前置/相关/后续 + 双向补链 | `features/knowledge-map.md` |

## 三、模板导航

| 模板 | 等级 | 文件 |
|------|------|------|
| 速记模板 | L1 | `templates/quick-note.md` |
| 知识点模板 | L2 | `templates/knowledge-note.md` |
| 专题模板 | L3 | `templates/deep-dive.md` |

写作时复制对应模板，替换 `{{占位符}}`。

## 四、规范参考

| 文件 | 内容 |
|------|------|
| `references/obsidian.md` | Obsidian 使用规范：三层管理（目录+元数据+关系）、链接/MOC/知识点规范（含链接跟随设置） |
| `references/vault-meta.md` | `.vault-meta/` 可选状态索引：index.json / taxonomy.yaml / relations.json / changelog.md |
| `references/coding-note.md` | 代码类笔记五要素 + 环境版本信息 |
| `references/learning-system.md` | 知识生命周期（learning/mastered/review/archived）+ 间隔复习 |

## 五、特色能力（features/）

| 能力 | 触发时机 | 文件 |
|------|---------|------|
| **知识关系维护** | 每篇 L2/L3 写完后 | `features/knowledge-map.md` |
| **学习路线生成** | "我要学 XX / 规划路径" | `features/learning-roadmap.md` |
| **事实验证** | 引用非用户素材的技术事实 | `features/fact-check.md` |
| **面试复习模式** | "出面试题 / 模拟面试 / 考前冲刺" | `features/interview-mode.md` |
| **架构锁定** | vault 分类变更 / 大规模迁移时 | `features/architecture.md` —— 架构状态（stable/experimental/migration）+ 迁移方案 |
| **增量整合** | 创建任何新笔记前 | `features/conflict-detection.md` —— 四层检测 + 关系分类 + 粒度判断 + 用户确认 |
| **修改权限** | 涉及 MOC/索引/移动/合并等 L2+L3 操作时 | `features/modification-rules.md` —— Level 0~3 四级权限 + 架构状态 × 操作白名单矩阵 |

## 六、Agent 快速开始（完整任务清单）

1. 读取 Vault 目录 + `.vault-meta/index.json`，了解现状。
2. 按 `workflow/classify.md` 做架构感知 → 三选一（复用/优化/新建）自适应归档。
3. 按 `workflow/analyze.md` 做重复检测：能扩展已有笔记就不新建。
4. 定等级（L1/L2/L3）→ 套模板 → 按 `workflow/write.md` 写作。
5. 跑 `workflow/review.md` 自检 → 补生命周期字段。
6. 执行 `workflow/maintain.md`：更新 MOC、`relations.json`、`changelog.md`，双向补链。
7. 返回**变更摘要**（新建/修改/归档了什么、索引更新了什么）。
