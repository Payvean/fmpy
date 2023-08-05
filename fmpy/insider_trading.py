from .utils import *
import requests
from typing import Union

url_api = f"apikey={api_key}"

__author__ = 'Lukas Schröder'
__date__ = '2023-05-20'
__version__ = '0.1.0'

__doc__ = """
This module is related to the insider trading section of the financial modeling prep API endpoint and 
provides section specific python functions.
"""

__all__ = [
    'get_insider_trading',
    'get_fail_to_deliver',
    'get_transaction_types_list',
    'get_cik_mapper',
    'get_insider_roaster',
    'get_insider_roaster_statistics',
    'get_insider_trading_rss_feed',
]


def get_transaction_types_list() -> list:
    url = f"{base_url_v4}insider-trading-transaction-type?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return json_data


def get_insider_trading(symbol: str = None, transaction_type: str = None,
                        reporting_cik: str = None, company_cik: str = None,
                        page: Union[int, str] = 0,
                        as_pandas: bool = True, *args, **kwargs) -> Union:
    local_base = f"{base_url_v4}insider-trading?apikey={api_key}&page={page}"
    if transaction_type is not None:
        url = local_base + f"&transactionType={transaction_type}"
    elif symbol is not None:
        url = local_base + f"&symbol={symbol}"
    elif reporting_cik is not None:
        url = local_base + f"&reportingCik={reporting_cik}"
    elif company_cik is not None:
        url = local_base + f"&companyCik={company_cik}"
    else:
        raise AttributeError("You are required to either pass a symbol,"
                             " transaction type, reporting cik or company cik")
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


def get_cik_mapper(symbol: str = None, name: str = None,
                   page: Union[int, str] = 2, as_pandas: bool = True,
                   *args, **kwargs):
    if symbol is not None:
        url = f"{base_url_v4}mapper-cik-company/{symbol}?apikey={api_key}&page={page}"
    else:
        url = f"{base_url_v4}mapper-cik-name?page={page}&apikey={api_key}"
        if name is not None:
            url += f"&name={name}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if symbol is not None:
        data = json_data[0]
        return data['companyCik']
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


def get_insider_roaster(symbol: str, as_pandas: bool = True,
                        *args, **kwargs):
    url = f"{base_url_v4}insider-roaster?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


def get_insider_roaster_statistics(symbol: str, as_pandas: bool = True,
                                   *args, **kwargs):
    url = f"{base_url_v4}insider-roaster-statistic?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    index = kwargs.pop('index_', 'year')
    return process_dataframe(json_data, index_=index, *args, **kwargs) if as_pandas else json_data


def get_insider_trading_rss_feed(page: Union[int, str] = 0, as_pandas: bool = True,
                                 *args, **kwargs):
    url = f"{base_url_v4}insider-trading-rss-feed?page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    index = kwargs.pop('index_', 'symbol')
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


def get_fail_to_deliver(symbol: str, page: Union[int, str] = 0,
                        as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v4}fail_to_deliver?symbol={symbol}&page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data
