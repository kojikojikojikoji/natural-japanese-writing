#!/usr/bin/env python3
"""回帰テスト。

1. examples/README.md の「前」「後」の各組で、「後」の★の数が「前」より少ないこと。
2. 「前」に含まれる数値と固有名詞（英数字の語）が「後」にも残っていること（事実の脱落を検出）。
3. SKILL.md 自身に、意図した例文以外で行末だけ落ちた句点が無いこと。

    python3 tests/test_examples.py
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from check import analyze, period_drop, strip_code  # noqa: E402


def pairs() -> list[tuple[str, str, str]]:
    md = open(os.path.join(ROOT, "examples", "README.md"), encoding="utf-8").read()
    out = []
    for sec in re.split(r"\n## ", md)[1:]:
        title = sec.split("\n", 1)[0]
        m = re.search(r"前:\n\n((?:> .*\n?)+)\n+後:\n\n((?:> .*\n?)+)", sec)
        if not m:
            continue
        before = "\n".join(l[2:] for l in m.group(1).strip().splitlines())
        after = "\n".join(l[2:] for l in m.group(2).strip().splitlines())
        out.append((title, before, after))
    return out


def facts(text: str) -> set[str]:
    """数値（単位付き）と英数字の語。書き直しで落ちてはいけないもの。"""
    nums = set(re.findall(r"\d[\d,\.]*(?:円|%|件|人|時間|日|分|倍|字)?", text))
    alnum = set(w for w in re.findall(r"[A-Za-z][A-Za-z0-9_.]{2,}", text))
    return nums | alnum


def main() -> int:
    failed = 0
    ps = pairs()
    assert ps, "examples/README.md に前後の組が見つからない"
    for title, before, after in ps:
        b = analyze(before)["star_total"]
        a = analyze(after)["star_total"]
        ok = a < b or (b == 0 and a == 0)
        print(f"[{'ok' if ok else 'NG'}] {title}: ★ {b} → {a}")
        failed += not ok
        lost = {f for f in facts(before) if f not in after}
        # 意図して外す識別子（読み手に合わせる例）は許容: 6-7 と 6-8 の例、および擬人化の例
        allow = any(k in title for k in ("Slack", "符号", "擬人化", "記号と常套句", "口語"))
        if lost and not allow:
            print(f"      事実の脱落の疑い: {sorted(lost)}")
            failed += 1
    skill = strip_code(open(os.path.join(ROOT, "SKILL.md"), encoding="utf-8").read())
    drops = [d for d in period_drop(skill) if not d.startswith("- 前:")]
    print(f"[{'ok' if not drops else 'NG'}] SKILL.md の句点落ち: {len(drops)}")
    for d in drops[:5]:
        print("      " + d[:70])
    failed += bool(drops)
    print("FAILED" if failed else "ALL OK")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
