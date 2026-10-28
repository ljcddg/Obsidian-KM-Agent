---
name: obsidian-note-writer
version: 2.6.0
description: 'Obsidian 个人知识库管理系统（Knowledge Management Agent）。不止生成 Markdown 笔记，更负责知识库的长期治理：知识分类引擎（领域/一级/二级分类/层级/路径）、统一 Vault 目录规划、创建前重复检测（更新/子笔记/关联笔记三选一）、导航页（MOC 地图 / 单页学习路线双形态）与索引自动维护、前置/相关/后续关系管理与双向链接、知识生命周期管理（learning/mastered/review/archived）、事实验证分级、frontmatter 语法红线与自动体检（防 Obsidian 属性面板异常）。When to use: 用户要求"写笔记/整理知识点/建MOC或学习路线/分类归档/规划学习路线/出面试题"，或提供代码与文档要求整理进 Obsidian 知识库时触发。纯方法论，不绑定任何学科，全行业通用。'
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
| 4 | **维护索引** | **导航页**（形态 A：MOC 地图；形态 B：单页《学习路线》）与 `.vault-meta/` 状态文件自动同步 |
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
更新索引（导航页 + .vault-meta + 双向链接）
   ↓
保存（写入文件，返回变更摘要）
```

**必须使用文件系统工具执行**（Bash / Glob / Grep / Read / Write / Edit），而不是"建议用户去做什么"：查目录、搜已有笔记、改导航页、写索引，都是 skill 的分内动作。

## 一、笔记等级（内容深度的第一决策点）

| 等级 | 适用对象 | 内容量 | 必备要素 |
|------|---------|--------|---------|
| **L1 速记** | 单个 API、单个概念 | ≤ 1000 字 | 定义 + 核心机制 + 一个例子 |
| **L2 知识点** | 一个主题 | 1000~2500 字 | L1 + 为什么 + 对比表 + 坑 + 自测 |
| **L3 专题** | 一个体系 | 2500 字以上 | L2 + 导航页 + 结构图（SVG 文件或对比表）+ 学习路线 + 多篇关联 |

选级规则：一个方法 → L1；一个概念 → L2；一组有演进关系的概念 → L3。**拿不准就低不就高**。

## 二、Agent 流程分步导航

| 阶段 | 做什么 | 文件 |
|------|--------|------|
| **1. 读取与分析** | 架构感知（读目录 + 模式识别），自适应归档（复用/优化/新建三选一） | `workflow/analyze.md`、`workflow/classify.md` |
| **2. 冲突检测** | 四层检测 + 粒度判断（A 合并/B 子笔记/C 独立/D 关联） | `workflow/analyze.md`（Step 4）、`features/conflict-detection.md` |
| **3. 写作** | 按等级匹配要素，事实分级标注 | `workflow/write.md`、`features/fact-check.md` |
| **4. 自检与复习** | 质量门禁 + 复习字段 | `workflow/review.md`、`references/learning-system.md` |
| **5. 维护** | 按权限矩阵执行索引更新、导航页同步、生命周期流转 | `workflow/maintain.md`、`features/modification-rules.md`、`references/vault-meta.md` |
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
| `references/obsidian.md` | Obsidian 使用规范：三层管理（目录+元数据+关系）、链接/导航页/知识点规范（含链接跟随设置） |
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
| **修改权限** | 涉及导航页/索引/移动/合并等 L2+L3 操作时 | `features/modification-rules.md` —— Level 0~3 四级权限 + 架构状态 × 操作白名单矩阵 |

## 六、Agent 快速开始（完整任务清单）

1. 读取 Vault 目录 + `.vault-meta/index.json`，了解现状。
2. 按 `workflow/classify.md` 做架构感知 → 三选一（复用/优化/新建）自适应归档。
3. 按 `workflow/analyze.md` 做重复检测：能扩展已有笔记就不新建。
4. 定等级（L1/L2/L3）→ 套模板 → 按 `workflow/write.md` 写作。
5. 跑 `workflow/review.md` 自检 → 补生命周期字段。
6. 执行 `workflow/maintain.md`：更新导航页（MOC 或《学习路线》）、`relations.json`、`changelog.md`，双向补链。
7. 返回**变更摘要**（新建/修改/归档了什么、索引更新了什么）。

## 七、写作风格红线（防表格/图滥用，重要）

本 skill 不禁止表格，但**严格区分"讲解型内容"与"对比型内容"**，禁止用表格替代表述原理。

### 7.1 内容分两类，写法不同

| 类型 | 含义 | 正确写法 |
|------|------|---------|
| **讲解型** | 逐层/逐模块的原理、职责、机制、协议详解（如"每一层负责什么""某协议怎么工作"） | **文字段落逐点说明**，每层/每协议独立成小节展开，不缩成表 |
| **对比型** | 两个及以上对象的横向比较（如 TCP vs UDP）、模型对照（OSI vs TCP/IP）、速查索引（协议→层） | 表格（维度清晰、适合横比） |

### 7.2 红线（违反即错）

- ❌ 把"逐层/逐模块原理详解"做成一张总览表（如一张表塞下 7 层职责+协议）。
- ❌ 用「项目 \| 内容」小表缩写本该文字展开的机制、协议、职责。
- ❌ 把 L3 的"可视化"误解为"全文表格化"——可视化仅指关系图（SVG 图片或表格），**核心机制必须文字**。
- ✅ 讲解型：文字逐点（职责 + 数据单元 + 关键协议逐条 + 要点）。
- ✅ 表格仅用于：纯对比（TCP vs UDP）、模型对照（OSI vs TCP/IP）、速查表（协议→所属层）、属性列举（可选）。
- ✅ 图一律画成独立 SVG 文件（见第八章）；节点超过 12 个就拆图或转表格；但"逐层详解"不要用表替文字。

### 7.3 判定口诀

**"讲原理用字，比东西用表"**——看到"负责什么 / 怎么工作 / 为什么"，写文字；看到"区别 / 对照 / 速查"，做表格。

### 7.4 折叠写法（自测题答案 / 长附录，重要）

需要"折叠 / 展开"的内容（自测题参考答案、长附录、可选延伸）一律用 **Obsidian callout 折叠** `> [!type]- 标题`：`-` 默认收起、`+` 或省略默认展开，每行内容加 `> ` 前缀。

- ❌ **禁用 `<details>`/`<summary>`**：它对 `<summary>` 后的空行敏感，Obsidian 遇空行会拦腰截断 HTML 块 → `<details>` 变空容器、答案跑到折叠区外"一直展开"；且内部 markdown（加粗 / 行内代码）不渲染。
- ✅ 自测题参考答案推荐写法（callout 类型 `[!answer]`，配 `assets/自测答案样式.css` 可定制配色字号）：
```markdown
1. **Function Calling 的三步流程是什么？**

