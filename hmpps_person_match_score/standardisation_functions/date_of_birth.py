from pyspark.sql.functions import expr
from pyspark.sql.functions import date_format, to_timestamp
from pyspark.sql.dataframe import DataFrame


def standardise_dob(
    df: DataFrame,
    dob_col: str,
    date_fmt_if_string: str = "yyyy-MM-dd",
    drop_orig: bool = True,
):
    """Create column called dob_std with dob as a string in yyyy-MM-dd format
    or null otherwise

    Args:
        df (DataFrame): Spark dataframe
        dob_col (str): Name of dob column
        date_fmt_if_string (str, optional): Date format if incoming dates are already string. Defaults to "yyyy-MM-dd".
        drop_orig (bool, optional): Drop original date of birth column. Defaults to True.

    Returns:
        DataFrame: Spark DataFrame with new standardised dob column called dob_std
    """

    dtypes = dict(df.dtypes)

    if dtypes[dob_col] == "date":
        df = df.withColumn("dob_std", date_format(dob_col, "yyyy-MM-dd"))

    if dtypes[dob_col] == "timestamp":
        df = df.withColumn("dob_std", date_format(dob_col, "yyyy-MM-dd"))

    if dtypes[dob_col] == "string":
        df = df.withColumn("dob_std", to_timestamp(dob_col, date_fmt_if_string))
        df = df.withColumn("dob_std", date_format("dob_std", "yyyy-MM-dd"))

    if drop_orig:
        if dob_col != "dob_std":
            df = df.drop(dob_col)

    return df


def null_suspicious_dob_std(df: DataFrame, dob_col: str = "dob_std"):
    """Null out suspicious dates of birth

    Args:
        df (DataFrame): Input Spark DataFrame.  Expects that dob column has already been standardised
        dob_col (str, optional): Name of standardised dob col. Defaults to "dob_std".

    Returns:
        DataFrame: Original dataframe with suspicious dates of birth nulled out 
    """    

    case_stmt = f"""
        case 
        when {dob_col} = "1900-01-01" then null 
        when {dob_col} = "1970-01-01" then null 
        else {dob_col} end

    """
    df = df.withColumn(dob_col, expr(case_stmt))

    return df

