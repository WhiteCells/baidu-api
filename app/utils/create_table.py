from sqlalchemy import (
    Engine, Table, Column, String, 
    MetaData, Integer, String, Float
)


def create_table(engine: Engine, table_name: str, metadata: MetaData) -> Table:
    table = Table(
        table_name,
        metadata,
        Column("id", Integer, primary_key=True, comment=""),
        Column("origin_table_name", String(255), comment=""),
        Column("origin_address", String(255), comment=""),
        Column("result", String(255), comment=""),
    )
    metadata.create_all(engine)
    return table
