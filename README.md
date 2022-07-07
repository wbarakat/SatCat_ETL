# Satellite Catalog ETL Pipeline

I built this pipeline to extract SatCat data from [SpaceTrack](https://www.space-track.org/) and visualized it using Google Data Studio.


## Motivation

To further develop my data engineering skills as well as learn more ETL processes and technologies.


## Architecture

<img src="https://github.com/wbarakat/SatCat_ETL/blob/815a1f890d503779b2a1218ff887aea80d92405f/images/Arch_Diagram.png" width=70% height=70%>

1. Create AWS resources with [Terraform](https://www.terraform.io)
1. Extract data using [SpaceTrack API](https://www.space-track.org/)
1. Load into [AWS S3](https://aws.amazon.com/s3/)
1. Copy into [AWS Redshift](https://aws.amazon.com/redshift/)
1. Orchestrate with [Airflow](https://airflow.apache.org) in [Docker](https://www.docker.com)
1. Transform using [dbt](https://www.getdbt.com)
1. Visualize with [Google Data Studio](https://datastudio.google.com) Dashboard

## Dashboard

<img src="https://github.com/wbarakat/SatCat_ETL/blob/d03cecab41d76622eac7fb7707b866477305ff77/images/SatCat_Dashboard.png" width=70% height=70%>

## Setup

In order to run this pipeline, first clone the repo then follow the instructions linked below.


  ```bash
  git clone https://github.com/wbarakat/SatCat_ETL.git
  cd SatCat_ETL
  ```

[Instructions](https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/instructions/overview.md)

## Future Steps

- Add unit tests for extraction functions
- Add more tests for data quality/validation: missing values, duplicates, etc
