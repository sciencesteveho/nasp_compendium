"""Structured text diffs between two NASP compendium states."""

from __future__ import annotations

import dataclasses
import re
from pathlib import Path
from typing import Any

from nasp_compendium import summarize_compendium
from nasp_compendium.style import ENTITY_FIELDS


@dataclasses.dataclass(frozen=True)
class EdgeKey:
    """Stable identity for one graph edge."""

    source: str
    target: str
    rel: str
    papers: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class EdgeChange:
    """An added or removed edge with its chain context."""

    key: EdgeKey
    edge: dict[str, Any]


@dataclasses.dataclass(frozen=True)
class ModifiedEdge:
    """An edge whose identity is unchanged but supported fields changed."""

    key: EdgeKey
    old_edge: dict[str, Any]
    new_edge: dict[str, Any]
    changed_fields: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class CompendiumDiff:
    """Structured diff result between two compendium states."""

    papers_added: tuple[str, ...]
    papers_removed: tuple[str, ...]
    entities_added: dict[str, dict[str, tuple[str, ...]]]
    entities_removed: dict[str, dict[str, tuple[str, ...]]]
    edges_added: tuple[EdgeChange, ...]
    edges_removed: tuple[EdgeChange, ...]
    edges_modified: tuple[ModifiedEdge, ...]

    @property
    def entity_added_count(self) -> int:
        """Return total number of added paper-block entity entries."""
        return _count_entities(self.entities_added)

    @property
    def entity_removed_count(self) -> int:
        """Return total number of removed paper-block entity entries."""
        return _count_entities(self.entities_removed)

    @property
    def has_changes(self) -> bool:
        """Return whether the diff contains any semantic changes."""
        return any(
            (
                self.papers_added,
                self.papers_removed,
                self.entity_added_count,
                self.entity_removed_count,
                self.edges_added,
                self.edges_removed,
                self.edges_modified,
            )
        )


def load_compendium_path(path: Path) -> summarize_compendium.Compendium:
    """Load either a compendium directory or a single compendium Markdown
    file.
    """
    if path.is_dir():
        return summarize_compendium.Compendium.from_dir(path)
    if path.is_file():
        papers, edges = summarize_compendium.parse_md(path)
        return summarize_compendium.Compendium(papers=papers, edges=edges)
    raise FileNotFoundError(f"Compendium path not found: {path}")


def diff_paths(old_path: Path, new_path: Path) -> CompendiumDiff:
    """Load two compendium paths and return their structured diff."""
    old = load_compendium_path(old_path)
    new = load_compendium_path(new_path)
    return diff_compendia(old, new)


def diff_compendia(
    old: summarize_compendium.Compendium,
    new: summarize_compendium.Compendium,
) -> CompendiumDiff:
    """Return a structured diff between two loaded compendia."""
    old_papers = set(old.papers)
    new_papers = set(new.papers)
    edge_diff = _diff_edges(old.edges, new.edges)

    return CompendiumDiff(
        papers_added=tuple(sorted(new_papers - old_papers)),
        papers_removed=tuple(sorted(old_papers - new_papers)),
        entities_added=_diff_entities(old.papers, new.papers, added=True),
        entities_removed=_diff_entities(old.papers, new.papers, added=False),
        edges_added=edge_diff[0],
        edges_removed=edge_diff[1],
        edges_modified=edge_diff[2],
    )


def format_diff(diff: CompendiumDiff, output_format: str = "text") -> str:
    """Format a structured diff as text or Markdown."""
    if output_format == "markdown":
        return _format_markdown(diff)
    if output_format == "text":
        return _format_text(diff)
    raise ValueError(f"Unsupported diff format: {output_format}")


def _diff_entities(
    old_papers: dict[str, dict[str, Any]],
    new_papers: dict[str, dict[str, Any]],
    *,
    added: bool,
) -> dict[str, dict[str, tuple[str, ...]]]:
    """Diff paper-block entity fields, grouped by paper and field."""
    result: dict[str, dict[str, tuple[str, ...]]] = {}
    for paper_id in sorted(set(old_papers) | set(new_papers)):
        old_paper = old_papers.get(paper_id, {})
        new_paper = new_papers.get(paper_id, {})
        field_changes: dict[str, tuple[str, ...]] = {}
        for field in ENTITY_FIELDS:
            old_values = _paper_values(old_paper, field)
            new_values = _paper_values(new_paper, field)
            values = (
                new_values - old_values if added else old_values - new_values
            )
            if values:
                field_changes[field] = tuple(sorted(values))
        if field_changes:
            result[paper_id] = field_changes
    return result


