from typing import List, AnyStr


def parse_option_columns(columns_string: str) -> List[AnyStr]:
    return list(filter(lambda x: x != "", "".join(columns_string.split(" ")).split(",")))