> [!answer]- 参考答案（点击展开）
> - ① 应用把 `@Tool` 方法生成 **JSON Schema** 放进请求 `tools` 数组发给模型
> - ② 模型返回 `tool_calls`（**只声明不执行**）
> - ③ 应用执行并**回喂**结果，模型据此生成最终回答
```
- 完整规范见 `references/self-test-answers.md`（写作 / 隐藏 / 样式）与 `references/obsidian.md` 第 7 节「callout 与标记」。

## 八、图一律用 SVG 文件（唯一载体，硬规范）

**红线：笔记里的任何图，都以独立 `.svg` 文件 + `![[...svg]]` 嵌入的形式存在。** 不使用 mermaid、不使用 ASCII 文本框图（`┌─┐` 那种）、不内联 `<svg>`。

三条理由：

1. **Obsidian 原生渲染、可缩放**：窗口缩放、导出 PDF、手机阅读都不失真；ASCII 图在等宽字体不统一时直接错位。
2. **样式可控**：mermaid 由渲染器决定外观，中文标签一长就撑爆单栏；SVG 的坐标、字号、配色都由自己定。
3. **资产可维护**：`.svg` 是文本，能 diff、能改色、能被多篇笔记复用（`![[同名.svg]]` 在任意篇都能嵌）。

### 8.1 存放与命名

- 与笔记**同目录**存放（如 `17-中间件/RabbitMQ 核心结构图.svg`），不建统一 assets 目录——按分类就近，删笔记时一起删。
- 命名：`{{主题}}核心结构图.svg` / `{{对象}}{{动作}}图.svg` / `{{算法}}流程图.svg`；文件名禁半角 `/`。
- 正文写法：独占一行 `![[{{文件名}}.svg]]`，图后必须跟 2~4 行文字解读（图不能自解释）。

### 8.2 画布与版式

- `viewBox` 用固定像素坐标（`0 0 W H`），并同时写 `width` / `height`；**W ≤ 1100**（再宽在单栏里会被缩小到看不清字）。
- 外层白底卡片：`<rect x="6" y="6" width="W-12" height="H-12" rx="12" fill="#FFFFFF" stroke="#E4E4E4"/>`。
- 圆角统一：节点 `rx=8`，容器与卡片 `rx=10~14`。

### 8.3 字号与间距（防溢出）

| 用途 | 字号 | 颜色 |
|------|------|------|
| 节点主标题 | 15 | `#2E2E38` |
| 节点副标题 / 英文名 | 10~11 | `#7B7B87` |
| 连线标签、图注 | 11.5 | `#546E7A` / `#90A4AE` |
| 最小字号 | **10**（再小缩放后不可读） | — |

