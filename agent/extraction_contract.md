# Evidence and record contract

Extract mechanistic insight about nucleic-acid sensing in aging, senescence,
inflammation and related disease. The paper establishes the claims; the graph
makes them navigable. A valid file is not necessarily a valid interpretation.

## Scientific decisions

For each finding identify **intervention → measured outcome → result → scope**.
Observational findings identify the comparison instead of an intervention.
Read Results and relevant figures, methods and controls; an abstract or author
model alone cannot establish an edge.

- Perturbing A and observing B and C establishes scoped A–B and A–C effects.
  It does not establish B→C. Rescue, epistasis or a specific mediator test can
  establish that missing step. Preserve experimentally resolved intermediates.
- A distal functional effect is legitimate when tested. Do not force it through
  tissue phenotypes or a textbook pathway whose intermediate roles were not
  resolved. State in context that mediation remains unresolved.
- Distinguish binding, abundance, activation and function. Co-localization is
  not recruitment; motif enrichment is not regulator perturbation; sensor
  abundance is not evidence of ligand recognition. Combined perturbations do
  not isolate each component's role.
- Keep central ligands, mediators, regulators, branches, specificity controls
  and tested negative results. Marker panels usually describe a program in
  context. Promote a marker to a mechanistic node only when its role is tested;
  retain an individual association only when useful to the paper's question.
- A negative edge describes a tested lack of effect under stated conditions.
  Absent promoter binding does not exclude an indirect functional effect.
  Unmeasured outcomes are not negative findings. Report uncertainty and power
  limits without turning nonsignificance into universal absence.
- Distinguish chronological age, cellular senescence, lifespan, mortality,
  inflammation signatures and model predictions. Do not invert or substitute
  these endpoints without an explicit analysis establishing the relationship.
- A canonical intermediate can provide optional context but is not a discovery
  of this paper. Keep an untested author hypothesis in review notes. A graph
  may be branched or incomplete; do not invent continuity.

## Identity and evidence

Use human gene symbols for genes, preserving species in context. Normalize
reusable programs/ligands using `agent/vocabulary.yaml`, the reviewed source of
terms and explicit aliases (`drift`). Use stable biological entities: put dose,
reagent, tissue, timing, expression/modification state and assay in context.
Represent a tested pore as pore→released ligand; include its constituent gene
only when a paper tests that constituent. Do not merge independently supported
sensor branches as interchangeable representations.

A new biological term is allowed: add a top-level `proposed_terms` list of
`{term: ..., reason: ...}` records. It produces a review warning. Never rebuild
vocabulary automatically from golds or drafts. New gene symbols belong in the
paper's `genes` list; this declares identity, not biological validity.

Choose evidence for the relationship itself:

| Label | Meaning |
| --- | --- |
| `direct_measured` | The stated relationship is directly assayed, e.g. binding or enzyme product; measuring both endpoints is insufficient. |
| `perturbation_supported` | Manipulating the source changes the target; specify intervention, readout and limits on specificity/mediation. |
| `strong_correlative` | A defined, well-supported association without a causal intervention. |
| `weak_correlative` | Exploratory/limited association, with its limitations stated. |
| `canonical_inferred` | Established background continuity, explicitly identified as untested here. |

Use the narrowest accurate relationship:
`activates`, `suppresses`, `induces`, `drives`, `required_for`, `upregulates`,
`downregulates`, `produces`, `forms_pore_for`, `binds_recruits`,
`retains`, `contains`, `correlates`, `negatively_correlates`,
`does_not_correlate`, `does_not_drive`, `inhibits`, `causes`.
Use `binds_recruits` only for demonstrated physical binding/recruitment;
`contains` states composition, not causality. `upregulates`/`downregulates`
describe abundance. Association and negative labels must remain explicit.

## Public record

A `.md` file contains plain YAML, without Markdown fences. Keep `paper` and
`edges`; optional term proposals are the only extra extraction block.

```yaml
paper:
  author_2026:
    cite: Author et al. (2026)
    url: https://doi.org/REPLACE
    summary: Brief paper-specific result, including its experimental scope.
    nucleic_acid_sensors: []
    genes: []
    pathways: []
    cell_types: []
    mechanisms: []
    model_systems: []
    evidence_type: []
    notes: Important limitations.
    relevance_to_project: Why this finding belongs in NASP.
edges:
  - chain_id: descriptive_branch
    step: 1
    source: SOURCE
    target: TARGET
    rel: activates
    evidence_strength: perturbation_supported
    context: Intervention, system, measured change, and mechanistic limits.
    support: main p. 4; Fig. 2b,c
    papers: [author_2026]
```

Use one-based **PDF page numbers**, not printed journal pagination. Each
support string includes a locator `main p. N` or `supplement_1 p. N` plus the
panel or Results passage. Cite multiple pages by repeating the source locator.
Source preparation assigns supplement IDs in supplied order. Panel wording
must match the actual paper. Rendering a cited page does not validate its claim.

Chains organize related findings; step numbers do not supply missing causality.
Keep context-specific edges separate when experiments differ. Each edge needs
non-empty context/support and a declared paper ID. Empty results require an
explained `--no-findings` disposition. Never fabricate an edge to pass a gate.

Evaluation-only fields (`tier`, `equiv_group`, `status`, `score_exclude`) belong
in reference files, not extraction drafts. Inferred continuity is supporting,
not core discovery. Unmatched reference comparisons require source review;
reference omission does not make a draft edge false.
