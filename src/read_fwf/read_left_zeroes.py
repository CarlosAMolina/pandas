"""
What this file tests: if a column has numbers that start with 0, read_fwf will
read them as int and drops the initial 0. This can cause errors, for example
when converting a value to date type with `pd.to_datetime(result["date"], format="%d%m%Y").dt.date`:
the value 03092024 in read as 3092024 and the conversion returns 2024-09-30 instead of 2024-09-03
"""
from pandas import DataFrame as Df
from pandas import read_fwf
from pandas.testing import assert_frame_equal

file_column_index_config = {
    "name": (8, 13),
    "birthday": (14, 22),
}

# https://stackoverflow.com/questions/36729392/pandas-read-fwf-specify-dtype
file_df = read_fwf(
    "file.txt",
    colspecs=list(file_column_index_config.values()),
    converters={"birthday":str},
    names=list(file_column_index_config.keys()),
    header=None
)
expected_result = Df(
    data={
        "name": ["jon", "edgar"],
        "birthday": ["03092024", "03092024"],
    }
)
assert_frame_equal(expected_result, file_df)
