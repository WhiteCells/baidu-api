from sqlalchemy import Table, MetaData, inspect
from app.utils.create_table import create_table
from app.utils.config import Config


def create_result_table_if_not_exists(engine, origin_table_name: str) -> Table:
    table_name = f"{Config.RESULT_TABLE_PREFIX}_{origin_table_name}"
    metadata = MetaData()

    inspector = inspect(engine)
    if table_name in inspector.get_table_names():
        return Table(table_name, metadata, autoload_with=engine)

    return create_table(engine, table_name, metadata)
