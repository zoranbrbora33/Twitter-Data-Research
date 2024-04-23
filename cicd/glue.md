# AWS Academy Tara - Glue Job Template

This Markdown document provides documentation for an AWS CloudFormation template used to create and configure AWS Glue jobs for the AWS Academy Tara project.

## Template Information

- **AWSTemplateFormatVersion**: "2010-09-09"
- **Description**: This CloudFormation template defines AWS Glue jobs for the AWS Academy Tara project.

## Parameters

The template includes the following parameters:

- **S3BucketDataName**: The name of the S3 bucket containing data (Type: String).
- Name: tara-academy-data
- **S3BucketScriptsName**: The name of the S3 bucket containing Glue job scripts (Type: String).
- Name: tara-academy-scripts
- **S3AdminDataName**: The name of the S3 bucket containing admin data (Type: String).
- Name: admin-academy-data
- **GlueJobName**: The name of the Glue job (Type: String).
- Name: tara-academy-glue-datalake-job
- **GlueJobAnalyticsName**: The name of the Glue analytics job (Type: String).
- Name: tara-academy-glue-analytics-job
- **GlueJobRoleName**: The name of the IAM role for the Glue job (Type: String).
- Name: tara-academy-glue-role
- **GlueAdminDatalakeName**: The name of the Glue data lake (Type: String).
- Name: admin-academy-twitter
- **GlueAdminDatalakeTableUsers**: The name of the table for users in the Glue data lake (Type: String).
- Name: users
- **GlueAdminDatalakeTableUserFollowers**: The name of the table for user followers in the Glue data lake (Type: String).
- Name: user_followers
- **GlueAdminDatalakeTableTweets**: The name of the table for tweets in the Glue data lake (Type: String).
- Name: tweets

## Resources

### GlueJobRole

- **Type**: "AWS::IAM::Role"
- **Description**: IAM role for the Glue job.
- **Properties**:
  - **RoleName**: The name of the IAM role (Referenced from `GlueJobRoleName` parameter).
  - **AssumeRolePolicyDocument**: The policy that defines who can assume this role.
  - **Policies**: List of policies associated with the role.

### GlueDatalakeJob

- **Type**: "AWS::Glue::Job"
- **Description**: AWS Glue job for data processing.
- **Properties**:
  - **Name**: The name of the Glue job (Referenced from `GlueJobName` parameter).
  - **Role**: The IAM role for the Glue job (Referenced from `GlueJobRole`).
  - **GlueVersion**: Glue version used for the job.
  - **Command**: Details of the job's command, including the script location.
  - **ExecutionProperty**: Configuration for job execution.
  - **MaxRetries**: Maximum number of retries for job execution.
  - **Timeout**: Maximum execution time for the job.
  - **DefaultArguments**: Default arguments passed to the job script.

### GlueAnalyticsJob

- **Type**: "AWS::Glue::Job"
- **Description**: AWS Glue analytics job.
- **Properties**:
  - **Name**: The name of the analytics job (Referenced from `GlueJobAnalyticsName` parameter).
  - **Role**: The IAM role for the analytics job (Referenced from `GlueJobRole`).
  - **GlueVersion**: Glue version used for the analytics job.
  - **Command**: Details of the job's command, including the script location and Python version.
  - **ExecutionProperty**: Configuration for job execution.
  - **MaxRetries**: Maximum number of retries for job execution.
  - **Timeout**: Maximum execution time for the job.

## Resource Description

- **GlueJobName**: This glue job is used to get data from admin s3 bucket, transform data,
and send that data tp s3 tara data bucket.

## Permissions

- **GlueJobRoleName**: The IAM role associated with the Glue jobs (`GlueJobRole`) has the necessary permissions to perform actions like accessing S3 buckets, accessing Glue catalog tables, and creating Redshift resources, as specified in the policy document.
