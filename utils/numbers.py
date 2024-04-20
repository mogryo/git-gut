"""Utils for numbers"""


def is_number(text: str) -> bool:
    """Check if text is a number"""
    try:
        float(text)
        return True
    except ValueError:
        return False
