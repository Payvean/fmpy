from .utils import *
import requests

__author__ = 'Lukas Schröder'
__date__ = '2023-08-05'
__version__ = '0.1.0'

__doc__ = """
This module is related to the market indexes section of the financial modeling prep API endpoint and 
provides section specific python functions.
"""

__all__ = [
    'get_all_major_indexes',
    'get_list_of_sp500_companies',
    'get_historical_sp500_constituents_list',
    'get_real_time_stock_market_index',
    'get_available_historical_stock_index_prices',
    'get_historical_stock_index_prices',
    'get_list_of_dow_jones_companies',
    'get_list_of_nasdaq100_companies',
    'get_historical_dow_jones_constituents_list',
]


def get_all_major_indexes(as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v3}quotes/index?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_real_time_stock_market_index(market_index: str = '%5EGSPC',
                                     as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v3}quote/{market_index}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


def get_list_of_sp500_companies(as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v3}sp500_constituent?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_historical_sp500_constituents_list(as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v3}historical/sp500_constituent?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_list_of_nasdaq100_companies(as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v3}nasdaq_constituent?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_list_of_dow_jones_companies(as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v3}dowjones_constituent?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_historical_dow_jones_constituents_list(as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v3}historical/dowjones_constituent?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_available_historical_stock_index_prices(as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v3}symbol/available-indexes?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_historical_stock_index_prices(market_index: str, interval: str = None,
                                      as_pandas: bool = True, *args, **kwargs):
    if interval is not None and interval != '1day' and interval != 'daily':
        local_base = f"{base_url_v3}historical-chart/{interval}"
    else:
        local_base = f"{base_url_v3}historical-price-full"
    url = f"{local_base}/{market_index}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)

    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data
