<div align="center">
  <h1>NASP knowledge compendium</h1>
</div>

Mechanism-centric curation and visualization of **N**ucleic **A**cid **S**ensing **P**athways (**NASP**).

+ a WIP agentic bio-entity-relationship extractor from literature.

<br>

## Installation
This repository is under active development.

### 1. System prerequisite: Graphviz


```sh
# macOS
brew install graphviz

# Debian / Ubuntu
sudo apt-get install graphviz

# Conda (cross-platform)
conda install -c conda-forge graphviz
```



### 2. Package install

```sh
conda create -n nasp_compendium python=3.11 -y
conda activate nasp_compendium
python -m pip install -U pip setuptools wheel

git clone https://github.com/sciencesteveho/nasp_compendium.git
cd nasp_compendium
pip install -e .
```

<br>

## Usage

### Render the pathway map

```sh
compendium render_graph \
  --directory docs/compendium \
  --annotate-papers
```

Options:

| Flag | Default | Notes |
|---|---|---|
| `--dir` / `--directory` | `docs/compendium` | Folder of per-paper Markdown files. |
| `--out` / `--output` | `nasp_pathway_map` | Output filename or stem. If an extension is included, it sets the format unless `--format` is also supplied. |
| `--format` | `png` | Any Graphviz output format (`svg`, `pdf`, `png`, …). |
| `--rankdir` | `LR` | Layout direction; `LR` left-to-right, `TB` top-to-bottom. |
| `--layout-engine` | `dot` | Graphviz layout engine. `dot` is directional; `fdp`, `sfdp`, and `neato` are more organic exploratory layouts. |
| `--annotate-papers` | off | Append a short paper citation to each edge label. |
| `--paper` / `--papers` | all papers | Render only selected paper IDs. May be repeated or comma-separated. |
| `--exclude-rel` / `--exclude-edge-type` | none | Omit selected relationship types, such as `does_not_correlate`. May be repeated or comma-separated. |
| `--no-aggregate-edges` | off | Render duplicate source-target-relationship edges separately instead of merging citations onto one edge. |
| `--compact` | off | Use tighter Graphviz spacing for denser pathway maps. |

Examples:

Render a single-paper graph:

```sh
compendium render_graph \
  --directory docs/compendium \
  --paper LopezPolo_natcomms_2024 \
  --annotate-papers \
  --output lopez_polo_2024.svg
```

Render a subset of papers:

```sh
compendium render_graph \
  --directory docs/compendium \
  --paper Dou_nature_2017,DeCecco_nature_2019 \
  --output cgas_sting_subset.pdf
```

Hide noisy edge classes:

```sh
compendium render_graph \
  --directory docs/compendium \
  --exclude-rel does_not_correlate \
  --exclude-rel does_not_drive \
  --output nasp_pathway_no_negative_edges.png
```

### Regenerate the marker-gene docs

```sh
compendium render_docs \
  --input data/marker_genes.tsv \
  --output-dir docs/marker_genes
```

### Trace an entity through the compendium

```sh
compendium trace CGAS
```

### Validate compendium files

```sh
compendium validate --dir docs/compendium
```

Use strict mode to treat warnings as failures:

```sh
compendium validate --dir docs/compendium --strict
```

Validation checks YAML shape, required edge fields, controlled relationship
and evidence vocabularies, undeclared edge endpoints, suspicious node names,
empty support/context fields, and duplicate exact edges.

### Diff two compendium states

```sh
compendium diff docs/compendium docs/compendium --format text
```

Each path can be either a compendium directory or a single `.md` file. The diff
reports paper IDs, paper-block entities, and graph edges added, removed, or
modified.

</br>
