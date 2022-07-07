# Satellite Catalog ETL Pipeline

I built this pipeline to extract SatCat Data and visualized it using Google Data Studio

## Motivation

Learn about different architectures and develop my data engineering skills.

## Architecture

<img src="https://github.com/wbarakat/SatCat_ETL/blob/815a1f890d503779b2a1218ff887aea80d92405f/images/Arch_Diagram.png" width=70% height=70%>

1. Extract data using [SpaceTrack API](https://www.space-track.org/)
1. Load into [AWS S3](https://aws.amazon.com/s3/)
1. Copy into [AWS Redshift](https://aws.amazon.com/redshift/)
1. Transform using [dbt](https://www.getdbt.com)
1. Create [Google Data Studio](https://datastudio.google.com) Dashboard 
1. Orchestrate with [Airflow](https://airflow.apache.org) in [Docker](https://www.docker.com)
1. Create AWS resources with [Terraform](https://www.terraform.io)

## Output

[<img src="https://github.com/wbarakat/SatCat_ETL/blob/815a1f890d503779b2a1218ff887aea80d92405f/images/SatCat%20_Dashboard.png" width=70% height=70%>]
