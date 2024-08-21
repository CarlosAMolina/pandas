import numpy as np
from pandas import DataFrame as Df

# Example of filter rows with `age` duplicated grouping by `id: and `id_new`.
users_df = Df(
    [
        [1, 2, 18, "john"],
        [1, 2, 18, "ana"],
        [2, 3, 20, "bob"],
    ],
    columns=["id", "id_new", "age", "name"],
)
values_and_is_duplicated_series = (
    users_df.groupby(by=["id", "id_new"])["age"].count() > 1
)
print("users_df")
print(users_df)
print("values_and_is_duplicated_series")
print(values_and_is_duplicated_series)
print("values_and_is_duplicated_series.values")
print(values_and_is_duplicated_series.values)
# Option 1. Get duplicates
condition_is_duplicated = [
    value is np.True_ for value in values_and_is_duplicated_series.values
]
duplicated_records = values_and_is_duplicated_series[condition_is_duplicated].keys()
print("duplicated_records")
print(duplicated_records)
# Option 2. Get duplicates
duplicated_records_b = values_and_is_duplicated_series[
    values_and_is_duplicated_series.values == True
].keys()
print("duplicated_records_b")
print(duplicated_records_b)
