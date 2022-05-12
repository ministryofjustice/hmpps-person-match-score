from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import expr, regexp_replace, col

def fix_zero_length_strings(df:DataFrame):
    """Convert any zero length strings or strings that contain only whitespace to a true null

    Args:
        df (DataFrame): Input Spark dataframe

    Returns:
        DataFrame: Spark Dataframe with clean strings
    """    

    string_cols = [item[0] for item in df.dtypes if item[1].startswith('string')]

    stmt = """
    case 
    when trim({c}) = '' then null
    else trim({c})
    end
    """

    for c in string_cols:
        df = df.withColumn(c, expr(stmt.format(c=c)))

    return df

