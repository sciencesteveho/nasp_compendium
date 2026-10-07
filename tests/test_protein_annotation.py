"""Tests for marker-gene protein annotation."""

from __future__ import annotations

import pandas as pd

from nasp_compendium.protein_annotation import count_sensor_partners
from nasp_compendium.protein_annotation import select_canonical_proteins


def _partner_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Return proteins, STRING ids and a network for three sensors.

    G links to sensors S1 and S2, to S3 below the 0.4 threshold, and to the
    non-sensor H. The G-S1 edge is listed in both directions. U has no STRING
    entry.
    """
    proteins = pd.DataFrame(
        {
            "gene_symbol": ["S1", "S2", "S3", "G", "H", "U"],
            "uniprot_id": ["P1", "P2", "P3", "P4", "P5", "P6"],
        }
    )
    string_ids = pd.DataFrame(
        {
            "accession": ["P1", "P2", "P3", "P4", "P5"],
            "string_id": ["s1", "s2", "s3", "g", "h"],
        }
    )
    network = pd.DataFrame(
        {
            "string_id_a": ["g", "s1", "g", "g", "g", "s1"],
            "string_id_b": ["s1", "g", "s2", "s3", "h", "s2"],
            "score": [0.9, 0.9, 0.5, 0.3, 0.99, 0.8],
        }
    )
    return proteins, string_ids, network


def test_count_sensor_partners_counts_distinct_sensors_above_threshold() -> (
    None
):
    """Each gene counts the distinct other sensors it links to at 0.4+."""
    proteins, string_ids, network = _partner_inputs()

    partners = count_sensor_partners(
        proteins, string_ids, network, ["S1", "S2", "S3"], min_score=0.4
    ).set_index("gene_symbol")["n_string_sensor_partners"]

    assert partners[["G", "S1", "S2", "S3", "H"]].tolist() == [2, 1, 1, 0, 0]


def test_count_sensor_partners_leaves_unmapped_genes_missing() -> None:
    """A gene absent from STRING is missing rather than zero partners."""
    proteins, string_ids, network = _partner_inputs()

    partners = count_sensor_partners(
        proteins, string_ids, network, ["S1", "S2", "S3"]
    ).set_index("gene_symbol")["n_string_sensor_partners"]

    assert pd.isna(partners["U"])
    assert partners["H"] == 0


def test_select_canonical_proteins_prefers_the_longest_protein() -> None:
    """Genes with several accessions report the longest protein's mass."""
    candidates = pd.DataFrame(
        {
            "gene_symbol": ["DDIT3", "DDIT3", "CDKN2A", "CDKN2A"],
            "accession": ["P0DPQ6", "P35638", "P42771", "Q8N726"],
            "hgnc_rank": [0, 1, 0, 1],
        }
    )
    sequences = pd.DataFrame(
        {
            "accession": ["P0DPQ6", "P35638", "P42771", "Q8N726"],
            "mass_da": [4284, 19175, 16533, 13903],
            "length": [34, 169, 156, 132],
        }
    )

    proteins = select_canonical_proteins(candidates, sequences)

    assert proteins.set_index("gene_symbol").to_dict("index") == {
        "CDKN2A": {"uniprot_id": "P42771", "monomer_kDa": "16.5"},
        "DDIT3": {"uniprot_id": "P35638", "monomer_kDa": "19.2"},
    }
