"""Tests for the gene module helper."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from nasp_compendium import GeneModules


class FakeAnnData:
    """AnnData-like object for marker-gene validation tests."""

    def __init__(self, var: pd.DataFrame) -> None:
        """Store var metadata and var_names."""
        self._var = var

    @property
    def var(self) -> pd.DataFrame:
        """Return variable metadata."""
        return self._var

    @property
    def var_names(self) -> pd.Index[Any]:
        """Return variable names."""
        return self._var.index


def _write_marker_panel(path: Path) -> None:
    """Write a minimal marker-gene panel for tests."""
    path.write_text(
        "\n".join(
            [
                "gene_symbol\tmodule_id\tscoring_direction",
                "CGAS\tNASP_DNA_SENSING\tpositive",
                "STING1\tNASP_DNA_SENSING\tPositive",
                "LMNB1\tNASP_DNA_SENSING\tinverse",
                "IFI16\tNASP_DNA_SENSING\tcontext_dependent",
                "DDX58\tNASP_RNA_SENSING\tpositive",
            ]
        )
        + "\n"
    )


def test_modules_resolves_suffix_and_splits_signed_genes(
    tmp_path: Path,
) -> None:
    """Module helper resolves suffixes and splits signed marker genes."""
    panel_path = tmp_path / "marker_genes.tsv"
    _write_marker_panel(panel_path)

    module = GeneModules.modules(
        module="dna_sensing",
        scorer="scanpy",
        panel_path=panel_path,
    )

    assert module.module_id == "NASP_DNA_SENSING"
    assert module.positive_genes == ("CGAS", "STING1")
    assert module.inverse_genes == ("LMNB1",)
    assert module.context_dependent_genes == ("IFI16",)
    assert module.positive_score_name == "NASP_DNA_SENSING_pos"
    assert module.inverse_score_name == "NASP_DNA_SENSING_inv"
    assert module.score_name == "NASP_DNA_SENSING_score"


def test_genes_returns_all_module_genes_by_default(tmp_path: Path) -> None:
    """Plain gene extraction returns all module genes in panel order."""
    panel_path = tmp_path / "marker_genes.tsv"
    _write_marker_panel(panel_path)

    genes = GeneModules.genes(module="dna_sensing", panel_path=panel_path)

    assert genes == ["CGAS", "STING1", "LMNB1", "IFI16"]


def test_modules_maps_symbols_to_var_names_for_scanpy(
    tmp_path: Path,
) -> None:
    """Validated Scanpy modules return matched var_names and missing genes."""
    panel_path = tmp_path / "marker_genes.tsv"
    _write_marker_panel(panel_path)
    adata = FakeAnnData(
        pd.DataFrame(
            {"gene_symbol": ["CGAS", "STING1", "DDX58"]},
            index=["ENSG_CGAS", "ENSG_STING1", "ENSG_DDX58"],
        )
    )

    module = GeneModules.modules(
        module="dna_sensing",
        scorer="scanpy",
        panel_path=panel_path,
        adata=adata,
    )

    assert module.gene_id_output == "var_names"
    assert module.positive_genes == ("ENSG_CGAS", "ENSG_STING1")
    assert module.inverse_genes == ()
    assert module.missing_inverse_genes == ("LMNB1",)
    assert module.missing_context_dependent_genes == ("IFI16",)


def test_validate_dataset_reports_symbol_column_matches(
    tmp_path: Path,
) -> None:
    """Validation reports present and missing genes with match metadata."""
    panel_path = tmp_path / "marker_genes.tsv"
    _write_marker_panel(panel_path)
    adata = FakeAnnData(
        pd.DataFrame(
            {"gene_symbol": ["CGAS", "STING1", "DDX58"]},
            index=["ENSG_CGAS", "ENSG_STING1", "ENSG_DDX58"],
        )
    )

    validation = GeneModules.validate_dataset(
        adata,
        panel_path=panel_path,
        module="dna_sensing",
    )

    validation_by_gene = validation.set_index("gene_symbol")
    assert bool(validation_by_gene.loc["CGAS", "present"])
    assert validation_by_gene.loc["CGAS", "matched_var_name"] == "ENSG_CGAS"
    assert validation_by_gene.loc["CGAS", "match_source"] == "var.gene_symbol"
    assert not bool(validation_by_gene.loc["LMNB1", "present"])
