"""Annotate genes with DepMap essentiality and GeneBayes s_het constraint.

DepMap labels genes as "SYMBOL (ENTREZ)" and GeneBayes keys s_het by HGNC ID.
Symbols are resolved through the HGNC complete set and matched to each source
by identifier, so renamed genes still match (for example, the panel's DDX58 is
RIGI in DepMap, and DepMap 26Q1's NCL is NUCLEOLIN in current HGNC).

Add or refresh the annotation columns of the bundled marker-gene panel in
place, leaving its curated columns unchanged:

    python -m nasp_compendium.gene_essentiality
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import logging
import os
from collections.abc import Iterable
from pathlib import Path

import pandas as pd

from nasp_compendium.gene_modules import GeneModules


logger = logging.getLogger(__name__)

__all__ = [
    "annotate_gene_essentiality",
    "load_depmap_common_essentials",
    "load_depmap_screened_genes",
    "load_genebayes_shet",
    "load_hgnc_genes",
    "resolve_hgnc_genes",
]


def annotate_gene_essentiality(
    gene_symbols: Iterable[str],
    *,
    hgnc_genes: pd.DataFrame,
    depmap_common_essentials: pd.DataFrame,
    depmap_screened_genes: pd.DataFrame,
    shet: pd.DataFrame,
) -> pd.DataFrame:
    """Annotate genes with DepMap common essentiality and GeneBayes s_het.

    DepMap status is matched on Entrez ID and s_het on HGNC ID. A gene absent
    from the DepMap screen is "not_screened" rather than non-essential; status
    is missing when a symbol has no HGNC match or the HGNC gene has no Entrez
    ID.

    Args:
      gene_symbols: Symbols to annotate; duplicates are collapsed.
      hgnc_genes: Output of `load_hgnc_genes`.
      depmap_common_essentials: Output of `load_depmap_common_essentials`.
      depmap_screened_genes: Output of `load_depmap_screened_genes`.
      shet: Output of `load_genebayes_shet`.

    Returns:
      One row per unique symbol, in input order, with the `resolve_hgnc_genes`
      columns, depmap_essentiality ("common_essential",
      "not_common_essential" or "not_screened"), and the GeneBayes s_het
      posterior mean with its 95% credible interval (missing when GeneBayes
      has no estimate).
    """
    annotation = resolve_hgnc_genes(gene_symbols, hgnc_genes)

    essential = annotation["entrez_id"].isin(
        depmap_common_essentials["entrez_id"]
    )
    screened = annotation["entrez_id"].isin(depmap_screened_genes["entrez_id"])
    annotation["depmap_essentiality"] = pd.Series(
        pd.NA, index=annotation.index, dtype="string"
    )
    has_entrez = annotation["entrez_id"].notna()
    annotation.loc[has_entrez, "depmap_essentiality"] = "not_screened"
    annotation.loc[screened, "depmap_essentiality"] = "not_common_essential"
    annotation.loc[essential, "depmap_essentiality"] = "common_essential"

    if n_undetermined := int((~has_entrez).sum()):
        logger.warning(
            "DepMap status undetermined for %d genes without an Entrez ID",
            n_undetermined,
        )
    return annotation.merge(shet, on="hgnc_id", how="left")


def resolve_hgnc_genes(
    gene_symbols: Iterable[str],
    hgnc_genes: pd.DataFrame,
) -> pd.DataFrame:
    """Resolve gene symbols to approved HGNC genes.

    Each symbol is matched to an approved symbol first, then to previous
    symbols, then to alias symbols. A previous or alias symbol shared by
    several approved genes is left unresolved rather than guessed.

    Args:
      gene_symbols: Symbols to resolve; duplicates are collapsed.
      hgnc_genes: Output of `load_hgnc_genes`.

    Returns:
      One row per unique symbol, in input order, with gene_symbol, hgnc_id,
      hgnc_symbol, entrez_id and symbol_match ("approved", "previous",
      "alias" or "unresolved").
    """
    approved = set(hgnc_genes["symbol"])
    history_lookups = {
        "previous": _symbol_history_lookup(hgnc_genes, column="prev_symbol"),
        "alias": _symbol_history_lookup(hgnc_genes, column="alias_symbol"),
    }

    matches = []
    for gene_symbol in dict.fromkeys(gene_symbols):
        hgnc_symbol, symbol_match = None, "unresolved"
        if gene_symbol in approved:
            hgnc_symbol, symbol_match = gene_symbol, "approved"
        else:
            for history, lookup in history_lookups.items():
                candidates = lookup.get(gene_symbol, [])
                if len(candidates) == 1:
                    hgnc_symbol, symbol_match = candidates[0], history
                if candidates:
                    break
        if hgnc_symbol is None:
            logger.warning("No unique HGNC match for %s", gene_symbol)
        matches.append(
            {
                "gene_symbol": gene_symbol,
                "hgnc_symbol": hgnc_symbol,
                "symbol_match": symbol_match,
            }
        )

    resolved = pd.DataFrame(matches).merge(
        hgnc_genes[["hgnc_id", "symbol", "entrez_id"]],
        left_on="hgnc_symbol",
        right_on="symbol",
        how="left",
    )
    return resolved[
        ["gene_symbol", "hgnc_id", "hgnc_symbol", "entrez_id", "symbol_match"]
    ]


def load_hgnc_genes(path: str | Path) -> pd.DataFrame:
    """Load approved HGNC genes with symbol history and Entrez IDs.

    Args:
      path: HGNC complete-set TSV, optionally gzip-compressed.

    Returns:
      hgnc_id, symbol, prev_symbol, alias_symbol and entrez_id for every
      approved gene. Symbol-history fields keep the source "|" delimiter.
    """
    hgnc_genes = pd.read_csv(
        path,
        sep="\t",
        dtype=str,
        usecols=[
            "hgnc_id",
            "symbol",
            "status",
            "prev_symbol",
            "alias_symbol",
            "entrez_id",
        ],
    )
    hgnc_genes = hgnc_genes[hgnc_genes["status"] == "Approved"]
    return hgnc_genes.drop(columns="status").reset_index(drop=True)


def load_depmap_common_essentials(
    path: str | Path,
    *,
    column: str = "Essentials",
) -> pd.DataFrame:
    """Load DepMap CRISPR inferred common-essential genes.

    Args:
      path: DepMap `CRISPRInferredCommonEssentials.csv`.
      column: Column holding "SYMBOL (ENTREZ)" gene labels.

    Returns:
      depmap_symbol and entrez_id for each common-essential gene.
    """
    labels = pd.read_csv(path, dtype=str)[column]
    return _parse_depmap_gene_labels(labels, source=Path(path))


def load_depmap_screened_genes(path: str | Path) -> pd.DataFrame:
    """Load the genes scored in a DepMap CRISPR gene-effect matrix.

    Only the header row is read, so `path` may be a full models-by-genes
    matrix such as `CRISPRGeneEffect.csv` or a file holding just its header.
    Unlabeled gene columns cannot be matched and are skipped with a warning.

    Args:
      path: DepMap gene-effect CSV whose first column indexes models.

    Returns:
      depmap_symbol and entrez_id for each labeled gene column.
    """
    with Path(path).open(newline="") as handle:
        gene_labels = next(csv.reader(handle))[1:]

    labeled = [label for label in gene_labels if label.strip()]
    if n_unlabeled := len(gene_labels) - len(labeled):
        logger.warning(
            "Skipping %d unlabeled gene columns in %s", n_unlabeled, path
        )
    return _parse_depmap_gene_labels(labeled, source=Path(path))


def load_genebayes_shet(path: str | Path) -> pd.DataFrame:
    """Load GeneBayes posterior s_het estimates keyed by HGNC ID.

    Args:
      path: GeneBayes `s_het_estimates.genebayes.tsv`.

    Returns:
      hgnc_id, shet_post_mean, shet_post_lower_95 and shet_post_upper_95.

    Raises:
      ValueError: If an HGNC ID is missing or has several estimates.
    """
    shet = pd.read_csv(path, sep="\t", dtype={"hgnc": str})
    if shet["hgnc"].isna().any() or shet["hgnc"].duplicated().any():
        raise ValueError(
            f"Expected one s_het estimate per HGNC ID in {path}; found missing "
            "or duplicated values in the hgnc column."
        )

    return shet.rename(
        columns={
            "hgnc": "hgnc_id",
            "post_mean": "shet_post_mean",
            "post_lower_95": "shet_post_lower_95",
            "post_upper_95": "shet_post_upper_95",
        }
    )[["hgnc_id", "shet_post_mean", "shet_post_lower_95", "shet_post_upper_95"]]


def _parse_depmap_gene_labels(
    labels: Iterable[str],
    *,
    source: Path,
) -> pd.DataFrame:
    """Split DepMap "SYMBOL (ENTREZ)" labels into symbol and Entrez ID."""
    labels = pd.Series(list(labels), dtype=str)
    genes = labels.str.extract(
        r"^(?P<depmap_symbol>\S+) \((?P<entrez_id>\d+)\)$"
    )
    if malformed := labels[genes["entrez_id"].isna()].tolist():
        raise ValueError(
            f"Expected DepMap gene labels formatted as 'SYMBOL (ENTREZ)' in "
            f"{source}; found {len(malformed)} others, e.g. {malformed[:3]}."
        )
    return genes


def _symbol_history_lookup(
    hgnc_genes: pd.DataFrame,
    *,
    column: str,
) -> dict[str, list[str]]:
    """Map each historical symbol in `column` to its approved symbols."""
    history = hgnc_genes[["symbol", column]].dropna()
    history = history.assign(**{column: history[column].str.split("|")})
    history = history.explode(column)
    history[column] = history[column].str.strip()
    candidates = history.groupby(column)["symbol"].agg(
        lambda symbols: sorted(set(symbols))
    )
    return {str(symbol): approved for symbol, approved in candidates.items()}


def _file_md5(path: Path) -> str:
    """Return the MD5 digest used by DepMap, Figshare and Zenodo listings."""
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _annotate_marker_panel(
    args: argparse.Namespace,
    *,
    annotation_columns: tuple[str, ...] = (
        "depmap_essentiality",
        "shet_post_mean",
        "shet_post_lower_95",
        "shet_post_upper_95",
    ),
) -> None:
    """Write the marker panel with annotation columns, and its manifest.

    Curated columns are copied verbatim, keeping the panel's line endings.
    Existing annotation columns are replaced, so reruns are idempotent. Every
    row of a gene listed in several modules carries the same annotation.
    """
    panel_path = args.marker_genes or GeneModules.default_panel_path()
    out_path = args.out or panel_path
    sources = {
        "hgnc": args.hgnc,
        "depmap_common_essentials": args.depmap_common_essentials,
        "depmap_gene_effect": args.depmap_gene_effect,
        "genebayes_shet": args.shet,
    }

    with panel_path.open(encoding="utf-8", newline="") as handle:
        line_terminator = "\r\n" if handle.readline().endswith("\r\n") else "\n"
    panel = pd.read_csv(
        panel_path, sep="\t", dtype=str, keep_default_na=False
    ).drop(columns=list(annotation_columns), errors="ignore")

    annotation = annotate_gene_essentiality(
        panel["gene_symbol"],
        hgnc_genes=load_hgnc_genes(args.hgnc),
        depmap_common_essentials=load_depmap_common_essentials(
            args.depmap_common_essentials
        ),
        depmap_screened_genes=load_depmap_screened_genes(
            args.depmap_gene_effect
        ),
        shet=load_genebayes_shet(args.shet),
    )
    annotated_panel = panel.merge(
        annotation[["gene_symbol", *annotation_columns]],
        on="gene_symbol",
        how="left",
        validate="many_to_one",
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    annotated_panel.to_csv(
        out_path,
        sep="\t",
        index=False,
        float_format="%.6g",
        lineterminator=line_terminator,
    )
    status_counts = (
        annotation["depmap_essentiality"].fillna("undetermined").value_counts()
    )
    manifest = {
        "created": dt.datetime.now().isoformat(timespec="seconds"),
        "script": "nasp_compendium/gene_essentiality.py",
        "n_genes": len(annotation),
        "depmap_essentiality_counts": {
            status: int(count) for status, count in status_counts.items()
        },
        "n_genes_with_shet": int(annotation["shet_post_mean"].notna().sum()),
        "inputs": {
            name: {
                "path": os.path.relpath(path, out_path.parent),
                "md5": _file_md5(Path(path)),
            }
            for name, path in sources.items()
        },
    }
    manifest_path = out_path.with_name(f"{out_path.name}.manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    logger.info(
        "Annotated %d genes in %d panel rows of %s",
        len(annotation),
        len(annotated_panel),
        out_path,
    )


def _parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    data_dir = Path(__file__).resolve().parent.parent / "data"
    source_dir = data_dir / "essentiality"

    parser = argparse.ArgumentParser(
        description=(
            "Annotate marker-panel genes with DepMap common essentiality and "
            "GeneBayes s_het."
        )
    )
    parser.add_argument(
        "--marker-genes",
        type=Path,
        default=None,
        help="Marker-gene TSV to annotate. Defaults to the bundled panel.",
    )
    parser.add_argument(
        "--hgnc",
        type=Path,
        default=source_dir / "hgnc" / "hgnc_complete_set_2026-09-25.txt.gz",
    )
    parser.add_argument(
        "--depmap-common-essentials",
        type=Path,
        default=source_dir
        / "depmap_26Q1"
        / "CRISPRInferredCommonEssentials.csv",
    )
    parser.add_argument(
        "--depmap-gene-effect",
        type=Path,
        default=source_dir / "depmap_26Q1" / "chronos_gene_effect_header.csv",
        help="DepMap gene-effect CSV or its header; defines screened genes.",
    )
    parser.add_argument(
        "--shet",
        type=Path,
        default=source_dir / "genebayes" / "s_het_estimates.genebayes.tsv",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Annotated TSV. Defaults to overwriting --marker-genes.",
    )
    return parser.parse_args()


def main() -> None:
    """Annotate the marker-gene panel with essentiality columns."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    _annotate_marker_panel(_parse_arguments())


if __name__ == "__main__":
    main()
