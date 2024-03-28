import pandas as pd

from hmpps_person_match_score.standardisation_functions import standardise_names


def test_names_1():
    names_list = [
        {"id": 1, "first_name": "John-paul", "surname": "smith jones"},
        {"id": 2, "first_name": "john", "surname": "Smith-Jones"},
        {"id": 3, "first_name": "john.smith", "surname": "jones"},
    ]

    df = pd.DataFrame(names_list)
    df_result = standardise_names(df, ["first_name", "surname"])

    df_expected = [
        {
            "id": 1,
            "surname_std": "jones",
            "forename1_std": "john",
            "forename2_std": "paul",
            "forename3_std": "smith",
            "forename4_std": None,
            "forename5_std": None,
        },
        {
            "id": 2,
            "surname_std": "jones",
            "forename1_std": "john",
            "forename2_std": "smith",
            "forename3_std": None,
            "forename4_std": None,
            "forename5_std": None,
        },
        {
            "id": 3,
            "surname_std": "jones",
            "forename1_std": "john",
            "forename2_std": "smith",
            "forename3_std": None,
            "forename4_std": None,
            "forename5_std": None,
        },
    ]

    df_expected = pd.DataFrame(df_expected)

    pd.testing.assert_frame_equal(df_result, df_expected)

    # This test tests standarisation options we do not use as standard
