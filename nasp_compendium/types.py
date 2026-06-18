"""Shared space for misc public types."""

from __future__ import annotations

import dataclasses
from typing import Any, Literal, Protocol, TypeAlias, cast

import pandas as pd


ScorerName: TypeAlias = Literal["scanpy", "aucell"]
GeneIdOutput: TypeAlias = Literal["symbols", "var_names"]


class AnnDataLike(Protocol):
    """Minimal AnnData interface needed for gene validation."""

    @property
    def var(self) -> pd.DataFrame:
        """Return the variable (feature) metadata frame."""
        ...

    @property
    def var_names(self) -> pd.Index[Any]:
        """Return the variable (feature) names index."""
        ...


@dataclasses.dataclass(frozen=True)
class GeneModule:
    """Signed gene lists and scoring helpers for one marker-gene module."""

    module_id: str
    scorer: ScorerName
    positive_genes: tuple[str, ...]
    inverse_genes: tuple[str, ...]
    context_dependent_genes: tuple[str, ...]
    gene_id_output: GeneIdOutput
    missing_positive_genes: tuple[str, ...] = ()
    missing_inverse_genes: tuple[str, ...] = ()
    missing_context_dependent_genes: tuple[str, ...] = ()

    @property
    def genes(self) -> tuple[str, ...]:
        """Return all genes in stable module order."""
        return (
            self.positive_genes
            + self.inverse_genes
            + self.context_dependent_genes
        )

    @property
    def has_inverse_genes(self) -> bool:
        """Return whether this module has inverse-scored genes."""
        return bool(self.inverse_genes)

    @property
    def positive_score_name(self) -> str:
        """Return the suggested positive score column name."""
        suffix = "pos" if self.scorer == "scanpy" else "pos_auc"
        return f"{self.module_id}_{suffix}"

    @property
    def inverse_score_name(self) -> str | None:
        """Return the suggested inverse score column name, if needed."""
        if not self.inverse_genes:
            return None
        suffix = "inv" if self.scorer == "scanpy" else "inv_auc"
        return f"{self.module_id}_{suffix}"

    @property
    def score_name(self) -> str:
        """Return the suggested final signed score column name."""
        suffix = "score" if self.scorer == "scanpy" else "auc"
        return f"{self.module_id}_{suffix}"

    def scanpy_score_kwargs(
        self,
        *,
        random_state: int = 0,
    ) -> list[dict[str, Any]]:
        """Return kwargs for sc.tl.score_genes (one per signed gene set).

        Args:
          random_state: Seed forwarded to scanpy.

        Returns:
          A kwargs dict for the positive set when positive genes exist, and a
          second for the inverse set when inverse genes exist.
        """
        calls: list[dict[str, Any]] = []

        if self.positive_genes:
            calls.append(
                {
                    "gene_list": list(self.positive_genes),
                    "score_name": self.positive_score_name,
                    "random_state": random_state,
                }
            )

        inverse_name = self.inverse_score_name
        if self.inverse_genes and inverse_name is not None:
            calls.append(
                {
                    "gene_list": list(self.inverse_genes),
                    "score_name": inverse_name,
                    "random_state": random_state,
                }
            )
        return calls

    def gene_sets(self) -> dict[str, list[str]]:
        """Return named gene sets for AUCell keyed by sub-score name.

        Returns:
          A mapping with the positive set when present and the inverse set
          when present.
        """
        sets: dict[str, list[str]] = {}
        if self.positive_genes:
            sets[self.positive_score_name] = list(self.positive_genes)

        inverse_name = self.inverse_score_name
        if self.inverse_genes and inverse_name is not None:
            sets[inverse_name] = list(self.inverse_genes)

        return sets

    def combine_scores(self, scores: pd.DataFrame) -> pd.Series:
        """Combine sub-scores into a signed module score.

        Args:
          scores: Per-cell frame carrying the positive sub-score and the
          inverse sub-score when the module has one.

        Returns:
          positive_score - inverse_score when both exist, the positive score
          alone when there is no inverse set, or the negated inverse score when
          there is no positive set. The Series is named score_name.

        Raises:
          ValueError: If the module has neither positive nor inverse genes.
        """
        inverse_name = self.inverse_score_name
        if self.positive_genes and inverse_name is not None:
            combined = scores[self.positive_score_name] - scores[inverse_name]
            return cast("pd.Series", combined).rename(self.score_name)
        if self.positive_genes:
            positive = cast("pd.Series", scores[self.positive_score_name])
            return positive.rename(self.score_name)
        if inverse_name is not None:
            inverse = cast("pd.Series", scores[inverse_name])
            return (-inverse).rename(self.score_name)
        raise ValueError(
            f"Module {self.module_id!r} has no scorable genes to combine."
        )

    def as_dict(self) -> dict[str, Any]:
        """Return a plain dict."""
        return dataclasses.asdict(self)
