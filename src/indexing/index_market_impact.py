import pandas as pd
from elasticsearch import Elasticsearch, helpers

PARQUET_PATH = r"C:\Users\Famille\WhaleProject\datalake\usage\market_impact_combined.parquet"
INDEX_NAME = "market_impact"

es = Elasticsearch("http://localhost:9200")

df = pd.read_parquet(PARQUET_PATH)
df = df.fillna("")

actions = [
    {
        "_index": INDEX_NAME,
        "_source": row
    }
    for row in df.to_dict(orient="records")
]

helpers.bulk(es, actions)

print(f"Indexed {len(df)} rows into {INDEX_NAME}")