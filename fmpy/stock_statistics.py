from .utils import *

import requests
from pandas import Series, DataFrame
from types import SimpleNamespace
from typing import Union, Optional, Any

__author__ = 'Lukas Schröder'
__date__ = '2023-05-22'
__version__ = '0.1.0'

__doc__ = """
This module is related to the stock statistics section of the financial modeling prep API endpoint and 
provides section specific python functions.
"""

__all__ = ['get_social_sentiment',
           'get_stock_grade',
           'get_earning_surprises',
           'get_analyst_estimates',
           'get_merger_and_acquisition', ]


def get_social_sentiment(symbol: Optional[str] = None, page: Union[int, str] = 0,
                         type_: Optional[str] = None, source: Optional[str] = None,
                         historical: bool = False, as_pandas: bool = True,
                         *args, **kwargs) -> Union[DataFrame, Any]:
    """
    type: bullish | bearish
    source: twitter | stocktwits

    """
    if historical:
        if symbol is None:
            raise AttributeError("If historical is True you are required to pass a symbol")
        url = f"{base_url_v4}historical/social-sentiment?symbol={symbol}&apikey={api_key}&page={page}"
    else:
        url = f"{base_url_v4}social-sentiment/trending?apikey={api_key}"
        if type_ is not None:
            url += f"&type={type_}"
        if source is not None:
            url += f"&source={source}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


def get_stock_grade(symbol: str, limit: Union[int, str] = 500,
                    as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v3}grade/{symbol}?limit={limit}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


def get_earning_surprises(symbol: str, as_pandas: bool = True,
                          *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v3}earnings-surprises/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data



def get_analyst_estimates(symbol: str, period: str = 'quarter',
                          limit: Union[int, str] = 30,
                          as_pandas: bool = True,
                          *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v3}analyst-estimates/{symbol}?limit={limit}&period={period}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


def get_merger_and_acquisition(search: bool = False, name: Optional[str] = None,
                               page: Union[int, str] = 0, as_pandas: bool = True,
                               *args, **kwargs) -> Union[Series, DataFrame, SimpleNamespace, Any]:
    if not search:
        url = f"{base_url_v4}mergers-acquisitions-rss-feed?page={page}&apikey={api_key}"
    elif name is None:
        raise AttributeError("If search is True you are required to pass a name")
    else:
        url = f"{base_url_v4}mergers-acquisitions/search?name={name}&apikey={api_key}&page={page}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas and search:
        data = convert_dict_keys_to_snake_case(json_data[0]) if len(json_data) > 0 else {'data': 'no_data'}
        return Series(data)
    if as_pandas:
        return process_dataframe(json_data, *args, **kwargs)
    if search:
        data = convert_dict_keys_to_snake_case(json_data[0]) if len(json_data) > 0 else {'data': 'no_data'}
        return SimpleNamespace(**data)
    return json_data
