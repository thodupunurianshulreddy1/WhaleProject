from datetime import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="whale_wallet_tracking_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["big-data", "crypto"],
) as dag:

    extract_etherscan = EmptyOperator(
        task_id="extract_etherscan_api"
    )

    extract_coingecko = EmptyOperator(
        task_id="extract_coingecko_api"
    )

    store_raw = EmptyOperator(
        task_id="store_raw_json_in_datalake"
    )

    format_etherscan = EmptyOperator(
        task_id="format_etherscan_json_to_parquet"
    )

    format_coingecko = EmptyOperator(
        task_id="format_coingecko_json_to_parquet"
    )

    combine_data = EmptyOperator(
        task_id="combine_datasets"
    )

    elasticsearch_index = EmptyOperator(
        task_id="index_to_elasticsearch"
    )

    kibana_visualization = EmptyOperator(
        task_id="visualize_in_kibana"
    )

    [extract_etherscan, extract_coingecko] >> store_raw

    store_raw >> [format_etherscan, format_coingecko]

    [format_etherscan, format_coingecko] >> combine_data

    combine_data >> elasticsearch_index >> kibana_visualization