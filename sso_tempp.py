import hashlib
import hmac
import json

def lambda_handler(event, context):
    # 共有の秘密鍵
    secret_key = "your_shared_secret_key"

    # リクエストヘッダーから必要な情報を取得
    client_signature = event['headers'].get('X-HMAC-Signature')
    request_body = event['body']

    # 署名の作成
    calculated_signature = create_hmac_signature(secret_key, request_body)

    # 署名の検証
    if client_signature == calculated_signature:
        response = {
            'statusCode': 200,
            'body': 'Authentication successful'
        }
    else:
        response = {
            'statusCode': 401,
            'body': 'Authentication failed'
        }

    return response


def create_hmac_signature(secret_key, data):
    # HMAC-SHA256を使用して署名を作成
    signature = hmac.new(secret_key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256)
    calculated_signature = signature.hexdigest()

    return calculated_signature
