---
name: paper_review
track: core
kind: local_analysis
provider: local deterministic parser
requires_env: []
inputs: [text, paper_id, focus]
outputs: [review, evidence, sections, quality_flags]
side_effect: false
---
# paper_review

Builds an evidence card from extracted paper text or text pasted by the user.
Use it **after** `paper_text` when the user asks to assess a specific arXiv
paper, or directly when they supply enough paper text. It extracts rather than
inventing: abstract, section excerpts, method/dataset signals, result sentences
containing measurements, and limitation sentences.

`focus` controls which section receives the most space:

- `full`: compact research review (default)
- `methodology`: method, data and experimental setup
- `results`: measured results and evaluation evidence
- `limitations`: caveats, failure cases and stated limitations

It does not establish that a claim is true; users should inspect the returned
`evidence` excerpts and cite the original paper URL/ID.
