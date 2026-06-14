<div align="center">
  <h1>NASP knowledge compendium</h1>
</div>

Mechanism-centric curation and visualization of **N**ucleic **A**cid
**S**ensing **P**athways (**NASP**).

This repository contains two connected parts:

1. [**An agentic curation tool** for extracting mechanistic relationships
   from literature](agent/README.md).

2.  [**A data compendium** of marker-gene modules and curated paper-level mechanism files with visualizations.](docs/README.md).

</br>
Follow the linked `README.md` files for detailed usage.

</br>

## Installation

This repository is under *active development* and `pyproject.toml` may not be fully up to date.

#### 2. Package install

```sh
# system prerequisite
conda install -c conda-forge graphviz

# prepare a fresh conda environment
conda create -n nasp_compendium python=3.11 -y
conda activate nasp_compendium
python -m pip install -U pip setuptools wheel

# download and install from source
git clone https://github.com/sciencesteveho/nasp_compendium.git
cd nasp_compendium
pip install -e .
```

</br>