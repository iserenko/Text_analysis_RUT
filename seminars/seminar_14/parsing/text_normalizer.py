from __future__ import annotations

import re
import unicodedata


def normalize_text(text: str) -> str:
    import re
    import unicodedata

    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u200b", "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ ]{2,}", " ", text)

    return text.strip()