- 文字宽度 ≤ 框宽 − 24px；一行标签 **≤ 14 汉字**，超了拆两行或下沉正文。
- 箭头间距 ≥ 24px；编号 chip 浮在箭头上方，不压线、不压框。

### 8.4 统一配色

| 语义 | 填充 | 描边 |
|------|------|------|
| 主体 / 普通节点 | `#EDE7F6` | `#B39DDB` |
| 正常、成功、已完成 | `#E8F5E9` | `#81C784` |
| 异常、失败、死信 | `#FFEBEE` | `#E57373` |
| 判定 / 条件框（虚线） | `#FFF8E1` | `#FFB74D` |
| 中性、外部系统 | `#ECEFF1` | `#CFD8DC` |

连线 `#455A64` + `<marker>` 箭头；一个文件内 marker 只定义一次。

### 8.5 出图后必须自查（强制）

```
chrome --headless=new --disable-gpu --hide-scrollbars --screenshot=check.png --window-size={{W}},{{H}} "file:///{{绝对路径}}/x.svg"
```

逐项看四件事：① 文字是否溢出或被裁 ② chip 是否压线 ③ 箭头是否对准框边 ④ 右侧与底部是否贴边。**简单图至少一轮，复杂图两轮**；改完再截，直到四项全过。

## 九、什么时候该画图（按语义分型）

"要不要画、画成什么样"按**内容语义**判断，不按工具判断。载体统一是 SVG（见第八章），本章只决定**画不画、画哪类**。

### 9.1 四类图

| 类型 | 表达什么 | 典型场景 | 载体 |
|------|----------|----------|------|
| **A 关系/位置图** | 实体间层级、包含、依赖、承接 | 协议栈位置、模块依赖、笔记承接 | SVG（分层块 / 连线图） |
| **B 结构/封装图** | 内部组成、字段位域、谁套谁 | TCP 首部位域、IP 包嵌套 TCP 段 | SVG（盒模型 / 位域条） |
| **C 流程/时序/状态图** | 随时间的交互、状态变迁 | 三次握手、TCP 状态机、MQ 消息一生 | SVG（纵向流程 / 泳道） |
| **D 对比表** | A vs B、属性列举、速查 | TCP vs UDP、首部字段表 | markdown 表格 |

