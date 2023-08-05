from .utils import *
import requests
import datetime as dt
from typing import Union

__author__ = 'Lukas Schröder'
__date__ = '2023-08-05'
__version__ = '0.1.0'

__doc__ = """
This module is related to the market performance section of the financial modeling prep API endpoint and 
provides section specific python functions.
"""

__all__ = [
    'get_sectors_pe_ratio',
    'get_industries_pe_ratio',
    'get_stock_market_sector_performance',
    'get_most_active_stock_companies',
    'get_most_gainer_stock_companies',
    'get_most_losers_stock_companies',
]


def get_sectors_pe_ratio(date: Union[dt.date, str] = None, exchange: str = 'NYSE',
                         as_pandas: bool = True, *args, **kwargs):
    if date is None:
        date = str(dt.date.today())
    url = f"{base_url_v4}sector_price_earning_ratio?date={date}&exchange={exchange}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


def get_industries_pe_ratio(date: Union[dt.date, str] = None, exchange: str = 'NYSE',
                            as_pandas: bool = True, *args, **kwargs):
    if date is None:
        date = str(dt.date.today())
    url = f"{base_url_v4}industry_price_earning_ratio?date={date}&exchange={exchange}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


def get_stock_market_sector_performance(historical: bool = False, as_pandas: bool = True,
                                        limit: Union[int, str] = 50, *args, **kwargs):
    url = f"{base_url_v3}sector-performance?apikey={api_key}"
    if historical:
        url = f"{base_url_v3}historical-sectors-performance?apikey={api_key}"
    url += f"&limit={limit}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        if not historical:
            index_ = kwargs.pop('index_', 'sector')
            return process_dataframe(json_data, index_=index_, *args, **kwargs)
        return process_dataframe(json_data, *args, **kwargs)
    return json_data


def get_most_gainer_stock_companies(as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v3}stock_market/gainers?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data

def get_most_losers_stock_companies(as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v3}stock_market/losers?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_most_active_stock_companies(as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v3}stock_market/actives?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data
