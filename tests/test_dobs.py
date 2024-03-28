import datetime

import pandas as pd
from hmpps_person_match_score.standardisation_functions import (
    standardise_dob,
    null_suspicious_dob_std,
)


def test_dob_1():
    dt = datetime.datetime(2020, 5, 25, 8, 5, 44, 815715)
    date = dt.date()
    date_str = date.strftime("%Y-%m-%d")
    date_str_alt = date.strftime("%d/%m/%Y")

    names_list = [
        {
            "A": dt,
            "B": date,
            "C": date_str,
            "D": date_str_alt,
            "E": None,
            "F": None,
            "G": None,
        }
    ]

    df = pd.DataFrame(names_list)

    expected = [
        {"dob_std": "2020-05-25"},
        {"dob_std": "2020-05-25"},
        {"dob_std": "2020-05-25"},
        {"dob_std": "2020-05-25"},
        {"dob_std": None},
        {"dob_std": None},
        {"dob_std": None},
    ]
    df_expected = pd.DataFrame(expected)

    df_result = standardise_dob(df[["A"]], "A")
    pd.testing.assert_frame_equal(
        df_result, df_expected.iloc[[0], :].reset_index(drop=True)
    )

    df_result = standardise_dob(df[["B"]], "B")
    pd.testing.assert_frame_equal(
        df_result, df_expected.iloc[[1], :].reset_index(drop=True)
    )

    df_result = standardise_dob(df[["C"]], "C")
    pd.testing.assert_frame_equal(
        df_result, df_expected.iloc[[2], :].reset_index(drop=True)
    )

    df_result = standardise_dob(df[["D"]], "D")
    pd.testing.assert_frame_equal(
        df_result, df_expected.iloc[[3], :].reset_index(drop=True)
    )

    df_result = standardise_dob(df[["E"]], "E")
    pd.testing.assert_frame_equal(
        df_result, df_expected.iloc[[4], :].reset_index(drop=True)
    )

    df_result = standardise_dob(df[["F"]], "F")
    pd.testing.assert_frame_equal(
        df_result, df_expected.iloc[[5], :].reset_index(drop=True)
    )

    df_result = standardise_dob(df[["G"]], "G")
    pd.testing.assert_frame_equal(
        df_result, df_expected.iloc[[6], :].reset_index(drop=True)
    )


# Unsure this is the best way of handling.  Should we be nulling instead of raising an error.  What about people who were actually born 1970-01-01?


def test_null_suspicious_dob_std():
    dt = datetime.datetime(1900, 1, 1, 8, 5, 44, 815715)
    date = dt.date()
    date_str = date.strftime("%Y-%m-%d")
    date_str_alt = date.strftime("%d/%m/%Y")

    names_list = [{"A": "1900-01-01", "B": "1970-01-01", "C": None}]

    df = pd.DataFrame(names_list)

    expected = [{"dob_std": None}, {"dob_std": None}, {"dob_std": None}]
    df_expected = pd.DataFrame(expected)

    df_result = null_suspicious_dob_std(df[["A"]], "A")
    pd.testing.assert_frame_equal(
        df_result, df_expected.iloc[[0], :].reset_index(drop=True)
    )

    df_result = null_suspicious_dob_std(df[["B"]], "B")
    pd.testing.assert_frame_equal(
        df_result, df_expected.iloc[[1], :].reset_index(drop=True)
    )

    df_result = null_suspicious_dob_std(df[["C"]], "C")
    pd.testing.assert_frame_equal(
        df_result, df_expected.iloc[[2], :].reset_index(drop=True)
    )
