import datetime
import pytest
import pandas as pd
from hmpps_person_match_score.standardisation_functions.date_of_birth import standardise_dob,null_suspicious_dob_std
from pyspark.sql import Row

def test_dob_1(spark):


    dt = datetime.datetime(2020, 5, 25, 8, 5, 44, 815715)
    date = dt.date()
    date_str = date.strftime("%Y-%m-%d")
    date_str_alt = date.strftime("%d/%m/%Y")

    names_list = [
            {"dob_datetime": dt, "dob_date": date,"dob_str":date_str},
            {"dob_datetime": dt, "dob_date": date,"dob_str":date_str_alt},
            {"dob_datetime": None, "dob_date": None,"dob_str":None}
            ]

    df = spark.createDataFrame(Row(**x) for x in names_list)

    expected = [
        {"dob_std": "2020-05-25"},
        {"dob_std": "2020-05-25"},
        {"dob_std": None}
        ]
    df_expected = pd.DataFrame(expected)
    df2 = standardise_dob(df.select("dob_datetime"), "dob_datetime")
    df_result = df2.toPandas()

    pd.testing.assert_frame_equal(df_result,df_expected)

    expected = [
        {"dob_std": "2020-05-25"},
        {"dob_std": "2020-05-25"},
        {"dob_std": None}
        ]
    df_expected = pd.DataFrame(expected)
    df2 = standardise_dob(df.select("dob_date"), "dob_date")
    df_result = df2.toPandas()

    pd.testing.assert_frame_equal(df_result,df_expected)


    expected = [
        {"dob_std": "2020-05-25"},
        {"dob_std": None},
        {"dob_std": None}
        ]
    df_expected = pd.DataFrame(expected)
    df2 = standardise_dob(df.select("dob_str"), "dob_str")
    df_result = df2.toPandas()

    pd.testing.assert_frame_equal(df_result,df_expected)


    expected = [
        {"dob_std": None},
        {"dob_std": "2020-05-25"},
        {"dob_std": None}
        ]
    df_expected = pd.DataFrame(expected)
    df2 = standardise_dob(df.select("dob_str"), "dob_str", "dd/MM/yyyy")
    df_result = df2.toPandas()

    pd.testing.assert_frame_equal(df_result,df_expected)
    
def test_null_suspicious_dob_std(spark):


    dt = datetime.datetime(1900, 1, 1, 8, 5, 44, 815715)
    date = dt.date()
    date_str = date.strftime("%Y-%m-%d")
    date_str_alt = date.strftime("%d/%m/%Y")

    names_list =  [
        {"dob_lol": "1900-01-01"},
        {"dob_lol": "1970-01-01"},
        {"dob_lol": None}
        ]
   

    df = spark.createDataFrame(Row(**x) for x in names_list)

    expected = [
        {"dob_lol": None},
        {"dob_lol": None},
        {"dob_lol": None}
        ]
    df_expected = pd.DataFrame(expected)
    df2 = null_suspicious_dob_std(df.select("dob_lol"), "dob_lol")
    df_result = df2.toPandas()

    pd.testing.assert_frame_equal(df_result,df_expected)