import json
from lib.s3_accessor import S3Accessor
from lib.step_function_accessor import StepFunctionAccessor


def lambda_handler(event, context):

    record = event.get('Records', [{}])[0]

    # S3 バケット名とオブジェクトキーを取得
    bucket_name = record.get('s3', {}).get('bucket', {}).get('name')
    object_key = record.get('s3', {}).get('object', {}).get('key')

    try:

        # 移動先のオブジェクトキーを指定
        new_object_key = f"{object_key.replace('/invoice/', '/invoice/temp/')}"

        # S3Accessor のインスタンスを作成
        s3_accessor = S3Accessor(bucket_name)

        # オブジェクトをコピー
        s3_accessor.copy_object(object_key, new_object_key)

        # 元のオブジェクトを削除
        s3_accessor.delete_object(object_key)

        # StepFunction のパラメーターを作成
        input_data = {"dynamicKey": new_object_key}

        # StepFunction の 実行
        StepFunctionAccessor().start_execution(
            json.dumps(input_data)
        )

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return generate_error_response(404, "No Data Found", str(ve))

    except Exception as e:
        print(f"An error occurred {e}")
        return generate_error_response(500, "Internal Server Error", str(e))

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully')
    }


def generate_error_response(status_code, error_type, message):
    error_message = message.encode('utf-8')
    decoded_message = error_message.decode('utf-8')

    response_body = {
        'error': error_type,
        'message': decoded_message
    }

    return {
        'statusCode': status_code,
        'body': json.dumps(response_body)
    }
