import boto3
import os

ce = boto3.client('ce', region_name=os.environ['AWS_REGION'])

def lambda_handler(event, context):
    start_date = event.get('startDate', '2022-03-01')
    end_date = event.get('endDate', '2022-03-31')
    instance_family = event.get('instanceFamily', 'a1')

    results = []
    token = None

    while True:
        if token:
            kwargs = {'NextPageToken': token}
        else:
            kwargs = {}
        
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=['UsageQuantity'],
            Filter={
                'And': [
                    {'Dimensions': {'Key': 'USAGE_TYPE_GROUP', 'Values': ['EC2: Running Hours']}},
                    {'Dimensions': {'Key': 'INSTANCE_TYPE_FAMILY', 'Values': [instance_family]}}
                ]
            },
            **kwargs
        )

        results += response['ResultsByTime']

        token = response.get('NextPageToken')

        if not token:
            break

    total_usage = sum(result['Total']['UsageQuantity']['Amount'] for result in results)

    return total_usage
