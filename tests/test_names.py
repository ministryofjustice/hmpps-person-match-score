import pytest
import pandas as pd
from hmpps_person_match_score.standardisation_functions.names import standardise_names
from pyspark.sql import Row

def test_names_1(spark):

    names_list = [
        {"id":1, "first_name":"John-paul","surname":"smith jones"},
        {"id":2, "first_name":"john","surname":"Smith-Jones"},
        {"id":3, "first_name":"john.smith","surname":"jones"}
        ]

    df = spark.createDataFrame(Row(**x) for x in names_list)
    df = standardise_names(df, ["first_name", "surname"])

    df_result = df.toPandas()

    df_expected = [
     {'id': 1, 'surname_std': 'jones', 'forename1_std': 'john', 'forename2_std': 'paul', 'forename3_std': 'smith', 'forename4_std': None, 'forename5_std': None},
     {'id': 2, 'surname_std': 'jones', 'forename1_std': 'john', 'forename2_std': 'smith', 'forename3_std': None, 'forename4_std': None, 'forename5_std': None},
     {'id': 3, 'surname_std': 'jones', 'forename1_std': 'john', 'forename2_std': 'smith', 'forename3_std': None, 'forename4_std': None, 'forename5_std': None}
     ]

    df_expected = pd.DataFrame(df_expected)

    pd.testing.assert_frame_equal(df_result,df_expected)


    names_list = [
        {"id":1, "first_name":"john", "middle_name": "james peter", "surname":"smith-jones"},
        {"id":2, "first_name":"john", "middle_name": "james peter smith", "surname":"jones"},
        ]

    df = spark.createDataFrame(Row(**x) for x in names_list)
    df = standardise_names(df, ["first_name", "middle_name", "surname"], retain_surname=True)

    df_result = df.toPandas()

    df_expected = [
     {'id': 1, 'surname_std': 'smith jones', 'forename1_std': 'john', 'forename2_std': 'james', 'forename3_std': "peter", 'forename4_std': None, 'forename5_std': None},
     {'id': 2, 'surname_std': 'jones', 'forename1_std': 'john', 'forename2_std': 'james', 'forename3_std': "peter", 'forename4_std': "smith", 'forename5_std': None},

     ]

    df_expected = pd.DataFrame(df_expected)

    pd.testing.assert_frame_equal(df_result,df_expected)


