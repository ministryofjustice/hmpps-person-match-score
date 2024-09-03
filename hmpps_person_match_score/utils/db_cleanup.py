def cleanup_splink_tables(linker, connection, input_table_alias):
    """
    Cleans up intermediate tables created by Splink in the DuckDB connection.

    Args:
    linker (DuckDBLinker): The Splink linker object.
    connection (duckdb.DuckDBPyConnection): The DuckDB connection.

    Returns:
    None
    """

    table_prefixes = ("__splink__df_concat_with_tf_", "__splink__df_predict_")

    for k, v in list(linker._intermediate_table_cache.items()):  # noqa: SLF001
        if k.startswith(table_prefixes):
            v.drop_table_from_database_and_remove_from_cache()

    input_table_alias = linker.input_table_aliases[0]
    connection.sql(f"DROP VIEW IF EXISTS {input_table_alias}")
