import boto3
import os
from datetime import datetime, timedelta

ce = boto3.client('ce', region_name=os.environ['AWS_REGION'])

def lambda_handler(event, context):
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=30)
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
                'Start': start_date.isoformat(),
                'End': end_date.isoformat()
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
