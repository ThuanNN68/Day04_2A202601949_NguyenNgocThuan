from __future__ import annotations

import re
from typing import Any

from tools._shared import err


MAX_INPUT_CHARS = 20_000
MAX_EXCERPT_CHARS = 1_600
SECTION_ALIASES = {
    "abstract": ("abstract", "tom tat"),
    "introduction": ("introduction", "gioi thieu"),
    "methodology": ("method", "methodology", "approach", "model", "phuong phap"),
    "experiments": ("experiment", "experiments", "experimental", "evaluation", "benchmark", "thuc nghiem"),
    "results": ("results", "findings", "ket qua"),
    "limitations": ("limitation", "limitations", "failure", "caveat", "han che"),
    "conclusion": ("conclusion", "conclusions", "discussion", "ket luan"),
}
RESULT_MARKERS = ("result", "achiev", "improv", "outperform", "accuracy", "f1", "score", "benchmark", "evaluation")
LIMITATION_MARKERS = ("limitation", "limited", "caveat", "failure", "challenge", "future work", "does not", "cannot")
METHOD_MARKERS = ("we propose", "we introduce", "our method", "architecture", "dataset", "training", "retrieval")


def _normalize(text: str) -> str:
    text = (text or "").replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _heading_key(line: str) -> str | None:
    clean = re.sub(r"^\s*(?:\d+(?:\.\d+)*[.)]?\s*)", "", line).strip(" :.-").lower()
    if not clean or len(clean) > 80:
        return None
    for key, aliases in SECTION_ALIASES.items():
        if clean in aliases or any(clean.startswith(alias + " ") for alias in aliases):
            return key
    return None


def _sections(text: str) -> dict[str, str]:
    lines = text.splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        key = _heading_key(line)
        if key:
            starts.append((index, key))

    result: dict[str, str] = {}
    for position, (start, key) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        excerpt = _normalize(" ".join(lines[start + 1:end]))
        if excerpt and key not in result:
            result[key] = excerpt[:MAX_EXCERPT_CHARS]

    if "abstract" not in result:
        match = re.search(r"\babstract\b\s*[:.]?\s*(.{80,1600}?)(?=\n\s*(?:1\.?\s*)?(?:introduction|keywords)\b|$)", text, flags=re.IGNORECASE | re.DOTALL)
        if match:
            result["abstract"] = _normalize(match.group(1))[:MAX_EXCERPT_CHARS]
    return result


def _sentences(text: str) -> list[str]:
    return [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", _normalize(text)) if len(sentence.strip()) >= 35]


def _evidence(sentences: list[str], markers: tuple[str, ...], *, require_number: bool = False) -> list[str]:
    selected: list[str] = []
    for sentence in sentences:
        lowered = sentence.lower()
        if any(marker in lowered for marker in markers) and (not require_number or bool(re.search(r"\d", sentence))):
            selected.append(sentence[:500])
        if len(selected) == 6:
            break
    return selected


def review_paper_text(text: str = "", paper_id: str = "", focus: str = "full") -> dict[str, Any]:
    """Extract a bounded, source-grounded evidence card from paper text."""
    try:
        normalized = _normalize(text)
        if len(normalized) < 200:
            raise ValueError("Provide at least 200 characters of extracted paper text.")

        truncated = len(normalized) > MAX_INPUT_CHARS
        normalized = normalized[:MAX_INPUT_CHARS]
        focus = focus if focus in {"full", "methodology", "results", "limitations"} else "full"
        sections = _sections(normalized)
        sentences = _sentences(normalized)
        evidence = {
            "method_signals": _evidence(sentences, METHOD_MARKERS),
            "result_sentences": _evidence(sentences, RESULT_MARKERS, require_number=True),
            "limitation_sentences": _evidence(sentences, LIMITATION_MARKERS),
        }

        focus_key = "experiments" if focus == "results" else focus
        highlighted = sections.get(focus_key, "") if focus != "full" else ""
        if not highlighted and focus != "full":
            highlighted = "No clearly labelled section was found in the supplied excerpt."

        quality_flags: list[str] = []
        if truncated:
            quality_flags.append("Input was truncated to 20,000 characters; later sections may be missing.")
        if not sections.get("abstract"):
            quality_flags.append("No clearly labelled abstract was detected.")
        if not evidence["result_sentences"]:
            quality_flags.append("No numeric result sentence was detected; inspect the paper tables and figures directly.")
        if not evidence["limitation_sentences"]:
            quality_flags.append("No explicit limitation sentence was detected; absence is not evidence of no limitations.")

        return {
            "tool": "review_paper_text",
            "paper_id": paper_id.strip() or None,
            "focus": focus,
            "review": {
                "abstract": sections.get("abstract", ""),
                "methodology_excerpt": sections.get("methodology", ""),
                "evaluation_excerpt": sections.get("experiments", "") or sections.get("results", ""),
                "limitations_excerpt": sections.get("limitations", ""),
                "conclusion_excerpt": sections.get("conclusion", ""),
                "focus_excerpt": highlighted[:MAX_EXCERPT_CHARS],
            },
            "sections_detected": sorted(sections),
            "evidence": evidence,
            "quality_flags": quality_flags,
            "source_boundary": "All excerpts are extracted from the supplied text. Verify claims against the original paper, including tables, figures and references.",
            "chars_analyzed": len(normalized),
        }
    except Exception as exc:
        return err("review_paper_text", exc)
