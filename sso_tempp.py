import boto3

def invoke_step_function(state_machine_arn, input_data):
    client = boto3.client('stepfunctions')

    response = client.start_execution(
        stateMachineArn=state_machine_arn,
        input=input_data
    )

    return response['executionArn']


# 設定
state_machine_arn = 'arn:aws:states:us-east-1:123456789012:stateMachine:MyStateMachine'
input_data = '{"key1": "value1", "key2": "value2"}'

# Step Functionsの呼び出し
execution_arn = invoke_step_function(state_machine_arn, input_data)

print(f'Started Step Functions execution: {execution_arn}')


import boto3

def assign_permission_set_to_account(permission_set_arn, account_id, instance_arn):
    client = boto3.client('sso-admin')

    response = client.attachManagedPolicyToPermissionSet(
        InstanceArn=instance_arn,
        PermissionSetArn=permission_set_arn,
        TargetId=account_id,
        TargetType='AWS_ACCOUNT'
    )

    return response['PermissionSetArn']


# 設定
permission_set_arn = 'arn:aws:sso:::permissionSet/xxxxxxxxxxxxxxxxxxxxxx'
account_id = '123456789012'
instance_arn = 'arn:aws:sso:::instance/xxxxxxxxxxxxxxxxxxxxxx'

# 許可セットの割り当て
assigned_permission_set_arn = assign_permission_set_to_account(permission_set_arn, account_id, instance_arn)

print(f'Permission set assigned: {assigned_permission_set_arn}')
