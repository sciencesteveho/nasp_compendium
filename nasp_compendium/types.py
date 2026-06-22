"""Shared space for misc public types."""

from __future__ import annotations

import dataclasses
from typing import Any, Literal, Protocol, TypeAlias

import pandas as pd


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
    """Signed gene lists for one marker-gene module."""

    module_id: str
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

    def as_dict(self) -> dict[str, Any]:
        """Return a plain dict."""
        return dataclasses.asdict(self)
