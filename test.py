c2 = boto3.client('ec2')

response = ec2.describe_instances(
    Filters=[        {            'Name': 'instance-state-name',            'Values': ['running']
        }
    ]
)

instances = []

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instances.append(instance['InstanceId'])

print(instances)
