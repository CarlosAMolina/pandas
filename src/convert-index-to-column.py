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
expected_result_df.to_csv("foo.csv")


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
        index = self._get_index()
        data = self._get_data()
        result = pd.DataFrame(
            data=data,
            index=index,
        )
        return result

    def _get_index(self) -> list:
        index = []
        for indexes in self._df.index:
            index_parent = indexes[0]
            if index_parent not in index:
                index += [index_parent]
        return index

    def _get_data(self) -> dict:
        # https://stackoverflow.com/questions/44823418/multi-index-pandas-dataframe-to-a-dictionary/44823657#44823657
        index_parent_name = self._df.index.names[0]
        df_without_parent_index = self._df.reset_index(
            level=[index_parent_name], drop=True
        )
        df_without_original_index = df_without_parent_index.reset_index()
        data_array = df_without_original_index.to_dict(orient="split")["data"]
        data = dict()
        for column_and_value in data_array:
            column, value = column_and_value
            if column in data.keys():
                data[column] += [value]
            else:
                data[column] = [value]
        return data


if __name__ == "__main__":
    print("Original:")
    print(original_df)
    print("\nExpected:")
    print(expected_result_df)
    result = ManualDfConverter(original_df).get_df()
    print("Result:")
    print(result)
    pd.testing.assert_frame_equal(expected_result_df, result)
