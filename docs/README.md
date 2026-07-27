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

PDF graph output requires `rsvg-convert` from librsvg so text can be stored as
fixed vector outlines rather than viewer-dependent font objects.

`render_graph`: writes one combined figure containing every
compendium `*.md` file:

```sh
compendium render_graph \
  --compendium-path docs/compendium \
  --out figures/all_literature_graph.pdf
```

Use `--paper PAPER_ID` with `render_graph` to render a selected subset instead.

</br>

`render_paper_graphs` writes one figure for each compendium `*.md` file:
```sh
compendium render_paper_graphs \
  --compendium-path docs/compendium \
  --output-dir figures \
  --format pdf
```

Both commands also accept `--annotate-papers`, `--compact`,
`--rankdir`, `--layout-engine`, `--exclude-rel`, and
`--no-aggregate-edges`.

Generate one combined Mermaid source and one source per compendium file:

```sh
compendium render_mermaid_graphs \
  --compendium-path docs/compendium \
  --output-dir docs/compendium_graphs
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
