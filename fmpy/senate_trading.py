from .utils import *
import requests
from typing import Union


__author__ = 'Lukas Schröder'
__date__ = '2023-05-20'
__version__ = '0.1.0'

__doc__ = """
This module is related to the senate trading section of the financial modeling prep API endpoint and 
provides section specific python functions.
"""

__all__ = [
    'get_senate_trading',
    'get_senate_disclosure',
    'get_senate_trading_rss_feed',
    'get_senate_disclosure_rss_feed'
]


def get_senate_trading(symbol: str, page: Union[int, str] = 0,
                       as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v4}senate-trading?symbol={symbol}&apikey={api_key}&page={page}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'last_name')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_senate_trading_rss_feed(page: Union[int, str] = 0,
                                as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v4}senate-trading-rss-feed?page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'last_name')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_senate_disclosure(symbol: str, page: Union[int, str] = 0,
                          as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v4}senate-disclosure?symbol={symbol}&page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


def get_senate_disclosure_rss_feed(page: Union[int, str] = 0,
                                   as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v4}senate-disclosure-rss-feed?page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data
