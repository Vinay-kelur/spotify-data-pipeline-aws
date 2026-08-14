# Spotify End-to-End Data Engineering Pipeline (AWS)

An automated, event-driven ETL pipeline that extracts music data from the Spotify API, transforms and processes it using AWS Lambda, stores the resulting datasets in Amazon S3, and makes them available for SQL-based analysis through Amazon Athena.

---

## Overview

This project implements an end-to-end serverless data engineering pipeline using AWS services.

The pipeline periodically extracts music data from the Spotify API and stores the raw data in Amazon S3. When new data arrives, an S3 event automatically triggers a second Lambda function that cleans, transforms, and separates the data by entity type. The transformed data is stored in the `processed` folder, while the original `to-be-processed` data is removed after successful processing.

AWS Glue then catalogs the processed datasets, making them available for SQL queries through Amazon Athena.

### Key Characteristics

* Serverless AWS architecture
* Automated scheduled data extraction
* Event-driven data processing
* Data transformation using Python and AWS Lambda
* Centralized storage using Amazon S3
* Automated schema discovery using AWS Glue
* SQL-based analytics using Amazon Athena
* No infrastructure or servers to manage

---

## Architecture

<img src="Architecture_diagram.png" alt="Spotify AWS Data Engineering Pipeline Architecture" width="900"/>

---

## Pipeline Workflow

### 1. Data Extraction

An AWS Lambda function connects to the Spotify API and extracts music data, including:

* Tracks
* Albums
* Artists

The extraction Lambda is scheduled using **Amazon EventBridge Scheduler** and runs once per day.

The extracted data is stored as raw files in the `to-be-processed` folder in Amazon S3.

---

### 2. Raw Data Storage

**Amazon S3** serves as the central storage layer for the pipeline.

The extracted Spotify data is initially stored in the `to-be-processed` folder. This location acts as the input area for the transformation stage.

Example:

```text
s3://spotify-data/to-be-processed/
```

---

### 3. Event-Driven Trigger

An **Amazon S3 Event Notification** monitors the `to-be-processed` location.

When a new raw file is uploaded, the S3 event automatically triggers the transformation Lambda function.

This allows the transformation stage to begin automatically as soon as new data becomes available.

---

### 4. Data Transformation and Processing

The second AWS Lambda function is responsible for transforming and processing the raw Spotify data.

The function:

1. Reads the raw data from the `to-be-processed` folder.
2. Cleans and restructures the data.
3. Separates the data by entity type.
4. Stores the transformed datasets in the `processed` folder.
5. Removes the processed data from the `to-be-processed` folder.

The resulting datasets are organized by entity type, such as:

```text
s3://spotify-data/processed/
│
├── tracks/
├── albums/
└── artists/
```

After successful transformation and storage, the `to-be-processed` data is deleted to keep the input location clean and prevent the same files from being processed again.

---

### 5. Schema Detection and Data Cataloging

An **AWS Glue Crawler** scans the transformed datasets stored in the `processed` folder.

The crawler automatically detects the structure and schema of the data and updates the **AWS Glue Data Catalog**.

The Data Catalog provides the metadata required by downstream analytics services.

---

### 6. Data Querying

**Amazon Athena** is used to query the cataloged datasets directly from Amazon S3.

Users can run standard SQL queries against the Spotify datasets without loading the data into a traditional relational database or data warehouse.

Example:

```sql
SELECT *
FROM tracks
LIMIT 10;
```

---

## Data Flow

```text
                    Spotify API
                         │
                         ▼
             EventBridge Scheduler
                         │
                    Daily Schedule
                         │
                         ▼
              Lambda — Extraction
                         │
                         ▼
              S3 — to-be-processed
                         │
                         │ S3 Event Notification
                         ▼
           Lambda — Transformation
                         │
             ┌───────────┼───────────┐
             │           │           │
             ▼           ▼           ▼
          Tracks      Albums      Artists
             │           │           │
             └───────────┼───────────┘
                         │
                         ▼
                  S3 — processed
                         │
                         │
              Delete to-be-processed
                         │
                         ▼
                  AWS Glue Crawler
                         │
                         ▼
                Glue Data Catalog
                         │
                         ▼
                   Amazon Athena
                         │
                         ▼
                    SQL Analysis
```

