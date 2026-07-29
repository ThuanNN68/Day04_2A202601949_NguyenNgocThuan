from __future__ import annotations

from typing import Any

from tools._shared import err


ALLOWED_CRITERIA = ("research_question", "methodology", "evaluation", "results", "limitations")
MISSING = "Not detected in the supplied evidence."
MAX_CELL_CHARS = 500


def _text(value: Any) -> str:
    if isinstance(value, str):
        return " ".join(value.split())
    if isinstance(value, list):
        return " ".join(_text(item) for item in value if _text(item))
    return ""


def _excerpt(value: Any) -> str:
    text = _text(value)
    if not text:
        return MISSING
    return text[: MAX_CELL_CHARS - 3] + "..." if len(text) > MAX_CELL_CHARS else text


def _card_value(card: dict[str, Any], criterion: str) -> str:
    review = card.get("review") if isinstance(card.get("review"), dict) else {}
    evidence = card.get("evidence") if isinstance(card.get("evidence"), dict) else {}
    if criterion == "research_question":
        return _excerpt(card.get("research_question") or review.get("abstract") or card.get("summary"))
    if criterion == "methodology":
        return _excerpt(card.get("methodology") or review.get("methodology_excerpt") or evidence.get("method_signals"))
    if criterion == "evaluation":
        return _excerpt(card.get("evaluation") or review.get("evaluation_excerpt"))
    if criterion == "results":
        return _excerpt(card.get("results") or evidence.get("result_sentences"))
    return _excerpt(card.get("limitations") or review.get("limitations_excerpt") or evidence.get("limitation_sentences"))


def _identity(card: dict[str, Any], index: int) -> dict[str, str]:
    title = _text(card.get("title")) or f"Paper {index}"
    source = _text(card.get("arxiv_id")) or _text(card.get("paper_id")) or _text(card.get("url"))
    return {"title": title, "source": source}


def compare_papers(
    papers: list[dict[str, Any]] | None = None,
    criteria: list[str] | None = None,
    headline: str = "",
) -> dict[str, Any]:
    """Create a source-grounded comparison table from paper/review cards."""
    try:
        cards = papers or []
        if not isinstance(cards, list) or not 2 <= len(cards) <= 10:
            raise ValueError("Provide between 2 and 10 paper cards.")
        if not all(isinstance(card, dict) for card in cards):
            raise ValueError("Each paper card must be an object.")

        requested = criteria or list(ALLOWED_CRITERIA)
        selected = [criterion for criterion in requested if criterion in ALLOWED_CRITERIA]
        if not selected:
            selected = list(ALLOWED_CRITERIA)

        rows: list[dict[str, Any]] = []
        missing_cells = 0
        for index, card in enumerate(cards, start=1):
            row = _identity(card, index)
            for criterion in selected:
                value = _card_value(card, criterion)
                row[criterion] = value
                missing_cells += value == MISSING
            rows.append(row)

        headings = {"research_question": "Research question", "methodology": "Method", "evaluation": "Evaluation", "results": "Reported results", "limitations": "Limitations"}
        columns = ["Paper", *[headings[criterion] for criterion in selected], "Source"]
        markdown_rows = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
        for row in rows:
            values = [row["title"], *[row[criterion] for criterion in selected], row["source"] or "—"]
            markdown_rows.append("| " + " | ".join(value.replace("|", "\\|") for value in values) + " |")

        flags: list[str] = []
        if missing_cells:
            flags.append(f"{missing_cells} comparison cell(s) lack supplied evidence; they were not inferred.")
        if all(not isinstance(card.get("review"), dict) or not card.get("review") for card in cards):
            flags.append("Comparison is based on discovery-level metadata/abstracts; review full text for a stronger survey.")

        return {
            "tool": "compare_papers",
            "headline": headline.strip() or "Paper comparison",
            "criteria": selected,
            "rows": rows,
            "markdown": "\n".join(markdown_rows),
            "coverage": {"papers": len(rows), "criteria": len(selected), "missing_cells": missing_cells},
            "quality_flags": flags,
            "source_boundary": "Rows contain only supplied paper metadata, excerpts, and evidence. They are not a citation graph, quality ranking, or independent replication.",
        }
    except Exception as exc:
        return err("compare_papers", exc)
