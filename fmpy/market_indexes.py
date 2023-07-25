from .utils import *

import requests
import pandas as pd
from types import SimpleNamespace


def get_all_major_indexes(as_pandas: bool = True):
    url = f"{base_url_v3}quotes/index?apikey={api_key}"
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


def get_real_time_stock_market_index(market_index: str = '%5EGSPC', as_pandas: bool = True):
    url = f"{base_url_v3}quote/{market_index}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = convert_dict_keys_to_snake_case(json_data[0])
    if as_pandas:
        return pd.Series(data)
    return SimpleNamespace(**data)


def get_list_of_sp500_companies(as_pandas: bool = True):
    url = f"{base_url_v3}sp500_constituent?apikey={api_key}"
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


def get_historical_sp500_constituents_list(as_pandas: bool = True, index_: str = 'symbol'):
    url = f"{base_url_v3}historical/sp500_constituent?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.set_index(index_, inplace=True)
        return df
    return json_data


def get_list_of_nasdaq100_companies(as_pandas: bool = True):
    url = f"{base_url_v3}nasdaq_constituent?apikey={api_key}"
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


def get_list_of_dow_jones_companies(as_pandas: bool = True):
    url = f"{base_url_v3}dowjones_constituent?apikey={api_key}"
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


def get_historical_dow_jones_constituents_list(as_pandas: bool = True, index_: str = 'symbol'):
    url = f"{base_url_v3}historical/dowjones_constituent?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.set_index(index_, inplace=True)
        return df
    return json_data


def get_available_historical_stock_index_prices(as_pandas: bool = True):
    url = f"{base_url_v3}symbol/available-indexes?apikey={api_key}"
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


def get_historical_stock_index_prices(market_index: str, interval: str = None,
                                      as_pandas: bool = True):
    if interval is not None and interval != '1day' and interval != 'daily':
        local_base = f"{base_url_v3}historical-chart/{interval}"
    else:
        local_base = f"{base_url_v3}historical-price-full"
    url = f"{local_base}/{market_index}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)

    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data) if interval is not None else pd.DataFrame(json_data['historical'])
        df = convert_columns_to_snake_case(df)
        df.set_index('date', inplace=True)
        return df
    return json_data
