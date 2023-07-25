from .utils import *

import requests
import pandas as pd


def get_symbols_list(as_pandas: bool = True):
    url = f"{base_url_v3}/stock/list?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.set_index('symbol', inplace=True)
        return df
    return json_data


def get_tradable_symbols_list(as_pandas: bool = True):
    url = f"{base_url_v3}/available-traded/list?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.set_index('symbol', inplace=True)
        return df
    return json_data


def get_etf_list(as_pandas: bool = True):
    url = f"{base_url_v3}/etf/list?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.set_index('symbol', inplace=True)
        return df
    return json_data
