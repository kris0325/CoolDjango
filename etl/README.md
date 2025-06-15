# OVERIEW
> 我来解释这个 ETL + AWS Glue + S3 (LocalStack 模拟) 的 demo 项目，并告诉你如何执行、调试。这个 demo 展示了如何使用 LocalStack 模拟 AWS 环境来开发和测试 ETL 流程。主要特点：

## 核心组件
- **LocalStack**: 在本地模拟 AWS S3、Glue 等服务
- **Docker Compose**: 管理容器化环境
- **Boto3**: Python 的 AWS SDK，用于与模拟的 AWS 服务交互

## ETL 流程
1. **Extract**: 从 S3 源桶读取 CSV 数据
2. **Transform**: 过滤 value > 150 的记录，添加状态列
3. **Load**: 将处理后的数据保存到目标 S3 桶

## 执行步骤
1. 运行 `docker-compose up -d` 启动 LocalStack
2. 创建测试数据并上传到模拟的 S3
3. 运行 Python ETL 脚本
4. 验证处理结果

## 调试技巧
- 使用 AWS CLI 连接 LocalStack 检查数据
- 查看容器日志排查问题
- 在脚本中添加详细的日志输出
- 验证中间处理结果

这个环境特别适合：
- 学习 AWS 数据服务
- 开发 ETL 流程
- 测试数据处理逻辑
- 避免产生 AWS 费用
---
---
> 需要我详细解释任何特定的部分吗？


# ETL + AWS Glue + S3 (LocalStack) Demo 执行指南

## 项目概述

这是一个使用 LocalStack 模拟 AWS 环境的 ETL (Extract, Transform, Load) 演示项目，主要组件：

- **LocalStack**: 模拟 AWS 服务（S3, Glue, DataBrew）
- **Docker Compose**: 容器编排管理
- **Boto3**: AWS SDK for Python
- **ETL 脚本**: 数据提取、转换、加载逻辑

## 执行步骤

### 1. 启动环境

```bash
# 启动 LocalStack 容器
docker-compose up -d

# 检查容器状态
docker-compose ps
```

### 2. 准备测试数据

有三种方式创建测试数据，选择其中一种即可：

#### 方法1: 使用 AWS CLI (需要安装)

```bash
# 安装 AWS CLI (如果未安装)
# Windows: https://awscli.amazonaws.com/AWSCLIV2.msi
# macOS: brew install awscli
# Linux: pip install awscli

# 配置 LocalStack 凭证
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1

# 或者使用 aws configure 设置
aws configure set aws_access_key_id test
aws configure set aws_secret_access_key test
aws configure set default.region us-east-1

# 创建源数据桶
aws --endpoint-url=http://localhost:4566 s3 mb s3://my-source-bucket-boto3

# 创建测试 CSV 文件
cat > input_data.csv << EOF
id,name,value
1,Alice,100
2,Bob,200
3,Charlie,50
4,David,300
5,Eve,175
EOF

# 上传测试数据到 S3
aws --endpoint-url=http://localhost:4566 s3 cp input_data.csv s3://my-source-bucket-boto3/raw/input_data.csv
```

#### 方法2: 使用 Python boto3 (推荐，无需安装 AWS CLI)

创建 `setup_data.py` 文件：

```python
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
```

运行设置脚本：
```bash
python setup_data.py
```

#### 方法3: 使用 Docker 中的 AWS CLI

```bash
# 使用包含 AWS CLI 的 Docker 容器
docker run --rm -it --network host \
  -e AWS_ACCESS_KEY_ID=test \
  -e AWS_SECRET_ACCESS_KEY=test \
  -e AWS_DEFAULT_REGION=us-east-1 \
  amazon/aws-cli \
  --endpoint-url=http://localhost:4566 \
  s3 mb s3://my-source-bucket-boto3

# 创建测试文件并上传
echo "id,name,value
1,Alice,100
2,Bob,200
3,Charlie,50
4,David,300
5,Eve,175" > input_data.csv

docker run --rm -it --network host \
  -v $(pwd):/aws \
  -e AWS_ACCESS_KEY_ID=test \
  -e AWS_SECRET_ACCESS_KEY=test \
  -e AWS_DEFAULT_REGION=us-east-1 \
  amazon/aws-cli \
  --endpoint-url=http://localhost:4566 \
  s3 cp /aws/input_data.csv s3://my-source-bucket-boto3/raw/input_data.csv
```

### 3. 运行 ETL 脚本

```bash
# 设置环境变量
export LOCALSTACK_ENDPOINT_URL=http://localhost:4566
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test

# 运行 ETL 脚本
python etl_demo.py
```

## ETL 逻辑详解

### Extract (提取)
- 从 S3 源桶读取 CSV 文件
- 使用 boto3 的 `get_object()` 方法

### Transform (转换)  
- 过滤 value > 150 的记录
- 添加 "status" 列标记为 "processed"
- 处理数据格式和异常值