### 9.2 选型决策（落笔前问自己）

- 讲"谁和谁关联 / 谁在谁上面" → **A 关系图**
- 讲"一个东西内部长啥样 / 字段怎么排 / 谁封装谁" → **B 结构图**
- 讲"随时间的步骤 / 交互 / 状态变化" → **C 流程 / 时序 / 状态图**
- 讲"对比两个 / 列属性 / 速查" → **D 对比表**
- 纯原理逐层展开、无结构/流程/对比 → **文字段落，不配图**

### 9.3 表优于图的判定

- **3 行以内** → 文字叙述
- **4~10 行** → 表格
- **10 行以上** → 拆表，或转 B 类结构图

### 9.4 构图约束

- **一张图只讲一件事**：节点 > 12 或连线 > 18 → 拆成两张图，或退回表格 + 文字。
- **图 ≠ 表**：结构图是形态可视化，表格是清单，二者不可互替。
- **不为"有图"而图**：纯文字原理不硬配图；图后必须跟解读。
- **旧图迁移**：遇到 mermaid 或 ASCII 框图，按本章重画成 SVG 并**替换**原代码块（不是两图并存）。

## 十、收尾固定栏目（每篇必带）

- 结构：… → 踩坑提醒 → **自测题（N 道）** → 相关笔记。
- **章节制 vault 必带「📍 本篇位置」行**（紧跟 H1 之后）：`> 📍 **本篇位置**：{{章}} 章 · N/M：{{链路}}（当前：**{{本篇}}**）`。新增/重编号/删除任一动作都要重算整章 7 篇以内的 N/M 与链路文字，否则新篇一加、全章分母全错。
- **自测题规范（必读 `references/self-test-answers.md`）**：带答案必须折叠（默认一题一折叠 `> [!answer]- 参考答案（点击展开）`，答案一点一行、要点加粗、只从正文提炼）；样式走 `assets/自测答案样式.css`（复制进 vault `.obsidian/snippets/` 并启用，见该 reference §三）。
- 同系列新笔记必须带自测题，且形态跟随最近一篇成熟笔记——**不许格式漂移**（review 门禁已含此检查）。
- **写完必跑 frontmatter 体检**：`python "<skill目录>/scripts/check_frontmatter.py" <vault路径>`，硬错误必须为 0（属性面板异常多源于此，见第十二章）。**脚本留在 skill 里用绝对路径调用，禁止复制进 vault**（复制会分叉出两份不同步的脚本）。
- **改完索引必跑一致性体检**：`python "<skill目录>/scripts/check_index_consistency.py" <vault路径>`，硬错误必须为 0；新建 / 修改 / 删除 / **改名 / 合并 / 重编号**笔记后都要跑（见第十三章）。

## 十一、配套资产与规范索引

| 文件 | 作用 |
|------|------|
| `references/self-test-answers.md` | 自测题答案规范：写作（一点一行）/ 隐藏（折叠 callout）/ 样式（CSS snippet）完整指南 |
| `assets/自测答案样式.css` | 折叠答案专属样式（teal 青、小字号），复制进 vault 即用 |
| `scripts/check_frontmatter.py` | frontmatter YAML 体检（零依赖）：抓保留字符起始 / 未闭合 / `": "` / 反斜杠等，退出码 1 表有硬错误 |
| `scripts/check_index_consistency.py` | 索引一致性体检（零依赖）：index 条数 vs 磁盘 / `file`↔`path` 一致性 / `related` 死链 / `category` 合法性 / taxonomy notes 覆盖 / relations 端点与 peer 双向 / lifecycle 合计 / **正文 `[[ ]]` 死链（警告）** / **位置行覆盖（警告）**，退出码 1 表有硬错误 |

## 十二、frontmatter 语法红线（Obsidian 属性面板异常的根因）

