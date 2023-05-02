import yaml
import re
import os
import sys

def execute_workflow(filename, input_data):
    # YAMLファイルを読み込む
    with open(filename, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    # workflowのループ
    for workflow in data:
        # conditionsのループ
        for condition in workflow['conditions']:
            # 入力データのマッチング
            if re.search(condition, input_data):
                # actionsのループ
                for action in workflow['actions']:
                    try:
                        # コマンドの実行
                        output = os.popen(f"filename={filename};{action}").read().rstrip()
                        print(output)
                    except Exception as e:
                        # 例外の発生
                        print(f"例外が発生しました: {e}")
                        raise e

# コマンドライン引数から入力データとYAMLファイル名を取得する
if len(sys.argv) < 3:
    print("引数が不足しています。YAMLファイル名と入力データを指定してください。")
    sys.exit(1)
filename = sys.argv[1]
input_data = sys.argv[2]

# ワークフローの実行
execute_workflow(filename, input_data)
