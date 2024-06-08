"""Functions to operate on text"""


def trim_side_quotes(text: str) -> str:
    """Trims quotes in the beginning and end of text, if they are present"""
    return text[1:-1] if len(text) > 1 and text[0] == '"' and text[-1] == '"' else text
