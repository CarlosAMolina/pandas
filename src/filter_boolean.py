from pandas import DataFrame as Df
from pandas import Series

users_df = Df(
   [
       [1, True],
       [2, False],
       [3, True],
   ],
   columns=["id", "is_adult"],
)

def print_is_expected_condition(condition: Series):
    if isinstance(condition, Series) and condition.to_list() == [True, False, True]:
        print('ok')
    else:
        print('wrong')

# Option 1
condition_equals = users_df.is_adult == True
print_is_expected_condition(condition_equals)
# Option 2
# The following condition has bool type, not Series.
condition_is = users_df.is_adult is True 
print_is_expected_condition(condition_is)
# Option 3
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.eq.html
condition_eq = users_df.is_adult.eq(True)
print_is_expected_condition(condition_eq)
