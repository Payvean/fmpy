from .utils import *

import requests
import pandas as pd
import datetime as dt
from typing import Union, Iterable
from types import SimpleNamespace

__author__ = 'Lukas Schröder'
__date__ = '2023-05-20'
__version__ = '0.1.0'

__doc__ = """
This module is related to the stock price section of the financial modeling prep API endpoint and 
provides section specific python functions.
"""

__all__ = [
    'get_stock_price_change',
    'get_technical_indicator',
    'get_prices_of_otc_companies',
    'get_stock_price_list',
    'get_historical_stock_split',
    'get_stock_historical_price',
    'get_company_quote',
    'get_real_time_price',
    'get_real_time_volume',
    'get_survivorship_bias_free_eod',
]


def get_company_quote(tickers: Union[str, Iterable], as_pandas: bool = True):
    if isinstance(tickers, list):
        tickers = ','.join(list(tickers))
    url = f"{base_url_v3}quote/{tickers}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if len(tickers) > 5:
        if as_pandas:
            df = pd.DataFrame(json_data)
            df = convert_columns_to_snake_case(df)
            return df
        return json_data
    data = json_data[0] if isinstance(json_data, list) else json_data
    data = convert_dict_keys_to_snake_case(data)
    if as_pandas:
        return pd.Series(data)
    return SimpleNamespace(**data)


def get_prices_of_otc_companies(tickers: Union[str, Iterable], as_pandas: bool = True):
    if not isinstance(tickers, str):
        tickers = ','.join(list(tickers))
    url = f"{base_url_v3}otc/real-time-price/{tickers}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if len(tickers) > 5:
        if as_pandas:
            df = pd.DataFrame(json_data)
            df = convert_columns_to_snake_case(df)
            return df
        return json_data
    data = json_data[0] if isinstance(json_data, list) else json_data
    data = convert_dict_keys_to_snake_case(data)
    if as_pandas:
        return pd.Series(data)
    return SimpleNamespace(**data)


@in_development
def get_stock_price_change(tickers: Union[str, Iterable], as_pandas: bool = True, *args, **kwargs):
    if isinstance(tickers, list):
        tickers = ','.join(list(tickers))
    url = f"{base_url_v3}stock-price-change/{tickers}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if len(tickers) > 5:
        if as_pandas:
            return process_dataframe(json_data, *args, **kwargs)
        return json_data
    data = json_data[0] if isinstance(json_data, list) else json_data
    data = convert_dict_keys_to_snake_case(data)
    if as_pandas:
        return pd.Series(data)
    return SimpleNamespace(**data)


def get_real_time_price(symbol: str):
    url = f"{base_url_v3}quote-short/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = json_data[0]
    return data['price']


def get_real_time_volume(symbol: str):
    url = f"{base_url_v3}quote-short/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = json_data[0]
    return data['volume']


@in_development
def get_stock_price_list(exchange: str = 'nyse', as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v3}quotes/{exchange}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, *args, **kwargs)
    return json_data


@in_development
def get_stock_historical_price(tickers: Union[str, Iterable],
                               interval: str = None, timeseries: Union[int, str] = None,
                               from_: str = '2008-01-01', to_: str = str(dt.date.today()),
                               serietype='line', as_pandas: bool = True, *args, **kwargs):
    if not isinstance(tickers, str):
        tickers = ','.join(list(tickers))
    if interval is None or interval == '1day':
        url = f"{base_url_v3}historical-price-full/{tickers}"
    else:
        url = f"{base_url_v3}historical-chart/{interval}/{tickers}"

    url += f"?apikey={api_key}&seriestype={serietype}"
    if timeseries is not None:
        url += f"&timeseries={timeseries}"
    else:
        url += f"&from={from_}&to={to_}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)

    json_data = response.json()
    if as_pandas:
        if interval is not None:
            df = process_dataframe(json_data, *args, **kwargs)
        if len(tickers) > 5:
            multi_df = pd.DataFrame()
            for symbol_data in json_data['historicalStockList']:
                symbol = symbol_data['symbol']
                historical_data = symbol_data['historical']
                df = pd.DataFrame(historical_data)
                df = convert_columns_to_snake_case(df)
                df['date'] = pd.to_datetime(df.date)
                df.set_index('date', inplace=True)
                df.columns = pd.MultiIndex.from_product([[symbol], df.columns])

                if multi_df.empty:
                    multi_df = df
                else:
                    multi_df = multi_df.join(df, how='outer')
            return multi_df
        else:
            df = process_dataframe(json_data, *args, **kwargs)
        return df
    return json_data


def get_historical_stock_split(symbol: str, as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v3}historical-price-full/stock_split/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data['historical'], *args, **kwargs) if as_pandas else json_data


def get_survivorship_bias_free_eod(symbol: str, date: str = str(dt.date.today()),
                                   as_pandas: bool = True):
    url = f"{base_url_v4}historical-price-full/{symbol}/{date}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        return pd.Series(json_data)
    return SimpleNamespace(**json_data)


def get_technical_indicator(symbol: str, type_: str, interval='daily',
                            period: Union[int, str] = 10, as_pandas: bool = True, *args, **kwargs):
    if interval == 'daily' or interval == '1day':
        url = f"{base_url_v3}technical_indicator/daily/{symbol}?period={period}&type={type_}"
    else:
        url = f"{base_url_v3}technical_indicator/{interval}/{symbol}?type={type_}"
    url += f"&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data
