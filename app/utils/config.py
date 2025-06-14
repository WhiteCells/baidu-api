import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()


class Config:
    # 日志文件目录
    WORKER_DIR = "worker1"
    
    # 进度文件目录
    PROGRESS_DIR = "progress1"

    # 特殊文件路径
    SPECIAL_FILE_PATH = "special.csv" 

    # limit 行批量处理
    BATCH_SIZE = 100

    # 结构表前缀
    RESULT_TABLE_PREFIX = "baiduapi_"

    # 完整路径列名
    ADDRESS_COLUMN_NAME = "completed_address"

    # Baidu  API
    BAIDU_API = os.getenv("BAIDU_API")
    BAIDU_KEY = os.getenv("BAIDU_KEY")

    # 输入数据库
    MYSQL_HOST: str = os.getenv("MYSQL_HOST")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT")
    MYSQL_USER: str = urllib.parse.quote_plus(os.getenv("MYSQL_USER"))
    MYSQL_PASS: str = urllib.parse.quote_plus(os.getenv("MYSQL_PASS")) # '#'
    MYSQL_DB: str = os.getenv("MYSQL_DB")
    MYSQL_POOL_CONNSIZE: int = 20    # 最大连接数
    MYSQL_POOL_OVERFLOW: int = 30    # 最大溢出连接
    MYSQL_POOL_TIMEOUT: int = 30     # 最大溢出连接
    MYSQL_POOL_RECYCLE: int = 1800   # 连接最大生命周期（秒） 

    # 输出数据库
    RESULT_MYSQL_HOST: str = os.getenv("RESULT_MYSQL_HOST")
    RESULT_MYSQL_PORT: str = os.getenv("RESULT_MYSQL_PORT")
    RESULT_MYSQL_USER: str = urllib.parse.quote_plus(os.getenv("RESULT_MYSQL_USER"))
    RESULT_MYSQL_PASS: str = urllib.parse.quote_plus(os.getenv("RESULT_MYSQL_PASS"))
    RESULT_MYSQL_DB: str = os.getenv("RESULT_MYSQL_DB")
    RESULT_MYSQL_POOL_CONNSIZE: int = 20    # 最大连接数
    RESULT_MYSQL_POOL_OVERFLOW: int = 30    # 最大溢出连接
    RESULT_MYSQL_POOL_TIMEOUT: int = 30     # 最大溢出连接
    RESULT_MYSQL_POOL_RECYCLE: int = 1800   # 连接最大生命周期（秒） 

    @staticmethod
    def DATABASE_URL() -> str:
        return (
            f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASS}"
            f"@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DB}"
        )

    @staticmethod
    def RESULT_DATABASE_URL() -> str:
        print("***", Config.RESULT_MYSQL_USER)
        print("***", Config.RESULT_MYSQL_PASS)
        print("***", Config.RESULT_MYSQL_HOST)
        print("***", Config.RESULT_MYSQL_DB)
        return (
            f"mysql+pymysql://{Config.RESULT_MYSQL_USER}:{Config.RESULT_MYSQL_PASS}"
            f"@{Config.RESULT_MYSQL_HOST}:{Config.RESULT_MYSQL_PORT}/{Config.RESULT_MYSQL_DB}"
        )
