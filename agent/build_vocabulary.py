#!/usr/bin/env python3
"""Check reviewed vocabulary use or print proposals from accepted papers.

Vocabulary is human-owned. This command never regenerates it from a corpus.
Gold references are excluded from discovery; audit candidates can carry inline
proposed_terms until terms are deliberately reviewed.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from nasp_compendium.validate_compendium import VOCABULARY_FIELDS
from nasp_compendium.vocab_tiers import load_vocabulary


def vocabulary_proposals(
    compendium_dir: Path, vocabulary_path: Path
) -> dict[str, list[str]]:
    """Return unapproved controlled terms used by accepted paper records."""
    if not compendium_dir.is_dir():
        raise FileNotFoundError(
            f"Compendium directory not found: {compendium_dir}"
        )
    vocabulary = load_vocabulary(vocabulary_path)
    proposals: dict[str, set[str]] = {
        field: set() for field in VOCABULARY_FIELDS
    }
    for path in sorted(compendium_dir.glob("*.md")):
        if path.name.endswith(".gold.md"):
            continue
        data = yaml.safe_load(path.read_text())
        for paper in data["paper"].values():
            for field in VOCABULARY_FIELDS:
                for term in paper.get(field, []):
                    if term not in vocabulary.canonical.get(field, set()):
                        proposals[field].add(term)
    return {field: sorted(terms) for field, terms in proposals.items() if terms}


def _parse_arguments() -> argparse.Namespace:
    """Parse the read-only vocabulary inspection command."""
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--compendium", type=Path, default=root / "docs" / "compendium"
    )
    parser.add_argument(
        "--vocabulary", type=Path, default=root / "agent" / "vocabulary.yaml"
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--out",
        type=Path,
        help="Optional new proposal file; never the vocabulary.",
    )
    return parser.parse_args()


def _report_proposals(args: argparse.Namespace) -> int:
    """Report vocabulary gaps or write a separate proposal."""
    proposals = vocabulary_proposals(args.compendium, args.vocabulary)
    if args.check:
        if proposals:
            print(
                yaml.safe_dump({"unreviewed_terms": proposals}, sort_keys=True)
            )
            return 1
        print("Accepted paper terms are covered by the reviewed vocabulary.")
        return 0
    rendered = yaml.safe_dump({"proposals": proposals}, sort_keys=True)
    if args.out:
        if args.out.resolve() == args.vocabulary.resolve() or args.out.exists():
            raise FileExistsError(
                "Choose a new proposal path; "
                "reviewed files are never overwritten."
            )
        args.out.write_text(rendered)
    else:
        print(rendered, end="")
    return 0


def main() -> None:
    """Report vocabulary coverage with a controlled process exit."""
    args = _parse_arguments()
    try:
        result = _report_proposals(args)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
    sys.exit(result)


if __name__ == "__main__":
    main()
