Description:

Client: Travel agency

We're interested in identifying the most influential individuals in Croatia and gaining insights into the locations they frequently mention in their tweets.
A travel agency seeking to attract more tourists to a specific destination might analyze Twitter data to identify travel enthusiasts and bloggers who frequently share their travel experiences.
These influencers can help showcase the destination's attractions, culture, and experiences, encouraging more people to visit.

### Architecture Overview:

This repository contains resources and CI/CD buildspec used in our project.

Through our project, we developed an AWS cloud architecture for the following key processes:

1. Data Extraction: Data is extracted from a landing S3 bucket.
2. Data Transformation: AWS Glue Jobs transform the extracted data, including data cleaning, structuring, and enrichment.
3. Data Storage: Transformed data is stored in a data lake S3 bucket.
4. Automated Data Processing: AWS Step Functions orchestrate daily processing, starting at 6:00 AM.
5. Data Loading: Upon Glue Job completion, AWS Lambda loads data into Amazon Redshift.
6. Data Analysis: A second Glue Job performs data analysis and creates views for analysis.
7. Business Intelligence Reporting: Power BI reports are generated for data-driven insights.

#### Project Components

##### AWS Glue Job: For data extraction and transformation.

##### Data Lake S3 Bucket: For data storage.

##### AWS Step Functions: For automated workflow.

##### AWS Lambda Function: For data loading into Amazon Redshift.

##### Amazon Redshift: For data warehousing.

##### Power BI Reports: For business intelligence.

#### Project Workflow

1. Data Extraction and Transformation: Raw data is processed by AWS Glue Jobs for cleansing and preparation.
2. Data Storage: Transformed data is stored centrally in a data lake S3 bucket.
3. Automated Data Processing: Daily data processing is scheduled using AWS Step Functions.
4. Data Loading into Redshift: AWS Lambda loads data into Amazon Redshift upon Glue Job completion.
5. Data Analysis and Reporting: A Glue Job performs data analysis and creates views for analysis.
6. Business Intelligence Reporting: Power BI reports are generated for data-driven decision-making.
