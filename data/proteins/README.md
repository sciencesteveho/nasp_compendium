# Protein sources

Inputs to the `uniprot_id`, `monomer_kDa`, `n_string_sensor_partners` and
`n_string_partners` columns of `data/marker_genes.tsv`. Snapshot the sources,
then add or refresh the columns in place from the repository root:

```sh
python -m nasp_compendium.protein_annotation fetch
python -m nasp_compendium.protein_annotation annotate
```

`fetch` queries the web services below for the current panel genes and writes
`manifest.json` with the retrieval time, STRING version, query parameters and
the MD5 of every snapshot. `annotate` works offline from the snapshots and the
HGNC table in `../essentiality/hgnc/`. Rerun both after adding genes to the
panel; `annotate` alone leaves new genes without these columns.

| File | Source |
| --- | --- |
| `protein_sequences.tsv` | Canonical sequence mass (Da) and length from the [EBI Proteins API](https://www.ebi.ac.uk/proteins/api/doc/), a UniProtKB mirror, for every HGNC-listed accession of a panel gene |
| `string_ids.tsv` | [STRING](https://string-db.org) protein for each chosen accession, mapped by accession or, where STRING lacks the accession, by gene symbol (`matched_by`) |
| `string_partners.tsv.gz` | Every STRING physical-network partner, anywhere in the human proteome, of each panel protein with combined score ≥ 0.15 |

UniProt and STRING data are released under CC BY 4.0.

## Interpretation

- `uniprot_id` is the gene's HGNC-listed UniProt accession. Where HGNC lists
  several, the longest protein is used: DDIT3 is CHOP (P35638), not its
  upstream-ORF peptide, and CDKN2A is p16INK4a (P42771), not p14ARF.
- `monomer_kDa` is that canonical sequence's mass in kDa, to one decimal place.
  It ignores isoforms, processing and modifications.
- `n_string_sensor_partners` counts the distinct DNA or RNA sensors tagged in
  the panel (`GeneModules.sensors("dna_rna")`) that share a STRING physical
  edge with the gene at combined score ≥ 0.4 (medium confidence). A sensor's own
  protein is not counted. It is blank only when STRING has no entry for the
  protein. STRING scores combine experimental, curated-database and
  text-mining evidence, so a count marks candidate partners, not confirmed
  complexes.
- `n_string_partners` counts all distinct physical partners at the same
  threshold. It largely tracks how well studied a protein is (BRD4 has 1,511),
  so it serves mainly as context for the sensor count.
- The sensor counts replace the earlier pilot values for the 38 sensors, whose
  STRING method could not be reproduced.
