from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

"""
Description
"""

output_name = "spacetracker_satcat_data.csv"

# Run our DAG monthly and ensures DAG run will kick off
# once Airflow is started, as it will try to "catch up"
schedule_interval = '@monthly'
start_date = days_ago(1)

default_args = {"owner": "airflow", "depends_on_past": False, "retries": 1}

with DAG(
    dag_id='spacetrack_satcat_pipeline',
    description ='SpaceTrack SatCat ELT',
    schedule_interval=schedule_interval,
    default_args=default_args,
    start_date=start_date,
    catchup=True,
    max_active_runs=1,
    tags=['SatCatETL'],
) as dag:

    extract_satcat_data = BashOperator(
        task_id = 'extract_satcat_data',
        bash_command = f"python /opt/airflow/extraction/extract_satcat_data.py {output_name}",
        dag = dag,
    )
    extract_satcat_data.doc_md = 'Extract SatCat data and store as CSV'

    upload_data_s3 = BashOperator(
        task_id = 'upload_data_s3',
        bash_command = f'python /opt/airflow/extraction/upload_data_s3.py {output_name}',
        dag = dag,
    )
    upload_data_s3.doc_md = 'Upload SatCat CSV data to S3 bucket'

    copy_data_redshift = BashOperator(
        task_id = 'copy_data_redshift',
        bash_command = f"python /opt/airflow/extraction/copy_data_redshift.py {output_name}",
        dag = dag,
    )
    copy_data_redshift.doc_md = 'Copy S3 CSV file to Redshift table'

extract_satcat_data >> upload_data_s3 >> copy_data_redshift
