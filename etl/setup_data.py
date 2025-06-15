import boto3
import os

# 配置 LocalStack 连接
s3_client = boto3.client(
    "s3",
    region_name="us-east-1",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# 创建测试 CSV 数据
test_data = """id,name,value
1,Alice,100
2,Bob,200
3,Charlie,50
4,David,300
5,Eve,175"""

try:
    # 创建源数据桶
    s3_client.create_bucket(Bucket="my-source-bucket-boto3")
    print("Created source bucket: my-source-bucket-boto3")
    
    # 上传测试数据
    s3_client.put_object(
        Bucket="my-source-bucket-boto3",
        Key="raw/input_data.csv",
        Body=test_data.encode('utf-8')
    )
    print("Uploaded test data to s3://my-source-bucket-boto3/raw/input_data.csv")
    
    # 验证上传成功
    objects = s3_client.list_objects_v2(Bucket="my-source-bucket-boto3")
    if 'Contents' in objects:
        print("Files in bucket:")
        for obj in objects['Contents']:
            print(f"  - {obj['Key']}")
    
except Exception as e:
    print(f"Error: {e}")