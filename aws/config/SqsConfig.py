# config/sqs_config.py
import boto3
from botocore.config import Config
import logging

# 配置日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SqsConfig:
    """AWS SQS 配置信息类，提供 SQS 客户端连接"""

    @staticmethod
    def get_sqs_client():
        """创建并返回 SQS 客户端，连接 LocalStack"""
        boto3_config = Config(
            region_name="us-east-1",  # 选择区域，LocalStack 支持所有区域
            signature_version="v4"
        )

        # 使用虚拟凭证连接 LocalStack 的 SQS 服务
        sqs_client = boto3.client(
            "sqs",
            aws_access_key_id="fakeAccessKey",  # 虚拟 AWS Access Key
            aws_secret_access_key="fakeSecretAccessKey",  # 虚拟 AWS Secret Key
            endpoint_url="http://localhost:4566",  # LocalStack 的本地端点
            config=boto3_config
        )
        logger.info("SQS Client created and connected to LocalStack")
        return sqs_client
