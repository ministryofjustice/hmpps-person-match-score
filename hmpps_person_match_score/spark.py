import logging
from pyspark.context import SparkContext, SparkConf
from pyspark.sql import SparkSession, types


def spark(jars):

    logging.info("Initialising spark...")
    conf = SparkConf()

    conf.set("spark.sql.shuffle.partitions", "1")
    conf.set("spark.driver.memory", "4g")
    conf.set("spark.sql.shuffle.partitions", "24")
    conf.set("spark.jars", jars)

    sc = SparkContext.getOrCreate(conf=conf)
    # sc.setCheckpointDir("temp_graphframes/")
    spark_session = SparkSession(sc)

    # Register UDFs
    spark_session.udf.registerJavaFunction(
        "jaro_winkler_sim",
        "uk.gov.moj.dash.linkage.JaroWinklerSimilarity",
        types.DoubleType(),
    )
    spark_session.udf.registerJavaFunction(
        "Dmetaphone", "uk.gov.moj.dash.linkage.DoubleMetaphone", types.StringType()
    )

    logging.info("Spark initialised")

    return spark_session
