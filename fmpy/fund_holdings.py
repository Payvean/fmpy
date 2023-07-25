# Helper functions and API Key for the user
from .utils import *

import requests
import pandas as pd

from pandas import DataFrame, Series
from io import StringIO
from types import SimpleNamespace
from typing import List, Union, Any, IO, Optional
from os import PathLike
from datetime import datetime, date

__author__ = 'Lukas Schröder'
__date__ = '2023-05-22'
__version__ = '0.1.0'
__rights__ = 'Copyright (c) 2023 Lukas Schröder'

__doc__ = """
This module is related to the stock calendars section of the financial modeling prep API endpoint and 
provides section specific python functions that can be used to retrieve the data easily and well processed.
"""


@check_arguments
def get_etf_expense_ratio(symbol: str, as_pandas: bool = True) -> Union[Series, SimpleNamespace]:
    url = f"{base_url_v4}etf-info?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = convert_dict_keys_to_snake_case(json_data[0]) if len(json_data) > 0 else json_data
    if as_pandas:
        return Series(data)
    return SimpleNamespace(**data)


@check_arguments
def get_institutional_holders(symbol: str, as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v3}institutional-holder/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'holder')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


@check_arguments
def get_mutual_fund_holders(symbol: str, as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v3}mutual-fund-holder/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'holder')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


@check_arguments
def get_etf_sector_weightings(symbol: str, as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v3}etf-sector-weightings/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'sector')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


@check_arguments
def get_etf_country_weightings(symbol: str, as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v3}etf-country-weightings/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'country')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


@check_arguments
def get_etf_stock_exposure(symbol: str, as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v3}etf-stock-exposure/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'etf_symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


@check_arguments
def get_13F_list(as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v3}cik_list?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'cik')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


@check_arguments
def get_cik_by_name(name: str, as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v3}cik-search/{name}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'cik')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


@check_arguments
def get_company_name_by_cik(cik: str):
    url = f"{base_url_v3}cik/{cik}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = json_data[0]
    if len(data) == 0:
        return None
    return data['name']


@check_arguments
def get_form_13F(cik: str, date: str = str(date.today()),
                 as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v3}form-thirteen/{cik}?date={date}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


@check_arguments
def get_filing_dates_by_cik(cik: str) -> Any:
    url = f"{base_url_v3}form-thirteen-date/{cik}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return json_data


@check_arguments
def get_cusip_mapper(cik: str) -> Any:
    url = f"{base_url_v3}cusip/{cik}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return json_data


def form_13F_asset_allocation_diversification():
    pass
