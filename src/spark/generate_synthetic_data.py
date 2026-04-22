"""
Generates synthetic financial transaction data, writes Parquet files to MinIO,
and registers the table in Hive Metastore so it is queryable via Trino.
"""

import os
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, TimestampType
)
from faker import Faker
import random
import uuid
from datetime import datetime, timedelta

S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://minio:9000")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "minioadmin")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin")
HIVE_METASTORE_URI = os.getenv("HIVE_METASTORE_URI", "thrift://hive-metastore:9083")
NUM_ROWS = int(os.getenv("NUM_ROWS", "1000"))

S3_TABLE_PATH = "s3a://datalake/sandbox/financial_transactions"
HIVE_DATABASE = "sandbox"
HIVE_TABLE = "financial_transactions"


def build_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("GenerateSyntheticData")
        .config("spark.hadoop.fs.s3a.endpoint", S3_ENDPOINT)
        .config("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY)
        .config("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_KEY)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.sql.warehouse.dir", "s3a://datalake/warehouse")
        .config("spark.hadoop.hive.metastore.uris", HIVE_METASTORE_URI)
        .enableHiveSupport()
        .getOrCreate()
    )


def generate_rows(fake: Faker, n: int) -> list:
    currencies = ["USD", "EUR", "BRL", "GBP", "JPY"]
    statuses = ["COMPLETED", "PENDING", "FAILED"]
    base_time = datetime(2024, 1, 1)
    rows = []
    for _ in range(n):
        rows.append((
            str(uuid.uuid4()),
            str(uuid.uuid4()),
            round(random.uniform(1.0, 10000.0), 2),
            random.choice(currencies),
            base_time + timedelta(seconds=random.randint(0, 365 * 24 * 3600)),
            random.choice(statuses),
            fake.company(),
        ))
    return rows


def main():
    fake = Faker()
    spark = build_spark_session()

    schema = StructType([
        StructField("transaction_id", StringType(), False),
        StructField("account_id", StringType(), False),
        StructField("amount", DoubleType(), False),
        StructField("currency", StringType(), False),
        StructField("transaction_date", TimestampType(), False),
        StructField("status", StringType(), False),
        StructField("merchant_name", StringType(), True),
    ])

    print(f"Generating {NUM_ROWS} synthetic rows...")
    rows = generate_rows(fake, NUM_ROWS)
    df = spark.createDataFrame(rows, schema)

    print(f"Creating Hive database '{HIVE_DATABASE}' if not exists...")
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {HIVE_DATABASE} "
              f"LOCATION 's3a://datalake/sandbox'")

    print(f"Writing Parquet data to {S3_TABLE_PATH} and registering in Hive...")
    (
        df.write
        .mode("overwrite")
        .format("parquet")
        .option("path", S3_TABLE_PATH)
        .saveAsTable(f"{HIVE_DATABASE}.{HIVE_TABLE}")
    )

    count = spark.sql(f"SELECT COUNT(*) FROM {HIVE_DATABASE}.{HIVE_TABLE}").collect()[0][0]
    print(f"Done. Table '{HIVE_DATABASE}.{HIVE_TABLE}' has {count} rows.")

    spark.stop()


if __name__ == "__main__":
    main()
