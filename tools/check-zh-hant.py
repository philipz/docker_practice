#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""正體中文檢查腳本（簡轉繁品質檢查）。

僅使用 Python3 標準庫，無任何外部相依、無外部服務。

檢查項目：
  (a) 翻譯檔不含「必簡字元」（僅收錄無歧義、不做繁簡一對多對應的簡體專用字）。
  (b) 術語符合 philipz 慣例（不得出現簡體術語）。
  (b2) 不得出現「正體禁詞」（正體字形但不符合慣例的詞，如「構建」應為「建立」）。
  (c) SUMMARY.md 中的條目對應檔案皆存在。
  (d) 翻譯檔內部的相對連結可解析（相對於該檔案所在目錄）。

用法：
    python3 tools/check-zh-hant.py [root]

預設 root 為腳本所在目錄的上一層（repo 根目錄）。
退出碼：0 表示全部通過；非 0 表示有違規。
"""

import os
import re
import sys

# ---------------------------------------------------------------------------
# (a) 必簡字元：僅收錄「簡體專用、無歧義」的字，避免一對多對應造成誤判。
#     例如「后」「里」「干」「发」等多義字不在此列。
# ---------------------------------------------------------------------------
REQUIRED_TRADITIONAL_CHARS = "们这为与从对时来发长现过会还当关开见车红给级经结统织线网语说请谢门问间题"

# ---------------------------------------------------------------------------
# (b) 術語慣例：簡體術語 -> 正體術語（philipz 慣例）。
#     若翻譯檔出現左邊的簡體術語即視為違規。
# ---------------------------------------------------------------------------
TERM_MAP = {
    "镜像": "映像檔",
    "仓库": "倉庫",
    "数据卷": "資料卷",
    "连接": "連線",
    "端口": "埠號",
    "信号": "訊號",
    "窗口": "視窗",
    "守护态": "常駐",
    "软件": "軟體",
    "组件": "元件",
    "界面": "介面",
    "自定义": "自訂",
    "搜索": "搜尋",
    "返回": "回傳",
    "立马": "立即",
    "获取": "取得",
    "构建": "建立",
    "配置": "設定",
    "服务器": "伺服器",
    "程序": "程式",
    "性能": "效能",
    "加载": "載入",
    "注释": "註解",
    "通信": "通訊",
    "信息": "資訊",
}

# ---------------------------------------------------------------------------
# (b2) 正體禁詞：以正體字形書寫、但不符合 philipz 術語慣例的詞。
#       例如「構建」這個混合了簡繁的詞，慣例應為「建立」。
#       注意：此處只收錄「構建」這類正體字形即可辨識的違規詞；
#       簡體術語（如「构建」）仍由上方 TERM_MAP 處理。
# ---------------------------------------------------------------------------
TRADITIONAL_FORBIDDEN_TERMS = {
    "構建": "建立",
}

# 檢查時排除的路徑前綴（不檢查這些目錄，避免誤判既有簡體內容）。
EXCLUDE_PREFIXES = (
    "tools/",  # 腳本本身可能含簡體字（但本腳本為正體，理應通過）
)

# 檢查範圍：僅檢查這些章節目錄下的 .md 檔（本工作項引入的翻譯檔）。
TARGET_DIRS = ("buildx", "compose", "dockerfile", "kubernetes", "kubernetes_setup", "etcd", "cloud", "ecosystem", "observability", "security", "cases_os", "case_devops")

# ---------------------------------------------------------------------------
# 輔助函式
# ---------------------------------------------------------------------------


def iter_md_files(root):
    """產生 root 下所有 .md 檔的絕對路徑（僅限 TARGET_DIRS）。"""
    for d in TARGET_DIRS:
        full = os.path.join(root, d)
        if not os.path.isdir(full):
            continue
        for dirpath, _dirnames, filenames in os.walk(full):
            for fn in sorted(filenames):
                if fn.endswith(".md"):
                    yield os.path.join(dirpath, fn)


def check_simplified_chars(path):
    """檢查必簡字元。回傳違規列表。"""
    issues = []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            for ch in line:
                if ch in REQUIRED_TRADITIONAL_CHARS:
                    issues.append((lineno, ch))
    return issues


def check_terms(path):
    """檢查簡體術語。回傳違規列表 (lineno, term)。"""
    issues = []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            for term in TERM_MAP:
                if term in line:
                    issues.append((lineno, term))
    return issues


def check_forbidden_terms(path):
    """檢查正體禁詞。回傳違規列表 (lineno, term)。

    對「構建」這類禁詞做邊界判斷：僅當「構」不是緊接在「架」「結」
    （即「架構」「結構」等正當詞）之後時，才視為違規的「構建」。
    """
    issues = []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            idx = 0
            while True:
                idx = line.find("構建", idx)
                if idx < 0:
                    break
                prev = line[idx - 1] if idx > 0 else ""
                if prev not in "架結":
                    issues.append((lineno, "構建"))
                idx += 1
    return issues


def check_summary(root):
    """檢查 SUMMARY.md 的條目對應檔案皆存在。"""
    summary_path = os.path.join(root, "SUMMARY.md")
    issues = []
    if not os.path.isfile(summary_path):
        return [("SUMMARY.md 不存在",)]
    link_re = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    with open(summary_path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            for m in link_re.finditer(line):
                target = m.group(1).strip()
                # 只處理相對連結（不含 scheme、不含錨點片段）
                if target.startswith("http://") or target.startswith("https://"):
                    continue
                if "#" in target:
                    target = target.split("#", 1)[0]
                if target == "":
                    continue
                resolved = os.path.normpath(os.path.join(root, target))
                if not os.path.isfile(resolved):
                    issues.append((lineno, target))
    return issues


def check_relative_links(path, root):
    """檢查檔案內部的相對連結可解析。回傳違規列表。"""
    issues = []
    link_re = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    base_dir = os.path.dirname(path)
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            for m in link_re.finditer(line):
                target = m.group(1).strip()
                if target.startswith("http://") or target.startswith("https://"):
                    continue
                if target.startswith("mailto:"):
                    continue
                if "#" in target:
                    target = target.split("#", 1)[0]
                if target == "":
                    continue
                resolved = os.path.normpath(os.path.join(base_dir, target))
                if not os.path.isfile(resolved):
                    issues.append((lineno, target))
    return issues


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if len(sys.argv) > 1:
        root = os.path.abspath(sys.argv[1])

    total_issues = 0

    # (a)(b) 簡體字與術語檢查
    for path in iter_md_files(root):
        rel = os.path.relpath(path, root)
        char_issues = check_simplified_chars(path)
        for lineno, ch in char_issues:
            print(f"[簡體字] {rel}:{lineno} 出現簡體字「{ch}」")
            total_issues += 1
        term_issues = check_terms(path)
        for lineno, term in term_issues:
            print(f"[簡體術語] {rel}:{lineno} 出現簡體術語「{term}」→ 應為「{TERM_MAP[term]}」")
            total_issues += 1
        forbidden_issues = check_forbidden_terms(path)
        for lineno, term in forbidden_issues:
            print(f"[正體禁詞] {rel}:{lineno} 出現正體禁詞「{term}」→ 應為「{TRADITIONAL_FORBIDDEN_TERMS[term]}」")
            total_issues += 1

    # (c) SUMMARY.md 完整性
    for item in check_summary(root):
        if isinstance(item, tuple):
            print(f"[SUMMARY] 第 {item[0]} 列的連結目標不存在：{item[1]}")
        else:
            print(f"[SUMMARY] {item[0]}")
        total_issues += 1

    # (d) 相對連結解析
    for path in iter_md_files(root):
        rel = os.path.relpath(path, root)
        for lineno, target in check_relative_links(path, root):
            print(f"[連結] {rel}:{lineno} 相對連結無法解析：{target}")
            total_issues += 1

    if total_issues == 0:
        print("正體中文檢查通過：無簡體字、無簡體術語、無正體禁詞、SUMMARY 完整、連結可解析。")
        return 0
    print(f"\n共發現 {total_issues} 個問題。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
