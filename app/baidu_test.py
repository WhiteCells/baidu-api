import requests
from app.utils.config import Config

def baidu_api(address):
    try:
        resp = requests.post(Config.BAIDU_API, json={"address": address})
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}
