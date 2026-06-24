"""Display-name helpers for NASP docs and figures."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType


MODULE_NAME_DISPLAY: dict[str, str] = {
    "CGAMP_TRANSPORT": "cGAMP transport",
    "ISR": "Integrated stress response",
    "NASP_DNA_SENSING": "DNA sensing",
    "NASP_RNA_SENSING": "RNA sensing",
    "SIGNALING_CONTEXT_IFN_JAK_STAT": "Signaling context IFN JAK/STAT",
    "SIGNALING_CONTEXT_TBK1_IRF": "Signaling context TBK1-IRF",
    "SIGNALING_CONTEXT_TLR": "Signaling context TLR",
}


def humanize_module_name(
    module_id: str,
    *,
    token_display: Mapping[str, str] = MappingProxyType(
        {
            "CGAMP": "cGAMP",
            "DNA": "DNA",
            "IFN": "IFN",
            "I": "I",
            "II": "II",
            "III": "III",
            "ISR": "ISR",
            "NA": "nucleic acid",
            "NASP": "NASP",
            "NFKB": "NF-κB",
            "OAS": "OAS",
            "RNA": "RNA",
            "RNASEL": "RNase L",
            "SASP": "SASP",
            "TE": "TE",
        }
    ),
    phrase_display: tuple[tuple[str, str], ...] = (
        ("IFN I", "IFN-I"),
        ("OAS RNase L", "OAS/RNase L"),
    ),
) -> str:
    """Return a human-readable label for a marker-gene module id."""
    normalized_module_id = module_id.strip().replace("-", "_").upper()
    if normalized_module_id in MODULE_NAME_DISPLAY:
        return MODULE_NAME_DISPLAY[normalized_module_id]

    tokens = [token for token in normalized_module_id.split("_") if token]
    if not tokens:
        return ""

    words = [
        token_display.get(token.upper(), token.lower()) for token in tokens
    ]
    label = " ".join(words)
    for source, replacement in phrase_display:
        label = label.replace(source, replacement)

    return label[:1].upper() + label[1:]