frontmatter 就是 Obsidian 的"笔记属性"（Properties）。**只要 YAML 有一个语法错误，整块属性都会解析失败**——表现为面板显示异常、tags/related 读不出来、Dataview 查询失准，且**肉眼极难发现**（字符串看着完全正常）。落笔时必须守住红线。

### 12.1 硬红线：flow 数组元素不得以 `@` 或反引号开头

YAML 规范中 `@` 与反引号是**保留指示符（c-reserved）**，不得作为 plain scalar 的**起始字符**。`tags` / `related` / `aliases` 若用 flow 序列（`[...]`）书写，其中任一元素以它们开头，**整个 frontmatter 解析即失败**（js-yaml 报 `missed comma between flow collection entries`，报错列号正好指向该字符）。

- ❌ `tags: [MQ, @RocketMQMessageListener, RocketMQListener]` → 整块属性炸掉
- ✅ `tags: [MQ, RocketMQMessageListener, RocketMQListener]` → **注解类名去掉 `@`**
- ✅ `tags: [MQ, "@RocketMQMessageListener"]` → 或加引号包裹

### 12.2 这些写法不算错（别误伤）

经 js-yaml 实测**解析正常**，不要"顺手改"（那是过度修改）：
- 值（source / 描述）里的 Windows 路径反斜杠：`source: 项目 D:\idea\work\MQ（...）` —— plain scalar 中反斜杠是普通字符。
- `@` 出现在值**中间**：`... + @RocketMQMessageListener）` —— 保留字符只在**首字符**位置非法。
- 全角标点（`：` `；` `（）`）与值中的全角冒号。

### 12.3 写完必须跑体检（不要靠肉眼，也不要只靠静态扫描）

静态启发式扫描**会误报**，最终判定要看真实解析器。本 skill 自带零依赖体检脚本：

```bash
python "<skill目录>/scripts/check_frontmatter.py" <vault路径>        # 全量报告
python "<skill目录>/scripts/check_frontmatter.py" <vault路径> --quiet # 只看硬错误
```

- 退出码 `1` = 存在硬错误，可挂到 review 门禁。
- 检查项：flow 元素保留字符起始（硬错误）/ frontmatter 未闭合（硬错误）/ 值含 `": "`（警告）/ 值含反斜杠（**提示**，按 §12.2 属合法写法，仅下游工具异常时再考虑加引号）/ 无 frontmatter（提示）。
- 需更权威判定时用 **Obsidian 同款解析器 js-yaml** 复核，它才是终审。

### 12.4 工程教训：任何文件写入都别用 `python -c "..."`（双引号）

在 bash 里用**双引号**包 `python -c "..."` 时，代码中的**反引号会被 shell 当作命令替换执行**，写入的内容被吃掉（实测两次：整段 changelog 文本残缺、当日工作日志三处丢字，且报一堆 `command not found`）。
**受影响范围不止「改笔记」**——追加工作日志、写 changelog、批量改索引，只要文本里有反引号或 `$` 都会中招。判断标准只有一条：**要写入的内容带反引号 → 不许用双引号内联**。

- ❌ `python -c "open(p,'w').write('...`反引号`...')"` → 反引号连同其中内容消失
- ✅ **Write 脚本文件 → `python 脚本.py`**（反引号 / `$` 不经 shell 解析）——**首选**
- ✅ `python -c '...'`（单引号，shell 不做任何解释）

## 十三、索引一致性公约（index / taxonomy / relations 三库同构）

`.vault-meta/` 下的三个索引 + MOC + 各篇 frontmatter，本质是**同一个事实的五种投影**——任何一处变更都要多处同步。以下为 2026-09-17 全库治理沉淀。

### 13.1 index.json 字段公约（唯一写法，勿再引入第二套）

