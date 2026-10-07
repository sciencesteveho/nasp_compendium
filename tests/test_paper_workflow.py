"""Behavioral checks for PDF intake and immutable, evidence-linked review."""

from __future__ import annotations

import json
import re
from pathlib import Path

import graphviz
import pytest
import yaml

from nasp_compendium.paper_review import review_paper
from nasp_compendium.paper_sources import file_sha256
from nasp_compendium.paper_sources import prepare_paper
from nasp_compendium.paper_sources import render_source_page


@pytest.fixture
def source_pdf(tmp_path: Path) -> Path:
    """Create an actual readable PDF through the graph dependency."""
    pytest.importorskip("pypdfium2")
    graph = graphviz.Digraph()
    graph.node("A", "Source experiment: A changes B")
    path = tmp_path / "source.pdf"
    path.write_bytes(graph.pipe(format="pdf"))
    return path


@pytest.fixture
def paper_run(tmp_path: Path, source_pdf: Path) -> tuple[Path, Path, Path]:
    """Prepare a source and a minimal valid one-claim extraction."""
    run = tmp_path / "run"
    prepare_paper(source_pdf, run, paper_id="test_2026")
    draft = run / "draft.md"
    draft.write_text(
        yaml.safe_dump(
            {
                "paper": {
                    "test_2026": {
                        "cite": "Test (2026)",
                        "url": "https://example.org/test",
                        "summary": "Synthetic review case.",
                        "genes": ["CGAS", "STING1"],
                    }
                },
                "edges": [
                    {
                        "chain_id": "sensing",
                        "step": 1,
                        "source": "CGAS",
                        "target": "STING1",
                        "rel": "activates",
                        "evidence_strength": "perturbation_supported",
                        "context": "Specific intervention changes readout.",
                        "support": "main p. 1; test experiment",
                        "papers": ["test_2026"],
                    }
                ],
            }
        )
    )
    collection = tmp_path / "accepted"
    collection.mkdir()
    return run, draft, collection


def test_sources_are_page_addressable_and_cannot_be_overwritten(
    tmp_path: Path,
    source_pdf: Path,
) -> None:
    """If indexed text/images lose their source identity, this fails."""
    run = tmp_path / "run"
    manifest = prepare_paper(source_pdf, run, paper_id="test_2026")
    data = json.loads(manifest.read_text())
    assert data["sources"][0]["sha256"] == file_sha256(source_pdf)
    assert (
        "Source experiment" in (run / "sources/main/page-0001.txt").read_text()
    )
    image = render_source_page(source_pdf, 1, run / "page.png")
    assert image.read_bytes().startswith(b"\x89PNG")
    with pytest.raises(FileExistsError, match="Run already exists"):
        prepare_paper(source_pdf, run)
    with pytest.raises(ValueError, match="outside"):
        render_source_page(source_pdf, 2, run / "invalid.png")
    assert not (run / "invalid.png").exists()


def test_unreadable_pdf_does_not_leave_a_successful_run(tmp_path: Path) -> None:
    """If an empty PDF is reported as prepared source evidence, this fails."""
    pdfium = pytest.importorskip("pypdfium2")
    path = tmp_path / "blank.pdf"
    with pdfium.PdfDocument.new() as document:
        document.new_page(100, 100).close()
        document.save(path)
    with pytest.raises(ValueError, match="No extractable text"):
        prepare_paper(path, tmp_path / "run")
    assert not (tmp_path / "run").exists()


def test_review_preserves_revisions_and_source_evidence(
    paper_run: tuple[Path, Path, Path],
) -> None:
    """If review loses evidence, overwrites or promotes, this fails."""
    run, draft, collection = paper_run
    first = review_paper(
        run,
        draft,
        compendium_dir=collection,
        supplement_coverage="missing",
        notes="Supp Fig. 2 unavailable.",
    )
    frozen = (first.parent / "draft.md").read_bytes()
    payload = json.loads(
        re.search(
            r'<script id="review-data" type="application/json">(.*?)</script>',
            first.read_text(),
            re.S,
        )[1]
    )
    record = payload["views"]["paper"]["edges"][0]["evidence_records"][0]
    assert "Specific intervention" in record["context"]
    assert (
        (first.parent / record["source_links"][0]["image"])
        .read_bytes()
        .startswith(b"\x89PNG")
    )
    assert payload["manifest"]["supplement_coverage"] == "missing"
    assert "CGAS --[activates]--> STING1" in payload["diff"]
    draft.write_text(
        draft.read_text().replace(
            "Specific intervention", "Revised intervention"
        )
    )
    second = review_paper(
        run,
        draft,
        compendium_dir=collection,
        supplement_coverage="complete",
        notes="",
    )
    assert first != second
    assert (first.parent / "draft.md").read_bytes() == frozen
    assert not list(collection.iterdir())


@pytest.mark.parametrize(
    "support", ["Fig. 1", "main p. 999; Fig. 1", "supplement_1 p. 1; Fig. 1"]
)
def test_review_blocks_unresolvable_evidence(
    paper_run: tuple[Path, Path, Path],
    support: str,
) -> None:
    """If missing or out-of-bounds page citations pass review, this fails."""
    run, draft, collection = paper_run
    data = yaml.safe_load(draft.read_text())
    data["edges"][0]["support"] = support
    draft.write_text(yaml.safe_dump(data))
    with pytest.raises(ValueError, match="source"):
        review_paper(
            run,
            draft,
            compendium_dir=collection,
            supplement_coverage="complete",
            notes="",
        )
    assert not (run / "reviews").exists()


def test_review_blocks_changed_source(
    paper_run: tuple[Path, Path, Path],
) -> None:
    """If a replaced source can silently inherit old provenance, this fails."""
    run, draft, collection = paper_run
    source = json.loads((run / "run.json").read_text())["sources"][0]
    Path(source["path"]).write_bytes(b"changed")
    with pytest.raises(ValueError, match="Source changed"):
        review_paper(
            run,
            draft,
            compendium_dir=collection,
            supplement_coverage="complete",
            notes="",
        )


def test_no_findings_requires_explicit_explained_disposition(
    paper_run: tuple[Path, Path, Path],
) -> None:
    """If unexplained emptiness passes or explained abstention fails, fail."""
    run, draft, collection = paper_run
    data = yaml.safe_load(draft.read_text())
    data["edges"] = []
    draft.write_text(yaml.safe_dump(data))
    with pytest.raises(ValueError, match="Empty edges"):
        review_paper(
            run,
            draft,
            compendium_dir=collection,
            supplement_coverage="complete",
            notes="",
        )
    with pytest.raises(ValueError, match="explanation"):
        review_paper(
            run,
            draft,
            compendium_dir=collection,
            supplement_coverage="complete",
            notes="",
            no_findings=True,
        )
    review = review_paper(
        run,
        draft,
        compendium_dir=collection,
        supplement_coverage="not_applicable",
        notes="No NASP mechanism investigated.",
        no_findings=True,
    )
    assert (
        json.loads((review.parent / "run.json").read_text())["disposition"]
        == "no_in_scope_findings"
    )
