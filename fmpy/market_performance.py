from .utils import *

import requests
import pandas as pd
import datetime as dt
from typing import Union


def get_sectors_pe_ratio(date: Union[dt.date, str] = None, exchange: str = 'NYSE',
                         as_pandas: bool = True):
    if date is None:
        date = str(dt.date.today())
    url = f"{base_url_v4}sector_price_earning_ratio?date={date}&exchange={exchange}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.index = df.date
        df.drop(['date'], axis=1, inplace=True)
        df.index.name = 'date'
        return df
    return json_data


def get_industries_pe_ratio(date: Union[dt.date, str] = None, exchange: str = 'NYSE',
                            as_pandas: bool = True):
    if date is None:
        date = str(dt.date.today())
    url = f"{base_url_v4}industry_price_earning_ratio?date={date}&exchange={exchange}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.index = df.date
        df.drop(['date'], axis=1, inplace=True)
        df.index.name = 'date'
        return df
    return json_data


def get_stock_market_sector_performance(historical: bool = False, as_pandas: bool = True,
                                        limit: Union[int, str] = 50):
    url = f"{base_url_v3}sector-performance?apikey={api_key}"
    if historical:
        url = f"{base_url_v3}historical-sectors-performance?apikey={api_key}"
    url += f"&limit={limit}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        if not historical:
            df.index = df.sector
            df.drop(['sector'], axis=1, inplace=True)
            df.index.name = 'sector'
        else:
            df.index = df.date
            df.drop(['date'], axis=1, inplace=True)
            df.index.name = 'date'
        return df
    return json_data


def get_most_gainer_stock_companies(as_pandas: bool = True):
    url = f"{base_url_v3}stock_market/gainers?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.index = df.symbol
        df.drop(['symbol'], inplace=True, axis=1)
        df.index.name = 'symbol'
        return df
    return json_data


def get_most_losers_stock_companies(as_pandas: bool = True):
    url = f"{base_url_v3}stock_market/losers?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.index = df.symbol
        df.drop(['symbol'], inplace=True, axis=1)
        df.index.name = 'symbol'
        return df
    return json_data


def get_most_active_stock_companies(as_pandas: bool = True):
    url = f"{base_url_v3}stock_market/actives?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.index = df.symbol
        df.drop(['symbol'], inplace=True, axis=1)
        df.index.name = 'symbol'
        return df
    return json_data
