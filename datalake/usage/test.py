import pandas as pd

path = r"C:\Users\Famille\WhaleProject\datalake\usage\market_impact_combined.parquet"

df = pd.read_parquet(path)

print(df.shape)
print(df.columns)
print(df.head())