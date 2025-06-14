import pandas as pd
import requests


class BaiduPlaceSearcher:
    """
    封装百度地图 Place API 查询功能。

    文档：
        https://lbsyun.baidu.com/faq/api?title=webapi/guide/webservice-placeapi/district
    """

    def __init__(self, ak: str, tag: str = ""):
        """
        初始化搜索器。

        参数：
            ak : str，百度地图开放平台 API Key
            tag : str，搜索的分类标签，例如 '高等院校'、'银行'，可选
            sleep_sec : float，每次请求的间隔时间，默认0.5秒
        """
        self.ak = ak
        self.tag = tag
        self.url = "https://api.map.baidu.com/place/v2/search"

    def query_address(self, query: str, region: str) -> str:
        """
        查询单个关键词在指定区域下的地址。

        返回：
            地址字符串，如果查询失败返回空字符串
        """
        params = {
            "query": query,
            "tag": self.tag,
            "region": region,
            "output": "json",
            "ak": self.ak
        }

        try:
            response = requests.get(url=self.url, params=params, timeout=10)
            if response.ok:
                data = response.json()
                if data.get("results"):
                    return data["results"][0].get("address", "")
                else:
                    print(f"[提示] 无查询结果: query={query}, region={region}")
            else:
                print(f"[警告] 请求失败: HTTP {response.status_code}")
        except requests.RequestException as e:
            print(f"[异常] 请求异常: {e}")

        return ""

    def apply_to_dataframe(self, df: pd.DataFrame,
                           key_word_col: str,
                           region_col: str,
                           address_col: str) -> pd.DataFrame:
        """
        批量查询并更新 DataFrame 中的地址列。

        参数：
            df : pd.DataFrame，包含关键词列和区域列
            key_word_col : str，要查询的关键词列名
            region_col : str，区域列名
            address_col : str，要替换的地址列名（会被新值覆盖）

        返回：
            更新后的 DataFrame
        """
        new_addresses = []

        for idx, row in df.iterrows():
            query = row[key_word_col]
            region = row[region_col]
            new_address = self.query_address(query, region)
            new_addresses.append(new_address)

        df[address_col] = new_addresses
        return df


"""

# 示例数据
df = pd.DataFrame({
    "name": ["清华大学", "北京大学"],
    "city": ["北京", "北京"],
    "address": ["原地址1", "原地址2"]
})

# 初始化搜索器
searcher = BaiduPlaceSearcher(ak="你的AK", tag="高等院校")

# 执行替换
df_new = searcher.apply_to_dataframe(df, key_word_col="name", region_col="city", address_col="address")

print(df_new)

"""