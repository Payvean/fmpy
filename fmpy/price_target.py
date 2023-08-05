from .utils import *

import requests
from pandas import DataFrame, Series
from types import SimpleNamespace
from typing import List, Union

__author__ = 'Lukas Schröder'
__date__ = '2023-08-05'
__version__ = '0.1.0'

__doc__ = """
This module is related to the price target section of the financial modeling prep API endpoint and 
provides section specific python functions.
"""
__all__ = [
    'get_price_target',
    'get_price_target_summary',
    'get_price_target_by_analyst_company',
    'get_price_target_by_analyst_name',
    'get_price_target_consensus',
    'get_price_target_rss_feed',
]


def get_price_target(symbol: str, as_pandas: bool = True,
                    *args, **kwargs) -> Union[DataFrame, List[dict]]:
    url = f"{base_url_v4}price-target?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


def get_price_target_summary(symbol: str, as_pandas: bool = True) -> Union[Series, SimpleNamespace]:
    url = f"{base_url_v4}price-target-summary?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        return Series(json_data[0])
    data = json_data[0]
    return SimpleNamespace(**data)


def get_price_target_by_analyst_name(name: str, as_pandas: bool = True) -> Union[Series, SimpleNamespace]:
    url = f"{base_url_v4}price-target-analyst-name?name={name}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = json_data[0]
    data = convert_dict_keys_to_snake_case(data)
    if as_pandas:
        return Series(data)
    return SimpleNamespace(**data)


def get_price_target_by_analyst_company(company: str, as_pandas: bool = True) -> Union[Series, SimpleNamespace]:
    url = f"{base_url_v4}price-target-analyst-company?company={company}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = json_data[0]
    data = convert_dict_keys_to_snake_case(data)
    if as_pandas:
        return Series(data)
    return SimpleNamespace(**data)


def get_price_target_consensus(symbol: str, as_pandas: bool = True) -> Union[Series, SimpleNamespace]:
    url = f"{base_url_v4}price-target-consensus?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = json_data[0]
    data = convert_dict_keys_to_snake_case(data)
    if as_pandas:
        return Series(data)
    return SimpleNamespace(**data)


def get_price_target_rss_feed(page: Union[str, int] = 0, as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v4}price-target-rss-feed?page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data
