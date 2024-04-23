AWS CodeBuild

Number of builds in a month
100

Average build duration (minutes)
5

Operating system
Linux

Compute instance type
arm1.small

Show calculations

100 builds per month x 5 minutes = 500.00 billed minutes (monthly)

500.00 minutes x 0.00385 USD = 1.93 USD

AWS CodeBuild cost (monthly): 1.93 USD

---

AWS CodePipeline

CodePipeline Pricing

Number of active pipelines used per account per month
1
An active pipeline is a pipeline that has existed for more than 30 days and has at least one code change that runs through it during the month. An active pipeline is not prorated for partial months.

Show calculations

1 active pipelines - 1 free active pipeline each month = 0 total active pipelines per month

CodePipeline cost (monthly): 0.00 USD

---

Amazon Simple Storage Service (S3)



Select S3 Storage classes and other featuresInfo

Data Transfer?

Show calculations

Tiered price for: 1 GB

1 GB x 0.0245000000 USD = 0.02 USD

Total tier cost = 0.0245 USD (S3 Standard storage cost)

350 PUT requests for S3 Standard Storage x 0.0000054 USD per request = 0.0019 USD (S3 Standard PUT requests cost)

50 GET requests in a month x 0.00000043 USD per request = 0.00 USD (S3 Standard GET requests cost)

1 GB x 0.0008 USD = 0.0008 USD (S3 select returned cost)

1 GB x 0.00225 USD = 0.0022 USD (S3 select scanned cost)

0.0245 USD + 0.0019 USD + 0.0008 USD + 0.0022 USD = 0.03 USD (Total S3 Standard Storage, data requests, S3 select cost)

S3 Standard cost (monthly): 0.03 USD

S3 Standard cost (upfront): 0.00 USD

---

AWS Glue,Catalog,Crawler

5 objects stored x 1000000 multiplier for million x 0.00001 USD = 50.00 USD (Data Catalog storage cost)

1 objects stored x 1000000 multiplier for million x 0.000001 USD = 1.00 USD (Data Catalog requests cost)

50.00 USD + 1.00 USD = 51 USD

Data Catalog storage and requests cost (monthly): 51.00 USD

---

AWS Redshift

Show calculations

1 instance(s) x 0.25 USD hourly x (100 / 100 Utilized/Month) x 730 hours in a month = 182.5000 USD

Redshift instance cost (monthly): 182.50 USD

Redshift instance cost (upfront): 0.00 USD

---
AWS Athena

Total number of queries: 50 per day * (730 hours in a month / 24 hours in a day) = 1520.83 queries per month
Amount of data scanned per query: 0.6 GB x 0.0009765625 TB in a GB = 0.0005859375 TB
Pricing calculations

Rounding (1520.83) = 1521 Rounded total number of queries

1,521 queries per month x 0.0005859375 TB x 5.00 USD = 4.46 USD

SQL queries with per query cost (monthly): 4.46 USD

Total SQL queries cost (monthly): 4.46 USD

---
Total sum monthly=239.92 USD


