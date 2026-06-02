# Quant Value Analyzer

Codex skill for listed-company quantitative value analysis, with a China A-share first workflow and support for other public equities when comparable public data is available. It combines F-Score financial risk screening, B-Score business quality scoring, doubt tracking, moat analysis, management verification, and two-stage DCF valuation.

This repository is adapted from a Coze skill package into a portable Codex skill format so other agents can install and reuse it.

## What It Does

- Runs a structured listed-company value analysis workflow.
- Calculates Piotroski F-Score for financial risk screening.
- Calculates quantitative and full B-Score for business quality.
- Tracks doubts raised by quantitative signals and requires qualitative closure.
- Estimates intrinsic value using a two-stage free cash flow DCF model.
- Produces a consistent final investment analysis report template.

## Language Support

The skill source is bilingual-friendly:

- Chinese users can ask in Chinese and receive Chinese reports.
- English users can ask in English and receive English reports.
- By default, the skill should answer in the user's language unless a target language is specified.

The current detailed workflow inside `SKILL.md` is written primarily in Chinese because the original Coze package targeted Chinese value-investing analysis. Modern coding agents such as Codex can still use it from English prompts; see the examples below.

## Repository Structure

```text
examples/
skills/
  quant-value-analyzer/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/
```

## Install In Codex

From a machine with access to this public GitHub repository:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo wangzehao661-commits/quant-value-analyzer \
  --path skills/quant-value-analyzer
```

Restart Codex after installation so the skill is picked up.

## Use

Ask Codex for a deep value analysis of a listed company, for example:

```text
Use $quant-value-analyzer to analyze 600519 贵州茅台 with the latest annual report, F-Score, B-Score, doubt tracking, and conservative DCF valuation.
```

```text
Use $quant-value-analyzer to analyze Berkshire Hathaway Class B (BRK.B) with the latest annual report, F-Score, B-Score, doubt tracking, and conservative DCF valuation.
```

The skill requires current public financial data. If the running agent cannot browse or access market data, provide the latest annual report, quarterly report, valuation metrics, and market price manually.

## Examples

- [Sample prompts](examples/sample-prompts.md)
- [Short output preview](examples/output-preview.md)
- [Berkshire Hathaway Class B validation example](examples/brkb-analysis.md)

## Scripts

All scripts use the Python standard library only.

```bash
python3 skills/quant-value-analyzer/scripts/f_score.py --help
python3 skills/quant-value-analyzer/scripts/b_score_quant.py --help
python3 skills/quant-value-analyzer/scripts/b_score_full.py --help
python3 skills/quant-value-analyzer/scripts/dcf_valuation.py --help
```

## Disclaimer

This skill is for research and education only. It is not financial advice, investment advice, or a recommendation to buy or sell securities.

## License

Apache-2.0. Redistributed versions should retain the `NOTICE` file attribution.
