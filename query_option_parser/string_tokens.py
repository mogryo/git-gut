"""String tokens: signs, condition join words and etc."""

NUMBER_SIGNS = {">", "<", ">=", "<=", "="}
TEXT_SIGNS = {"="}
ALLOWED_SIGNS = NUMBER_SIGNS.union(TEXT_SIGNS)
CONDITION_JOIN = {"and"}
TOP_LEVEL_STATEMENT_KEYWORDS = {'SHOW', 'FROM', 'WHERE', 'ORDERBY'}
