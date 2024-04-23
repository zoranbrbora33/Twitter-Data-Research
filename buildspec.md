# AWS CodePipeline Build Specification

## Version
- **Version**: 0.2

## Phases

### Install
- **Commands**:
  - Start Initialization
  - Set User Information
  - Define S3 Stack parameters
  - Define Glue Stack parameters
  - Define Lambda Stack parameters
  - Define State Machine Stack parameters
  - Zip Lambda file for datalake
  - End Initialization

### Build
- **Commands**:
  - Start Build

#### S3 Stack Deployment
- Deploy S3 Stack
- Send `glueetl.py` to Scripts Bucket
- Send `lambda_datalake.zip` to Scripts Bucket
- Connected to s3.yml

#### Glue Stack Deployment
- Deploy Glue Stack
- Connected to glue.yml

#### Lambda Stack Deployment
- Deploy Lambda Stack
- Connected to lambda.yml

#### State Machine Stack Deployment
- Deploy State Machine Stack
-  Connected to statemachine.yml

- End Build
