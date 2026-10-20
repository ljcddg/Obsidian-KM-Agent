#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_index_consistency.py —— Obsidian vault 索引一致性体检（零依赖）

用法:
    python check_index_consistency.py <vault目录> [--quiet]

检查项（全部基于 .vault-meta/ 三个索引 + 磁盘实际文件）:
  1. index.json 条目数 == 磁盘 .md 文件数
  2. index.file 唯一、不含目录、不含 .md
  3. index.file == index.path 的 basename（去扩展名）
  4. index.path 在磁盘上真实存在
  5. index.category 均为合法分类（默认取 taxonomy 的 name 集合）
  6. index.tags 元素不以 YAML 保留字符 @ / 反引号 开头（Obsidian 属性面板红线）
  7. index.related 无死链（每个引用都能在磁盘找到同名笔记）
  8. taxonomy 各分类的 notes ⊆ 磁盘文件
  9. relations.from / to 均能在 index.file 或磁盘文件中找到
 10. relations 的 hierarchy / peer 关系双向成对
 11. taxonomy 的 lifecycle 计数合计 == 条目数

退出码: 0 = 全部通过；1 = 发现问题（human-readable 输出到 stdout）
"""
import io
import json
import os
import re
import sys

SKIP_DIRS = {'.vault-meta', '.workbuddy', '.obsidian', '.git', '.trash'}


def load_json(path):
    return json.load(io.open(path, encoding='utf-8'))


def scan_disk(vault):
    """返回 {笔记名(无扩展名): 相对路径(用/分隔)}"""
    disk = {}
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith('.md'):
                rel = os.path.relpath(os.path.join(root, f), vault).replace('\\', '/')
                name = f[:-3]
                disk.setdefault(name, []).append(rel)
    return disk


def parse_taxonomy_names(text):
    """从 taxonomy.yaml 提取 (name 集合, folder→name 映射, notes 列表)"""
    names, folder2name, notes = set(), {}, []
    cur_id = cur_name = cur_folder = None
    mode = None
    for line in text.split('\n'):
        m = re.match(r'^\s*-\s*id:\s*(\S+)', line)
        if m:
            cur_id, cur_name, cur_folder, mode = m.group(1), None, None, None
            continue
        m = re.match(r'^\s*name:\s*"([^"]*)"', line)
        if m and cur_id is not None:
            cur_name = m.group(1)
            names.add(cur_name)
            continue
        m = re.match(r'^\s*folder:\s*"([^"]*)"', line)
        if m and cur_id is not None:
            cur_folder = m.group(1)
            if cur_name is not None and cur_folder:
                folder2name[cur_folder] = cur_name
            continue
        m = re.match(r'^\s*notes:\s*\[(.*)\]\s*$', line)
        if m:
            for item in m.group(1).split(','):
                item = item.strip().strip('"').strip("'")
                if item:
                    notes.append(item)
            continue
        if re.match(r'^\s*notes:\s*$', line):
            mode = 'notes'
            continue
        if re.match(r'^\s*(description|folder|name|id):', line) or re.match(r'^\S', line):
            mode = None
        if mode == 'notes':
            m = re.match(r'^\s*-\s*(.+?)\s*$', line)
            if m:
                notes.append(m.group(1))
    return names, folder2name, notes


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    quiet = '--quiet' in sys.argv
    if not args:
        print('用法: python check_index_consistency.py <vault目录> [--quiet]')
        return 2
    vault = os.path.abspath(args[0])
    meta = os.path.join(vault, '.vault-meta')
    errs, warns = [], []

    ip = os.path.join(meta, 'index.json')
    tp = os.path.join(meta, 'taxonomy.yaml')
    rp = os.path.join(meta, 'relations.json')
    if not os.path.isfile(ip):
        print(f'[ERROR] 找不到 {ip}')
        return 1

    idx = load_json(ip)
    notes = idx.get('notes', [])
    disk = scan_disk(vault)
    disk_names = set(disk)

    dup_disk = {k: v for k, v in disk.items() if len(v) > 1}
    for k, v in dup_disk.items():
        warns.append(f'磁盘重名笔记「{k}」出现在多处: {v}（索引只能记一条）')

    # 1 条数
    if len(notes) != len(disk_names):
        errs.append(f'条目数不一致: index.json {len(notes)} 条 vs 磁盘 {len(disk_names)} 篇')
    # 2-4 file / path
    seen = set()
    for n in notes:
        f = n.get('file', '')
        if '/' in f or '\\' in f or f.endswith('.md'):
            errs.append(f'file 应为纯文件名: {f!r}')
        if f in seen:
            errs.append(f'file 重复: {f!r}')
        seen.add(f)
        path = n.get('path')
        if not path:
            errs.append(f'缺 path 字段: {f!r}')
            continue
        if not os.path.isfile(os.path.join(vault, path.replace('/', os.sep))):
            errs.append(f'path 指向的文件不存在: {path!r}（{f}）')
        elif os.path.splitext(os.path.basename(path))[0] != f:
            errs.append(f'file 与 path 的 basename 不一致: {f!r} vs {path!r}')
        # 6 tags
        for t in n.get('tags', []):
            if t and t[0] in '@`':
                errs.append(f'tag 以 YAML 保留字符开头（Obsidian 属性面板会解析失败）: {t!r}（{f}）')
        # 7 related 死链
        for r in n.get('related', []):
            if r not in disk_names:
                errs.append(f'related 死链: 「{f}」引用了不存在的笔记「{r}」')

    # 5 category（用 taxonomy name 集合校验）
    tax_names, folder2name, tax_notes = set(), {}, []
    if os.path.isfile(tp):
        tax_names, folder2name, tax_notes = parse_taxonomy_names(io.open(tp, encoding='utf-8').read())
        if tax_names:
            for n in notes:
                c = n.get('category')
                if c not in tax_names:
                    errs.append(f'category 不在 taxonomy 的 name 集合中: {c!r}（{n.get("file")}）')
    # 8 taxonomy notes ⊆ 磁盘
    for t in tax_notes:
        if t not in disk_names:
            errs.append(f'taxonomy 收录了磁盘上不存在的笔记: {t!r}')
    if tax_notes and len(tax_notes) != len(disk_names):
        warns.append(f'taxonomy 收录 {len(tax_notes)} 篇 vs 磁盘 {len(disk_names)} 篇')

    # 9-10 relations
    if os.path.isfile(rp):
        rel = load_json(rp)
        RR = rel.get('relations', [])
        # 注意：不要靠「总条目数是否为奇数」判断单边关系——
        # hierarchy（父→子）、source（笔记→源码）、evolution（演进）按语义本就允许单向，
        # 总数奇偶无意义。真正要求对称的只有 peer，见下方逐条检查。
        for x in RR:
            for side in ('from', 'to'):
                v = x.get(side)
                if v not in disk_names:
                    errs.append(f'relations.{side} 指向不存在的笔记: {v!r}（{x.get("from")} → {x.get("to")}，{x.get("type")}）')
        pair = {}
        for x in RR:
            pair[(x.get('from'), x.get('to'), x.get('type'))] = True
        oneway = []
        for (a, b, ty) in list(pair):
            # hierarchy 按定义是「父 → 子」单向（MOC → 笔记），不强制反向；
            # peer 是同级关联，语义对称，必须成对。
            if ty == 'peer' and (b, a, 'peer') not in pair:
                oneway.append(f'{a} → {b}')
        if oneway:
            warns.append(f'relations 有 {len(oneway)} 处 peer 单向（缺反向），建议补齐；前 5 条：'
                         + '；'.join(oneway[:5]))

    # 11 lifecycle
    if os.path.isfile(tp):
        txt = io.open(tp, encoding='utf-8').read()
        lc = re.search(r'^lifecycle:[ \t]*\n((?:[ \t]+\w+:[ \t]*\d+[ \t]*\n?)+)', txt, re.M)
        if lc:
            tot = sum(int(m) for m in re.findall(r':\s*(\d+)', lc.group(1)))
            if tot != len(notes):
                errs.append(f'taxonomy lifecycle 合计 {tot} ≠ index 条目数 {len(notes)}')

    # 12 MOC 目录树标注的篇数
    for fn in os.listdir(vault):
        if fn.startswith('MOC') and fn.endswith('.md'):
            mtxt = io.open(os.path.join(vault, fn), encoding='utf-8').read()
            for mt in re.finditer(r'([0-9A-Za-z\u4e00-\u9fa5\-]+/)\s+\((\d+)\s*篇\)',
                                  '\n'.join(mtxt.split('\n')[:80])):
                folder, claimed = mt.group(1).rstrip('/'), int(mt.group(2))
                fp = os.path.join(vault, folder)
                if os.path.isdir(fp):
                    actual = len([x for x in os.listdir(fp) if x.endswith('.md')])
                    if actual != claimed:
                        errs.append(f'MOC 目录树标注与磁盘不符: {folder}/ 标注 {claimed} 篇、实际 {actual} 篇')
            break

    # 13 正文 [[ ]] 双链死链（跳过代码块与嵌入；「待创建」预告属正常，故记为警告）
    link_re = re.compile(r'\[\[([^\]|#]+?)(?:[|#][^\]]*)?\]\]')
    body_dead = []
    for paths in disk.values():
        for fp in paths:
            fp = fp if os.path.isabs(fp) else os.path.join(vault, fp)
            txt = io.open(fp, encoding='utf-8').read()
            txt = re.sub(r'```.*?```', '', txt, flags=re.S)
            txt = re.sub(r'!\[\[.*?\]\]', '', txt)
            for m in link_re.finditer(txt):
                target = m.group(1).strip()
                if target and target not in disk_names:
                    body_dead.append(f'{os.path.relpath(fp, vault)} → {target}')
    if body_dead:
        warns.append(f'正文双链指向未创建笔记 {len(body_dead)} 处（若是「待创建」预告可忽略）；前 5 条：'
                     + '；'.join(body_dead[:5]))

    # 14 位置行覆盖（章节制 vault：有编号前缀的笔记建议都带 📍 本篇位置）
    no_loc = []
    for paths in disk.values():
        for fp in paths:
            fp = fp if os.path.isabs(fp) else os.path.join(vault, fp)
            base = os.path.basename(fp)
            if base[:2].isdigit() and '📍' not in io.open(fp, encoding='utf-8').read():
                no_loc.append(os.path.relpath(fp, vault))
    if no_loc:
        warns.append(f'有 {len(no_loc)} 篇编号笔记缺「📍 本篇位置」行；前 5 条：' + '；'.join(no_loc[:5]))

    # 输出
    if not quiet or errs:
        print(f'vault: {vault}')
        print(f'index 条目 {len(notes)} | 磁盘 md {len(disk_names)} | '
              f'relations {len(load_json(rp).get("relations", [])) if os.path.isfile(rp) else "?"} | '
              f'taxonomy 收录 {len(tax_notes)}')
    for w in warns:
        print(f'[WARN] {w}')
    for e in errs:
        print(f'[ERROR] {e}')
    if errs:
        print(f'\n结果: 失败（{len(errs)} 个错误, {len(warns)} 个警告）')
        return 1
    print(f'\n结果: 通过（0 错误, {len(warns)} 个警告）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
