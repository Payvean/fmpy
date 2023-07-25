from .utils import *

import requests
import pandas as pd

from pandas import Series, DataFrame
from types import SimpleNamespace
from typing import Union, List, Any

__author__ = 'Lukas Schröder'
__date__ = '2023-05-14'
__version__ = '0.1.0'
__rights__ = 'Copyright (c) 2023 Lukas Schröder. Copyright (c) 2023 AHL.'

__doc__ = """
This module is related to the company information data section of the financial modeling prep API endpoint and 
provides section specific python functions that can be used to retrieve the data easily and well processed.
"""

__all__ = ['get_company_profile',
           'get_key_executives',
           'get_stock_peers',
           'get_market_capitalization',
           'get_symbol_change',
           'get_company_outlook',
           'get_delisted_companies',
           'get_company_core_information',
           'get_NYSE_holidays_and_trading_hours']


@check_arguments
def get_company_profile(symbol: str, as_pandas: bool = True) -> Union[Series, SimpleNamespace]:
    url = f"{base_url_v3}profile/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = convert_dict_keys_to_snake_case(json_data[0]) if len(json_data) > 0 else {'data': 'no_data'}
    if as_pandas:
        return Series(data)
    return SimpleNamespace(**data)


@check_arguments
def get_key_executives(symbol: str, as_pandas: bool = True) -> Union[Series, SimpleNamespace]:
    url = f"{base_url_v3}key-executives/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = convert_dict_keys_to_snake_case(json_data[0]) if len(json_data) > 0 else {'data': 'no_data'}
    if as_pandas:
        return Series(data)
    return SimpleNamespace(**data)


@check_arguments
def get_market_capitalization(symbol: str, historical: bool = False,
                              as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any, float]:
    local_base = 'market-capitalization' if not historical else 'historical-market-capitalization'
    url = f"{base_url_v3}{local_base}/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = json_data[0] if len(json_data) > 0 else {'marketCap': 'no_data'}
    if historical and as_pandas:
        return process_dataframe(json_data, *args, **kwargs)
    elif historical:
        return json_data
    market_cap: float = data['marketCap']
    return market_cap


# TODO: A lot to figure out with this function
@check_arguments
def get_company_outlook(symbol: str):
    url = f"{base_url_v4}company-outlook?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return SimpleNamespace(**json_data)


@check_arguments
def get_stock_peers(symbol: str) -> List[str]:
    url = f"{base_url_v4}stock_peers?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = convert_dict_keys_to_snake_case(json_data[0]) if len(json_data) > 0 else {'peer_list': 'no_data'}
    return data['peers_list']


# TODO: Functioning
@check_arguments
def get_NYSE_holidays_and_trading_hours(as_pandas=True):
    url = f"{base_url_v3}is-the-market-open?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        return df
    return json_data


@check_arguments
def get_delisted_companies(page: Union[int, str] = 0,
                           as_pandas: bool = True,
                           *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v3}delisted-companies?page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


@check_arguments
def get_symbol_change(as_pandas: bool = True,
                      *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v4}symbol_change?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


@check_arguments
def get_company_core_information(symbol: str, as_pandas: bool = True) -> Union[Series, Any]:
    url = f"{base_url_v4}company-core-information?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = convert_dict_keys_to_snake_case(json_data[0]) if len(json_data) > 0 else {'data': 'no_data'}
    if as_pandas:
        return Series(data)
    return SimpleNamespace(**data)
