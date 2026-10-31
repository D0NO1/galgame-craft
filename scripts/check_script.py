#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""静态检查 Ren'Py 剧本里的常见硬伤。

用法：
    python check_script.py <project_dir>            # 例如 D:/app/RenPyProjects/homestay
    python check_script.py <project_dir> --max 45   # 自定义单句字数上限

检查项：
  1. jump / call 目标 label 不存在（悬空跳转）
  2. voice 引用的音频文件不存在
  3. 单句台词过长（默认 > 45 个中文字，对话框会挤）
  4. menu 块里没有任何变量修改（选项白给）
  5. 同一 label 重复定义

退出码：0 = 无问题，1 = 有问题。
"""
import os
import re
import sys

DIALOG = re.compile(r'^\s*(?:voice\s+"[^"]*"\s*)?([A-Za-z_]\w*)\s+"((?:[^"\\]|\\.)*)"\s*$')
LABEL = re.compile(r'^label\s+([A-Za-z_]\w*)\s*:')
JUMP = re.compile(r'^\s*(?:jump|call)\s+([A-Za-z_]\w*)\s*$')
VOICE = re.compile(r'^\s*voice\s+"([^"]+)"')


def cjk_len(s):
    return sum(1 for ch in s if '\u4e00' <= ch <= '\u9fff')


def main():
    if len(sys.argv) < 2:
        print("用法: python check_script.py <project_dir> [--max N]")
        return 1
    proj = sys.argv[1]
    max_len = 45
    if "--max" in sys.argv:
        max_len = int(sys.argv[sys.argv.index("--max") + 1])

    game = os.path.join(proj, "game")
    if not os.path.isdir(game):
        print(f"[ERR] 找不到 {game}")
        return 1

    issues = []
    labels = {}
    jumps = []
    voices = []

    files = [os.path.join(game, f) for f in os.listdir(game) if f.endswith(".rpy")]
    for path in files:
        name = os.path.basename(path)
        with open(path, encoding="utf-8-sig") as fh:
            lines = fh.readlines()

        in_menu = False
        menu_start = 0
        menu_touched = False

        for i, raw in enumerate(lines, 1):
            line = raw.rstrip("\n")

            m = LABEL.match(line)
            if m:
                if m.group(1) in labels:
                    issues.append(f"[重复 label] {m.group(1)} 在 {name}:{i}，首次出现于 {labels[m.group(1)]}")
                labels[m.group(1)] = f"{name}:{i}"
                continue

            m = JUMP.match(line)
            if m:
                jumps.append((m.group(1), f"{name}:{i}"))
                continue

            m = VOICE.match(line)
            if m:
                voices.append((m.group(1), f"{name}:{i}"))

            # menu 块跟踪（靠缩进）
            if re.match(r'^\s*menu\s*:', line):
                in_menu, menu_start, menu_touched = True, i, False
                continue
            if in_menu:
                if re.match(r'^\s*\$\s+', line) or re.match(r'^python\s*:', line):
                    menu_touched = True
                if line and not line.startswith((" ", "\t")) and not re.match(r'^\s*$', line):
                    if not menu_touched:
                        issues.append(f"[选项白给] {name}:{menu_start} 的 menu 里没有任何变量修改")
                    in_menu = False

            m = DIALOG.match(line)
            if m:
                who, text = m.group(1), m.group(2)
                if who in ("play", "scene", "show", "hide", "with", "image", "define"):
                    continue
                n = cjk_len(text)
                if n > max_len:
                    issues.append(f"[台词过长] {name}:{i} 共 {n} 字（上限 {max_len}）：{text[:18]}…")

        # 文件结束时菜单还没收口，也要结算
        if in_menu and not menu_touched:
            issues.append(f"[选项白给] {name}:{menu_start} 的 menu 里没有任何变量修改")

    for target, where in jumps:
        if target not in labels:
            issues.append(f"[悬空跳转] {where} 跳到不存在的 label: {target}")

    for rel, where in voices:
        p = os.path.join(game, rel.replace("/", os.sep))
        if not os.path.isfile(p):
            issues.append(f"[缺音频] {where} 引用不存在的文件: {rel}")

    print(f"扫描 {len(files)} 个 .rpy，{len(labels)} 个 label")
    if not issues:
        print("✅ 无问题")
        return 0
    for it in issues:
        print(" -", it)
    print(f"\n共 {len(issues)} 条问题")
    return 1


if __name__ == "__main__":
    sys.exit(main())
