"use strict";
const data = JSON.parse(document.getElementById("review-data").textContent);
const el = id => document.getElementById(id);
let current, zoom = 1;
const text = (tag, value, parent) => { const item = document.createElement(tag); item.textContent = value; parent.append(item); return item; };
el("summary").textContent = Object.values(data.views.paper.papers)[0].summary;
el("status").textContent = `Awaiting scientific review · supplements: ${data.manifest.supplement_coverage} · ${data.manifest.disposition.replaceAll("_", " ")}`;
el("notes").textContent = [data.manifest.notes || "No unresolved findings recorded.", ...data.manifest.validation_warnings].join("\n\n");
el("diff").textContent = data.diff;
for (const source of data.manifest.sources) text("p", `${source.id}: ${source.pages} PDF pages · SHA-256 ${source.sha256} · sparse text pages: ${source.sparse_text_pages.join(", ") || "none"}`, el("sources"));
function applyZoom() { const svg = el("canvas").querySelector("svg"); if(svg) { svg.style.width = `${svg.viewBox.baseVal.width * zoom}px`; svg.style.height = `${svg.viewBox.baseVal.height * zoom}px`; } }
function loadView() {
  current = data.views[el("view").value];
  el("canvas").innerHTML = current.svg;
  el("paper").replaceChildren(); text("option", "All papers", el("paper")).value = "";
  for (const paper of Object.keys(current.papers)) text("option", paper, el("paper")).value = paper;
  el("entities").replaceChildren(); for (const node of Object.keys(current.nodes)) text("option", node, el("entities")).value = node;
  for (const [node, id] of Object.entries(current.nodes)) el(id)?.addEventListener("click", () => { el("entity").value = node; filter(); });
  for (let index=0; index<current.edges.length; index++) el(`edge_${index}`)?.addEventListener("click", () => showEvidence(index));
  el("evidence").textContent = "Select a claim."; zoom=1; applyZoom(); filter();
}
function filteredRecords(edge) { return edge.evidence_records.filter(record => !el("paper").value || record.papers.includes(el("paper").value)); }
function filter() {
  el("claims").replaceChildren(); const nodes = new Set(); let count = 0;
  current.edges.forEach((edge, index) => {
    const query = el("entity").value.trim().toLowerCase();
    const inferred = edge.evidence_strength === "canonical_inferred";
    const association = ["correlates", "negatively_correlates", "does_not_correlate"].includes(edge.rel);
    const visible = (!inferred || el("inferred").checked) && (!association || el("associations").checked) && filteredRecords(edge).length && (!query || [edge.source,edge.target].some(node => node.toLowerCase().includes(query)));
    el(`edge_${index}`).style.display = visible ? "" : "none";
    if (visible) { count++; nodes.add(edge.source); nodes.add(edge.target); const button = text("button", `${edge.source} → ${edge.target} · ${edge.rel.replaceAll("_"," ")}`, el("claims")); button.addEventListener("click", () => showEvidence(index)); }
  });
  for (const [node, id] of Object.entries(current.nodes)) el(id).style.display = nodes.has(node) ? "" : "none";
  el("count").textContent = `${count} of ${current.edges.length} relationships visible · ${nodes.size} entities`;
  if (!count && current.edges.length) text("p", "No claims match these controls. Clear the paper/entity filter or enable associations and inferred continuity.", el("claims"));
  el("evidence").textContent = "Select a visible claim.";
}
function showEvidence(index) {
  const edge = current.edges[index], panel = el("evidence"); panel.replaceChildren();
  document.querySelectorAll("#canvas .selected").forEach(item => item.classList.remove("selected")); el(`edge_${index}`).classList.add("selected");
  text("h3", `${edge.source} ${edge.rel.replaceAll("_"," ")} ${edge.target}`, panel);
  for (const record of filteredRecords(edge)) {
    const block = text("div", "", panel); block.className = "record";
    text("p", `${record.papers.join(", ")} · ${record.evidence_strength.replaceAll("_"," ")}`, block).className="badge";
    text("p", record.context, block); text("p", record.support, block);
    for (const link of record.source_links) {
      const a = text("a", `Open ${link.label} in PDF`, block); a.href=link.pdf; a.target="_blank"; a.rel="noopener";
      const imageLink = text("a", "", block); imageLink.href=link.image; imageLink.target="_blank";
      const image = document.createElement("img"); image.src=link.image; image.alt=`Evidence page ${link.label}`; image.loading="lazy"; imageLink.append(image);
    }
    if (!record.source_links.length) text("p", "Legacy evidence: locator is shown above; this paper has no source pages attached to this run.", block);
  }
}
el("view").addEventListener("change", loadView);
for (const id of ["entity","paper","inferred","associations"]) el(id).addEventListener("input", filter);
el("plus").addEventListener("click", () => { zoom=Math.min(4,zoom*1.25); applyZoom(); });
el("minus").addEventListener("click", () => { zoom=Math.max(.2,zoom/1.25); applyZoom(); });
el("reset").addEventListener("click", () => { el("entity").value=""; el("paper").value=""; zoom=1; applyZoom(); filter(); });
loadView();
