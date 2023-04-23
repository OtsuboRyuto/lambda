import boto3

pricing_client = boto3.client('pricing', region_name='us-east-1')

response = pricing_client.get_products(
    ServiceCode='AmazonEC2',
    Filters=[
        {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': 't2.micro'},
        {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': 'Linux'}
    ],
    MaxResults=1
)

product = response['PriceList'][0]['product']
sku = product['sku']

price_response = pricing_client.get_products(
    ServiceCode='AmazonEC2',
    Skus=[sku]
)

price_dimension = price_response['PriceList'][0]['terms']['OnDemand'][sku]['priceDimensions']

usd_per_unit = float(price_dimension.values()[0]['pricePerUnit']['USD'])

total_price = usd_per_unit * 100

print(total_price)
