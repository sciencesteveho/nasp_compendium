"""Helper for extracting and validating marker-gene modules."""

from __future__ import annotations

import dataclasses
from collections.abc import Iterable
from pathlib import Path
from typing import Any, ClassVar

import pandas as pd

from nasp_compendium.types import AnnDataLike
from nasp_compendium.types import GeneIdOutput
from nasp_compendium.types import GeneModule
from nasp_compendium.types import ScorerName


@dataclasses.dataclass(frozen=True)
class _GeneMatch:
    """Resolved dataset match for one marker gene."""

    gene_symbol: str
    var_name: str
    match_source: str


class GeneModules:
    """Loads and validates marker-gene modules for scoring.

    Derives signed gene sets directly from the marker gene tsv, provides
    utilities to validate names against a dataset, and returns arguments to drop
    into sc.tl.score_genes or AUCell.

    For positive-only modules combine_scores returns the positive score alone;
    for inverse-only modules it returns the negated inverse score.

    Entry points:
      genes(module): flat gene list for expression plots
      modules(module, scorer): a GeneModule with signed sets and score names
      validate_dataset(adata, module): per-gene dataset-coverage DataFrame

    Scoring backends:
      "scanpy": score the positive and inverse sets with sc.tl.score_genes, then
        subtract via combine_scores
      "aucell": run AUCell (via pySCENIC) on the named gene_sets, then subtract
        the AUCs via combine_scores

    Attributes:
      panel_path: Path to the marker-gene TSV that was loaded
      panel: Normalized marker-gene panel as a DataFrame

    Examples:
      >>> import scanpy as sc
      >>> from nasp_compendium import GeneModules

      List modules
      >>> GeneModules().module_ids()

      Pull genes for a multi-panel UMAP
      >>> genes = GeneModules.genes("dna_sensing")
      >>> positive_genes = GeneModules.genes("dna_sensing",
      ...   directions=["positive"])
      >>> nucleic_acid_sensors = GeneModules.sensors("dna_rna")
      >>> all_sensors = GeneModules.sensors("all")

      Scanpy scoring
      >>> module = GeneModules.modules("dna_sensing", scorer="scanpy")
      >>> module.score_name
      ...   'NASP_DNA_SENSING_score'
      >>> for kwargs in module.scanpy_score_kwargs(random_state=0):
      ...   sc.tl.score_genes(adata, **kwargs)
      >>> adata.obs[module.score_name] = module.combine_scores(adata.obs)

      Validate against a dataset and map symbols to its var_names.
      >>> coverage = GeneModules.validate_dataset(adata, module="dna_sensing")
      >>> matched = GeneModules.modules("dna_sensing", adata=adata)
      >>> matched.gene_id_output
      ...   'var_names'
      >>> missing = matched.missing_positive_genes

      AUCell scoring on the same module.
      >>> auc = GeneModules.modules("dna_sensing", scorer="aucell")
      >>> gene_sets = auc.gene_sets()
      >>> signed = auc.combine_scores(auc_df)

      User-supplied panel via an instance.
      >>> catalog = GeneModules.from_tsv("my_panel.tsv")
      >>> custom_genes = catalog.get_genes("dna_sensing")
      >>> spec = catalog.get_module("dna_sensing").as_dict()
    """

    DEFAULT_PANEL_PATH: ClassVar[Path] = (
        Path(__file__).resolve().parent.parent / "data" / "marker_genes.tsv"
    )
    REQUIRED_COLUMNS: ClassVar[frozenset[str]] = frozenset(
        {"gene_symbol", "module_id", "scoring_direction"}
    )
    SENSOR_COLUMN: ClassVar[str] = "sensor"
    VALID_SCORERS: ClassVar[frozenset[str]] = frozenset({"scanpy", "aucell"})
    SENSOR_FILTER_ALIASES: ClassVar[dict[str, str]] = {
        "all": "all",
        "all_sensors": "all",
        "dna": "dna",
        "dna_sensor": "dna",
        "dna_sensors": "dna",
        "rna": "rna",
        "rna_sensor": "rna",
        "rna_sensors": "rna",
        "dna_rna": "dna_rna",
        "dna+rna": "dna_rna",
        "dna + rna": "dna_rna",
        "dna_and_rna": "dna_rna",
        "nucleic_acid": "dna_rna",
        "nucleic_acid_sensors": "dna_rna",
    }
    SCORING_DIRECTIONS: ClassVar[frozenset[str]] = frozenset(
        {"positive", "inverse"}
    )
    SIGNED_DIRECTIONS: ClassVar[frozenset[str]] = frozenset(
        {"positive", "inverse", "context_dependent"}
    )
    GENE_SYMBOL_COLUMNS: ClassVar[tuple[str, ...]] = (
        "gene_symbol",
        "gene_symbols",
        "symbol",
        "gene_name",
        "gene_names",
        "feature_name",
        "features",
    )

    def __init__(
        self,
        panel_path: str | Path | None = None,
        *,
        encoding: str = "utf-8",
    ) -> None:
        """Load marker-gene modules from a TSV file.

        Args:
          panel_path: Path to a marker-gene TSV. Defaults to
            `data/marker_genes.tsv`.
          encoding: Text encoding for the TSV.
        """
        self.panel_path = Path(panel_path or self.DEFAULT_PANEL_PATH)
        self.panel = self._load_panel(self.panel_path, encoding=encoding)

    @classmethod
    def from_tsv(
        cls,
        panel_path: str | Path,
        *,
        encoding: str = "utf-8",
    ) -> GeneModules:
        """Create a module catalog from a user-provided TSV path."""
        return cls(panel_path=panel_path, encoding=encoding)

    @classmethod
    def modules(
        cls,
        module: str,
        scorer: ScorerName = "scanpy",
        *,
        panel_path: str | Path | None = None,
        adata: AnnDataLike | None = None,
        gene_symbol_column: str | None = None,
        output: GeneIdOutput | None = None,
        strict: bool = False,
    ) -> GeneModule:
        """Return signed gene lists for one module.

        Args:
          module: Module id or suffix.
          scorer: Scoring backend name used to choose score-name suffixes.
          panel_path: Optional user-provided marker-gene TSV.
          adata: Optional AnnData-like object for dataset validation.
          gene_symbol_column: Optional `adata.var` column with gene symbols.
          output: Return matched module genes as source symbols or var names.
          strict: Raise if any marker gene is absent from `adata`.

        Returns:
          A `GeneModule` containing positive and inverse gene lists.
        """
        return cls(panel_path=panel_path).get_module(
            module=module,
            scorer=scorer,
            adata=adata,
            gene_symbol_column=gene_symbol_column,
            output=output,
            strict=strict,
        )

    @classmethod
    def genes(
        cls,
        module: str,
        *,
        panel_path: str | Path | None = None,
        adata: AnnDataLike | None = None,
        gene_symbol_column: str | None = None,
        output: GeneIdOutput = "symbols",
        directions: Iterable[str] | None = None,
        strict: bool = False,
    ) -> list[str]:
        """Return genes for one module as a simple list.

        Args:
          module: Module id or suffix.
          panel_path: Optional user-provided marker-gene TSV.
          adata: Optional AnnData-like object for dataset validation.
          gene_symbol_column: Optional `adata.var` column with gene symbols.
          output: Return source symbols or matched `adata.var_names`.
          directions: Optional scoring directions to keep.
          strict: Raise if any selected marker gene is absent from `adata`.

        Returns:
          Ordered marker genes for downstream visualization or analysis.
        """
        return cls(panel_path=panel_path).get_genes(
            module=module,
            adata=adata,
            gene_symbol_column=gene_symbol_column,
            output=output,
            directions=directions,
            strict=strict,
        )

    @classmethod
    def sensors(
        cls,
        sensor_type: str = "all",
        *,
        panel_path: str | Path | None = None,
        module: str | None = None,
        adata: AnnDataLike | None = None,
        gene_symbol_column: str | None = None,
        output: GeneIdOutput = "symbols",
        strict: bool = False,
    ) -> list[str]:
        """Return annotated sensors.

        Args:
          sensor_type: Sensor filter. Use `rna`, `dna`, `dna_rna` for the union
            of DNA and RNA sensors, or `all` for any `*_sensor` annotation.
          panel_path: Optional user-provided marker-gene TSV.
          module: Optional module id or suffix to restrict the sensor search.
          adata: Optional AnnData-like object for dataset validation.
          gene_symbol_column: Optional `adata.var` column with gene symbols.
          output: Return source symbols or matched `adata.var_names`.
          strict: Raise if any selected marker gene is absent from `adata`.

        Returns:
          Ordered sensor genes for downstream visualization or analysis.
        """
        return cls(panel_path=panel_path).get_sensors(
            sensor_type=sensor_type,
            module=module,
            adata=adata,
            gene_symbol_column=gene_symbol_column,
            output=output,
            strict=strict,
        )

    @classmethod
    def validate_dataset(
        cls,
        adata: AnnDataLike,
        *,
        panel_path: str | Path | None = None,
        module: str | None = None,
        gene_symbol_column: str | None = None,
    ) -> pd.DataFrame:
        """Validate marker genes against a single-cell dataset."""
        return cls(panel_path=panel_path).validate(
            adata=adata,
            module=module,
            gene_symbol_column=gene_symbol_column,
        )

    def get_module(
        self,
        module: str,
        scorer: ScorerName = "scanpy",
        *,
        adata: AnnDataLike | None = None,
        gene_symbol_column: str | None = None,
        output: GeneIdOutput | None = None,
        strict: bool = False,
    ) -> GeneModule:
        """Return signed gene lists for one module from this catalog."""
        self._validate_scorer(scorer)
        resolved_output = self._resolve_output(
            output, scorer=scorer, adata=adata
        )
        module_id = self.resolve_module_id(module)
        module_panel = self._module_panel(module_id)

        validation = self._validation_for_module(
            module_panel=module_panel,
            adata=adata,
            gene_symbol_column=gene_symbol_column,
            strict=strict,
        )

        positive_genes, missing_positive_genes = self._genes_by_direction(
            validation=validation,
            direction="positive",
            output=resolved_output,
            adata=adata,
        )
        inverse_genes, missing_inverse_genes = self._genes_by_direction(
            validation=validation,
            direction="inverse",
            output=resolved_output,
            adata=adata,
        )
        context_genes, missing_context_genes = self._genes_by_direction(
            validation=validation,
            direction="context_dependent",
            output=resolved_output,
            adata=adata,
        )

        if adata is not None and not positive_genes and not inverse_genes:
            raise ValueError(
                f"No scorable marker genes from {module_id} were found in "
                "the dataset."
            )

        return GeneModule(
            module_id=module_id,
            scorer=scorer,
            positive_genes=positive_genes,
            inverse_genes=inverse_genes,
            context_dependent_genes=context_genes,
            gene_id_output=resolved_output,
            missing_positive_genes=missing_positive_genes,
            missing_inverse_genes=missing_inverse_genes,
            missing_context_dependent_genes=missing_context_genes,
        )

    def get_genes(
        self,
        module: str,
        *,
        adata: AnnDataLike | None = None,
        gene_symbol_column: str | None = None,
        output: GeneIdOutput = "symbols",
        directions: Iterable[str] | None = None,
        strict: bool = False,
    ) -> list[str]:
        """Return selected marker genes from one module."""
        module_id = self.resolve_module_id(module)
        module_panel = self._module_panel(module_id)
        selected_directions = self._normalize_directions(directions)
        if selected_directions is not None:
            module_panel = module_panel[
                module_panel["scoring_direction"].isin(selected_directions)
            ]

        validation = self._validation_for_module(
            module_panel=module_panel,
            adata=adata,
            gene_symbol_column=gene_symbol_column,
            strict=strict,
        )
        if adata is None:
            return self._dedupe_preserving_order(
                validation["gene_symbol"].tolist()
            )

        matched = validation[validation["present"]].copy()
        output_column = self._output_column(output)
        return self._dedupe_preserving_order(matched[output_column].tolist())

    def get_sensors(
        self,
        sensor_type: str = "all",
        *,
        module: str | None = None,
        adata: AnnDataLike | None = None,
        gene_symbol_column: str | None = None,
        output: GeneIdOutput = "symbols",
        strict: bool = False,
    ) -> list[str]:
        """Return selected sensor genes from this catalog.

        `dna_rna` returns genes tagged as either `dna_sensor` or `rna_sensor`.
        `all` returns genes with any token ending in `_sensor`, including misc
        sensor classes such as inflammasome, LPS, or metabolite sensors.
        """
        panel = self.panel
        if module is not None:
            module_id = self.resolve_module_id(module)
            panel = self._module_panel(module_id)

        sensor_panel = self._sensor_panel(panel, sensor_type=sensor_type)
        validation = self._validation_for_module(
            module_panel=sensor_panel,
            adata=adata,
            gene_symbol_column=gene_symbol_column,
            strict=strict,
        )
        if adata is None:
            return self._dedupe_preserving_order(
                validation["gene_symbol"].tolist()
            )

        matched = validation[validation["present"]].copy()
        output_column = self._output_column(output)
        return self._dedupe_preserving_order(matched[output_column].tolist())

    def validate(
        self,
        adata: AnnDataLike,
        *,
        module: str | None = None,
        gene_symbol_column: str | None = None,
    ) -> pd.DataFrame:
        """Validate marker genes against an AnnData-like object.

        Args:
          adata: AnnData-like object with `var` and `var_names`.
          module: Optional module id or suffix to restrict validation.
          gene_symbol_column: Optional `adata.var` column with gene symbols.

        Returns:
          DataFrame with one row per marker gene and match metadata.
        """
        panel = self.panel
        if module is not None:
            module_id = self.resolve_module_id(module)
            panel = self._module_panel(module_id)
        return self._validation_for_module(
            module_panel=panel,
            adata=adata,
            gene_symbol_column=gene_symbol_column,
            strict=False,
        )

    def module_ids(self) -> list[str]:
        """Return sorted module ids present in the marker panel."""
        return sorted(self.panel["module_id"].unique().tolist())

    def resolve_module_id(self, module: str) -> str:
        """Resolve a module id or suffix to a canonical panel module_id."""
        query = self._normalize_module_id(module)
        module_ids = self.module_ids()
        normalized_module_ids = {
            self._normalize_module_id(module_id): module_id
            for module_id in module_ids
        }

        if query in normalized_module_ids:
            return normalized_module_ids[query]

        suffix_matches = [
            module_id
            for module_id in module_ids
            if self._normalize_module_id(module_id).endswith(f"_{query}")
        ]
        if len(suffix_matches) == 1:
            return suffix_matches[0]
        if len(suffix_matches) > 1:
            candidates = ", ".join(suffix_matches)
            raise ValueError(
                f"Module name '{module}' is ambiguous. Matches: {candidates}"
            )

        available = ", ".join(module_ids)
        raise ValueError(
            f"No module found for '{module}'. Available modules: {available}"
        )

    @classmethod
    def _load_panel(cls, panel_path: Path, *, encoding: str) -> pd.DataFrame:
        """Load and normalize a marker-gene panel TSV."""
        if not panel_path.exists():
            raise FileNotFoundError(f"Marker-gene TSV not found: {panel_path}")

        panel = pd.read_csv(panel_path, sep="\t", dtype=str, encoding=encoding)
        if missing_columns := cls.REQUIRED_COLUMNS.difference(panel.columns):
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(
                f"Marker-gene TSV is missing required columns: {missing}"
            )

        panel = panel.copy()
        for column in cls.REQUIRED_COLUMNS:
            panel[column] = panel[column].fillna("").str.strip()
        if cls.SENSOR_COLUMN not in panel.columns:
            panel[cls.SENSOR_COLUMN] = ""
        else:
            panel[cls.SENSOR_COLUMN] = (
                panel[cls.SENSOR_COLUMN].fillna("").str.strip()
            )

        panel = panel[
            (panel["gene_symbol"] != "") & (panel["module_id"] != "")
        ].copy()
        panel["scoring_direction"] = (
            panel["scoring_direction"].str.lower().str.strip()
        )
        panel = panel.drop_duplicates(
            subset=["gene_symbol", "module_id", "scoring_direction"]
        )

        if invalid_directions := sorted(
            set(panel["scoring_direction"])
            - {"", "positive", "inverse", "context_dependent"}
        ):
            invalid = ", ".join(invalid_directions)
            raise ValueError(f"Invalid scoring_direction values: {invalid}")

        cls._check_direction_conflicts(panel)
        return panel.reset_index(drop=True)

    @classmethod
    def _check_direction_conflicts(cls, panel: pd.DataFrame) -> None:
        """Raise if a gene carries conflicting directions within a module.

        A gene that appears in one module under more than one signed
        direction (for example both positive and inverse) is a curation
        error that would silently corrupt a module score.

        Raises:
          ValueError: If any (module_id, gene_symbol) pair maps to more than
            one distinct signed direction.
        """
        directions_by_gene: dict[tuple[str, str], set[str]] = {}
        for module_id, gene_symbol, direction in zip(
            panel["module_id"],
            panel["gene_symbol"],
            panel["scoring_direction"],
            strict=True,
        ):
            direction_text = str(direction)
            if direction_text not in cls.SIGNED_DIRECTIONS:
                continue
            key = (str(module_id), str(gene_symbol))
            directions_by_gene.setdefault(key, set()).add(direction_text)

        if conflicts := sorted(
            f"{gene_symbol} in {module_id}"
            for (module_id, gene_symbol), directions in (
                directions_by_gene.items()
            )
            if len(directions) > 1
        ):
            details = "; ".join(conflicts)
            raise ValueError(
                f"Genes with conflicting scoring directions: {details}"
            )

    def _module_panel(self, module_id: str) -> pd.DataFrame:
        """Return panel rows for a resolved module id."""
        return self.panel[self.panel["module_id"] == module_id].reset_index(
            drop=True
        )

    def _sensor_panel(
        self,
        panel: pd.DataFrame,
        *,
        sensor_type: str,
    ) -> pd.DataFrame:
        """Return panel rows matching a sensor annotation filter."""
        resolved_sensor_type = self._normalize_sensor_type(sensor_type)
        selected = [
            self._sensor_matches(value, sensor_type=resolved_sensor_type)
            for value in panel[self.SENSOR_COLUMN].tolist()
        ]
        mask = pd.Series(selected, index=panel.index, dtype=bool)
        return panel.loc[mask].reset_index(drop=True)

    @classmethod
    def _normalize_sensor_type(cls, sensor_type: str) -> str:
        """Normalize a public sensor filter option."""
        normalized = sensor_type.strip().lower().replace("-", "_")
        if normalized in cls.SENSOR_FILTER_ALIASES:
            return cls.SENSOR_FILTER_ALIASES[normalized]

        valid = ", ".join(["all", "dna", "dna_rna", "rna"])
        raise ValueError(
            f"Unsupported sensor_type '{sensor_type}'. Use one of {valid}."
        )

    @classmethod
    def _sensor_matches(cls, value: Any, *, sensor_type: str) -> bool:
        """Return whether one `sensor` cell matches the requested filter."""
        tokens = cls._sensor_tokens(value)
        if sensor_type == "all":
            return any(token.endswith("_sensor") for token in tokens)
        if sensor_type == "dna":
            return "dna_sensor" in tokens
        if sensor_type == "rna":
            return "rna_sensor" in tokens
        if sensor_type == "dna_rna":
            return bool(tokens.intersection({"dna_sensor", "rna_sensor"}))
        raise ValueError(f"Unsupported normalized sensor_type: {sensor_type}")

    @staticmethod
    def _sensor_tokens(value: Any) -> set[str]:
        """Return normalized semicolon-separated sensor tokens."""
        if pd.isna(value):
            return set()
        return {
            token.strip().lower()
            for token in str(value).split(";")
            if token.strip()
        }

    def _validation_for_module(
        self,
        *,
        module_panel: pd.DataFrame,
        adata: AnnDataLike | None,
        gene_symbol_column: str | None,
        strict: bool,
    ) -> pd.DataFrame:
        """Return validation rows for selected panel rows."""
        validation = module_panel[
            ["module_id", "gene_symbol", "scoring_direction"]
        ].copy()
        validation["matched_gene_symbol"] = validation["gene_symbol"]
        validation["matched_var_name"] = validation["gene_symbol"]
        validation["match_source"] = "panel"
        validation["match_count"] = 0
        validation["present"] = adata is None

        if adata is None:
            return validation

        lookup = self._build_gene_lookup(
            adata=adata,
            gene_symbol_column=gene_symbol_column,
        )
        records: list[dict[str, Any]] = []
        missing_genes: list[str] = []
        for raw_row in validation.to_dict(orient="records"):
            row = {str(key): value for key, value in raw_row.items()}
            gene_symbol = str(row["gene_symbol"])
            if matches := self._lookup_gene(gene_symbol, lookup):
                first_match = matches[0]
                row["matched_gene_symbol"] = first_match.gene_symbol
                row["matched_var_name"] = first_match.var_name
                row["match_source"] = first_match.match_source
                row["match_count"] = len(matches)
                row["present"] = True
            else:
                row["matched_gene_symbol"] = pd.NA
                row["matched_var_name"] = pd.NA
                row["match_source"] = pd.NA
                row["match_count"] = 0
                row["present"] = False
                missing_genes.append(gene_symbol)

            records.append(row)

        if strict and missing_genes:
            missing = ", ".join(missing_genes)
            raise ValueError(f"Marker genes not found in dataset: {missing}")

        return pd.DataFrame.from_records(records)

    @classmethod
    def _build_gene_lookup(
        cls,
        *,
        adata: AnnDataLike,
        gene_symbol_column: str | None,
    ) -> dict[str, list[_GeneMatch]]:
        """Build lookup maps for dataset genes."""
        var = adata.var
        var_names = pd.Index(adata.var_names).astype(str)
        if len(var_names) != len(var):
            raise ValueError("adata.var_names length does not match adata.var.")

        symbol_columns = cls._resolve_gene_symbol_columns(
            var=var,
            gene_symbol_column=gene_symbol_column,
        )
        lookup: dict[str, list[_GeneMatch]] = {}

        for column in symbol_columns:
            symbols = var[column]
            for var_name, symbol in zip(var_names, symbols, strict=True):
                if pd.isna(symbol):
                    continue
                cls._add_gene_match(
                    lookup=lookup,
                    key=str(symbol).strip(),
                    match=_GeneMatch(
                        gene_symbol=str(symbol).strip(),
                        var_name=str(var_name),
                        match_source=f"var.{column}",
                    ),
                )

        for var_name in var_names:
            cls._add_gene_match(
                lookup=lookup,
                key=str(var_name),
                match=_GeneMatch(
                    gene_symbol=str(var_name),
                    var_name=str(var_name),
                    match_source="var_names",
                ),
            )

        return lookup

    @classmethod
    def _resolve_gene_symbol_columns(
        cls,
        *,
        var: pd.DataFrame,
        gene_symbol_column: str | None,
    ) -> list[str]:
        """Return dataset symbol columns to search before var_names."""
        if gene_symbol_column is not None:
            if gene_symbol_column not in var.columns:
                raise ValueError(
                    f"Gene symbol column not found in adata.var: "
                    f"{gene_symbol_column}"
                )
            return [gene_symbol_column]

        return [
            column
            for column in cls.GENE_SYMBOL_COLUMNS
            if column in var.columns
        ]

    @staticmethod
    def _add_gene_match(
        *,
        lookup: dict[str, list[_GeneMatch]],
        key: str,
        match: _GeneMatch,
    ) -> None:
        """Add one gene match to a lookup while preserving first occurrence."""
        if not key:
            return
        keys = (key, key.casefold())
        for lookup_key in keys:
            matches = lookup.setdefault(lookup_key, [])
            if match.var_name not in {item.var_name for item in matches}:
                matches.append(match)

    @staticmethod
    def _lookup_gene(
        gene_symbol: str,
        lookup: dict[str, list[_GeneMatch]],
    ) -> list[_GeneMatch]:
        """Return exact matches, falling back to case-insensitive matches."""
        exact_matches = lookup.get(gene_symbol, [])
        if exact_matches:
            return exact_matches
        return lookup.get(gene_symbol.casefold(), [])

    @classmethod
    def _genes_by_direction(
        cls,
        *,
        validation: pd.DataFrame,
        direction: str,
        output: GeneIdOutput,
        adata: AnnDataLike | None,
    ) -> tuple[tuple[str, ...], tuple[str, ...]]:
        """Return present and missing genes for one scoring direction."""
        rows = validation[validation["scoring_direction"] == direction].copy()
        if adata is None:
            genes = cls._dedupe_preserving_order(rows["gene_symbol"].tolist())
            return tuple(genes), ()

        output_column = cls._output_column(output)
        present = rows[rows["present"]]
        missing = rows[~rows["present"]]
        genes = cls._dedupe_preserving_order(present[output_column].tolist())
        missing_genes = cls._dedupe_preserving_order(
            missing["gene_symbol"].tolist()
        )
        return tuple(genes), tuple(missing_genes)

    @classmethod
    def _normalize_directions(
        cls,
        directions: Iterable[str] | None,
    ) -> set[str] | None:
        """Normalize optional direction filters."""
        if directions is None:
            return None

        normalized = {direction.strip().lower() for direction in directions}
        if invalid := normalized.difference(
            {"positive", "inverse", "context_dependent"}
        ):
            invalid_text = ", ".join(sorted(invalid))
            raise ValueError(f"Invalid direction filters: {invalid_text}")
        return normalized

    @classmethod
    def _validate_scorer(cls, scorer: str) -> None:
        """Raise if scorer is not a supported backend label."""
        if scorer not in cls.VALID_SCORERS:
            valid = ", ".join(sorted(cls.VALID_SCORERS))
            raise ValueError(
                f"Unsupported scorer '{scorer}'. Use one of {valid}."
            )

    @staticmethod
    def _resolve_output(
        output: GeneIdOutput | None,
        *,
        scorer: ScorerName,
        adata: AnnDataLike | None,
    ) -> GeneIdOutput:
        """Choose a gene-id output mode for module scoring."""
        if output is not None:
            return output
        return (
            "var_names"
            if adata is not None and scorer == "scanpy"
            else "symbols"
        )

    @staticmethod
    def _output_column(output: GeneIdOutput) -> str:
        """Return the validation column used for a gene output mode."""
        if output == "symbols":
            return "matched_gene_symbol"
        if output == "var_names":
            return "matched_var_name"
        raise ValueError(f"Unsupported gene output mode: {output}")

    @staticmethod
    def _normalize_module_id(module_id: str) -> str:
        """Normalize user-facing module ids for forgiving lookup."""
        return module_id.strip().replace("-", "_").upper()

    @staticmethod
    def _dedupe_preserving_order(values: Iterable[Any]) -> list[str]:
        """Return non-empty string values with duplicates removed."""
        seen: set[str] = set()
        deduped: list[str] = []
        for value in values:
            if pd.isna(value):
                continue
            string_value = str(value).strip()
            if not string_value or string_value in seen:
                continue
            seen.add(string_value)
            deduped.append(string_value)
        return deduped
