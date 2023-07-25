from .utils import *

import requests
import pandas as pd
from types import SimpleNamespace

from typing import Iterable, Union


def get_available_euronext_symbols(as_pandas: bool = True, index_: str = 'symbol'):
    url = f"{base_url_v3}symbol/available-euronext?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.set_index(index_, inplace=True)
        return df
    return json_data


def get_all_real_time_euronext_prices(as_pandas: bool = True, index_: str = 'symbol'):
    url = f"{base_url_v3}quotes/euronext?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.set_index(index_, inplace=True)
        return df
    return json_data


def get_real_time_edf_price(symbol: Union[str, Iterable] = 'EDF.PA',
                            as_pandas: bool = True, index_: str = 'symbol'):
    if not isinstance(symbol, str):
        symbol = ','.join(list(symbol))
    url = f"{base_url_v3}quote/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
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


def get_historical_euronext_prices(symbol: str, interval: str = None,
                                   as_pandas: bool = True, index_: str = 'date'):
    if interval is not None and interval != '1day' and interval != 'daily':
        local_base = f"{base_url_v3}historical-chart/{interval}"
    else:
        local_base = f"{base_url_v3}historical-price-full"
    url = f"{local_base}/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)

    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data) if interval is not None else pd.DataFrame(json_data['historical'])
        df = convert_columns_to_snake_case(df)
        df.set_index(index_, inplace=True)
        return df
    return json_data
