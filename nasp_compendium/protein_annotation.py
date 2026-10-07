"""Annotate marker genes with UniProt proteins, mass and STRING sensor partners.

Each gene's UniProt accession comes from HGNC. When HGNC lists several, the
longest protein is used (DDIT3's CHOP rather than its upstream-ORF peptide,
CDKN2A's p16INK4a rather than p14ARF). monomer_kDa is that canonical
sequence's mass from the EBI Proteins API, a UniProtKB mirror.

n_string_sensor_partners counts the distinct DNA or RNA sensors tagged in the
panel that share a STRING physical-network edge with the gene at or above a
combined score (default 0.4, STRING's medium confidence). A sensor's own
protein is not counted. The count is blank when STRING has no entry for the
gene's protein, which differs from zero partners.

Snapshot the sources once, then annotate the panel offline from them:

    python -m nasp_compendium.protein_annotation fetch
    python -m nasp_compendium.protein_annotation annotate
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import logging
import os
import urllib.parse
import urllib.request
from collections.abc import Iterable
from pathlib import Path

import pandas as pd

from nasp_compendium.gene_essentiality import resolve_hgnc_genes
from nasp_compendium.gene_modules import GeneModules
from nasp_compendium.marker_panel_annotation import read_marker_panel
from nasp_compendium.marker_panel_annotation import set_gene_annotation
from nasp_compendium.marker_panel_annotation import write_marker_panel


logger = logging.getLogger(__name__)

__all__ = [
    "count_sensor_partners",
    "fetch_protein_sequences",
    "fetch_string_ids",
    "fetch_string_network",
    "list_uniprot_candidates",
    "select_canonical_proteins",
]


def list_uniprot_candidates(
    gene_symbols: Iterable[str],
    hgnc_genes: pd.DataFrame,
) -> pd.DataFrame:
    """List each gene's HGNC UniProt accessions.

    Args:
      gene_symbols: Panel symbols, resolved through HGNC symbol history.
      hgnc_genes: Approved HGNC genes with the `resolve_hgnc_genes` columns
        and uniprot_ids ("|"-delimited).

    Returns:
      gene_symbol, accession and hgnc_rank (HGNC listing order), one row per
      accession. Genes without an accession are absent.
    """
    resolved = resolve_hgnc_genes(gene_symbols, hgnc_genes)
    candidates = resolved[["gene_symbol", "hgnc_id"]].merge(
        hgnc_genes[["hgnc_id", "uniprot_ids"]], on="hgnc_id", how="inner"
    )
    candidates = candidates.assign(
        accession=candidates["uniprot_ids"].str.split("|")
    ).explode("accession")
    candidates = candidates[candidates["accession"].notna()]
    candidates["hgnc_rank"] = candidates.groupby("gene_symbol").cumcount()
    return candidates.loc[
        :, ["gene_symbol", "accession", "hgnc_rank"]
    ].reset_index(drop=True)


def select_canonical_proteins(
    candidates: pd.DataFrame,
    sequences: pd.DataFrame,
) -> pd.DataFrame:
    """Choose one protein per gene and report its monomer mass.

    The longest candidate sequence is chosen, ties going to the first HGNC
    listing. A gene whose candidates all lack sequence data keeps its first
    HGNC accession with a blank mass.

    Args:
      candidates: Output of `list_uniprot_candidates`.
      sequences: accession, mass_da and length per UniProt entry.

    Returns:
      gene_symbol, uniprot_id and monomer_kDa (text with one decimal place).
    """
    ranked = candidates.merge(sequences, on="accession", how="left")
    ranked = ranked.sort_values(
        ["gene_symbol", "length", "hgnc_rank"],
        ascending=[True, False, True],
        na_position="last",
    )
    proteins = ranked.drop_duplicates("gene_symbol")

    monomer_kda = (proteins["mass_da"] / 1000).map(
        lambda kda: "" if pd.isna(kda) else f"{kda:.1f}"
    )
    return pd.DataFrame(
        {
            "gene_symbol": proteins["gene_symbol"],
            "uniprot_id": proteins["accession"],
            "monomer_kDa": monomer_kda,
        }
    ).reset_index(drop=True)


def count_sensor_partners(
    proteins: pd.DataFrame,
    string_ids: pd.DataFrame,
    network: pd.DataFrame,
    sensor_genes: Iterable[str],
    *,
    min_score: float = 0.4,
) -> pd.DataFrame:
    """Count each gene's distinct sensor partners in a STRING network.

    Args:
      proteins: gene_symbol and uniprot_id, one row per gene.
      string_ids: accession and string_id for proteins STRING maps.
      network: string_id_a, string_id_b and combined score in [0, 1].
      sensor_genes: Gene symbols whose proteins count as sensors.
      min_score: Lowest combined score counted as an edge.

    Returns:
      gene_symbol and n_string_sensor_partners, missing for genes whose
      protein has no STRING entry.
    """
    nodes = proteins.merge(
        string_ids, left_on="uniprot_id", right_on="accession", how="left"
    )
    sensor_ids = (
        nodes.loc[nodes["gene_symbol"].isin(list(sensor_genes)), "string_id"]
        .dropna()
        .tolist()
    )

    edges = network.loc[
        network["score"] >= min_score, ["string_id_a", "string_id_b"]
    ]
    pairs = pd.concat(
        [
            edges.set_axis(["protein", "partner"], axis=1),
            edges.set_axis(["partner", "protein"], axis=1),
        ]
    )
    pairs = pairs.loc[
        pairs["partner"].isin(sensor_ids)
        & (pairs["protein"] != pairs["partner"])
    ]
    counts = pairs.drop_duplicates()["protein"].value_counts()

    n_partners = nodes["string_id"].map(counts).fillna(0).astype("Int64")
    n_partners[nodes["string_id"].isna()] = pd.NA
    return pd.DataFrame(
        {
            "gene_symbol": nodes["gene_symbol"],
            "n_string_sensor_partners": n_partners,
        }
    )


def fetch_protein_sequences(
    accessions: Iterable[str],
    *,
    url: str = "https://www.ebi.ac.uk/proteins/api/proteins",
    batch_size: int = 100,
    timeout: float = 120,
) -> pd.DataFrame:
    """Fetch canonical sequence mass and length from the EBI Proteins API.

    Args:
      accessions: UniProt accessions; duplicates are fetched once.
      url: Proteins API endpoint.
      batch_size: Accessions per request; the API accepts at most 100.
      timeout: Seconds to wait for each response.

    Returns:
      accession, mass_da and length for each entry returned. Accessions the
      API does not return are absent.
    """
    unique_accessions = list(dict.fromkeys(accessions))
    records = []
    for start in range(0, len(unique_accessions), batch_size):
        batch = unique_accessions[start : start + batch_size]
        query = urllib.parse.urlencode(
            {"offset": 0, "size": len(batch), "accession": ",".join(batch)}
        )
        request = urllib.request.Request(
            f"{url}?{query}", headers={"Accept": "application/json"}
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            entries = json.load(response)
        records += [
            {
                "accession": entry["accession"],
                "mass_da": entry["sequence"]["mass"],
                "length": entry["sequence"]["length"],
            }
            for entry in entries
        ]

    if missing := set(unique_accessions) - {r["accession"] for r in records}:
        logger.warning(
            "Proteins API returned no entry for %d accessions: %s",
            len(missing),
            sorted(missing),
        )
    sequences = pd.DataFrame(records).reindex(
        columns=["accession", "mass_da", "length"]
    )
    return sequences


def fetch_string_ids(
    identifiers: Iterable[str],
    *,
    species: int = 9606,
    url: str = "https://string-db.org/api",
    timeout: float = 300,
) -> pd.DataFrame:
    """Map protein identifiers, such as UniProt accessions, to STRING.

    Returns:
      identifier and string_id for each identifier STRING maps.
    """
    mapped = _post_string_tsv(
        f"{url}/tsv/get_string_ids",
        {
            "identifiers": "\r".join(dict.fromkeys(identifiers)),
            "species": species,
            "limit": 1,
            "echo_query": 1,
        },
        timeout=timeout,
    )
    return mapped.rename(
        columns={"queryItem": "identifier", "stringId": "string_id"}
    ).loc[:, ["identifier", "string_id"]]


def fetch_string_network(
    string_ids: Iterable[str],
    *,
    species: int = 9606,
    network_type: str = "physical",
    required_score: int = 150,
    url: str = "https://string-db.org/api",
    timeout: float = 300,
) -> pd.DataFrame:
    """Fetch STRING edges among the given proteins.

    Args:
      string_ids: STRING protein identifiers.
      species: NCBI taxon.
      network_type: "physical" or "functional".
      required_score: Lowest combined score, on STRING's 0-1000 scale.
      url: STRING API root.
      timeout: Seconds to wait for the response.

    Returns:
      string_id_a, string_id_b, the preferred names and combined score in
      [0, 1].
    """
    network = _post_string_tsv(
        f"{url}/tsv/network",
        {
            "identifiers": "\r".join(dict.fromkeys(string_ids)),
            "species": species,
            "network_type": network_type,
            "required_score": required_score,
        },
        timeout=timeout,
    )
    return network.rename(
        columns={
            "stringId_A": "string_id_a",
            "stringId_B": "string_id_b",
            "preferredName_A": "preferred_name_a",
            "preferredName_B": "preferred_name_b",
        }
    ).loc[
        :,
        [
            "string_id_a",
            "string_id_b",
            "preferred_name_a",
            "preferred_name_b",
            "score",
        ],
    ]


def _map_proteins_to_string(proteins: pd.DataFrame) -> pd.DataFrame:
    """Map each gene's protein to STRING, falling back to its gene symbol.

    STRING misses some current UniProt accessions, such as accessions newer
    than its release, that it still covers under the gene symbol.

    Returns:
      accession, string_id and matched_by ("accession" or "symbol").
    """
    by_accession = fetch_string_ids(proteins["uniprot_id"]).rename(
        columns={"identifier": "accession"}
    )
    unmapped = proteins.loc[
        ~proteins["uniprot_id"].isin(by_accession["accession"])
    ]
    by_symbol = unmapped.merge(
        fetch_string_ids(unmapped["gene_symbol"]),
        left_on="gene_symbol",
        right_on="identifier",
    ).rename(columns={"uniprot_id": "accession"})
    if not by_symbol.empty:
        logger.info(
            "Mapped %s to STRING by gene symbol",
            by_symbol["gene_symbol"].tolist(),
        )
    return pd.concat(
        [
            by_accession.assign(matched_by="accession"),
            by_symbol.loc[:, ["accession", "string_id"]].assign(
                matched_by="symbol"
            ),
        ],
        ignore_index=True,
    )


def _post_string_tsv(
    url: str,
    fields: dict[str, object],
    *,
    timeout: float,
    caller_identity: str = "nasp_compendium",
) -> pd.DataFrame:
    """POST a STRING API request and parse its TSV response."""
    data = urllib.parse.urlencode(
        {**fields, "caller_identity": caller_identity}
    ).encode()
    with urllib.request.urlopen(url, data=data, timeout=timeout) as response:
        return pd.read_csv(response, sep="\t")


def _fetch_string_version(url: str, *, timeout: float = 60) -> str:
    """Return the STRING version the API serves."""
    with urllib.request.urlopen(f"{url}/json/version", timeout=timeout) as r:
        return str(json.load(r)[0]["string_version"])


def _load_hgnc_uniprot(path: Path) -> pd.DataFrame:
    """Load approved HGNC genes with symbol history and UniProt accessions."""
    hgnc_genes = pd.read_csv(path, sep="\t", dtype=str)
    return hgnc_genes.loc[
        hgnc_genes["status"] == "Approved",
        [
            "hgnc_id",
            "symbol",
            "prev_symbol",
            "alias_symbol",
            "entrez_id",
            "uniprot_ids",
        ],
    ].reset_index(drop=True)


def _file_md5(path: Path) -> str:
    """Return the MD5 digest of `path`."""
    return hashlib.md5(path.read_bytes()).hexdigest()


def _fetch_sources(args: argparse.Namespace) -> None:
    """Snapshot protein masses, STRING identifiers and the STRING network."""
    panel, _ = read_marker_panel(args.marker_genes)
    candidates = list_uniprot_candidates(
        panel["gene_symbol"], _load_hgnc_uniprot(args.hgnc)
    )

    sequences = fetch_protein_sequences(candidates["accession"])
    proteins = select_canonical_proteins(candidates, sequences)
    string_ids = _map_proteins_to_string(proteins)
    network = fetch_string_network(
        string_ids["string_id"], required_score=args.required_score
    )

    args.source_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "protein_sequences": args.source_dir / "protein_sequences.tsv",
        "string_ids": args.source_dir / "string_ids.tsv",
        "string_network": args.source_dir / "string_network.tsv",
    }
    sequences.to_csv(outputs["protein_sequences"], sep="\t", index=False)
    string_ids.to_csv(outputs["string_ids"], sep="\t", index=False)
    network.to_csv(outputs["string_network"], sep="\t", index=False)

    manifest = {
        "retrieved": dt.datetime.now().isoformat(timespec="seconds"),
        "script": "nasp_compendium/protein_annotation.py",
        "string_version": _fetch_string_version("https://string-db.org/api"),
        "string_network_type": "physical",
        "string_required_score": args.required_score,
        "n_genes": int(candidates["gene_symbol"].nunique()),
        "n_accessions": int(candidates["accession"].nunique()),
        "n_string_mapped": string_ids["matched_by"].value_counts().to_dict(),
        "n_string_edges": len(network),
        "files": {
            name: {
                "path": os.path.relpath(path, args.source_dir),
                "md5": _file_md5(path),
            }
            for name, path in outputs.items()
        },
    }
    (args.source_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )
    logger.info(
        "Saved %d sequences, %d STRING ids and %d edges to %s",
        len(sequences),
        len(string_ids),
        len(network),
        args.source_dir,
    )


def _annotate_marker_panel(
    args: argparse.Namespace,
    *,
    sensor_type: str = "dna_rna",
) -> None:
    """Write uniprot_id, monomer_kDa and n_string_sensor_partners columns."""
    out_path = args.out or args.marker_genes
    panel, line_terminator = read_marker_panel(args.marker_genes)

    proteins = select_canonical_proteins(
        list_uniprot_candidates(
            panel["gene_symbol"], _load_hgnc_uniprot(args.hgnc)
        ),
        pd.read_csv(args.source_dir / "protein_sequences.tsv", sep="\t"),
    )
    partners = count_sensor_partners(
        proteins,
        pd.read_csv(args.source_dir / "string_ids.tsv", sep="\t"),
        pd.read_csv(args.source_dir / "string_network.tsv", sep="\t"),
        GeneModules(args.marker_genes).get_sensors(sensor_type),
        min_score=args.min_score,
    )

    set_gene_annotation(panel, proteins.merge(partners, on="gene_symbol"))
    write_marker_panel(panel, out_path, line_terminator=line_terminator)
    logger.info(
        "Annotated %d genes; %d lack a STRING entry",
        len(partners),
        int(partners["n_string_sensor_partners"].isna().sum()),
    )


def _parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    data_dir = Path(__file__).resolve().parent.parent / "data"

    parser = argparse.ArgumentParser(
        description=(
            "Annotate marker genes with UniProt proteins, monomer mass and "
            "STRING sensor partners."
        )
    )
    parser.add_argument(
        "--marker-genes",
        type=Path,
        default=GeneModules.default_panel_path(),
        help="Marker-gene TSV. Defaults to the bundled panel.",
    )
    parser.add_argument(
        "--hgnc",
        type=Path,
        default=data_dir
        / "essentiality"
        / "hgnc"
        / "hgnc_complete_set_2026-09-25.txt.gz",
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=data_dir / "proteins",
        help="Directory of protein and STRING snapshots.",
    )
    subparsers = parser.add_subparsers(required=True)

    fetch = subparsers.add_parser(
        "fetch", help="Snapshot protein masses and the STRING network."
    )
    fetch.add_argument(
        "--required-score",
        type=int,
        default=150,
        help="Lowest STRING combined score to keep, on the 0-1000 scale.",
    )
    fetch.set_defaults(func=_fetch_sources)

    annotate = subparsers.add_parser(
        "annotate", help="Write protein columns into the panel."
    )
    annotate.add_argument(
        "--min-score",
        type=float,
        default=0.4,
        help="Lowest STRING combined score, in [0, 1], counted as an edge.",
    )
    annotate.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Annotated TSV. Defaults to overwriting --marker-genes.",
    )
    annotate.set_defaults(func=_annotate_marker_panel)
    return parser.parse_args()


def main() -> None:
    """Fetch protein sources or annotate the marker panel."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = _parse_arguments()
    args.func(args)


if __name__ == "__main__":
    main()
