graph TD
    subgraph 数据源
        A[核心银行系统] --> K[Kafka]
        B[CRM 系统] --> K
        C[外部数据源] --> K
    end

    subgraph 数据摄取
        K --> SS[Spark Streaming]
    end

    subgraph 数据处理
        SS --> H[Hadoop HDFS]
        H --> SB[Spark Batch]
        SB --> I[Apache Iceberg]
        SB --> DQM[数据质量监控器]
    end

    subgraph 数据存储
        I --> HV[Hive]
        I --> T[Trino]
    end

    subgraph 调度
        AF[Airflow] --> SB
        AF --> DQM
    end

    subgraph 可视化
        T --> TB[Tableau]
    end

    subgraph 分析
        FFA[资金流向分析器] --> I
        FFA --> TB
    end

    AN[分析师] --> TB
    AN --> AF