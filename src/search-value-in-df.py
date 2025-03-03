from pandas import DataFrame as Df


df = Df(
    {"name": ["joAChn", "mark", "jaACne"], "city": ["cuenca", "maACdrid", "cuenca"]}
)
term = "ac"
result: dict[str, list[str]] = {}
for header in df.columns:
    condition = df[header].str.lower().str.contains(term.lower())
    result[header] = df.loc[condition, header].tolist()

assert {"name": ["joAChn", "jaACne"], "city": ["maACdrid"]} == result