---

## S3 Data Organization

The S3 bucket is organized into separate locations for incoming and processed data.

```text
spotify-data/
│
├── to-be-processed/
│
└── processed/
    ├── tracks/
    ├── albums/
    └── artists/
```

### `to-be-processed`

Contains newly extracted raw Spotify data waiting for transformation.

### `processed`

Contains cleaned and structured datasets separated by entity type and made available for downstream cataloging and querying.

Once the transformation is completed successfully, the contents of `to-be-processed` are removed.

---

## AWS Services

| Service                          | Purpose                                            |
| -------------------------------- | -------------------------------------------------- |
| **AWS Lambda**                   | Handles Spotify data extraction and transformation |
| **Amazon EventBridge Scheduler** | Triggers the extraction Lambda on a daily schedule |
| **Amazon S3**                    | Stores raw and processed datasets                  |
| **Amazon S3 Event Notification** | Triggers transformation when new data arrives      |
| **AWS Glue Crawler**             | Detects schemas from processed datasets            |
| **AWS Glue Data Catalog**        | Stores metadata and table definitions              |
| **Amazon Athena**                | Queries processed datasets using SQL               |
| **Amazon CloudWatch**            | Provides Lambda execution logs and monitoring      |

---

## Technology Stack

* **Cloud:** AWS
* **Programming Language:** Python
* **API:** Spotify Web API
* **Storage:** Amazon S3
* **Compute:** AWS Lambda
* **Scheduling:** Amazon EventBridge Scheduler
* **Event Processing:** Amazon S3 Event Notifications
* **Data Catalog:** AWS Glue
* **Query Engine:** Amazon Athena
* **Monitoring:** Amazon CloudWatch

---

## Project Structure

```text
spotify-data-pipeline/
│
├── extraction/
│   └── lambda_function.py
│
├── transformation/
│   └── lambda_function.py
│
├── architecture/
│   └── Architecture_diagram.png
│
└── README.md
```

---

## End-to-End Process

The complete pipeline follows the sequence below:

```text
Spotify API
     ↓
EventBridge Scheduler
     ↓
Extraction Lambda
     ↓
S3 — to-be-processed
     ↓
S3 Event Notification
     ↓
Transformation Lambda
     ↓
Clean & Restructure
     ↓
Separate by Entity Type
     ↓
S3 — processed
     ↓
Remove to-be-processed Data
     ↓
AWS Glue Crawler
     ↓
Glue Data Catalog
     ↓
Amazon Athena
     ↓
SQL Analysis
```

---

## What This Project Demonstrates

This project demonstrates practical implementation of:

* Serverless data engineering on AWS
* End-to-end ETL pipeline development
* Third-party API integration
* Scheduled data ingestion
* Event-driven architecture
* Data transformation using Python
* Data organization and storage in Amazon S3
* Automated data processing with AWS Lambda
* Schema discovery using AWS Glue
* Metadata management using the Glue Data Catalog
* SQL analytics using Amazon Athena
* Cloud-based data pipeline design
* AWS monitoring using CloudWatch

---

## Future Improvements

Potential enhancements to the pipeline include:

* Data quality and validation checks
* Incremental data processing
* Error handling and retry mechanisms
* Dead-letter queues for failed processing
* AWS Step Functions for workflow orchestration
* S3 partitioning for improved Athena performance
* Amazon QuickSight for data visualization
* CloudWatch alarms and automated monitoring
* Improved data lineage and pipeline observability

---

## Author

**Vinay A Kelur**

[LinkedIn](#) • [GitHub](#)
