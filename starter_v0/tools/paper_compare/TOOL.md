---
name: paper_compare
track: core
kind: local_analysis
provider: local deterministic formatter
requires_env: []
inputs: [papers, criteria, headline]
outputs: [rows, markdown, coverage, quality_flags]
side_effect: false
---
# paper_compare

Compares two to ten paper cards that have already been collected. A paper card
may be an arXiv result (`title`, `summary`, `url`, `arxiv_id`) or a review card
with the `review` and `evidence` fields emitted by `paper_review`.

The tool only aligns excerpts and evidence supplied in `papers`; it does not
retrieve papers, calculate a scientific ranking, or infer missing results.
Use it after `papers` for an abstract-level landscape, and preferably after
`paper_text` → `paper_review` for a defensible survey.

Available criteria are `research_question`, `methodology`, `evaluation`,
`results`, and `limitations`. Missing evidence is displayed explicitly. Treat
the returned markdown as a draft comparison table and cite the source URLs/IDs
when presenting a survey.