| 字段 | 唯一约定 | 历史反例（勿再出现） |
|------|---------|--------------------|
| `file` | **纯文件名**（无目录、无 `.md`）＝主键 | `5-并发多线程/ThreadLocal 知识点.md` |
| `path` | **完整相对路径**（含 `.md`） | 缺该字段 |
| `category` | **taxonomy 的 `name`**（不带编号） | `13-微服务`、`并发/多线程` |
| `level` | `L1` / `L2` / `L3` | — |
| `status` | `learning` / `mastered` / `archived` / `review` | — |
| `tags` | flow 数组，元素**不得以 `@`、反引号开头**（§12.1） | `@RocketMQMessageListener` |
| `related` | 用**纯文件名**引用（与 `file`、`relations.from/to` 同构） | 写 Markdown 标题 |

字段顺序固定：`file, path, title, level, status, category, tags, related`。

**为什么 `file` 必须纯名**：`relations.json` 的 `from/to`、笔记 `related` 都 100% 用纯名；三者同构后，索引之间可直接 join 查询。目录信息只保留在 `path` 里。

### 13.2 改名 / 合并 / 删除笔记：必同步「四处 + 三个隐藏面」（否则产生死链）

1. 该篇 frontmatter 的 `title`；
2. **其他笔记正文里的 `[[旧名]]` 双链**（最易漏！只查 frontmatter 会漏掉正文；要覆盖 `[[旧名]]` / `[[旧名|别名]]` / `[[旧名#锚点]]` 三种形式）；
3. `index.json` 的 `file` / `path` / `title`，**以及每个条目的 `related` 数组**（2026-10-19 实测漏了它，体检爆 387 死链）；
4. `relations.json` 的 `from` / `to`，以及 `taxonomy.yaml` 的 `notes`；
5. **导航页的条目、步号与篇数标注**（形态 A 是 MOC 节点，形态 B 是《学习路线》第 N 步；篇数按「除导航页自身外」计数）；
6. **各篇正文的「📍 本篇位置」行**（`N/M` 分母、链路文字）——新增/重编号时最易漏，漏了整章位置行全部失真。

