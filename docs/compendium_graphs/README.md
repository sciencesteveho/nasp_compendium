# Compendium Mermaid graphs

These files are generated from `docs/compendium/*.md` and render directly on
GitHub. Regenerate them rather than editing them manually:

```sh
compendium render_mermaid_graphs \
  --compendium-path docs/compendium \
  --output-dir docs/compendium_graphs
```

`all_literature_graph.mermaid` combines every source file. The remaining
`.mermaid` files correspond one-to-one with compendium files; held-out inputs
retain `.gold` in the generated filename so they cannot overwrite a regular
paper graph with the same stem.

Node fill and border colors preserve entity classes. Edge color preserves the
relationship class, while solid, dashed, and dotted lines preserve evidence
strength. Mermaid cross endings approximate Graphviz inhibition tees, circle
endings represent correlation, and open edges represent explicit no-effect
relationships. The source comment above each edge records its exact
relationship, evidence strength, and papers.
