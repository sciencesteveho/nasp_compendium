# NASP data compendium

The data compendium is a shared NASP-centric resource designed for iterative refinement and knowledge acquisition. It contains
paper-level mechanism records, marker-gene module pages, and generated
visualizations for reviewing relationships across nucleic-acid sensing,
inflammation, senescence, and aging-related biology.

</br>

## Repository structure

* [`docs/compendium/ `](compendium/): Paper mechanism records.
* [`docs/marker_genes/ `](marker_genes/): Rendered marker-gene modules, with visualizations for each module class.
* [`data/marker_genes.tsv `](../data/marker_genes.tsv): Raw marker gene .tsv.

</br>

## Usage

Render the full mechanism graph:

```sh
compendium render_graph \
  --dir docs/compendium \
  --out docs/compendium/nasp_pathway_map.png
```

#### Optional arguments:

| Flag | Use |
| --- | --- |
| `--compact` | Force compact layout. |
| `--annotate-papers` | Add paper citations to edge labels. |
| `--paper` / `--papers` | Render an individual paper or a comma-separated subset. |
| `--exclude-rel` | Hide noisy edge classes such as `does_not_correlate`. |
| `--no-aggregate-edges` | Show duplicate source-target-relationship edges separately. |
| `--format` | Choose `svg`, `pdf`, `png`, or another Graphviz format. |
| `--rankdir` | Use `LR` for left-to-right or `TB` for top-to-bottom layout. |
| `--layout-engine` | Use `dot`, `fdp`, `sfdp`, or `neato`. |

</br>
