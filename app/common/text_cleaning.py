import re


def clean_text(value: str | None) -> str:
    if not value:
        return ""

    text = value.lower().strip()
    text = re.sub(r"\s+", " ", text)

    return text


def combine_text(*values: str | None) -> str:
    return clean_text(" ".join([value for value in values if value]))
