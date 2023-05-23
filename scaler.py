import boto3

def get_autoscaling_instance_ids(group_name):
    autoscaling = boto3.client('autoscaling')
    response = autoscaling.describe_auto_scaling_groups(AutoScalingGroupNames=[group_name])
    
    instance_ids = []
    if 'AutoScalingGroups' in response and len(response['AutoScalingGroups']) > 0:
        instances = response['AutoScalingGroups'][0]['Instances']
        instance_ids = [instance['InstanceId'] for instance in instances]
    
    return instance_ids

# Auto Scalingグループ名を指定してインスタンスIDを取得
group_name = 'your-autoscaling-group-name'
instance_ids = get_autoscaling_instance_ids(group_name)

print("Instance IDs:")
for instance_id in instance_ids:
    print(instance_id)
    
def get_autoscaling_min_size(group_name):
    autoscaling = boto3.client('autoscaling')
    response = autoscaling.describe_auto_scaling_groups(AutoScalingGroupNames=[group_name])
    
    min_size = None
    if 'AutoScalingGroups' in response and len(response['AutoScalingGroups']) > 0:
        min_size = response['AutoScalingGroups'][0]['MinSize']
    
    return min_size

# Auto Scalingグループ名を指定して最小インスタンス数を取得
group_name = 'your-autoscaling-group-name'
min_size = get_autoscaling_min_size(group_name)

print("Minimum Instance Size:", min_size)
