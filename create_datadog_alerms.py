import pandas as pd

def generate_terraform(monitor_name, query, threshold, tags):
    terraform_code = f'''
resource "datadog_monitor" "{monitor_name}" {{
  name               = "{monitor_name}"
  type               = "query alert"
  query              = "{query}"
  message            = "Triggered alert for {monitor_name}"
  threshold_warning  = {threshold}
  tags               = {tags}
}}
'''

    return terraform_code

def csv_to_terraform(csv_file):
    df = pd.read_csv(csv_file)

    terraform_code = ""
    for _, row in df.iterrows():
        monitor_name = row['Monitor Name']
        query = row['Query']
        threshold = row['Threshold']
        tags = row['Tags']
        
        terraform_code += generate_terraform(monitor_name, query, threshold, tags)

    return terraform_code

# CSVファイル名と出力するTerraformファイル名を指定してください
csv_file = 'monitors.csv'
terraform_file = 'datadog_monitors.tf'

# CSVファイルからTerraformのコードを生成
terraform_code = csv_to_terraform(csv_file)

# Terraformファイルにコードを書き出す
with open(terraform_file, 'w') as f:
    f.write(terraform_code)

print(f'Terraformコードが {terraform_file} に書き出されました。')
