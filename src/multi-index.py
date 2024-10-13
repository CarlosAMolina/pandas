from pandas import DataFrame as Df
import pandas as pd

# https://pandas.pydata.org/pandas-docs/stable/user_guide/cookbook.html#multiindexing
df_no_multi_index = Df(
    data={
        "pro_downloads": [1, 2, 3, 4],
        "pro_size":      [1.1, 2.2, 3.3, 4.4],
        "dev_downloads": [10, 20, 30, 40],
        "dev_size":      [1.11, 2.22, 3.33, 4.44],
    },
    index= ["folder_1_file_1", "folder_1_file_2", "folder_2_file_1", "folder_2_file_2"],
)

def get_df_multi_index(df: Df) -> Df:
    result = df.copy()
    result.columns = pd.MultiIndex.from_tuples([get_multi_index_from_column_name(column_name) for column_name in result.columns])
    result.index = pd.MultiIndex.from_tuples([get_multi_index_from_index(index) for index in result.index])
    return result

def get_multi_index_from_column_name(column_name: str) -> tuple[str, str]:
    environment, key = column_name.split("_")
    return environment, key

def get_multi_index_from_index(index: str) -> tuple[str, str]:
    folder_name = '_'.join(index.split("_")[:2])
    file_name = '_'.join(index.split("_")[2:])
    result = (folder_name, file_name)
    return result

def access_values():
    # https://stackoverflow.com/questions/18470323/selecting-columns-from-pandas-multiindex
    assert 3 == df_no_multi_index.loc["folder_2_file_1", "pro_downloads"]
    df_multi_index = get_df_multi_index(df_no_multi_index)
    assert 3 == df_multi_index.loc[('folder_2', 'file_1'), ('pro', 'downloads')]

if __name__ == "__main__":
    print(df_no_multi_index)
    print(get_df_multi_index(df_no_multi_index))
    access_values()
