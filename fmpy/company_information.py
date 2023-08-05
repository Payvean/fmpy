from .utils import *
import requests
from pandas import Series, DataFrame
from types import SimpleNamespace
from typing import Union, List, Any
from warnings import warn

__author__ = 'Lukas Schröder'
__date__ = '2023-05-14'
__version__ = '0.1.0'

__doc__ = """
This module is related to the company information data section of the financial modeling prep API endpoint and 
provides section specific python functions.
"""

__all__ = ['get_company_profile',
           'get_key_executives',
           'get_stock_peers',
           'get_market_capitalization',
           'get_symbol_change',
           'get_company_outlook',
           'get_delisted_companies',
           'get_company_core_information',
           'get_nyse_holidays_and_trading_hours']


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
    market_cap: float = float(data['marketCap'])
    return market_cap


def get_company_outlook(symbol: str):
    warn("This function is still in development and may not work as expected.")
    url = f"{base_url_v4}company-outlook?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return SimpleNamespace(**json_data)


def get_stock_peers(symbol: str) -> List[str]:
    url = f"{base_url_v4}stock_peers?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = convert_dict_keys_to_snake_case(json_data[0]) if len(json_data) > 0 else {'peer_list': 'no_data'}
    return data['peers_list']


def get_nyse_holidays_and_trading_hours(as_pandas=True, *args, **kwargs):
    url = f"{base_url_v3}is-the-market-open?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


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


def get_symbol_change(as_pandas: bool = True,
                      *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v4}symbol_change?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


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