**三个隐藏面（本轮实测新增）**：
- **frontmatter `related` 有两种写法**：flow 数组 `related: [A, B]` **和块式列表**（`related:` 换行 `  - A`）——批量改名脚本只认 flow 会漏掉块式那一半；
- **taxonomy 的 `notes` 也有两种写法**：块式 `- 名字` 和 flow 数组 `notes: [A, B]`（树形/概率/设计模式三章是 flow）——只做行替换会漏 4 篇；
- **批量改名（加序号前缀）的可靠流程**：全量备份 → 构建旧名→新名映射 → 全库替换 `[[ ]]` 三形式 → related（flow + 块式）映射 → os.rename → index（file/path/**related**）/ relations / taxonomy 同步 → 双体检 + **正文 `[[ ]]` 死链自扫**（SVG 嵌入、代码块 `[[ ]]`、历史 changelog、"待创建"预告链接都是误报，别当死链强修）。

> **实测教训**：`Java线程池核心知识全解` → `Java线程池的执行流程与常见配置` 改名后，正文里残留 **3 处 `[[旧名]]`** 双链；首轮只改了 frontmatter 的 `related`，二次抽查才抓到。**rename 后务必 grep 旧名扫全文，不能只看 frontmatter。**

### 13.3 改完跑体检

```bash
python "<skill目录>/scripts/check_index_consistency.py" <vault路径>
```

检查项：条数一致 / `file` 唯一且纯名 / `file`↔`path` basename 一致 / `path` 真实存在 / `category` 合法 / `tags` 保留字符 / `related` 死链 / **正文 `[[ ]]` 死链（警告）** / taxonomy `notes` ⊆ 磁盘 / relations 端点与 peer 双向 / lifecycle 合计 / **位置行覆盖（警告）** / relations 端点存在 / **peer 关系双向**（hierarchy 按定义是「父→子」，允许单向）/ lifecycle 合计 = 条目数。

### 13.4 批量改动工程手法（本次实战提炼）

- **先侦察再动手**：发现 `file`/`path`/`category` 三重不一致后，先跑 5 轮侦察（磁盘映射 / taxonomy 映射 / `related` 引用约定 / frontmatter 实际值分布 / 导航页交叉引用点）才定方案，**不照着最初的粗报直接改**。
- **让数据决定规范**：`related`(283/285) 与 `relations.from/to` 全用纯名 → 反推 `file` 应为纯名；`taxonomy.name` 不带编号 → 反推 `category` 应为 `name`。
- **先备份**：结构改动前把 `index.json` 复制到 `.workbuddy/_backup_index_<日期>/`（可回退）。
- **脚本化 + 断言**：一个脚本做完全部改动，每处 `replace` 断言 `count == 1`，写回后回读校验；JSON 写回用 `with open(...)` 显式关闭。
- **补链用幂等 `add()`**：「已存在即跳过」的双向补链，比硬编码增量安全。
- **两层都要扫**：`related`（索引层）与 `[[ ]]`（正文层）是两回事——**只扫一层必漏**。
- **区分刻意保留的「未创建链接」**：导航页历史记录、系列预告篇、显式标注「待创建」的链接属正常，不要当死链强修。
- **导航页学习路线重编号**：路线条目是 `^N. **...**` 有序列表，插入 / 删除步骤后编号会错乱（实测出现过两个「18.」）。手法：**先做内容增删 → 再对 `## 三`～`## 四` 之间所有 `^\d+\. \*\*` 行顺序重排**，并 `assert` 条数兜底；比手改编号安全、可靠。
- **多会话并发写同一 vault**：① 改导航页 / changelog / taxonomy 前**现读现构造 old_string**（别凭上一轮记忆），否则断言常被并行改动打断；② 删临时脚本**别用 `_tmp_*.py` 通配**（会误删并行会话正在跑的脚本），只删自己创建的精确文件名；③ 发现别的会话正在写某分类时，**其索引由其自行收尾更安全**，不要抢写共享索引（会互相覆盖）。

### 13.5 笔记文件名命名红线（禁用半角 `/`）

**落盘文件名一律不得含半角 `/`**——Windows 会把它当作路径分隔符。2026-10-09 血案：新笔记拟名「SQL 集合运算与 SQL 注入防护（UNION / 差集 / count 对比）」，落盘时 `/` 被解释为目录分隔、只剩尾部 → 生成畸形文件 `9-SQL/ count 对比）.md`（以空格开头），直接导致 index / relations / taxonomy 与磁盘错位（20 个体检错误）+ 遗留难以删除的空壳目录。

- ✅ 分隔符改用**空格、`·`、`、` 或全角 `／`**，例如 `...（UNION 差集 count 对比）`。
- ✅ frontmatter `title` / `# H1` 里出现 `/` 无妨——**只有落盘文件名受限**。
- ⚠️ `[[ ]]` 按**文件名**解析：名字畸变或重命名后，正文与 `related` 里的旧名双链会全部失效，须按 §13.2「改名必同步四处」处理。

### 13.6 导航页双形态与章内重编号约定（2026-10-20 实战沉淀）

**导航页有两种形态，一个 vault 只选一种，不要并存：**

- **形态 A · MOC 地图**：多主题大型库，`MOC-{{主题}}.md` 放项目根，含目录树 + 按分类分组的 bullet + 学习路线章节。
- **形态 B · 单页路线页**：以"学习顺序"为唯一导航时用（Obsidian 文件树即目录，且文件名已带 `01/02` 序号前缀），根目录一份 `学习路线.md`，只有一条有序路线 + 每步的双链与要点，不再维护分类 bullet 与图谱。

形态 B 的维护口径（实测踩过）：

- **篇数标注按「除导航页自身外」计数**：vault 有 94 篇正文 + 1 份导航页 → 写"全库 94 篇"，不是 95。改计数前先看原口径（原值是 N，新增 1 篇就写 N+1），别按索引总条数填。
- **路线步骤插入/删除后必须整段重排编号**，并 `assert` 条数兜底（历史上出现过两个"18."）。
- **导航页与 MOC 不得并存**：迁移时删除旧形态，同时摘掉各篇指向旧导航页的反链（正文 `[[MOC]]`、frontmatter related、index 条目 related 数组五面都要清）。

**章内重编号（插队式新增）的决策流程**：

1. **先评估引用面**：`grep -c "[[待编号篇名"` 数正文双链、数 index `related` 引用、数 relations 端点数。三处都 ≤20 才值得重编号，否则把新篇追加到章末。
2. **语义优先**：重编号是为了让"文件名从上往下 = 学习顺序"成立（新篇在概念上属于第 5 步，就别塞到第 7 步）。
3. 顺序：备份 → 全库 `[[ ]]` 三形式替换 → frontmatter related（flow + 块式）→ `os.rename` → index（file/path/related）→ relations（端点）→ taxonomy `notes` → 位置行 N/M 与链路 → 导航页步号 → changelog → 双体检。
4. **重编号后必须重跑双体检**：只有体检能证明五面都同步了，肉眼看不出 index `related` 数组里的旧名。

## 十四、版本记录

- **2.7.0（2026-10-28）图统一为 SVG**，斌宝明确"以后笔记都用 svg 图片"：
  1. **载体收敛**：所有图一律独立 `.svg` 文件 + `![[...svg]]` 嵌入，**废弃 mermaid 与 ASCII 文本框图**（B 类结构图也改 SVG）。第八章从"mermaid 数量上限"整章重写为「图一律用 SVG 文件」，补画布尺寸、字号、配色、无头 Chrome 自查四项硬规范。
  2. **第九章重写**：只保留"按语义分型（A 关系 / B 结构 / C 流程 / D 表格）"的选题决策，渲染方式统一指向 SVG。
  3. **连带改动**：`templates/deep-dive.md`（图说明与示例改 SVG）、`workflow/write.md`（§7 可视化 + 风格红线）、`workflow/review.md`、`workflow/maintain.md`、`features/{learning-roadmap,interview-mode}.md`、`references/{obsidian,coding-note}.md`。
  4. **存量迁移**：vault 内 15 处 ASCII 框图按批次改 SVG（首批 5 张已落地：类加载七阶段、四层技术架构、Git 三大区、RAG 检索流程、Linux 用户/内核空间）。

- **2.6.0（2026-10-20）全量修订**，起因是实战复盘发现 skill 与真实 vault 脱节：
  1. **导航页双形态**：MOC 从"唯一形态"改为"形态 A"，新增"形态 B · 单页路线页"（`学习路线.md`）。同步改动 SKILL.md 核心流程 / 等级表 / 流程表 / 快速开始 / `workflow/maintain.md` Step2 / `features/{knowledge-map,learning-roadmap,modification-rules,architecture,conflict-detection}.md` / `references/{obsidian,vault-meta}.md`。
  2. **L3 不再强制 mermaid 关系图**：`templates/deep-dive.md` 的"A 类关系图（必备）"降级为"按需，可用对比表替代"，与 §7–9 及"大图撑屏难看"的实测偏好对齐。
  3. **模板补「📍 本篇位置」占位**：三个模板全部加（章节制 vault 必带，独立篇可删）。
  4. **脚本路径明确为绝对路径**，并写明"禁止复制进 vault"（曾因相对路径歧义在 vault 里重建一份，导致两份脚本能力分叉）。
  5. **体检脚本升级**：`check_index_consistency.py` 新增正文 `[[ ]]` 死链扫描 + 位置行覆盖检查（相对路径 bug 已修）；`check_frontmatter.py` 把"反斜杠"从警告降为提示（与 §12.2 口径一致，消除 3 条假警告）。
  6. **新增 §13.6**：导航页双形态、篇数计数口径（除自身外）、章内重编号的引用面评估与七步流程。
  7. **§12.4 扩为"任何文件写入"**：追加工作日志同样不能用双引号 `python -c`（实测丢字）。

