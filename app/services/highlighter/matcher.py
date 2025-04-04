
def check_highlight(text: str, highlight: str) -> tuple[bool, int]:
    count = text.lower().count(highlight.lower())
    return count > 0, count
