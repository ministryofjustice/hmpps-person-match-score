import pytest
import pandas as pd
from hmpps_person_match_score.standardisation_functions import fix_zero_length_strings


def test_fix_1():
    names_list = [
        {"id": 1, "first_name": "", "surname": "a"},
        {"id": 2, "first_name": " ", "surname": "b"},
        {"id": 3, "first_name": " john", "surname": None},
    ]

    df = pd.DataFrame(names_list)
    df = df[names_list[0].keys()]

    df_result = fix_zero_length_strings(df)

    df_expected = [
        {"id": 1, "first_name": None, "surname": "a"},
        {"id": 2, "first_name": None, "surname": "b"},
        {"id": 3, "first_name": "john", "surname": None},
    ]

    df_expected = pd.DataFrame(df_expected)

    pd.testing.assert_frame_equal(df_result, df_expected)
