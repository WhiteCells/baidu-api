from sqlalchemy.orm import sessionmaker
from app.automap import reflect_table, get_result_engine, get_all_table_names
from app.baidu_test import baidu_api
from app.utils.result_table import create_result_table_if_not_exists
from app.utils.logger import get_logger, get_progress, save_progress
from app.utils.config import Config


def process_table(table_name: str, column_name: str, batch_size: int = Config.BATCH_SIZE):
    logger = get_logger(table_name)
    logger.info(f"Processing table: {table_name}")

    # 反射原始表结构
    table, engine = reflect_table(table_name)
    Session = sessionmaker(bind=engine)

    # 创建/连接结果表
    result_engine = get_result_engine()
    result_Session = sessionmaker(bind=result_engine)
    result_table = create_result_table_if_not_exists(result_engine, table_name)

    # 检查原始表中指定的列是否存在
    if column_name not in table.c:
        logger.error(f"Table {table_name} does not have column {column_name}")
        return

    # 初始化偏移量
    offset = get_progress(table_name)
    logger.info(f"[{table_name}] Starting offset: {offset}")

    while True:
        session = Session()
        result_session = result_Session()

        try:
            rows = (
                session.query(table)
                .order_by(table.c.timestamp_process)
                .offset(offset)
                .limit(batch_size)
                .all()
            )
            logger.info(f"> [{table_name}] offset: {offset}")
            if not rows:
                logger.info(f"[{table_name}] No more rows to process.")
                break

            for row in rows:
                print(f">>> Table {table_name}:{offset}")
                address = getattr(row, column_name)

                if not address:
                    logger.warning(f"[{table_name}] Skipping row at offset {offset}: empty address")
                    offset += 1
                    continue

                try:
                    # 调用 API 并保存结果
                    resp = baidu_api(address)
                    logger.info(f"[{table_name}] {address} -> {resp}")
                    stmt = result_table.insert().values(
                        origin_address=address,
                        # result=json.dumps(resp),
                        result=resp["address"],
                    )
                    result_session.execute(stmt)
                    offset += 1
                except Exception as e:
                    logger.error(f"[{table_name}] Error at offset {offset}: {e}")
                finally:
                    # offset += 1
                    save_progress(table_name, offset)

            result_session.commit()

        except Exception as e:
            logger.error(f"[{table_name}] Fatal error in batch starting at offset {offset}: {e}")
            session.rollback()
            result_session.rollback()

        finally:
            session.close()
            result_session.close()


if __name__ == "__main__":
    # table, engine = reflect_table("test")
    # create_result_table_if_not_exists(engine, "test111")
    # process_table("address", "address")

    allname = get_all_table_names()
    for t in allname:
        if t == "dwd_amap_hb_procuratorate_2025":
            process_table(t, "completed_address")
        # if t == "dwd_amap_hb_finance_insurance_2025":
        #     process_table(t, "completed_address")
        # if t == "dwd_amap_hb_govsocorginfo_2025":
        #     process_table(t, "completed_address")
