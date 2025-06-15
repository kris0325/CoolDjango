from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

# 配置 Spark，并启用 Web UI
conf = SparkConf().setAppName("WordCount").setMaster("local[*]")
conf.set("spark.ui.port", "4040")  # 默认 Spark UI 端口
sc = SparkContext(conf=conf)

# 创建 SparkSession，用于执行 SQL 查询
spark = SparkSession(sc)

# 读取文本文件
input_file = "sample.txt"
text_file = sc.textFile(input_file)

# 分割单词并统计出现的频率
words = text_file.flatMap(lambda line: line.split(" "))
word_counts = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

# 转换为 DataFrame，以便使用 Spark SQL API
word_df = word_counts.toDF(["word", "count"])
word_df.createOrReplaceTempView("word_counts")

# 执行简单的 SQL 查询
result_df = spark.sql("SELECT word, count FROM word_counts WHERE count > 1")

# 展示查询结果
result_df.show()

# 停止 SparkContext
sc.stop()
