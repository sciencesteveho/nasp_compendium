"""Display-name helpers for NASP docs and figures."""

from __future__ import annotations


MODULE_NAME_DISPLAY: dict[str, str] = {
    "CGAMP_TRANSPORT": "cGAMP transport",
    "ISR": "Integrated stress response",
    "NASP_DNA_SENSING": "DNA sensing",
    "NASP_RNA_SENSING": "RNA sensing",
    "SIGNALING_CONTEXT_IFN_JAK_STAT": "Signaling context IFN JAK/STAT",
    "SIGNALING_CONTEXT_TBK1_IRF": "Signaling context TBK1-IRF",
    "SIGNALING_CONTEXT_TLR": "Signaling context TLR",
}

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
    normalized_module_id = module_id.strip().replace("-", "_").upper()
    if normalized_module_id in MODULE_NAME_DISPLAY:
        return MODULE_NAME_DISPLAY[normalized_module_id]

    tokens = [
        token
        for token in normalized_module_id.split("_")
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
