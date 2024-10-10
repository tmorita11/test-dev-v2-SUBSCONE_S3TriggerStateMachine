import boto3
import os
from lib.custom_exceptions import StepFunctionError


class StepFunctionAccessor:
    def __init__(self):
        self.region = os.getenv('S3_REGION')
        self.client = boto3.client('stepfunctions', region_name=self.region)
        self.state_machine_arn = os.getenv('STATE_MACHINE_ARN')

    def is_execution_running(self):
        try:
            response = self.client.list_executions(
                stateMachineArn=self.state_machine_arn,
                statusFilter='RUNNING'
            )
            return len(response['executions']) > 0  # 実行中のものがあるかどうか
        except Exception as e:
            raise StepFunctionError(f"実行状況の取得中にエラーが発生しました: {e}")

    def start_execution(self, input_data=None):
        if self.is_execution_running():
            # 実行中の Step Function がある場合に例外をスロー
            raise StepFunctionError("既に実行中の Step Function が存在します。新しい実行は開始できません。")

        try:
            response = self.client.start_execution(
                stateMachineArn=self.state_machine_arn,
                input=input_data
            )
            print(f"Step Function の実行を開始しました: {response['executionArn']}")
            return response
        except Exception as e:
            raise StepFunctionError(f"Step Function の実行開始中にエラーが発生しました: {e}")
