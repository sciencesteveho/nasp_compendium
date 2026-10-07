# Gene essentiality sources

Inputs to the `depmap_essentiality` and `shet_post_*` columns of
`data/marker_genes.tsv`. Add or refresh them in place from the repository root
with:

```sh
python -m nasp_compendium.gene_essentiality
```

The run copies curated columns verbatim, replaces any earlier annotation
columns, and writes `marker_genes.tsv.manifest.json` beside the panel,
recording the MD5 of every source. Rerun it after adding genes to the panel;
new rows otherwise have empty annotation columns.

| File | Source | Retrieved | MD5 |
| --- | --- | --- | --- |
| `depmap_26Q1/CRISPRInferredCommonEssentials.csv` | DepMap Public 26Q1 portal download (`downloads-by-canonical-id/26q1-public-3b44.1/`) | 2026-09-28 | `f9b12f368abf7684fcd97af31e8a39a2` |
| `depmap_26Q1/chronos_gene_effect_header.csv` | Header row only of `gene_effect.csv` from DepMap's [Chronos parameters (Public 26Q1)](https://doi.org/10.6084/m9.figshare.31660582.v2) Figshare deposit (file 67214582, 413 MB) | 2026-09-28 | `09ca370c73b968aa5830589828719300` |
| `genebayes/s_het_estimates.genebayes.tsv` | GeneBayes s_het estimates, [Zenodo 10403254](https://zenodo.org/records/10403254) (Zeng et al. 2024, *Nat Genet*, [10.1038/s41588-024-01820-9](https://doi.org/10.1038/s41588-024-01820-9)) | 2026-09-28 | `a377c95fb1b785f740d8601905890f21` |
| `hgnc/hgnc_complete_set_2026-09-25.txt.gz` | [HGNC complete set](https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt), last modified 2026-09-25; gzip-compressed here | 2026-09-28 | `d418753c024e0ad44badfa2d5bee8f08` |

DepMap data are released under CC BY 4.0.

## Interpretation

- `depmap_essentiality` is "common_essential" when DepMap's Chronos-inferred
  common-essential list includes the gene: it is a dependency in most cancer
  cell lines. "not_common_essential" means screened but not on that list; the
  gene may still be a selective dependency. "not_screened" means absent from
  the 26Q1 CRISPR gene-effect matrix (for example, mitochondrially encoded
  genes).
- The screened-gene universe is the 26Q1 Chronos gene-effect header. All 1,827
  common essentials are in it by Entrez ID. One header column is unlabeled
  upstream and is skipped.
- `shet_post_mean` is the GeneBayes posterior mean selection coefficient
  against heterozygous loss of function (higher is more constrained), with its
  95% credible interval. It is missing for genes GeneBayes did not estimate.
- DepMap is matched by Entrez ID and GeneBayes by HGNC ID after resolving
  panel symbols through HGNC, so symbol renames on either side do not drop
  genes.
