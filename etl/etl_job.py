import boto3
import os
import csv
import io # 用于在内存中处理 CSV 数据

# 配置 boto3 指向 LocalStack
# 在真实 AWS 环境中，boto3 会自动查找凭证和区域
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "test")
LOCALSTACK_ENDPOINT_URL = os.environ.get("LOCALSTACK_ENDPOINT_URL", "http://localhost:4566")

# 创建 S3 客户端，指向 LocalStack
s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    endpoint_url=LOCALSTACK_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# --- ETL 逻辑 ---

source_bucket = "my-source-bucket-boto3"
source_key = "raw/input_data.csv"
target_bucket = "my-target-bucket-boto3"
target_key = "processed/filtered_data.csv" # 输出为新的 CSV 文件

print(f"--- Boto3 ETL Demo ---")
print(f"Reading from s3://{source_bucket}/{source_key}")

try:
    # 1. 提取 (Extract)：从 S3 下载文件内容
    response = s3_client.get_object(Bucket=source_bucket, Key=source_key)
    file_content = response['Body'].read().decode('utf-8')

    print("Successfully read data from S3.")

    # 使用 io.StringIO 将字符串内容模拟成文件，方便 csv 模块处理
    csvfile = io.StringIO(file_content)
    reader = csv.reader(csvfile)

    header = next(reader) # 读取头部行
    processed_rows = []
    processed_rows.append(header + ["status"]) # 添加一个状态列到头部

    # 2. 转换 (Transform)：读取每一行，过滤 value > 150 的行，并添加状态信息
    print("Starting data transformation...")
    for row in reader:
        # 假设 CSV 格式是 id,name,value
        if len(row) >= 3:
            try:
                # 尝试将 value 转换为整数进行过滤
                value = int(row[2])
                if value > 150:
                    processed_rows.append(row + ["processed"]) # 保留符合条件的行并添加状态
            except ValueError:
                # 如果 value 不是数字，跳过或按需处理
                print(f"Skipping row due to invalid value: {row}")
                pass # 忽略非数字的 value 行

    # 将处理后的行转换为新的 CSV 字符串
    output_csv_buffer = io.StringIO()
    writer = csv.writer(output_csv_buffer)
    writer.writerows(processed_rows)
    output_content = output_csv_buffer.getvalue()

    print(f"Transformation complete. Filtered {len(processed_rows) - 1} rows (excluding header).")

    # 3. 加载 (Load)：将转换后的数据上传到目标 S3 桶
    print(f"Writing processed data to s3://{target_bucket}/{target_key}")

    # 创建目标桶（如果不存在） - 更好的做法是在部署时确保桶存在
    try:
        s3_client.head_bucket(Bucket=target_bucket)
        # print(f"Target bucket {target_bucket} already exists.")
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print(f"Target bucket {target_bucket} does not exist. Creating it...")
            s3_client.create_bucket(Bucket=target_bucket)
            print(f"Target bucket {target_bucket} created.")
        else:
            raise # Re-raise the exception if it's not a 404

    # 上传处理后的内容
    s3_client.put_object(Bucket=target_bucket, Key=target_key, Body=output_content.encode('utf-8'))

    print("ETL process simulated successfully (using boto3).")

except Exception as e:
    print(f"An error occurred during Boto3 ETL process: {e}")

print(f"--- Demo Finished ---")