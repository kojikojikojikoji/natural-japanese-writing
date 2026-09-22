#!/usr/bin/env python3
"""評価セットで人の文章と AI の文章を比べ、指標ごとの分離度を出す。

    python3 eval/measure.py eval/human eval/ai

各指標について、人・AI それぞれの中央値と、AUC（AI を高く並べられる確率。0.5 が偶然、1.0 が完全分離）を出す。
"""
from __future__ import annotations

import glob
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from check import analyze  # noqa: E402


def features(path: str) -> dict:
    raw = open(path, encoding="utf-8").read()
    r = analyze(raw, "business")
    n = max(len(raw), 1) / 1000  # 千字あたりに正規化
    rh = r["rhythm"]
    star_words = sum(v["count"] for k, v in r["words"].items() if k.startswith("★"))
    all_words = sum(v["count"] for v in r["words"].values())
    return {
        "★語彙/千字": star_words / n,
        "語彙全体/千字": all_words / n,
        "太字/千字": r["marks"].get("★太字（**）", 0) / n,
        "全角ダッシュ/千字": r["marks"].get("★全角ダッシュ", 0) / n,
        "句点落ち/千字": r["period_drop_count"] / n,
        "否定対比/千字": r["words"].get("★否定対比（〜ではなく 等）", {"count": 0})["count"] / n,
        "文長CV": rh.get("cv", float("nan")),
        "平均文長": rh.get("mean_len", float("nan")),
        "読点/文": rh.get("commas_per_sentence", float("nan")),
        "体言止め率": (rh.get("taigen", 0) / rh["sentences"]) if rh.get("sentences") else float("nan"),
        "同語尾連続": rh.get("same_ending_run", float("nan")),
        "★合計/千字": r["star_total"] / n,
    }


def auc(pos: list[float], neg: list[float]) -> float:
    """AI(pos) が人(neg) より大きい確率。"""
    pairs = [(p, q) for p in pos for q in neg if p == p and q == q]
    if not pairs:
        return float("nan")
    return sum(1.0 if p > q else 0.5 if p == q else 0.0 for p, q in pairs) / len(pairs)


def med(xs: list[float]) -> float:
    xs = [x for x in xs if x == x]
    return statistics.median(xs) if xs else float("nan")


def main() -> None:
    hd, ad = sys.argv[1], sys.argv[2]
    H = [features(f) for f in sorted(glob.glob(os.path.join(hd, "*.txt")))]
    A = [features(f) for f in sorted(glob.glob(os.path.join(ad, "*.txt")))]
    print(f"人 {len(H)} 本 / AI {len(A)} 本\n")
    print(f"{'指標':<14}{'人 中央値':>10}{'AI 中央値':>10}{'AUC':>8}  向き")
    for k in H[0]:
        h = [x[k] for x in H]
        a = [x[k] for x in A]
        s = auc(a, h)
        direction = "AIが大" if s > 0.5 else "AIが小"
        eff = max(s, 1 - s)
        mark = "◎" if eff >= 0.8 else "○" if eff >= 0.65 else "  "
        print(f"{k:<14}{med(h):>10.2f}{med(a):>10.2f}{s:>8.2f}  {direction} {mark}")


if __name__ == "__main__":
    main()