def _diff_edges(
    old_edges: list[dict[str, Any]],
    new_edges: list[dict[str, Any]],
    *,
    compare_fields: tuple[str, ...] = (
        "evidence_strength",
        "context",
        "support",
    ),
) -> tuple[
    tuple[EdgeChange, ...],
    tuple[EdgeChange, ...],
    tuple[ModifiedEdge, ...],
]:
    """Diff edge lists by stable identity and comparable fields."""
    old_by_key = _edges_by_key(old_edges)
    new_by_key = _edges_by_key(new_edges)
    old_keys = set(old_by_key)
    new_keys = set(new_by_key)

    added = tuple(
        EdgeChange(key=key, edge=new_by_key[key])
        for key in sorted(new_keys - old_keys, key=_edge_sort_key)
    )
    removed = tuple(
        EdgeChange(key=key, edge=old_by_key[key])
        for key in sorted(old_keys - new_keys, key=_edge_sort_key)
    )
    modified = []
    for key in sorted(old_keys & new_keys, key=_edge_sort_key):
        if changed_fields := tuple(
            field
            for field in compare_fields
            if _normalize_value(old_by_key[key].get(field))
            != _normalize_value(new_by_key[key].get(field))
        ):
            modified.append(
                ModifiedEdge(
                    key=key,
                    old_edge=old_by_key[key],
                    new_edge=new_by_key[key],
                    changed_fields=changed_fields,
                )
            )

    return added, removed, tuple(modified)


def _edges_by_key(edges: list[dict[str, Any]]) -> dict[EdgeKey, dict[str, Any]]:
    """Index edge dictionaries by source, target, rel, and papers tuple."""
    result: dict[EdgeKey, dict[str, Any]] = {}
    for edge in edges:
        key = _edge_key(edge)
        if key is not None:
            result[key] = edge
    return result


def _edge_key(edge: dict[str, Any]) -> EdgeKey | None:
    """Return a stable edge identity key if all required identity fields
    exist.
    """
    papers = edge.get("papers")
    if not isinstance(papers, list) or not papers:
        return None
    source = edge.get("source")
    target = edge.get("target")
    rel = edge.get("rel")
    if source is None or target is None or rel is None:
        return None
    return EdgeKey(
        source=_normalize_identity(source),
        target=_normalize_identity(target),
        rel=_normalize_identity(rel),
        papers=tuple(_normalize_identity(paper) for paper in papers),
    )


def _format_text(diff: CompendiumDiff) -> str:
    """Format a compact terminal-readable diff."""
    lines = [
        "Compendium diff",
        _summary_line(diff),
    ]
    if not diff.has_changes:
        lines.append("No compendium differences.")
        return "\n".join(lines)

    _append_papers(lines, diff, markdown=False)
    _append_entities(
        lines, "Entities added", diff.entities_added, markdown=False
    )
    _append_entities(
        lines, "Entities removed", diff.entities_removed, markdown=False
    )
    _append_edge_changes(lines, "Edges added", diff.edges_added, markdown=False)
    _append_edge_changes(
        lines, "Edges removed", diff.edges_removed, markdown=False
    )
    _append_modified_edges(lines, diff.edges_modified, markdown=False)
    return "\n".join(lines)


def _format_markdown(diff: CompendiumDiff) -> str:
    """Format a Markdown report for a structured compendium diff."""
    lines = [
        "# Compendium Diff",
        "",
        f"**Summary:** {_summary_line(diff)}",
    ]
    if not diff.has_changes:
        lines.extend(("", "No compendium differences."))
        return "\n".join(lines)

    _append_papers(lines, diff, markdown=True)
    _append_entities(
        lines, "Entities Added", diff.entities_added, markdown=True
    )
    _append_entities(
        lines, "Entities Removed", diff.entities_removed, markdown=True
    )
    _append_edge_changes(lines, "Edges Added", diff.edges_added, markdown=True)
    _append_edge_changes(
        lines, "Edges Removed", diff.edges_removed, markdown=True
    )
    _append_modified_edges(lines, diff.edges_modified, markdown=True)
    return "\n".join(lines)


def _append_papers(
    lines: list[str],
    diff: CompendiumDiff,
    *,
    markdown: bool,
) -> None:
    """Append paper added/removed sections to formatted output."""
    if not diff.papers_added and not diff.papers_removed:
        return
    _append_heading(lines, "Papers", markdown=markdown)
    if diff.papers_added:
        lines.append(f"  + added: {', '.join(diff.papers_added)}")
    if diff.papers_removed:
        lines.append(f"  - removed: {', '.join(diff.papers_removed)}")


