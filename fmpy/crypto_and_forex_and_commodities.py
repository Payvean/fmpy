from .utils import *

import requests
import pandas as pd
from types import SimpleNamespace

from typing import Iterable, Union


def get_available_crypto_symbols(as_pandas: bool = True, index_: str = 'symbol'):
    url = f"{base_url_v3}symbol/available-cryptocurrencies?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, 'Failed to fetch available cryptocurrencies symbols')
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.set_index(index_, inplace=True)
        return df


def get_all_real_time_crypto_prices(as_pandas: bool = True, index_: str = 'symbol'):
    url = f"{base_url_v3}quotes/crypto?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, 'Failed to fetch all crypto prices')
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.set_index(index_, inplace=True)
        return df
    return json_data


def get_real_time_crypto_price(symbol: Union[str, Iterable],
                               as_pandas: bool = True, index_: str = 'symbol'):
    if not isinstance(symbol, str):
        symbol = ','.join(list(symbol))
    url = f"{base_url_v3}quote/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, f'Failed to real time crypto price for {symbol}')
    json_data = response.json()
    if count_string_chars(symbol, ',') > 0:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.set_index(index_, inplace=True)
        return df
    data = convert_dict_keys_to_snake_case(json_data[0])
    if as_pandas:
        return pd.Series(data)
    return SimpleNamespace(**data)


def get_historical_crypto_prices(symbol: str, interval: str = None,
                                 as_pandas: bool = True, index_: str = 'date'):
    if interval is not None and interval != '1day' and interval != 'daily':
        local_base = f"{base_url_v3}historical-chart/{interval}"
    else:
        local_base = f"{base_url_v3}historical-price-full"
    url = f"{local_base}/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, f'Failed to fetch crypto prices for {symbol}')

    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data) if interval is not None else pd.DataFrame(json_data['historical'])
        df = convert_columns_to_snake_case(df)
        df.set_index(index_, inplace=True)
        return df
    return json_data


def get_currency_exchange_rates(as_pandas: bool = True, index_: str = 'ticker'):
    url = f"{base_url_v3}fx?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, 'Failed to fetch exchange rates')
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.set_index(index_, inplace=True)
        return df
    return json_data


def get_currency_exchange_rate_single(symbol: str, as_pandas: bool = True):
    url = f"{base_url_v3}fx/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, f'Failed to fetch exchange rate for {symbol}')
    json_data = response.json()
    data = convert_dict_keys_to_snake_case(json_data[0])
    if as_pandas:
        return pd.Series(data)
    return SimpleNamespace(**data)


def get_currency_real_time_price(symbol: str, as_pandas: bool = True, index_: str = 'symbol'):
    if not isinstance(symbol, str):
        symbol = ','.join(list(symbol))
    url = f"{base_url_v3}quote/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, f'Failed to real time currency price for {symbol}')
    json_data = response.json()
    if count_string_chars(symbol, ',') > 0:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.set_index(index_, inplace=True)
        return df
    data = convert_dict_keys_to_snake_case(json_data[0])
    if as_pandas:
        return pd.Series(data)
    return SimpleNamespace(**data)


def get_historical_forex_prices(symbol: str, interval: str = None,
                                as_pandas: bool = True, index_: str = 'date'):
    if interval is not None and interval != '1day' and interval != 'daily':
        local_base = f"{base_url_v3}historical-chart/{interval}"
    else:
        local_base = f"{base_url_v3}historical-price-full"
    url = f"{local_base}/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, f'Failed to fetch forex prices for {symbol}')

    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data) if interval is not None else pd.DataFrame(json_data['historical'])
        df = convert_columns_to_snake_case(df)
        df.set_index(index_, inplace=True)
        return df
    return json_data


def get_available_commodities_symbols(as_pandas: bool = True, index_: str = 'symbol'):
    url = f"{base_url_v3}symbol/available-commodities?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, 'Failed to fetch available commodities symbols')
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.set_index(index_, inplace=True)
        return df


def get_all_real_time_commodity_prices(as_pandas: bool = True, index_: str = 'symbol'):
    url = f"{base_url_v3}quotes/commodity?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, 'Failed to fetch all commodity prices')
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.set_index(index_, inplace=True)
        return df
    return json_data


def get_real_time_commodity_price(symbol: Union[str, Iterable],
                                  as_pandas: bool = True, index_: str = 'symbol'):
    if not isinstance(symbol, str):
        symbol = ','.join(list(symbol))
    url = f"{base_url_v3}quote/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, f'Failed to real time commodity price for {symbol}')
    json_data = response.json()
    if count_string_chars(symbol, ',') > 0:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.set_index(index_, inplace=True)
        return df
    data = convert_dict_keys_to_snake_case(json_data[0])
    if as_pandas:
        return pd.Series(data)
    return SimpleNamespace(**data)


def get_historical_commodity_prices(symbol: str, interval: str = None,
                                    as_pandas: bool = True, index_: str = 'date'):
    if interval is not None and interval != '1day' and interval != 'daily':
        local_base = f"{base_url_v3}historical-chart/{interval}"
    else:
        local_base = f"{base_url_v3}historical-price-full"
    url = f"{local_base}/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, f'Failed to fetch commodity prices for {symbol}')

    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data) if interval is not None else pd.DataFrame(json_data['historical'])
        df = convert_columns_to_snake_case(df)
        df.set_index(index_, inplace=True)
        return df
    return json_data