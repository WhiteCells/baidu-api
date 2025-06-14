from multiprocessing import Process, Queue, cpu_count
from app.automap import get_all_table_names
from app.task import process_table
from app.utils.special import get_special_dict
from app.utils.config import Config


def get_tables_queue() -> Queue:
    """
    读取所有表名，并返回一个队列（线程安全）
    """
    tables = get_all_table_names()
    que = Queue()
    for table in tables:
        que.put(table)
    return que


def worker(table_queue: Queue):
    """
    线程工作函数
    table_queue: 队列
    """
    special_dict = get_special_dict(Config.SPECIAL_FILE_PATH)
    while not table_queue.empty():
        try:
            table_name = table_queue.get_nowait()
            if table_name := special_dict.get(table_name):
                process_table(table_name, special_dict[table_name])
            else:
                process_table(table_name, Config.ADDRESS_COLUMN_NAME)
            # process_table(table_name, "completed_address")
        except Exception as e:
            print(f"[ERROR] Worker failed on table: {e}")


def run_multi_process():
    tables_queue = get_tables_queue()

    num_processes = cpu_count()
    processes = [Process(target=worker, args=(tables_queue,)) for _ in range(num_processes)]

    for p in processes:
        p.start()
    for p in processes:
        p.join()


if __name__ == "__main__":
    run_multi_process()
