import boto3

ec2 = boto3.client('ec2')
savingsplans = boto3.client('savingsplans')

def get_instance_savings_plan_discount(instance_type):
    # インスタンスタイプに一致する Savings Plan を取得する
    response = savingsplans.describe_savings_plans_offering_rates(
        filters=[
            {
                'Name': 'productType',
                'Values': ['EC2 Instance Savings Plan']
            },
            {
                'Name': 'instanceFamily',
                'Values': [instance_type.split('.')[0]]
            },
            {
                'Name': 'instanceType',
                'Values': [instance_type]
            }
        ]
    )

    # Savings Plan の割引率を返す
    return response['SearchResults'][0]['SavingsPlanOfferingRates'][0]['Rate']

# 例：t2.micro インスタンスタイプの Savings Plans 割引率を取得する
discount = get_instance_savings_plan_discount('t2.micro')
print(discount)
