# Compendium Mermaid graphs

These files are generated from `docs/compendium/*.md` and render directly on
GitHub. Regenerate them rather than editing them manually:

```sh
compendium render_mermaid_graphs \
  --compendium-path docs/compendium \
  --output-dir docs/compendium_graphs
```

`all_literature_graph.mermaid` combines accepted records only. Ordinary graph
generation excludes `.gold.md` references, forbidden shortcuts and excluded
claims. The current accepted collection contains Gulen; candidate records
enter it only after scientific approval. Per-paper files use the same rule.

Earlier graph snapshots included evaluation references. They are preserved in
[the refactor archive](../../agent/archive/pre_refactor_20261007/compendium_graphs/)
and are not current collective-graph assertions. The
[reference audit](../gold_review/20261007_audit.md) provides proposed corrections
with interactive evidence reviews.

Node fill and border colors preserve entity classes. Edge color preserves the
relationship class, while solid, dashed, and dotted lines preserve evidence
strength. Mermaid cross endings approximate Graphviz inhibition tees, circle
endings represent correlation, and open edges represent explicit no-effect
relationships. The source comment above each edge records its exact
relationship, evidence strength, and papers.
