import pytest

import pyspark
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import types

@pytest.fixture(scope="function")
def spark():
    
    conf = SparkConf()

    conf.set("spark.sql.shuffle.partitions", "1")
    conf.set("spark.jars",
        "hmpps_person_match_score/jars/scala-udf-similarity-0.0.8.jar,hmpps_person_match_score/jars/graphframes-0.8.0-spark3.0-s_2.12.jar",)
    conf.set("spark.driver.memory", "4g")
    conf.set("spark.sql.shuffle.partitions", "24")

    sc = SparkContext.getOrCreate(conf=conf)

    spark = SparkSession(sc)


    SPARK_EXISTS = True

    yield spark