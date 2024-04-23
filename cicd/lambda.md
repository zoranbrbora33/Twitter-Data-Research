# AWS Academy Tara - Lambda CloudFormation Template

## Description
This AWS CloudFormation template is designed for creating AWS resources related to Lambda functions and associated IAM roles. 

## Parameters
- **S3BucketDataName**: The name of the S3 bucket containing data (Type: String).
- Name: tara-academy-data
- **S3BucketScriptsName**: The name of the S3 bucket containing Glue job scripts (Type: String).
- Name: tara-academy-scripts
- **Owner**: The owner's name or identifier.
- Name: tara@iolap.com
- **GlueJobName**: The name of the Glue job (Type: String).
- Name: tara-academy-glue-datalake-job
- **LambdaDatalakeName**: The name of the Lambda function for data lake operations.
- Name: tara-academy-lambda-datalake
- **LambdaDatalakeRoleName**: The name of the IAM role associated with the Lambda function.
- Name: tara-academy-lambda-datalake-role
- **LambdaDatalakeUploadUNIXT**: The UNIX timestamp used for uploading the Lambda code.

## Resources

### LambdaDatalakeExecutionRole
- **Type**: AWS IAM Role
- **Description**: This IAM role is assumed by the Lambda function for data lake operations.
- **AssumeRolePolicyDocument**: Defines the permissions for assuming this role.
- **Policies**: Specifies the policies attached to this role, granting permissions for S3 and Redshift operations.

### LambdaDatalakeFunction
- **Type**: AWS Lambda Function
- **Description**: This Lambda function is responsible for creating a schema in Redshift using data from the S3 bucket.
- **Runtime**: Python 3.8
- **Role**: The IAM role assumed by this Lambda function.
- **Handler**: The Python handler function within the Lambda code.
- **Layers**: Custom Lambda layers used by this function for AWS SDK, psycopg2, and data preprocessing.
- **Code**: The location of the Lambda function's code stored in an S3 bucket.
- **PackageType**: Zip
- **MemorySize**: The allocated memory for this function.
- **Timeout**: The maximum execution time for the function.

## Resource Description

- **LambdaDatalakeName**:   Lambda that is used to get data from s3 storage send it to redshift.

## Permissions

- **LambdaDatalakeRoleName**: The IAM role associated with the Lambda (`LambdaDatalakeName`) has the necessary permissions to perform actions like accessing S3 buckets and creating Redshift resources, as specified in the policy document.
