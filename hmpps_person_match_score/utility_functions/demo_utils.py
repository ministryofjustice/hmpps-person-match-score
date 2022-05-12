from pyspark.context import SparkContext, SparkConf
from pyspark.sql import SparkSession

def get_spark():
    conf = SparkConf()

    # Load in a jar that provides extended string comparison functions such as Jaro Winkler.
    # Splink
    conf.set(
        "spark.jars",
        "hmpps_person_match_score/jars/scala-udf-similarity-0.0.8.jar,hmpps_person_match_score/jars/graphframes-0.8.0-spark3.0-s_2.12.jar",
    )

    sc = SparkContext.getOrCreate(conf=conf)
    sc.setCheckpointDir("temp_graphframes/")
    spark = SparkSession(sc)

    # Register UDFs
    from pyspark.sql import types

    spark.udf.registerJavaFunction(
        "jaro_winkler_sim",
        "uk.gov.moj.dash.linkage.JaroWinklerSimilarity",
        types.DoubleType(),
    )
    spark.udf.registerJavaFunction(
        "Dmetaphone", "uk.gov.moj.dash.linkage.DoubleMetaphone", types.StringType()
    )
    return spark