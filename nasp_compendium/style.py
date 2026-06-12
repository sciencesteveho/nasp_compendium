"""Shared styling constants for NASP mechanism visualization."""

ENTITY_FIELDS: tuple[str, ...] = (
    "nucleic_acid_sensors",
    "genes",
    "pathways",
    "cell_types",
    "mechanisms",
    "model_systems",
    "evidence_type",
)

ENTITY_FILL_COLORS: dict[str, str] = {
    "nucleic_acid_sensors": "#FFF2CC",
    "genes": "#DCE6F2",
    "pathways": "#FCE4D6",
    "mechanisms": "#E2EFDA",
    "cell_types": "#FADBD8",
    "model_systems": "#E8DAEF",
    "evidence_type": "#EAEDED",
}

ENTITY_BORDER_COLORS: dict[str, str] = {
    "nucleic_acid_sensors": "#B45F06",
    "genes": "#4C72B0",
    "pathways": "#DD8452",
    "mechanisms": "#55A868",
    "cell_types": "#C44E52",
    "model_systems": "#8172B3",
    "evidence_type": "#937860",
}

DEFAULT_FILL_COLOR: str = "#F2F2F2"
DEFAULT_BORDER_COLOR: str = "#666666"

REL_ARROWHEAD: dict[str, str] = {
    "suppresses": "tee",
    "inhibits": "tee",
    "activates": "normal",
    "drives": "normal",
    "required_for": "normal",
    "produces": "normal",
    "causes": "normal",
    "binds_recruits": "normal",
    "correlates": "odot",
    "induces": "normal",
    "downregulates": "tee",
    "upregulates": "normal",
    "retains": "normal",
    "contains": "diamond",
    "negatively_correlates": "odot",
    "does_not_correlate": "none",
    "does_not_drive": "none",
    "forms_pore_for": "normal",
}

REL_COLOR: dict[str, str] = {
    "suppresses": "#C44E52",
    "inhibits": "#C44E52",
    "activates": "#55A868",
    "drives": "#55A868",
    "required_for": "#4C72B0",
    "produces": "#4C72B0",
    "causes": "#333333",
    "binds_recruits": "#8172B3",
    "correlates": "#999999",
    "induces": "#55A868",
    "downregulates": "#C44E52",
    "upregulates": "#55A868",
    "retains": "#55A868",
    "contains": "#8172B3",
    "negatively_correlates": "#C44E52",
    "does_not_correlate": "#CCCCCC",
    "does_not_drive": "#CCCCCC",
    "forms_pore_for": "#4C72B0",
}

EVIDENCE_STYLES: dict[str, str] = {
    "direct_measured": "solid",
    "perturbation_supported": "solid",
    "canonical_inferred": "dashed",
    "strong_correlative": "dotted",
    "weak_correlative": "dotted",
}

DEFAULT_REL_COLOR: str = "#555555"
DEFAULT_ARROWHEAD: str = "normal"
DEFAULT_EVIDENCE_STYLE: str = "solid"
