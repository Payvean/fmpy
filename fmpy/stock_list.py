from .utils import *
import requests
import pandas as pd

__author__ = 'Lukas Schröder'
__date__ = '2023-05-20'
__version__ = '0.1.0'

__doc__ = """
This module is related to the stock list section of the financial modeling prep API endpoint and 
provides section specific python functions.
"""

__all__ = [
    'get_symbols_list',
    'get_etf_list',
    'get_tradable_symbols_list',
]

def get_symbols_list(as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v3}/stock/list?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data

def get_tradable_symbols_list(as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v3}/available-traded/list?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_etf_list(as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v3}/etf/list?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data
