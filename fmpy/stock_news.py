from .utils import *

import requests
import pandas as pd
from typing import Union, Iterable, Any

__author__ = 'Lukas Schröder'
__date__ = '2023-05-14'
__version__ = '0.1.0'

__doc__ = """
This module is related to the stock news section of the financial modeling prep API endpoint and 
provides section specific python functions.
"""

__all__ = [
    'get_fmp_articles',
    'get_stock_news',
    'get_crypto_news',
    'get_forex_news',
    'get_general_news',
    'get_press_releases',
    'get_stock_news_with_sentiment',
]


def get_fmp_articles(page: Union[int, str] = 0, size: Union[int, str] = 5, as_pandas: bool = True,
                     *args, **kwargs):
    url = f"{base_url_v3}fmp/articles?page={page}&size={size}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = json_data['content']
    return process_dataframe(data, *args, **kwargs) if as_pandas else json_data



def get_stock_news(tickers: Union[str, Iterable],
                   page: Union[int, str] = 0, limit: Union[int, str] = 50,
                   as_pandas: bool = True, *args, **kwargs) -> Union[pd.DataFrame, Any]:
    if not isinstance(tickers, str):
        tickers = ','.join(list(tickers))
    url = f"{base_url_v3}stock_news?tickers={tickers}&page={page}&limit={limit}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        return process_dataframe(json_data, *args, **kwargs)
    return json_data



def get_stock_news_with_sentiment(page: Union[int, str] = 0,
                                  limit: Union[int, str] = 50,
                                  as_pandas: bool = True,
                                  *args, **kwargs) -> Union[pd.DataFrame, list]:
    url = f"{base_url_v4}stock-news-sentiments-rss-feed?page={page}&limit={limit}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    index = kwargs.pop('index_', 'symbol')
    return process_dataframe(json_data, *args, **kwargs)



def get_crypto_news(symbol: str = None, page: Union[int, str] = 0, as_pandas: bool = True,
                    *args, **kwargs):
    url = f"{base_url_v4}crypto_news?page={page}&apikey={api_key}"
    url = url + f"&symbol={symbol}" if symbol is not None else url
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data



def get_forex_news(symbol: str = None, page: Union[int, str] = 0, as_pandas: bool = True,
                   *args, **kwargs):
    url = f"{base_url_v4}forex_news?page={page}&apikey={api_key}"
    url = url + f"&symbol={symbol}" if symbol is not None else url
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data



def get_general_news(page: Union[int, str] = 0, as_pandas: bool = True,
                     *args, **kwargs):
    url = f"{base_url_v4}general_news?page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data



def get_press_releases(symbol: str, page: Union[int, str] = 0, as_pandas: bool = True,
                       *args, **kwargs):
    url = f"{base_url_v3}press-releases/{symbol}?page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data
