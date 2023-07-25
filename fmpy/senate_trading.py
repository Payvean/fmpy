from .utils import *

import requests
import pandas as pd
from typing import Union


def get_senate_trading(symbol: str, page: Union[int, str] = 0,
                       as_pandas: bool = True, index_: str = 'last_name'):
    url = f"{base_url_v4}senate-trading?symbol={symbol}&apikey={api_key}&page={page}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.index = df[index_]
        df.drop([index_, 'link'], axis=1, inplace=True)
        df.index.name = index_
        return df
    return json_data


def get_senate_trading_rss_feed(page: Union[int, str] = 0,
                                as_pandas: bool = True, index_: str = 'last_name'):
    url = f"{base_url_v4}senate-trading-rss-feed?page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.index = df[index_]
        df.drop([index_, 'link'], axis=1, inplace=True)
        df.index.name = index_
        return df
    return json_data


def get_senate_disclosure(symbol: str, page: Union[int, str] = 0,
                          as_pandas: bool = True, index_: str = 'disclosure_date'):
    url = f"{base_url_v4}senate-disclosure?symbol={symbol}&page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.index = df[index_]
        df.drop([index_, 'link'], axis=1, inplace=True)
        df.index.name = index_
        return df
    return json_data


def get_senate_disclosure_rss_feed(page: Union[int, str] = 0,
                                   as_pandas: bool = True, index_: str = 'disclosure_date'):
    url = f"{base_url_v4}senate-disclosure-rss-feed?page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.index = df[index_]
        df.drop([index_, 'link'], axis=1, inplace=True)
        df.index.name = index_
        return df
    return json_data
