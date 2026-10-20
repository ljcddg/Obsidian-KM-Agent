# -*- coding: utf-8 -*-
"""
Obsidian Vault frontmatter 语法体检（零依赖，仅用标准库）

为什么需要：Obsidian 的属性面板（Properties）用 YAML 解析 frontmatter。
只要 frontmatter 有一个语法错误，**整块属性都会解析失败**——表现为面板显示
异常、tags/related 读取不到、Dataview 查询失准。而错误极难肉眼发现。

本脚本检查最常见的几类"静默炸雷"，尤其是本库真实踩过的坑：
  [硬错误] flow 数组元素（tags / related / aliases）以 YAML 保留指示符开头
           —— `@` 与反引号是 c-reserved，不得作为 plain scalar 起始字符。
           例：tags: [MQ, @RocketMQMessageListener]  → 整个 frontmatter 解析失败
  [硬错误] frontmatter 未闭合（首行 --- 之后找不到第二个 ---）
  [警告]   值含 ": "（半角冒号+空格），会被 YAML 当成嵌套映射截断
  [警告]   值含未加引号的 Windows 路径反斜杠（部分解析器/工具会出问题）
  [提示]   文件无 frontmatter（与库内其他笔记格式不一致）

用法:
    python check_frontmatter.py <vault路径> [--quiet]
退出码:
    0 = 无硬错误；1 = 存在硬错误（可挂到写作流程的 review 门禁）
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

RESERVED_START = '@`'          # YAML 保留指示符，不可作 plain scalar 起始
FLOW_KEYS = ('tags:', 'related:', 'aliases:', 'cssclasses:')
SKIP_DIRS = ('.vault-meta', '.workbuddy', '.obsidian', '.git', '_backup', '_tmp', 'node_modules')


def split_frontmatter(text):
    """返回 (fm行列表, 状态)。状态: ok / none / unclosed"""
    lines = text.split('\n')
    if not lines or lines[0].strip() != '---':
        return None, 'none'
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            return lines[1:i], 'ok'
    return None, 'unclosed'


def iter_flow_elems(line):
    """从 `key: [a, b, c]` 中逐个产出元素文本"""
    lb = line.find('[')
    if lb == -1:
        return
    body = line[lb + 1:]
    rb = body.rfind(']')
    if rb != -1:
        body = body[:rb]
    for e in body.split(','):
        e = e.strip()
        if e:
            yield e


def check_file(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    fm, status = split_frontmatter(text)
    errs, warns, notes = [], [], []
    if status == 'none':
        notes.append('无 frontmatter（首行不是 ---）')
        return errs, warns, notes
    if status == 'unclosed':
        errs.append('frontmatter 未闭合：找不到第二个 ---')
        return errs, warns, notes

    for idx, line in enumerate(fm, start=2):
        stripped = line.lstrip()
        low = stripped.lower()
        # [硬错误] flow 元素以保留指示符开头
        if low.startswith(FLOW_KEYS):
            for elem in iter_flow_elems(line):
                if elem[0] in RESERVED_START:
                    errs.append(
                        f'L{idx} flow 元素以保留字符 {elem[0]!r} 开头 → 整个 frontmatter 会解析失败：{elem}'
                    )
        # [警告] 值含 ": "
        if ':' in line and not stripped.startswith('#'):
            _, _, val = line.partition(':')
            if val and not val.strip().startswith(('"', "'", '[', '{', '|', '>')):
                if re.search(r'\S:(?=\s)', val):
                    warns.append(f'L{idx} 值中含 ": "（半角冒号+空格），可能被截断为嵌套映射')
        # [警告] 未加引号的值含反斜杠
        if ':' in line:
            val = line.split(':', 1)[1]
            if '\\' in val and not val.strip().startswith(('"', "'", '|', '>')):
                notes.append(f'L{idx} 值含反斜杠（YAML 合法，仅提示；下游工具异常时再考虑加单引号）')
    return errs, warns, notes


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    vault = sys.argv[1]
    quiet = '--quiet' in sys.argv
    hard = 0
    warn_total = 0
    note_total = 0
    files = 0
    for root, dirs, fs in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in sorted(fs):
            if not fn.endswith('.md'):
                continue
            files += 1
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, vault)
            try:
                errs, warns, notes = check_file(path)
            except Exception as e:
                print(f'[读取失败] {rel}: {e}')
                hard += 1
                continue
            if errs:
                hard += len(errs)
                print(f'\n❌ [硬错误] {rel}')
                for e in errs:
                    print(f'     - {e}')
            if warns and not quiet:
                warn_total += len(warns)
                print(f'\n⚠️  [警告] {rel}')
                for w in warns:
                    print(f'     - {w}')
            if notes and not quiet:
                note_total += len(notes)
                print(f'\nℹ️  [提示] {rel}')
                for n in notes:
                    print(f'     - {n}')
    print(f'\n{"=" * 52}')
    print(f'共扫描 {files} 篇 | 硬错误 {hard} 处 | 警告 {warn_total} 处 | 提示 {note_total} 处')
    if hard == 0:
        print('✅ frontmatter 体检通过')
    else:
        print('❌ 存在硬错误，Obsidian 属性面板会异常，请修复后重跑')
    return 1 if hard else 0


if __name__ == '__main__':
    sys.exit(main())
