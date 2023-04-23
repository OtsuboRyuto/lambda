import json
import boto3

pricing = boto3.client('pricing')

def calculate_savings_plan(instance_family, commitment, coverage):
    # AWSのPricing APIから、インスタンスファミリーの現在のオンデマンド料金を取得
    response = pricing.get_products(
        ServiceCode='AmazonEC2',
        Filters=[
            {
                'Type': 'TERM_MATCH',
                'Field': 'instanceFamily',
                'Value': instance_family
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'operatingSystem',
                'Value': 'Linux'
            }
        ],
        FormatVersion='aws_v1',
        MaxResults=1
    )
    ondemand_price = float(response['PriceList'][0]['terms']['OnDemand']['USD'])

    # 必要なカバレッジを計算
    required_coverage = 1.0
    while True:
        # 必要なSavings Plansの数量を計算
        required_savings_plans = round(ondemand_price * commitment / (ondemand_price * (1 - coverage)))
        
        # 必要な購入コストを計算
        savings_plans_price = get_savings_plans_price(instance_family, coverage, commitment)
        required_cost = savings_plans_price * required_savings_plans
        
        # カバレッジが100%以上になった場合、計算結果を返す
        if required_coverage >= 1.0:
            return {
                'required_savings_plans': required_savings_plans,
                'required_cost': required_cost,
                'required_coverage': required_coverage
            }
        
        # 購入コストが$0以下の場合、カバレッジを増やす
        if required_cost <= 0:
            required_coverage += 0.01
        # 購入コストが$0より大きい場合、計算結果を返す
        else:
            return {
                'required_savings_plans': required_savings_plans,
                'required_cost': required_cost,
                'required_coverage': required_coverage
            }

def get_savings_plans_price(instance_family, coverage, commitment):
    # AWSのPricing APIから、Savings Plansの価格を取得
    response = pricing.get_products(
        ServiceCode='AWSSavingsPlans',
        Filters=[
            {
                'Type': 'TERM_MATCH',
                'Field': 'instanceFamily',
                'Value': instance_family
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'productFamily',
                'Value': 'ComputeSavingsPlans'
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'savingsPlanType',
                'Value': 'Compute'
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'termType',
                'Value': 'Commitment'
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'region',
                'Value': 'US East (N. Virginia)'
            }],
                FormatVersion='aws_v1',
                MaxResults=1
        )
    discount_rate = float(response['PriceList'][0]['product']['attributes']['savingsPlanEffectiveDiscountRate'])
    term_length = int(response['PriceList'][0]['product']['attributes']['termLength'])
    term_payment_option = response['PriceList'][0]['product']['attributes']['paymentOption']
    upfront_price = float(response['PriceList'][0]['terms']['Upfront']['USD'])
    hourly_price = float(response['PriceList'][0]['terms']['Hourly']['USD'])

    # オンデマンド利用料に対するSavings Plansの割引率を計算
    ondemand_discount_rate = 1 - (upfront_price / (term_length * 365 * 24) / commitment + hourly_price) / ondemand_price

    # 必要なカバレッジに基づいたSavings Plansの割引率を計算
    required_discount_rate = coverage * (ondemand_discount_rate - 1) + 1

    # 必要なSavings Plansの割引率に対応する価格を計算
    if term_payment_option == 'No Upfront':
        savings_plans_price = hourly_price * required_discount_rate
    else:
        savings_plans_price = upfront_price / commitment + hourly_price * required_discount_rate

    return savings_plans_price

def lambda_handler(event, context):
    # イベントから必要な情報を取得
    commitment = int(event['commitment'])
    instance_family = event['instance_family']
    # カバレッジを100％にするために必要なSavings Plansの購入量を計算
    result = calculate_savings_plan(instance_family, commitment, 0.0)
    required_savings_plans = result['required_savings_plans']
    required_cost = result['required_cost']

    # 必要なSavings Plansの購入量を追加計算
    for i in range(1, 101):
        result = calculate_savings_plan(instance_family, commitment, i / 100)
        if result['required_cost'] <= required_cost:
            required_savings_plans = result['required_savings_plans']
            required_cost = result['required_cost']

    # 結果を返す
    return {
        'required_savings_plans': required_savings_plans,
        'required_cost': required_cost
    }