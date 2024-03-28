import pandas as pd
from hmpps_person_match_score.standardisation_functions import standardise_pnc_number


def test_pnc_1():
    pnc_list = [
        {"id": 1, "pnc_number": "2012/0443841T"},
        {"id": 2, "pnc_number": " 2012/0443841T "},
        {"id": 3, "pnc_number": "2012/0443841t"},
        {"id": 4, "pnc_number": "2012/ 0443841t"},
        {"id": 5, "pnc_number": "2012/0443841TA"},
        {"id": 6, "pnc_number": None},
    ]

    df = pd.DataFrame(pnc_list)
    df_result = standardise_pnc_number(df, "pnc_number")

    df_expected = [
        {"id": 1, "pnc_number_std": "2012/0443841T"},
        {"id": 2, "pnc_number_std": "2012/0443841T"},
        {"id": 3, "pnc_number_std": "2012/0443841T"},
        {"id": 4, "pnc_number_std": "2012/0443841T"},
        {"id": 5, "pnc_number_std": None},
        {"id": 6, "pnc_number_std": None},
    ]

    df_expected = pd.DataFrame(df_expected)

    pd.testing.assert_frame_equal(df_result, df_expected)


def test_pnc_2():
    pnc_list = [
        {"id": 1, "pnc_number": "2012/0443841T"},
        {"id": 2, "pnc_number": " 2012/0443841T "},
        {"id": 3, "pnc_number": "2012/0443841t"},
        {"id": 4, "pnc_number": "2012/ 0443841t"},
        {"id": 5, "pnc_number": "2012/0443841TA"},
        {"id": 6, "pnc_number": None},
    ]

    df = pd.DataFrame(pnc_list)
    df_result = standardise_pnc_number(df, "pnc_number", drop_orig=False)

    df_expected = [
        {"id": 1, "pnc_number": "2012/0443841T", "pnc_number_std": "2012/0443841T"},
        {"id": 2, "pnc_number": " 2012/0443841T ", "pnc_number_std": "2012/0443841T"},
        {"id": 3, "pnc_number": "2012/0443841t", "pnc_number_std": "2012/0443841T"},
        {"id": 4, "pnc_number": "2012/ 0443841t", "pnc_number_std": "2012/0443841T"},
        {"id": 5, "pnc_number": "2012/0443841TA", "pnc_number_std": None},
        {"id": 6, "pnc_number": None, "pnc_number_std": None},
    ]

    df_expected = pd.DataFrame(df_expected)

    pd.testing.assert_frame_equal(df_result, df_expected)


def test_pnc_3():
    pnc_list = [
        {"id": 1, "pnc_number": "1933/0993399H"},
        {"id": 2, "pnc_number": "2033/0993399H"},
        {"id": 3, "pnc_number": "2003/0993399B"},
        {"id": 4, "pnc_number": "1999/0339933H"},
        {"id": 5, "pnc_number": "2003/0993399H"},
    ]

    df = pd.DataFrame(pnc_list)
    df_result = standardise_pnc_number(df, "pnc_number", drop_orig=False)

    df_expected = [
        {"id": 1, "pnc_number": "1933/0993399H", "pnc_number_std": None},
        {"id": 2, "pnc_number": "2033/0993399H", "pnc_number_std": None},
        {"id": 3, "pnc_number": "2003/0993399B", "pnc_number_std": None},
        {"id": 4, "pnc_number": "1999/0339933H", "pnc_number_std": None},
        {"id": 5, "pnc_number": "2003/0993399H", "pnc_number_std": None},
    ]

    df_expected = pd.DataFrame(df_expected)

    pd.testing.assert_frame_equal(df_result, df_expected)
