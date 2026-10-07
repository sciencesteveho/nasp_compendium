"""Prepare local, page-addressable paper sources for agent curation."""

from __future__ import annotations

import hashlib
import json
import math
import tempfile
from collections.abc import Sequence
from pathlib import Path


try:
    import pypdfium2 as pdfium
except ModuleNotFoundError:
    pdfium = None


def prepare_paper(
    paper_path: Path,
    run_dir: Path,
    *,
    supplements: Sequence[Path] = (),
    paper_id: str | None = None,
    instruction_paths: Sequence[Path] = (),
) -> Path:
    """Create a new local run with indexed text and source provenance.

    Existing runs are never overwritten. Images and extracted text belong in
    ignored run directories; original PDFs are referenced without copying.
    Sparse-text pages require visual inspection, not inferred missing biology.

    Args:
      paper_path: Main paper PDF.
      run_dir: New directory for this extraction run.
      supplements: Available supplementary PDFs, in source-ID order.
      paper_id: Record identifier, defaulting to the main PDF's stem.
      instruction_paths: Instructions whose hashes identify the run protocol.

    Returns:
      Path to the source manifest.
    """
    if pdfium is None:
        raise ImportError('Install PDF tools with pip install ".[extraction]".')
    if run_dir.exists():
        raise FileExistsError(f"Run already exists: {run_dir}. Use a new run.")
    paths = [paper_path.resolve(), *(path.resolve() for path in supplements)]
    for path in [*paths, *instruction_paths]:
        if not path.is_file():
            raise FileNotFoundError(f"Source or instruction not found: {path}")
    if len(set(paths)) != len(paths):
        raise ValueError("Each source PDF must be supplied only once.")

    run_dir.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=run_dir.parent) as temporary:
        staging = Path(temporary) / "run"
        staging.mkdir()
        (staging / ".gitignore").write_text("*\n")
        sources = []
        for index, path in enumerate(paths):
            source_id = "main" if index == 0 else f"supplement_{index}"
            source_dir = staging / "sources" / source_id
            source_dir.mkdir(parents=True)
            pages = []
            with pdfium.PdfDocument(path) as document:
                for page_index in range(len(document)):
                    page = document[page_index]
                    text_page = page.get_textpage()
                    text = text_page.get_text_bounded().replace("\r\n", "\n")
                    text_page.close()
                    page.close()
                    page_number = page_index + 1
                    (source_dir / f"page-{page_number:04d}.txt").write_text(
                        text, encoding="utf-8"
                    )
                    pages.append(len(text.strip()))
            if not pages or not any(pages):
                raise ValueError(
                    f"No extractable text in {path}; prepare an OCR-enabled "
                    "PDF, then retry intake with that source."
                )
            sources.append(
                {
                    "id": source_id,
                    "path": str(path),
                    "sha256": file_sha256(path),
                    "pages": len(pages),
                    "sparse_text_pages": [
                        index + 1
                        for index, length in enumerate(pages)
                        if length < 40
                    ],
                }
            )
        manifest = {
            "paper_id": paper_id or paper_path.stem,
            "status": "sources_prepared",
            "sources": sources,
            "supplement_coverage": "unchecked",
            "instructions": {
                str(path): file_sha256(path) for path in instruction_paths
            },
            "pdf_reader": str(pdfium.PYPDFIUM_INFO),
        }
        (staging / "run.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )
        staging.rename(run_dir)
    return run_dir / "run.json"


def render_source_page(
    pdf_path: Path,
    page_number: int,
    output_path: Path,
    *,
    scale: int = 2,
) -> Path:
    """Render a one-based PDF page for inspecting figures and scanned text."""
    if pdfium is None:
        raise ImportError('Install PDF tools with pip install ".[extraction]".')
    if not math.isfinite(scale) or scale <= 0:
        raise ValueError("Page scale must be positive and finite.")
    if output_path.exists():
        raise FileExistsError(f"Page image already exists: {output_path}")
    with pdfium.PdfDocument(pdf_path) as document:
        if page_number < 1 or page_number > len(document):
            raise ValueError(
                f"Page {page_number} is outside 1-{len(document)}: {pdf_path}"
            )
        page = document[page_number - 1]
        bitmap = page.render(scale=scale)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        bitmap.to_pil().save(output_path, format="PNG")
        bitmap.close()
        page.close()
    return output_path


def file_sha256(path: Path) -> str:
    """Return the SHA-256 of a source or frozen draft without loading it all."""
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()
