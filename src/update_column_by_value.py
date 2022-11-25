import pandas as pd

df = pd.DataFrame(
    data={
        "name": ["carlos", "john", "steve", "bill"],
        "computer": [
            "debian",
            "windows",
            "mac",
            "windows",
        ],
    }
)

df_expected_result = pd.DataFrame(
    data={
        "name": ["carlos", "john", "steve", "bill"],
        "computer": [
            "debian",
            "ubuntu",
            "arch",
            "ubuntu",
        ],
    }
)


def get_df_update_column_by_value(df: pd.DataFrame) -> pd.DataFrame:
    result_df = df.copy()
    result_df["computer"].replace(
        to_replace={"windows": "ubuntu", "mac": "arch"}, inplace=True
    )
    return result_df


if __name__ == "__main__":
    df_result = get_df_update_column_by_value(df)
    assert df_result.equals(df_expected_result)
