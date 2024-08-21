from pandas import DataFrame as Df
import numpy as np
import pandas as pd


def get_original_df() -> Df:
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
    return original_df


original_df = get_original_df()


def get_expected_result() -> Df:
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
    return expected_result_df


expected_result_df = get_expected_result()


class DfConverter:
    def __init__(self, df: Df):
        self._df = df

    def get_df(self) -> Df:
        result = self._df.copy()
        result = self._get_df_set_month_indexes_as_columns(result)
        result = self._get_df_drop_columns_multi_index_set_only_months(result)
        result = self._get_df_sort_columns(result)
        return result

    def _get_df_set_month_indexes_as_columns(self, df: Df) -> Df:
        return df.unstack(level="month")

    def _get_df_drop_columns_multi_index_set_only_months(self, df: Df) -> Df:
        result = df.copy()
        result.columns = result.columns.droplevel(level=0)
        return result

    def _get_df_sort_columns(self, df: Df) -> Df:
        column_names = ["january", "february", "march"]
        return df.reindex(columns=column_names)


if __name__ == "__main__":
    print("Original:")
    print(original_df)
    print("\nExpected:")
    print(expected_result_df)
    result = DfConverter(original_df).get_df()
    print("Result:")
    print(result)
    pd.testing.assert_frame_equal(expected_result_df, result)
