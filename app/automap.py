from sqlalchemy import create_engine, select, MetaData, Table
from app.utils.config import Config


def get_engine():
    return create_engine(Config.DATABASE_URL(),
        pool_size=Config.MYSQL_POOL_CONNSIZE,
        max_overflow=Config.MYSQL_POOL_OVERFLOW,
        pool_timeout=Config.MYSQL_POOL_TIMEOUT,
        pool_recycle=Config.MYSQL_POOL_RECYCLE,
    )


def get_result_engine():
    return create_engine(Config.RESULT_DATABASE_URL(),
        pool_size=Config.RESULT_MYSQL_POOL_CONNSIZE,
        max_overflow=Config.RESULT_MYSQL_POOL_OVERFLOW,
        pool_timeout=Config.RESULT_MYSQL_POOL_TIMEOUT,
        pool_recycle=Config.RESULT_MYSQL_POOL_RECYCLE,
    )


def get_all_table_names() -> list:
    engine = get_engine()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return list(metadata.tables.keys())


def reflect_table(table_name):
    engine = get_engine()
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine)
    return table, engine


def get_columns_values(table, engine, column):
    with engine.connect() as conn:
        stmt = select(table.c[column])
        result = conn.execute(stmt)
        return [row[0] for row in result]


if __name__ ==  "__main__":
    # all tables
    print(get_all_table_names())

    table_name = "dwd_amap_hb_court_2025"
    table, engine = reflect_table(table_name)
    # all columns
    print(table.columns.keys())

    # get column values
    print(get_columns_values(table, engine, "completed_address"))
    