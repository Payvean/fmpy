from .utils import *
import requests
import pandas as pd
from types import SimpleNamespace
from typing import Iterable, Union

__author__ = 'Lukas Schröder'
__date__ = '2023-08-05'
__version__ = '0.1.0'

__doc__ = """This module is related to the euronext data section of the financial modeling 
prep API endpoint and provides section specific python functions."""

__all__ = [
    'get_available_euronext_symbols',
    'get_historical_euronext_prices',
    'get_all_real_time_euronext_prices',
    'get_real_time_edf_price',
]


def get_available_euronext_symbols(as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v3}symbol/available-euronext?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_all_real_time_euronext_prices(as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v3}quotes/euronext?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_real_time_edf_price(symbol: Union[str, Iterable] = 'EDF.PA',
                            as_pandas: bool = True, *args, **kwargs):
    if not isinstance(symbol, str):
        symbol = ','.join(list(symbol))
    url = f"{base_url_v3}quote/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if count_string_chars(symbol, ',') > 0:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    data = convert_dict_keys_to_snake_case(json_data[0])
    if as_pandas:
        return pd.Series(data)
    return SimpleNamespace(**data)


def get_historical_euronext_prices(symbol: str, interval: str = None,
                                   as_pandas: bool = True, *args, **kwargs):
    if interval is not None and interval != '1day' and interval != 'daily':
        local_base = f"{base_url_v3}historical-chart/{interval}"
    else:
        local_base = f"{base_url_v3}historical-price-full"
    url = f"{local_base}/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        return process_dataframe(json_data, *args, **kwargs) if interval is not None else process_dataframe(
            json_data['historical'], *args, **kwargs)
    return json_data
