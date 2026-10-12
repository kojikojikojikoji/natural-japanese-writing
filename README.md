# natural-japanese-writing

English | [日本語](README.ja.md)

An agent skill that rewrites Japanese text that reads as AI-generated into natural Japanese, without changing the facts. Works with Claude Code, Codex and Cursor.

Existing humanizer skills (humanizer, avoid-ai-writing) target English tells such as "delve", "tapestry" and the em dash. Japanese has its own tells, and those skills do not cover them. This skill is built from Japanese-language measurements and research, plus its own evaluation set.

You do not need to read Japanese to use it. The checklist inside `SKILL.md` is written in Japanese because every example and every detected phrase is Japanese; the agent reads it as is.

## Who it is for

- Developers shipping Japanese UI copy, docs or support replies written with an LLM
- Teams that have AI draft Japanese reports, proposals, meeting minutes or Slack messages
- Anyone who writes in Japanese with AI help and keeps hearing "this sounds like ChatGPT"

## What it does

- **Picks the document type first.** Business documents (reports, proposals, minutes, Slack) get no added anecdotes or emotion. Casual reading (blogs, note.com) keeps the writer's voice.
- **Checks six layers**: notation, vocabulary, sentence endings and rhythm, syntax, structure, and content. 59 tells in total, 25 of them starred.
- **Weighs tells by strength.** A starred (★) tell is fixed on sight. Weaker tells are fixed only when three or more different ones appear in the same paragraph. Phrases that an external study found more common in human writing (such as 最後に and まさに) are left alone.
- **Measures its own thresholds.** 40 human and 40 AI texts were scored per metric (AUC), and thresholds were set from the human distribution. See `eval/README.md`.
- **Comes with a counter.** `scripts/check.py` counts bold text, em dashes, lines whose last sentence lacks a period while earlier ones have it, "not X but Y" contrasts, overused words, sentence-ending repetition and sentence-length variance.

Examples of Japanese-specific tells it fixes:

| Tell | Example |
|---|---|
| Uniform sentence endings | 「〜です。〜です。〜ます。〜です。」 |
| No noun-ending sentences (体言止め) in casual writing | In an external study of 406 texts, AI articles used none; 60% of human articles did |
| Bold label followed by a colon | 「**速度：** 処理が3倍に」 |
| Overused abstract words | 「重要です」「適切な」「本質」「シームレスに」 |
| Template openings and closings | 「本記事では〜について解説します」「いかがでしたでしょうか」 |
| Internal identifiers used as the subject in reports to non-engineers | 「plan_config の価格が〜」 |

Before/after samples are in [`examples/README.md`](examples/README.md) (Japanese).

## Install

Claude Code:

```
mkdir -p ~/.claude/skills
git clone https://github.com/kojikojikojikoji/natural-japanese-writing ~/.claude/skills/natural-japanese-writing
```

- **Cursor** also reads `~/.claude/skills/`, so the same command works. `~/.cursor/skills/` works too.
- **Codex** reads `~/.agents/skills/`. Link it with `mkdir -p ~/.agents/skills && ln -s ~/.claude/skills/natural-japanese-writing ~/.agents/skills/`.
- **Grok Build** (xAI's CLI) is reported to load Claude Code skills. Not tested by the author.

## Usage

Ask the agent in either language:

- "Make this Japanese sound less AI-written."
- 「AIっぽさを消して」「自然な日本語にして」

Pass a file name and it rewrites the prose in place.

To count tells only:

```
python3 scripts/check.py draft.md
pbpaste | python3 scripts/check.py      # from the macOS clipboard
```

The report is in Japanese.

## Layout

| Path | Contents |
|---|---|
| `SKILL.md` | Workflow and the six-layer checklist (Japanese) |
| `scripts/check.py` | Tell counter (Python 3.9+, no dependencies) |
| `examples/` | Before/after rewrites |
| `eval/` | Evaluation set (40 AI texts included; the human texts are internal and not published) and the scoring script |
| `tests/` | Regression tests: `python3 tests/test_examples.py` |

## Sources

The "参考にしたもの" (references) section at the end of `SKILL.md` lists the articles, research and earlier skills this draws on. Earlier skills informed the approach only; no text or code was copied.

## License

MIT