### Load (加载)
- 创建目标桶（如果不存在）
- 将处理后的数据上传到目标 S3 桶

## 调试方法

### 1. 检查 LocalStack 状态

```bash
# 查看容器日志
docker-compose logs localstack

# 检查 S3 服务是否正常
curl http://localhost:4566/_localstack/health
```

### 2. 验证 S3 桶和对象

#### 使用 AWS CLI (如果已安装)
```bash
# 列出所有桶
aws --endpoint-url=http://localhost:4566 s3 ls

# 查看源桶内容
aws --endpoint-url=http://localhost:4566 s3 ls s3://my-source-bucket-boto3/raw/

# 查看目标桶内容
aws --endpoint-url=http://localhost:4566 s3 ls s3://my-target-bucket-boto3/processed/

# 下载处理后的文件查看结果
aws --endpoint-url=http://localhost:4566 s3 cp s3://my-target-bucket-boto3/processed/filtered_data.csv ./output.csv
```

#### 使用 Python boto3 验证 (推荐)
创建 `verify_s3.py` 文件：

```python
import boto3

s3_client = boto3.client(
    "s3",
    region_name="us-east-1",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

try:
    # 列出所有桶
    buckets = s3_client.list_buckets()
    print("Available buckets:")
    for bucket in buckets['Buckets']:
        print(f"  - {bucket['Name']}")
    
    # 查看源桶内容
    print("\nSource bucket contents:")
    try:
        objects = s3_client.list_objects_v2(Bucket="my-source-bucket-boto3")
        if 'Contents' in objects:
            for obj in objects['Contents']:
                print(f"  - {obj['Key']} ({obj['Size']} bytes)")
        else:
            print("  (empty)")
    except Exception as e:
        print(f"  Error: {e}")
    
    # 查看目标桶内容
    print("\nTarget bucket contents:")
    try:
        objects = s3_client.list_objects_v2(Bucket="my-target-bucket-boto3")
        if 'Contents' in objects:
            for obj in objects['Contents']:
                print(f"  - {obj['Key']} ({obj['Size']} bytes)")
        else:
            print("  (empty)")
    except Exception as e:
        print(f"  Error: {e}")
    
    # 下载并查看处理后的文件内容
    print("\nProcessed file content:")
    try:
        response = s3_client.get_object(
            Bucket="my-target-bucket-boto3", 
            Key="processed/filtered_data.csv"
        )
        content = response['Body'].read().decode('utf-8')
        print(content)
    except Exception as e:
        print(f"  Error: {e}")

except Exception as e:
    print(f"Connection error: {e}")
```

运行验证脚本：
```bash
python verify_s3.py
```

### 3. Python 脚本调试

在 ETL 脚本中添加调试代码：

```python
# 添加详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 打印中间结果
print(f"原始数据行数: {len(list(csv.reader(io.StringIO(file_content))))}")
print(f"处理后数据行数: {len(processed_rows)}")

# 查看处理的具体数据
for i, row in enumerate(processed_rows[:5]):  # 只显示前5行
    print(f"Row {i}: {row}")
```

## 常见问题排查

### 1. 连接问题
- **确保** LocalStack 容器已启动: `docker-compose ps`
- 检查端口是否可访问: `curl http://localhost:4566`

### 2. 权限问题
- 确保环境变量设置正确
- LocalStack 使用固定的测试凭证

### 3. 数据问题
- 检查源文件是否存在且格式正确
- 验证 CSV 数据格式和编码

### 4. 内存问题
- 对于大文件，考虑流式处理而非一次性加载到内存

## 扩展功能

### 1. 添加 AWS Glue 作业
```python
import boto3

glue_client = boto3.client(
    'glue',
    region_name='us-east-1',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

# 创建 Glue 数据库
glue_client.create_database(
    DatabaseInput={
        'Name': 'etl_database',
        'Description': 'ETL demo database'
    }
)
```

### 2. 数据质量检查
```python
def validate_data(processed_rows):
    """验证处理后的数据质量"""
    valid_rows = 0
    for row in processed_rows[1:]:  # 跳过标题行
        if len(row) >= 4 and row[3] == "processed":
            valid_rows += 1
    return valid_rows
```

### 3. 错误处理和重试
```python
import time
from botocore.exceptions import ClientError

def upload_with_retry(s3_client, bucket, key, data, max_retries=3):
    """带重试机制的上传"""
    for attempt in range(max_retries):
        try:
            s3_client.put_object(Bucket=bucket, Key=key, Body=data)
            return True
        except ClientError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # 指数退避
    return False
```

## 清理环境

```bash
# 停止并删除容器
docker-compose down

# 删除数据卷（可选）
docker-compose down -v
```

这个 demo 展示了一个完整的本地 ETL 开发和测试环境，可以在不产生 AWS 费用的情况下学习和实验 AWS 数据处理服务。