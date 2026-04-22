import re


def clean_resume_text(text: str) -> str:
    text = text.replace("\x00", "")
    text = re.sub(r"[\ue000-\uf8ff]", "", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)

    lines = [line.strip() for line in text.split("\n")]
    normalized = "\n".join(lines)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)

    return normalized.strip()


def build_text_preview(text: str, max_length: int = 2000) -> str:
    if len(text) <= max_length:
        return text

    return f"{text[:max_length].rstrip()}..."
