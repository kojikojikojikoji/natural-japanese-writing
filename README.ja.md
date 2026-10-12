# natural-japanese-writing

[English](README.md) | 日本語

AIが書いたように読める日本語を、事実を変えずに自然な日本語へ直すスキル。Claude Code・Codex・Cursor で使える。

英語圏の同種スキル（humanizer、avoid-ai-writing）は「delve」「tapestry」「em dash」など英語の癖を対象にしていて、日本語特有の癖は扱わない。このスキルは日本語の癖を、国内の実測記事・研究と、自前の評価セットでの計測を根拠に扱う。

## 何が違うか

- 文書の種類を先に決める。業務文書（報告・提案書・議事録・Slack）では体験談や感情を足さない。読み物（ブログ・note）では残す。
- 6層で点検する。表記・語彙・文末とリズム・構文・構成・中身。癖は全59項目（★は25項目）。
- 癖の強さで扱いを変える。★の癖は1つ見つけたら直す。それ以外は、同じ段落に違う種類の癖が3つ以上重なったら直す。外部の計測で人の文章に多かった表現（「最後に」「まさに」）は直さない。
- 根拠を自分で測っている。人40本・AI 40本の評価セットで、指標ごとに人とAIをどれだけ見分けられるか（AUC）を出し、人の文章の分布を見てしきい値を決めた。評価セットで人のほうが多く使っていた表現（「に関して」「〜することができます」）は、癖の一覧から外した。
- 数える道具がある。`scripts/check.py` が、太字・全角ダッシュ・最後の文だけ句点が無い行・「〜ではなく」・頻出語・提案書に残った「御社」・語尾の連続・文の長さのばらつきを数える。
- 日本語の文章に特有の癖を扱う。1行の中で最後の文だけ句点が無い、読点の打ちすぎ、コロンの後の半角スペース、「」の入れ子、体言止めが1つも無い、直しすぎて常体が混ざる、など。
- 実務の文書の癖も扱う。技術事象の比喩・擬人化（「台帳が壊れた」）、内部の識別子を主語にした説明（「plan_config の価格が〜」）、非エンジニア宛の報告に書かれたファイルパス、A案・B案と経緯に頼った資料。

## 導入

Claude Code:

```
mkdir -p ~/.claude/skills
git clone https://github.com/kojikojikojikoji/natural-japanese-writing ~/.claude/skills/natural-japanese-writing
```

- Cursor は `~/.claude/skills/` も読むので、上と同じ手順でよい（`~/.cursor/skills/` に置いてもよい）。
- Codex は `~/.agents/skills/` を読む。`mkdir -p ~/.agents/skills && ln -s ~/.claude/skills/natural-japanese-writing ~/.agents/skills/` でリンクを張る。
- Grok Build（xAI のコマンドライン版）は Claude Code のスキルを読み込むと報告されている。作者は動作を確認していない。

## 使い方

「AIっぽさを消して」「自然な日本語にして」「人が書いたように直して」と頼む。ファイル名を渡せば、地の文だけを直して上書きする。

数えるだけなら:

```
python3 scripts/check.py 文章.md
pbpaste | python3 scripts/check.py      # macOS のクリップボードから
```

## 構成

| ファイル | 内容 |
|---|---|
| `SKILL.md` | 手順と6層の点検表 |
| `scripts/check.py` | 機械チェック（Python 3.9 以上、依存なし） |
| `examples/` | 書き直し前後の例 |
| `eval/` | 評価セット（AI 40本を同梱、人の側は非公開）と計測スクリプト。しきい値の根拠は `eval/README.md` |
| `tests/` | 回帰テスト。`python3 tests/test_examples.py` |

## 根拠

SKILL.md 末尾の「参考にしたもの」に、実測記事・研究・先行スキルを挙げている。先行スキルからは考え方だけを参考にし、文面とコードは流用していない。

## ライセンス

MIT
