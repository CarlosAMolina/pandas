import re

from pandas import Series

# Documentation: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.contains.html


s1 = Series(["dog", "xA|Bx"])
assert [False, True] == s1.str.contains("a|b", case=False, regex=False).tolist()
# Flags does no work if no regex
assert [False, False] == s1.str.contains(
    "a|b", flags=re.IGNORECASE, regex=False
).tolist()
