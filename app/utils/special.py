"""
读取 `special.csv` 文件，获取一个字典
{"table_name": "column_name"}
"""

import csv


def get_special_dict(file_path: str) -> dict:
    special_map = {}
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            table_name = row.get("table_name")
            column_name = row.get("column_name")
            print(f"table_name: {table_name}, column_name: {column_name}")
            if table_name and column_name:
                special_map[table_name.strip()] = column_name.strip()
    return special_map


if __name__ == '__main__':
    special_dict = get_special_dict("special.csv")
    print(special_dict)
