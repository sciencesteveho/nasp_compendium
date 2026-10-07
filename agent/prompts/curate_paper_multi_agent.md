# Optional independent review

Follow the single-paper extraction prompt and contract. The parent is the only
writer. Gate and hash-freeze the initial draft in its run before review.

Launch `recall_reviewer` and `precision_reviewer` in parallel with the same PDF,
available supplements, frozen draft/hash and current instructions. Give neither
golds, prior audit answers, expected findings, nor the other's findings. They
remain read-only. Recall searches for omitted mechanisms; precision checks
emitted claims. Require concrete proposed changes and source page/panel evidence.

Wait for both before editing. Check the frozen hash. Adjudicate each proposal
against sources, recording accept/reject/modify, support and reason in run notes.
Write a revised working draft, rerun exact validation and freeze a new review
revision. Show the initial/revised diff and unresolved points. Never promote or
commit through this optional workflow. During blind evaluation use an isolated
collection for review previews. Follow the held-out protocol before claiming
reviewer benefit.
