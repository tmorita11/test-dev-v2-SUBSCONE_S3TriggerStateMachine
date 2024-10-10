# test-dev-v2-SUBSCONE_S3TriggerStateMachine
請求書通知: S3トリガーでステートマシン起動

## 概要
このLambda関数は、請求書通知機能のステートマシン起動を行います。
- S3へのファイル配置(PUT/POST/COPY)によりLambdaを実行
  - バケット: dev-v2-subscone-s3-export
  - プレフィックス: input/invoice/to_sendgrid_
  - サフィックス: .json
- S3のファイル（JSON形式）を作業フォルダ(input/invoice/temp)に移動
- StepFunctions(請求書通知ステートマシン)の起動中でないことを確認(二重起動防止チェック)
- StepFunctions(請求書通知ステートマシン)の起動


## 動作確認手順
1. AWSコンソールにアクセス
   - 環境: [test-dev-v2-SUBSCONE_InvoiceNotify_S3TriggerStateMachine](https://ap-northeast-1.console.aws.amazon.com/lambda/home?region=ap-northeast-1#/functions/test-dev-v2-SUBSCONE_InvoiceNotify_S3TriggerStateMachine?tab=code)
1. Lambda関数のテストを実行
   - Lambda管理画面でテストイベントを設定し、以下のJSONを入力します。
        ```
        {
          "Records": [
            {
              "s3": {
                "bucket": {
                  "name": "dev-v2-subscone-s3-export"
                },
                "object": {
                  "key": "R0601DJICPA001/input/invoice/to_sendgrid_20241010185015_886.json"
                }
              }
            }
          ]
        }
        ```
   - 「実行」ボタンを押下してLambda関数を実行します。
2. CloudWatch Logsの確認
  - AWSコンソールで「CloudWatch」にアクセスしてエラーになっていないことを確認
    - 環境: [/aws/lambda/test-dev-v2-SUBSCONE_InvoiceNotify_S3TriggerStateMachine](https://ap-northeast-1.console.aws.amazon.com/cloudwatch/home?region=ap-northeast-1#logsV2:log-groups/log-group/$252Faws$252Flambda$252Ftest-dev-v2-SUBSCONE_InvoiceNotify_S3TriggerStateMachine)
  - StepFunctions(請求書通知ステートマシン)が起動されることを確認
    - 環境: [test-dev-v2-SUBSCONE_InvoiceNotify_StateMachine](https://ap-northeast-1.console.aws.amazon.com/states/home?region=ap-northeast-1#/statemachines/view/arn%3Aaws%3Astates%3Aap-northeast-1%3A576020323393%3AstateMachine%3Atest-dev-v2-SUBSCONE_InvoiceNotify_StateMachine?type=%E6%A8%99%E6%BA%96)
