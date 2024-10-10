import os
import boto3
from lib.custom_exceptions import S3Error


class S3Accessor:
    def __init__(self, backet_name):
        self.bucket = backet_name
        self.region = os.getenv('S3_REGION')
        self.s3_client = boto3.client('s3', region_name=self.region)

    def copy_object(self, source_key, destination_key):
        try:
            self.s3_client.copy_object(
                Bucket=self.bucket,
                CopySource={'Bucket': self.bucket, 'Key': source_key},
                Key=destination_key
            )
            print(f"{source_key} から {destination_key} にオブジェクトをコピーしました。")
        except Exception as e:
            raise S3Error(f"オブジェクトのコピー中にエラーが発生しました: {e}")

    def delete_object(self, object_key):
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket,
                Key=object_key
            )
            print(f"{object_key} を削除しました。")
        except Exception as e:
            raise S3Error(f"オブジェクトの削除中にエラーが発生しました: {e}")
