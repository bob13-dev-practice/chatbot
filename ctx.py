import requests
from config import conf
import json

CTX_KEY = conf['ctx']

def ctx(query_item, query_type):
    """ ctx api """
    result = {}
    if query_type == 'ip':
        result = requests.get(
            f'https://api.ctx.io/v1/ip/report/{query_item}',
            headers={"x-api-key": CTX_KEY}
        )
    elif query_type == 'domain':
        result = requests.get(
            f'https://api.ctx.io/v1/domain/report/{query_item}',
            headers={"x-api-key": CTX_KEY}
        )
    elif query_type == 'url':
        # URL에 대한 요청 추가
        pass
    elif query_type == 'hash':
        result = requests.get(
            f'https://api.ctx.io/v1/file/report/{query_item}',
            headers={"x-api-key": CTX_KEY}
        )

    json_result = result.json()
    if 'ctx_data' in json_result:
        return json_result['ctx_data']
    else:
        return json_result