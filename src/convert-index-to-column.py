from pandas import DataFrame as Df
import numpy as np
import pandas as pd

# https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html#creating-a-multiindex-hierarchical-index-object
index_tuples = [
    ("light", "january"),
    ("light", "february"),
    ("light", "march"),
    ("water", "january"),
    ("water", "february"),
]
index = pd.MultiIndex.from_tuples(index_tuples, names=["concept", "month"])
original_df = Df([1.1, 2.2, 3.3, 4.4, 5.5], columns=["cost"], index=index)

index = pd.Index(["light", "water"])
index = index.set_names("concept")
expected_result_df = pd.DataFrame(
    data={
        "january": [1.1, 4.4],
        "february": [2.2, 5.5],
        "march": [3.3, np.nan],
    },
    index=index,
)
expected_result_df.columns = expected_result_df.columns.set_names("month")


class ManualDfConverter:
    def __init__(self, df: Df):
        self._df = df

    def get_df(self) -> Df:
        result = self._df.copy()
        result = result.unstack(level=-1)
        result.columns = result.columns.droplevel(level=0)
        column_names = ["january", "february", "march"]
        result = result.reindex(columns=column_names)
        return result


if __name__ == "__main__":
    print("Original:")
    print(original_df)
    print("\nExpected:")
    print(expected_result_df)
    result = ManualDfConverter(original_df).get_df()
    print("Result:")
    print(result)
    pd.testing.assert_frame_equal(expected_result_df, result)
