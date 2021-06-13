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
            datetime.datetime(2001, 1, 1),
            datetime.datetime(2002, 1, 1),
            datetime.datetime(2003, 1, 1),
            datetime.datetime(2004, 1, 1),
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
            datetime.datetime(2101, 1, 1),
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
            datetime.datetime(2001, 1, 1),
            datetime.datetime(2002, 1, 1),
            pd.NaT,
            datetime.datetime(2104, 1, 1),
        ],
    }
)


def _update_column_with_other_df_based_on_expression(
    df_to_update: pd.DataFrame,
    df_with_new_values: pd.DataFrame,
    column_to_update: str,
    column_index: str,
    expression: pd.Series,
) -> pd.DataFrame:
    result_df = copy.deepcopy(df_to_update)
    column_to_update_new = f"{column_to_update}_new"
    result_df = result_df.merge(
        df_with_new_values.rename(columns={column_to_update: column_to_update_new}),
        on=column_index,
        how="left",
    )
    result_df.loc[expression, column_to_update] = result_df[expression][
        column_to_update_new
    ]
    return result_df.drop(columns=column_to_update_new)


if __name__ == "__main__":
    expression = df_old["date"] > datetime.datetime(2002, 1, 1)
    df_result = _update_column_with_other_df_based_on_expression(
        df_old, df_new, "date", "id", expression
    )
    assert df_result.equals(df_expected_result)