def _append_entities(
    lines: list[str],
    title: str,
    entities: dict[str, dict[str, tuple[str, ...]]],
    *,
    markdown: bool,
) -> None:
    """Append entity changes grouped by paper and entity field."""
    if not entities:
        return
    _append_heading(lines, title, markdown=markdown)
    for paper_id, fields in entities.items():
        lines.append(f"- {paper_id}" if markdown else f"  {paper_id}")
        for field, values in fields.items():
            prefix = "  - " if markdown else "    "
            lines.append(f"{prefix}{field}: {', '.join(values)}")


def _append_edge_changes(
    lines: list[str],
    title: str,
    changes: tuple[EdgeChange, ...],
    *,
    markdown: bool,
) -> None:
    """Append added or removed edges grouped by chain."""
    if not changes:
        return
    _append_heading(lines, title, markdown=markdown)
    for chain_id, chain_changes in _group_edge_changes(changes).items():
        lines.append(f"- {chain_id}" if markdown else f"  {chain_id}")
        for change in chain_changes:
            prefix = "  - " if markdown else "    "
            lines.append(f"{prefix}{_format_edge_key(change.key)}")


def _append_modified_edges(
    lines: list[str],
    changes: tuple[ModifiedEdge, ...],
    *,
    markdown: bool,
) -> None:
    """Append modified edges grouped by chain."""
    if not changes:
        return
    _append_heading(lines, "Edges Modified", markdown=markdown)
    for chain_id, chain_changes in _group_modified_edges(changes).items():
        lines.append(f"- {chain_id}" if markdown else f"  {chain_id}")
        for change in chain_changes:
            prefix = "  - " if markdown else "    "
            fields = ", ".join(change.changed_fields)
            lines.append(f"{prefix}{_format_edge_key(change.key)}")
            detail_prefix = "    - " if markdown else "      "
            lines.append(f"{detail_prefix}changed: {fields}")


def _append_heading(
    lines: list[str],
    title: str,
    *,
    markdown: bool,
) -> None:
    """Append a section heading in the requested output style."""
    lines.extend(("", f"## {title}" if markdown else title))


def _group_edge_changes(
    changes: tuple[EdgeChange, ...],
) -> dict[str, list[EdgeChange]]:
    """Group edge changes by chain id in insertion order."""
    grouped: dict[str, list[EdgeChange]] = {}
    for change in changes:
        chain_id = str(change.edge.get("chain_id") or "(no_chain)")
        grouped.setdefault(chain_id, []).append(change)
    return grouped


def _group_modified_edges(
    changes: tuple[ModifiedEdge, ...],
) -> dict[str, list[ModifiedEdge]]:
    """Group modified edges by new chain id in insertion order."""
    grouped: dict[str, list[ModifiedEdge]] = {}
    for change in changes:
        chain_id = str(change.new_edge.get("chain_id") or "(no_chain)")
        grouped.setdefault(chain_id, []).append(change)
    return grouped


def _format_edge_key(key: EdgeKey) -> str:
    """Format an edge key as a compact source-rel-target listing."""
    papers = ", ".join(key.papers)
    return f"{key.source} --[{key.rel}]--> {key.target} ({papers})"


def _summary_line(diff: CompendiumDiff) -> str:
    """Return the compact count summary for a diff."""
    return (
        f"{len(diff.papers_added)} papers added, "
        f"{len(diff.papers_removed)} papers removed, "
        f"{diff.entity_added_count} entities added, "
        f"{diff.entity_removed_count} entities removed, "
        f"{len(diff.edges_added)} edges added, "
        f"{len(diff.edges_removed)} edges removed, "
        f"{len(diff.edges_modified)} edges modified"
    )


def _paper_values(paper: dict[str, Any], field: str) -> set[str]:
    """Return normalized string values from one paper metadata field."""
    values = paper.get(field)
    return (
        {str(value) for value in values} if isinstance(values, list) else set()
    )


def _count_entities(entities: dict[str, dict[str, tuple[str, ...]]]) -> int:
    """Count entity changes in a nested paper-field mapping."""
    return sum(
        len(values)
        for fields in entities.values()
        for values in fields.values()
    )


def _edge_sort_key(key: EdgeKey) -> tuple[str, str, str, tuple[str, ...]]:
    """Return a deterministic sort key for edge keys."""
    return (key.source, key.target, key.rel, key.papers)


def _normalize_identity(value: object) -> str:
    """Normalize identity fields without changing semantic spelling."""
    return str(value).strip()


def _normalize_value(value: object) -> str:
    """Normalize comparable fields so whitespace-only changes are ignored."""
    return "" if value is None else re.sub(r"\s+", " ", str(value)).strip()
