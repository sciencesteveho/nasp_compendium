"""Tests for the gene module helper."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from nasp_compendium import GeneModules
from nasp_compendium import gene_modules
from nasp_compendium import render_docs
from nasp_compendium.visualization import gene_modules as viz_gene_modules


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


def _write_sensor_panel(path: Path) -> None:
    """Write a marker-gene panel with sensor annotations for tests."""
    path.write_text(
        "\n".join(
            [
                "gene_symbol\tmodule_id\tscoring_direction\tsensor",
                "CGAS\tNASP_DNA_SENSING\tpositive\tdna_sensor",
                "DDX58\tNASP_RNA_SENSING\tpositive\trna_sensor",
                "DDX41\tNASP_DNA_SENSING\tpositive\tdna_sensor; rna_sensor",
                "NLRP3\tINFLAMMASOME\tpositive\tinflammasome_sensor",
                "MRE11\tNASP_DNA_SENSING\tpositive\tdna_damage_sensor",
                "JMJD6\tNASP_DNA_SENSING\tpositive\tconfirmed",
                "CGAS\tSIGNALING_CONTEXT\tpositive\tdna_sensor",
            ]
        )
        + "\n"
    )


def _write_overlap_panel(path: Path) -> None:
    """Write a minimal marker-gene panel with cross-module overlaps."""
    path.write_text(
        "\n".join(
            [
                "gene_symbol\tmodule_id",
                "A\tMODULE_ONE",
                "B\tMODULE_ONE",
                "B\tMODULE_TWO",
                "C\tMODULE_TWO",
                "C\tMODULE_THREE",
                "D\tMODULE_THREE",
                "D\tMODULE_THREE",
            ]
        )
        + "\n"
    )


def test_default_panel_path_loads_repo_marker_genes() -> None:
    """Default catalog loads the repo-bundled marker genes."""
    catalog = GeneModules()

    assert catalog.panel_path.name == "marker_genes.tsv"
    assert catalog.panel_path.exists()
    assert "NASP_DNA_SENSING" in catalog.module_ids()


def test_default_panel_uses_repo_data_not_legacy_package_data(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Repo-level marker data is canonical when both locations exist."""
    package_root = tmp_path / "nasp_compendium"
    package_data_dir = package_root / "data"
    package_data_dir.mkdir(parents=True)
    _write_sensor_panel(package_data_dir / "marker_genes.tsv")

    repo_data_dir = tmp_path / "data"
    repo_data_dir.mkdir()
    _write_marker_panel(repo_data_dir / "marker_genes.tsv")

    monkeypatch.setattr(
        gene_modules,
        "__file__",
        str(package_root / "gene_modules.py"),
    )

    catalog = GeneModules()

    assert catalog.module_ids() == ["NASP_DNA_SENSING", "NASP_RNA_SENSING"]


