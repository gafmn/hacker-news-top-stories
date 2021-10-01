from airflow import DAG

with DAG(
    dag_id="hacker-news",
    schedule_interval=None,
    catchup=False,
    tags=["hacker-news"],
) as dag:
    
    def fetch_data():
        pass

    def parse_data():
        pass

    def save_data():
        pass
