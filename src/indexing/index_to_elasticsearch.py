import sys
from pyspark.sql import SparkSession

def index_usage_to_elasticsearch(date_str):
   
    spark = SparkSession.builder \
        .appName("Index-To-Elasticsearch") \
        .config("es.nodes", "localhost") \
        .config("es.port", "9200") \
        .config("es.resource", "whale_market_impact") \
        .config("es.nodes.wan.only", "true") \
        .getOrCreate()
        
    usage_path = f"datalake/usage/analytics/market_impact/{date_str}/*"
    
    try:
        df_usage = spark.read.parquet(usage_path)
        
        print(f"Loaded {df_usage.count()} analytical documents from the usage layer.")
        print("Streaming records to Elasticsearch cluster")
        
        df_usage.write \
            .format("org.elasticsearch.spark.sql") \
            .mode("append") \
            .save()
            
        print(f"Successfully indexed data partition {date_str} to Elasticsearch index 'whale_market_impact'!")
        
    except Exception as e:
        print(f"Indexing layer failed: {e}")
        print("\nTroubleshooting: Ensure your local Elasticsearch Docker instance or service is running successfully.")
    finally:
        spark.stop()

if __name__ == "__main__":
    date_arg = sys.argv[1] if len(sys.argv) > 1 else "20260529"
    index_usage_to_elasticsearch(date_arg)