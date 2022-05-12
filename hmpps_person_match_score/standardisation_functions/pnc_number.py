import pyspark.sql.functions as f
from pyspark.sql.dataframe import DataFrame
# from pyspark.sql.types import StringType


def standardise_pnc_number(
    df: DataFrame,
    pnc_col: str,
    drop_orig: bool = True,
):
    """Create a standardised column called pnc_number_std
    Args:
        df (DataFrame): Spark dataframe
        pnc_col (str): Name of PNC number column
        drop_orig (bool, optional): Drop original PNC number column. Defaults to True.
    Returns:
        DataFrame: Spark DataFrame with new standardised PNC number column called pnc_number_std
    """

    # Upper case and trim white space
    df = df.withColumn("pnc_number_std", f.expr("upper(trim({}))".format(pnc_col)))
    # Remove all other white space
    df = df.withColumn(
        "pnc_number_std", f.expr("regexp_replace(pnc_number_std, ' ', '')")
    )
    # Remove any PNC number entries that are too long or too short
    df = df.withColumn(
        "pnc_number_std",
        f.expr(
            "case when length(pnc_number_std) <> 13 then null else pnc_number_std end"
        ),
    )

    # Remove any bad pnc numbers
    bad_pnc_list = (
        "1933/0993399H",
        "2033/0993399H",
        "2003/0993399B",
        "1999/0339933H",
        "2003/0993399H",
    )

    pnc_sql = f"""
    case
    when upper(trim(pnc_number_std)) in {bad_pnc_list} then null
    else upper(trim(pnc_number_std))
    end
    """
    df = df.withColumn("pnc_number_std", f.expr(pnc_sql))

    if drop_orig:
        if pnc_col != "pnc_number_std":
            df = df.drop(pnc_col)

    return df