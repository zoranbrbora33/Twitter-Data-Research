# AWS Academy Tara - State Machine CloudFormation Template

## Description
This AWS CloudFormation template is designed for creating AWS resources related to state machines, IAM roles, and event triggers. 

## Parameters
- **StateMachineName**: The name of the state machine.
- Name: tara-academy-statemachine
- **StateMachineRoleName**: The name of the IAM role associated with the state machine.
- Name: tara-academy-statemachine-role
- **StateMachineTriggerRoleName**: The name of the IAM role associated with the state machine trigger.
- Name: tara-academy-statemachine-trigger-role
- **Owner**: The owner's name or identifier.
- Name: tara@iolap.com
- **GlueJobName**: The name of the Glue job (Type: String).
- Name: tara-academy-glue-datalake-job
- **LambdaDatalakeName**: The name of the Lambda function for data lake operations.
- Name: tara-academy-lambda-datalake
- **GlueJobAnalyticsName**: The name of the Glue analytics job (Type: String).
- Name: tara-academy-glue-analytics-job

## Resources

### StateMachineRole
- **Type**: AWS IAM Role
- **Description**: This IAM role is assumed by the state machine.
- **AssumeRolePolicyDocument**: Defines the permissions for assuming this role.
- **ManagedPolicyArns**: Specifies managed policies attached to this role for Lambda and Glue service roles.

### StateMachineTriggerRole
- **Type**: AWS IAM Role
- **Description**: This IAM role is assumed by the state machine trigger.
- **AssumeRolePolicyDocument**: Defines the permissions for assuming this role.
- **Policies**: Specifies custom policies attached to this role for interacting with the state machine.

### AcademyStateMachine
- **Type**: AWS Step Functions State Machine
- **Description**: This state machine orchestrates Glue and Lambda operations.
- **StateMachineName**: The name of the state machine.
- **RoleArn**: The IAM role assumed by the state machine.
- **DefinitionString**: JSON definition of the state machine.

### AcademyStateMachineTrigger
- **Type**: AWS CloudWatch Events Rule
- **Description**: This event trigger invokes the state machine on a schedule.
- **State**: DISABLED
- **RoleArn**: The IAM role assumed by the trigger.
- **ScheduleExpression**: Cron expression for triggering the state machine.
- **Targets**: Specifies the state machine to be triggered.

## Resource Description

- **StateMachineName**:  State machine that executes in order GlueJobName, LambdaDatalakeName
GlueJobAnalyticsName.

- **AcademyStateMachineTrigger**: Cron job that runs state machine every day at 6 AM. 
Currently disabled.

## Permissions

- **StateMachineRoleName**: The name of the IAM role associated with the state machine that gives
permissions to state machine.

**StateMachineTriggerRoleName**: The name of the IAM role associated with the state machine trigger
that gives state machine trigger permissions to execute.

