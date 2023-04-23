import boto3
import datetime

ce = boto3.client('ce', region_name='us-east-1')

# 現在時刻の1時間前を取得
start = datetime.datetime.utcnow() - datetime.timedelta(hours=1)

# クエリパラメータを設定
params = {
    'TimePeriod': {
        'Start': start.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'End': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    },
    'Granularity': 'HOURLY',
    'Metrics': ['UnblendedCost'],
    'GroupBy': [{'Type': 'DIMENSION', 'Key': 'SERVICE'}],
    'Filter': {
        'And': [
            {
                'Dimensions': {
                    'Key': 'USAGE_TYPE_GROUP',
                    'Values': ['EC2 Instance Usage']
                }
            },
            {
                'Dimensions': {
                    'Key': 'OPERATION',
                    'Values': ['RunInstances']
                }
            },
            {
                'Dimensions': {
                    'Key': 'LEGAL_ENTITY_NAME',
                    'Values': ['Amazon Web Services, Inc.']
                }
            },
            {
                'Dimensions': {
                    'Key': 'USAGE_TYPE',
                    'Values': ['BoxUsage']
                }
            }
        ]
    }
}

# コスト情報を取得
response = ce.get_cost_and_usage(**params)

# サービスごとのコスト情報を取得
for result_by_time in response['ResultsByTime']:
    for group in result_by_time['Groups']:
        if group['Keys'][0] == 'Amazon Elastic Compute Cloud - Compute':
            hourly_cost = float(group['Metrics']['UnblendedCost']['Amount']) / 1.0
            print(f'1時間あたりのオンデマンド利用料は {hourly_cost:.4f} USD です。')
