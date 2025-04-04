import re
from html import unescape

def clean_text(text: str) -> str:
    if not text:
        return ""

    # Remove tags HTML
    text = re.sub(r"<[^>]+>", " ", text)

    # Substitui quebras de linha e tabulação por espaço
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")

    # Remove aspas triplas, especiais e caracteres invisíveis
    text = text.replace('"""', '"').replace("ã»", "").replace("“", '"').replace("”", '"')

    # Remove espaços duplicados
    text = re.sub(r"\s+", " ", text)

    # Remove emojis e caracteres não UTF-8 (opcional)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # Decode entidades HTML
    return unescape(text).strip()
