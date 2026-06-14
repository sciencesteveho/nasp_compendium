"""Display-name helpers for NASP docs and figures."""

from __future__ import annotations


MODULE_TOKEN_DISPLAY: dict[str, str] = {
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

MODULE_PHRASE_DISPLAY: tuple[tuple[str, str], ...] = (
    ("IFN I", "IFN-I"),
    ("OAS RNase L", "OAS/RNase L"),
)


def humanize_module_name(module_id: str) -> str:
    """Return a human-readable label for a marker-gene module id."""
    tokens = [
        token
        for token in module_id.strip().replace("-", "_").split("_")
        if token
    ]
    if not tokens:
        return ""

    words = [
        MODULE_TOKEN_DISPLAY.get(token.upper(), token.lower())
        for token in tokens
    ]
    label = " ".join(words)
    for source, replacement in MODULE_PHRASE_DISPLAY:
        label = label.replace(source, replacement)

    return label[:1].upper() + label[1:]
