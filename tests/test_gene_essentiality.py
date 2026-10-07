"""Tests for annotating the marker panel with gene essentiality."""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any

import pandas as pd

from nasp_compendium import gene_essentiality


def _write_annotation_inputs(directory: Path) -> list[str]:
    """Write a CRLF marker panel and miniature sources; return CLI arguments.

    DDX41 is listed in two modules. DepMap screens CGAS and DDX41 and calls
    only DDX41 common essential; MT-ND1 is unscreened and lacks an s_het.
    """
    panel_path = directory / "marker_genes.tsv"
    panel_path.write_bytes(
        b"gene_symbol\tmodule_id\tscoring_direction\taliases\r\n"
        b"CGAS\tNASP_DNA_SENSING\tpositive\tMB21D1\r\n"
        b"DDX41\tNASP_DNA_SENSING\tpositive\t\r\n"
        b"DDX41\tNASP_RNA_SENSING\tpositive\t\r\n"
        b"MT-ND1\tMITOCHONDRIAL_NA_SENSING\tpositive\t"
    )
    hgnc_path = directory / "hgnc.txt"
    hgnc_path.write_text(
        "hgnc_id\tsymbol\tstatus\tprev_symbol\talias_symbol\tentrez_id\n"
        "HGNC:21367\tCGAS\tApproved\tC6orf150|MB21D1\th-cGAS\t115004\n"
        "HGNC:18674\tDDX41\tApproved\t\tABS\t51428\n"
        "HGNC:7455\tMT-ND1\tApproved\tMTND1\t\t4535\n"
    )
    common_essentials_path = directory / "common_essentials.csv"
    common_essentials_path.write_text("Essentials\nDDX41 (51428)\n")
    gene_effect_path = directory / "gene_effect.csv"
    gene_effect_path.write_text("ModelID,CGAS (115004),DDX41 (51428)\n")
    shet_path = directory / "shet.tsv"
    shet_path.write_text(
        "hgnc\tpost_mean\tpost_lower_95\tpost_upper_95\n"
        "HGNC:21367\t0.00114\t0.000111\t0.00362\n"
        "HGNC:18674\t0.0203\t0.0114\t0.0309\n"
    )
    return [
        "--marker-genes",
        str(panel_path),
        "--hgnc",
        str(hgnc_path),
        "--depmap-common-essentials",
        str(common_essentials_path),
        "--depmap-gene-effect",
        str(gene_effect_path),
        "--shet",
        str(shet_path),
    ]


def _annotate_panel(monkeypatch: Any, arguments: list[str]) -> None:
    """Run the essentiality command line with `arguments`."""
    monkeypatch.setattr(sys, "argv", ["gene_essentiality", *arguments])
    gene_essentiality.main()


def test_annotation_leaves_curated_panel_bytes_unchanged(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Annotation only appends fields, keeping curated text and CRLF endings."""
    arguments = _write_annotation_inputs(tmp_path)
    panel_path = tmp_path / "marker_genes.tsv"
    curated_lines = panel_path.read_bytes().split(b"\r\n")
    n_curated_fields = len(curated_lines[0].split(b"\t"))

    _annotate_panel(monkeypatch, arguments)

    annotated_lines = (
        panel_path.read_bytes().removesuffix(b"\r\n").split(b"\r\n")
    )
    assert [
        b"\t".join(line.split(b"\t")[:n_curated_fields])
        for line in annotated_lines
    ] == curated_lines


def test_annotation_marks_every_panel_row_of_a_gene(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Each panel row carries its gene's DepMap status and s_het estimate."""
    arguments = _write_annotation_inputs(tmp_path)

    _annotate_panel(monkeypatch, arguments)

    annotated = pd.read_csv(tmp_path / "marker_genes.tsv", sep="\t")
    assert annotated["depmap_essentiality"].tolist() == [
        "not_common_essential",
        "common_essential",
        "common_essential",
        "not_screened",
    ]
    shet = annotated["shet_post_mean"].tolist()
    assert shet[:3] == [0.00114, 0.0203, 0.0203]
    assert math.isnan(shet[3])


def test_rerunning_annotation_leaves_panel_unchanged(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Annotating an already annotated panel rewrites identical bytes."""
    arguments = _write_annotation_inputs(tmp_path)
    panel_path = tmp_path / "marker_genes.tsv"
    _annotate_panel(monkeypatch, arguments)
    first_pass = panel_path.read_bytes()

    _annotate_panel(monkeypatch, arguments)

    assert panel_path.read_bytes() == first_pass
