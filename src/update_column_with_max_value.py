import datetime
import copy

import pandas as pd

df_old = pd.DataFrame(
    data={
        "id": [
            1,
            2,
            3,
            4,
        ],
        "date": [
            datetime.datetime(1901, 1, 1),
            datetime.datetime(2100, 1, 1),
            datetime.datetime(1903, 1, 1),
            datetime.datetime(2100, 1, 1),
        ],
    }
)

df_new = pd.DataFrame(
    data={
        "id": [
            1,
            4,
            2,
        ],
        "date": [
            datetime.datetime(1900, 1, 1),
            datetime.datetime(2104, 1, 1),
            datetime.datetime(2102, 1, 1),
        ],
    }
)

df_expected_result = pd.DataFrame(
    data={
        "id": [
            1,
            2,
            3,
            4,
        ],
        "date": [
            datetime.datetime(1901, 1, 1),
            datetime.datetime(2102, 1, 1),
            datetime.datetime(1903, 1, 1),
            datetime.datetime(2104, 1, 1),
        ],
    }
)


def _update_column_with_max_value_by_primary_key(
    df_to_update: pd.DataFrame,
    df_with_new_values: pd.DataFrame,
    column_to_update: str,
    column_primary_key: str,
) -> pd.DataFrame:
    result_df = copy.deepcopy(df_to_update)
    column_to_update_new = f"{column_to_update}_new"
    result_df = result_df.merge(
        df_with_new_values.rename(columns={column_to_update: column_to_update_new}),
        on=column_primary_key,
        how="left",
    )
    result_df[[column_to_update]] = result_df[
        [column_to_update, column_to_update_new]
    ].max(axis=1)
    return result_df.drop(columns=column_to_update_new)


if __name__ == "__main__":
    df_result = _update_column_with_max_value_by_primary_key(
        df_old, df_new, "date", "id"
    )
    assert df_result.equals(df_expected_result)