def test_default_panel_loads_packaged_data_file(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Installed packages can load the bundled marker-gene data file."""
    install_root = tmp_path / "target"
    package_root = install_root / "nasp_compendium"
    package_root.mkdir(parents=True)
    installed_data_dir = install_root / "share" / "nasp_compendium" / "data"
    installed_data_dir.mkdir(parents=True)
    _write_marker_panel(installed_data_dir / "marker_genes.tsv")

    class FakeDistribution:
        """Distribution metadata for an installed package."""

        def locate_file(self, path: str) -> Path:
            """Resolve a distribution-relative path."""
            return install_root / path

        def read_text(self, name: str) -> str | None:
            """Return no local source-tree metadata."""
            assert name == "direct_url.json"
            return None

    def fake_distribution(name: str) -> FakeDistribution:
        """Return fake distribution metadata for nasp_compendium."""
        assert name == "nasp_compendium"
        return FakeDistribution()

    monkeypatch.setattr(
        gene_modules,
        "__file__",
        str(package_root / "gene_modules.py"),
    )
    monkeypatch.setattr(gene_modules.sys, "prefix", str(tmp_path / "env"))
    monkeypatch.setattr(
        gene_modules.metadata,
        "distribution",
        fake_distribution,
    )

    assert GeneModules().module_ids() == [
        "NASP_DNA_SENSING",
        "NASP_RNA_SENSING",
    ]


def test_module_gene_overlap_matrix_counts_intersections(
    tmp_path: Path,
) -> None:
    """Overlap matrix counts shared genes and grays the self diagonal."""
    panel_path = tmp_path / "marker_genes.tsv"
    _write_overlap_panel(panel_path)

    overlap = viz_gene_modules.module_gene_overlap_matrix(panel_path)

    assert overlap.index.tolist() == [
        "MODULE_ONE",
        "MODULE_THREE",
        "MODULE_TWO",
    ]
    assert overlap.loc["MODULE_ONE", "MODULE_ONE"] == 0
    assert overlap.loc["MODULE_ONE", "MODULE_TWO"] == 1
    assert overlap.loc["MODULE_TWO", "MODULE_THREE"] == 1
    assert overlap.loc["MODULE_ONE", "MODULE_THREE"] == 0


def test_module_gene_overlap_matrix_can_include_self_counts(
    tmp_path: Path,
) -> None:
    """Overlap matrix can keep module gene counts on the diagonal."""
    panel_path = tmp_path / "marker_genes.tsv"
    _write_overlap_panel(panel_path)

    overlap = viz_gene_modules.module_gene_overlap_matrix(
        panel_path,
        include_self=True,
    )

    assert overlap.loc["MODULE_THREE", "MODULE_THREE"] == 2


def test_render_index_embeds_overlap_heatmap() -> None:
    """Marker-gene README can include the shared-gene overlap heatmap."""
    markdown = render_docs.render_index(
        ["NASP_DNA_SENSING"],
        figure_relpath="assets/taxonomy_class_barplot.png",
        overlap_figure_relpath="assets/module_gene_overlap_heatmap.png",
    )

    assert "![Module taxonomy](assets/taxonomy_class_barplot.png)" in markdown
    assert (
        "![Inter-module shared-gene overlaps]"
        "(assets/module_gene_overlap_heatmap.png)"
    ) in markdown


def _write_docs_panel(path: Path) -> None:
    """Write a marker panel with every column the docs renderer requires."""
    header = (
        "gene_symbol\tmodule_id\tmodule_class\tsensor_family\tactivation_tier"
        "\tscoring_direction\tcell_type_breadth\tdetectability\talso_in_module"
        "\tdoi\taliases\tsensor\tpanel_source"
    )
    rows = [
        ("CDKN1A", "AGING_HALLMARKS", "senescence_marker", ""),
        ("AIM2", "INFLAMMASOME", "inflammasome_sensor", "dna_sensor"),
        ("NLRP3", "INFLAMMASOME", "inflammasome_sensor", "inflammasome_sensor"),
        ("CGAS", "NASP_DNA_SENSING", "dna_sensing_core", "dna_sensor"),
        ("DDX58", "NASP_RNA_SENSING", "rna_sensing_core", "rna_sensor"),
    ]
    lines = [
        f"{gene}\t{module}\t{module_class}\t\tEarly\tpositive\tBroad\tlow\t\t\t"
        f"\t{sensor}\t"
        for gene, module, module_class, sensor in rows
    ]
    path.write_text("\n".join([header, *lines]) + "\n")


def test_render_docs_lists_na_sensor_page_first(tmp_path: Path) -> None:
    """The docs index links the All NA sensors page ahead of every module."""
    panel_path = tmp_path / "marker_genes.tsv"
    _write_docs_panel(panel_path)
    docs_dir = tmp_path / "docs"

    render_docs.render_docs(panel_path, docs_dir)

    index = (docs_dir / "index.md").read_text()
    first_link = next(
        line for line in index.splitlines() if line.startswith("- [")
    )
    label, target = first_link.removeprefix("- [").removesuffix(")").split("](")
    assert label == "All NA sensors"
    assert (docs_dir / target).read_text().startswith("# All NA sensors\n")


def test_na_sensor_page_lists_only_dna_and_rna_sensors(tmp_path: Path) -> None:
    """The All NA sensors page spans modules and omits non-NA sensors."""
    panel_path = tmp_path / "marker_genes.tsv"
    _write_docs_panel(panel_path)
    docs_dir = tmp_path / "docs"

    render_docs.render_docs(panel_path, docs_dir)

    sensor_page = next(
        page.read_text()
        for page in docs_dir.glob("*.md")
        if page.read_text().startswith("# All NA sensors\n")
    )
    table_rows = [
        line
        for line in sensor_page.splitlines()
        if line.startswith("| ") and not line.startswith(("| Gene ", "| --- "))
    ]
    listed_genes = {row.split("|")[1].strip() for row in table_rows}
    assert listed_genes == {"AIM2", "CGAS", "DDX58"}


def test_module_page_shows_every_panel_field(tmp_path: Path) -> None:
    """A module page row carries each of the gene's TSV values."""
    panel = pd.DataFrame(
        {
            "gene_symbol": ["CGAS"],
            "hgnc_id": ["HGNC:21367"],
            "module_id": ["NASP_DNA_SENSING"],
            "module_class": ["dna_sensing_core"],
            "sensor_family": ["cGAS-STING"],
            "activation_tier": ["Early"],
            "scoring_direction": ["positive"],
            "cell_type_breadth": ["Broad"],
            "detectability": ["low"],
            "also_in_module": ["SENESCENCE"],
            "doi": [""],
            "aliases": ["MB21D1"],
            "sensor": ["dna_sensor"],
            "panel_source": ["curated"],
            "s_het_mean": ["0.00114308"],
            "curator_note": ["checked"],
        }
    )
    panel_path = tmp_path / "marker_genes.tsv"
    panel.to_csv(panel_path, sep="\t", index=False)
    docs_dir = tmp_path / "docs"

    render_docs.render_docs(panel_path, docs_dir)

    module_page = (docs_dir / "nasp_dna_sensing.md").read_text()
    cgas_cells = next(
        {cell.strip() for cell in line.split("|")}
        for line in module_page.splitlines()
        if line.startswith("| CGAS ")
    )
    expected = set(panel.drop(columns="module_id").iloc[0]) - {""}
    assert expected <= cgas_cells


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
    assert not bool(validation_by_gene.loc["LMNB1", "present"])


def test_sensors_filter_sensor_column_tokens(tmp_path: Path) -> None:
    """Sensor helper filters exact DNA/RNA tags and all sensor-like tags."""
    panel_path = tmp_path / "marker_genes.tsv"
    _write_sensor_panel(panel_path)

    assert GeneModules.sensors("rna", panel_path=panel_path) == [
        "DDX58",
        "DDX41",
    ]
    assert GeneModules.sensors("dna", panel_path=panel_path) == [
        "CGAS",
        "DDX41",
    ]
    assert GeneModules.sensors("dna_rna", panel_path=panel_path) == [
        "CGAS",
        "DDX58",
        "DDX41",
    ]
    assert GeneModules.sensors("all", panel_path=panel_path) == [
        "CGAS",
        "DDX58",
        "DDX41",
        "NLRP3",
        "MRE11",
    ]


def test_sensors_support_aliases_and_module_filter(tmp_path: Path) -> None:
    """Sensor helper supports user-facing aliases and module scoping."""
    panel_path = tmp_path / "marker_genes.tsv"
    _write_sensor_panel(panel_path)
    catalog = GeneModules.from_tsv(panel_path)

    assert catalog.get_sensors("dna + rna") == ["CGAS", "DDX58", "DDX41"]
    assert catalog.get_sensors("all", module="inflammasome") == ["NLRP3"]
    assert catalog.get_sensors("dna", module="dna_sensing") == [
        "CGAS",
        "DDX41",
    ]


def test_sensors_can_return_matched_var_names(tmp_path: Path) -> None:
    """Sensor helper can validate sensors against AnnData-like var metadata."""
    panel_path = tmp_path / "marker_genes.tsv"
    _write_sensor_panel(panel_path)
    adata = FakeAnnData(
        pd.DataFrame(
            {"gene_symbol": ["CGAS", "NLRP3"]},
            index=["ENSG_CGAS", "ENSG_NLRP3"],
        )
    )

    sensors = GeneModules.sensors(
        "all",
        panel_path=panel_path,
        adata=adata,
        output="var_names",
    )

    assert sensors == ["ENSG_CGAS", "ENSG_NLRP3"]
