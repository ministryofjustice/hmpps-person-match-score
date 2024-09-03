import uuid
from typing import List


def generate_view_uuid():
    return f"v_{uuid.uuid4().hex.replace('-', '')[:16]}"


def cleanup_splink_tables(linker, connection, input_table_alias: List[str]):
    """
    Cleans up intermediate tables created by Splink in the DuckDB connection
    """

    table_prefixes = ("__splink__df_concat_with_tf_", "__splink__df_predict_")

    for k, v in list(linker._intermediate_table_cache.items()):  # noqa: SLF001
        if k.startswith(table_prefixes):
            v.drop_table_from_database_and_remove_from_cache()

    for alias in input_table_alias:
        connection.sql(f"DROP VIEW IF EXISTS {alias}")
