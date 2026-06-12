#!/usr/bin/env bash
#
# Bundled repo cleanup for nasp_compendium. Run from the repo root.
#
#   1. Make the `.gold.md` suffix hold papers out: the loader and validator
#      skip `*.gold.md`, so gold standards can live in docs/compendium/ without
#      entering the graph, the validation set, or the agent's style examples.
#   2. Move vocabulary.yaml out of the package into agent/ and repoint the one
#      path constant that loads it.
#   3. Remove the four drift terms that were double-listed under
#      canonical.mechanisms (they already live in the drift table).
#   4. Note the gold convention in AGENTS.md so the agent ignores `*.gold.md`.
#
# Every edit is anchored and asserted: if the repo has drifted from the expected
# text the script aborts instead of writing a wrong change. Safe to read before
# running; safe to re-run (it aborts cleanly once the edits are already applied).

set -euo pipefail

if [[ ! -f nasp_compendium/validate_compendium.py || ! -f nasp_compendium/summarize_compendium.py ]]; then
  echo "error: run this from the repo root (expected nasp_compendium/ package dir)." >&2
  exit 1
fi

# --- 1 + 2: edit the two package modules -----------------------------------
python3 - <<'PY'
import sys
from pathlib import Path


def replace_once(path, old, new):
  text = path.read_text()
  count = text.count(old)
  if count != 1:
    sys.exit(f"error: expected exactly one match in {path}, found {count}.\n"
             f"anchor:\n{old}")
  path.write_text(text.replace(old, new))
  print(f"patched: {path}")


summarize = Path("nasp_compendium/summarize_compendium.py")
validate = Path("nasp_compendium/validate_compendium.py")

# Gold-skip in Compendium.from_dir (covers render_graph, trace, diff).
replace_once(
    summarize,
    '        for md_path in sorted(directory.glob("*.md")):\n'
    '            file_papers, file_edges = parse_md(md_path)\n',
    '        for md_path in sorted(directory.glob("*.md")):\n'
    '            if md_path.name.endswith(".gold.md"):\n'
    '                continue\n'
    '            file_papers, file_edges = parse_md(md_path)\n',
)

# Gold-skip in validate_directory.
replace_once(
    validate,
    '    for path in sorted(directory.glob("*.md")):\n'
    '        data = _load_yaml_file(path, errors)\n',
    '    for path in sorted(directory.glob("*.md")):\n'
    '        if path.name.endswith(".gold.md"):\n'
    '            continue\n'
    '        data = _load_yaml_file(path, errors)\n',
)

# Repoint VOCABULARY_PATH at the new agent/ location.
replace_once(
    validate,
    'VOCABULARY_PATH: Path = Path(__file__).with_name("vocabulary.yaml")\n',
    'VOCABULARY_PATH: Path = (\n'
    '    Path(__file__).resolve().parent.parent / "agent" / "vocabulary.yaml"\n'
    ')\n',
)
PY

# --- move vocabulary.yaml into agent/ --------------------------------------
mkdir -p agent
if git ls-files --error-unmatch nasp_compendium/vocabulary.yaml >/dev/null 2>&1; then
  git mv nasp_compendium/vocabulary.yaml agent/vocabulary.yaml
  echo "moved (git): nasp_compendium/vocabulary.yaml -> agent/vocabulary.yaml"
else
  mv nasp_compendium/vocabulary.yaml agent/vocabulary.yaml
  echo "moved (fs):  nasp_compendium/vocabulary.yaml -> agent/vocabulary.yaml"
fi

# --- 3: drop the four double-listed drift terms from canonical.mechanisms ---
python3 - <<'PY'
import sys
from pathlib import Path

vocab = Path("agent/vocabulary.yaml")
text = vocab.read_text()
for term in (
    "CCF_formation",
    "chromatin_accessibility",
    "cytosolic_L1_cDNA_accumulation",
    "L1_de-repression",
):
  line = f"    - {term}\n"  # 4-space list item is unique to canonical.mechanisms
  count = text.count(line)
  if count != 1:
    sys.exit(f"error: expected one canonical.mechanisms entry for {term}, "
             f"found {count}. Leaving vocabulary.yaml unchanged.")
  text = text.replace(line, "")
vocab.write_text(text)
print(f"patched: {vocab} (removed 4 drift dupes from canonical.mechanisms)")
PY

# --- 4: note the gold convention in AGENTS.md ------------------------------
if [[ -f AGENTS.md ]]; then
  python3 - <<'PY'
from pathlib import Path

agents = Path("AGENTS.md")
text = agents.read_text()
anchor = "- `docs/compendium/`: per-paper mechanistic YAML-in-Markdown files.\n"
note = (
    "- `docs/compendium/`: per-paper mechanistic YAML-in-Markdown files. Files\n"
    "  ending in `.gold.md` are held-out calibration targets: the tooling skips\n"
    "  them and the agent must not read them as style examples until they are\n"
    "  promoted (renamed to `.md`).\n"
)
if note in text:
  print("skipped: AGENTS.md gold note already present")
elif text.count(anchor) == 1:
  agents.write_text(text.replace(anchor, note))
  print("patched: AGENTS.md (gold-file note)")
else:
  print("warning: AGENTS.md layout bullet not found; add the gold note by hand")
PY
fi

# --- caveat: is vocabulary.yaml declared as package data anywhere? ----------
if grep -RInq "vocabulary.yaml" pyproject.toml MANIFEST.in 2>/dev/null; then
  echo
  echo "note: pyproject.toml/MANIFEST.in references vocabulary.yaml. It is now"
  echo "      outside the package; for a non-editable (wheel) install, drop that"
  echo "      package-data entry or point it at agent/. Editable installs (-e)"
  echo "      read from the working tree and are unaffected."
fi

echo
echo "done. suggested check:"
echo "  compendium validate --dir docs/compendium"
