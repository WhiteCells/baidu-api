### Baidu API

#### 安装环境

```sh
conda create -n baidu-api-env_38 python=3.8
conda activate baidu-api-env_38
pip install -r requirements.txt
```

复制 `.env.example` 文件，并修改 `.env` 文件。

```sh
cp .env.example .env
```

#### 启动

```sh
python run.py
```

服务通过 `systemd` 管理。


#### !!! Note !!!

后续的表必须包含 `timestamp_process` 字段（被用于排序，因为表中没有主键，导致 limit 获取数据时无法保证数据顺序）


> 反射数据库结构，获取指定数据库的所有表名。
> 
> 表名入队，然后按照队列的方式多进程访问每个表。
> 
> 访问指定的表字段，分页获取数据。
> 
> 每个进程访问每个表都有独立的日志，记录当前进程访问的表以及访问位置，便于恢复重启。
> 
> 将访问到的数据，传入 BaiDu API 接口，然后将接口的结果数据传入新的数据库以及新的表，新表以原始的表名为基础（添加前缀）。
