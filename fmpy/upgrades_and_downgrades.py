from .utils import *

import requests
import pandas as pd
from types import SimpleNamespace
from typing import Union

__author__ = 'Lukas Schröder'
__date__ = '2023-05-22'
__version__ = '0.1.0'

__doc__ = """
This module is related to the upgrades and downgrades section of the financial modeling prep API endpoint and 
provides section specific python functions.
"""
__all__ = [
    'get_upgrades_and_downgrades',
    'get_upgrades_and_downgrades_by_company',
    'get_upgrades_and_downgrades_rss_feed',
    'get_upgrades_and_downgrades_consensus'
]

@in_development
def get_upgrades_and_downgrades(symbol: str, as_pandas=True, *args, **kwargs):
    url = f"{base_url_v4}upgrades-downgrades?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


def get_upgrades_and_downgrades_rss_feed(page: Union[str, int] = 0, as_pandas=True, *args, **kwargs):
    url = f"{base_url_v4}upgrades-downgrades-rss-feed?page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


def get_upgrades_and_downgrades_consensus(symbol: str, as_pandas=True):
    url = f"{base_url_v4}upgrades-downgrades-consensus?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = convert_dict_keys_to_snake_case(json_data[0])
    if as_pandas:
        return pd.Series(data)
    return SimpleNamespace(**data)


def get_upgrades_and_downgrades_by_company(company: str, as_pandas=True, *args, **kwargs):
    url = f"{base_url_v4}upgrades-downgrades-grading-company?company={company}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data
