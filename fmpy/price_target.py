from .utils import *

import requests
import pandas as pd
from pandas import DataFrame, Series
from types import SimpleNamespace
from typing import List, Union


def get_price_target(symbol: str, as_pandas: bool = True,
                     index_: str = 'published_date') -> Union[DataFrame, List[dict]]:
    url = f"{base_url_v4}price-target?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, f"Failed to fetch price target for {symbol}")
    json_data = response.json()
    if as_pandas:
        df = DataFrame(json_data)
        df = convert_columns_to_snake_case(df)

        # TODO: More sophisticated way
        df['published_date'] = df['published_date'].apply(lambda x: x[0:10])
        df.set_index(index_, inplace=True)
        df.drop(['news_ur_l'], axis=1, inplace=True)
        return df
    return json_data


def get_price_target_summary(symbol: str, as_pandas: bool = True) -> Union[Series, SimpleNamespace]:
    url = f"{base_url_v4}price-target-summary?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, f"Failed to fetch price target for {symbol}")
    json_data = response.json()
    if as_pandas:
        return Series(json_data[0])
    data = json_data[0]
    return SimpleNamespace(**data)


def get_price_target_by_analyst_name(name: str, as_pandas: bool = True) -> Union[Series, SimpleNamespace]:
    url = f"{base_url_v4}price-target-analyst-name?name={name}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, f"Failed to fetch price target for {name}")
    json_data = response.json()
    data = json_data[0]
    data = convert_dict_keys_to_snake_case(data)
    if as_pandas:
        return Series(data)
    return SimpleNamespace(**data)


def get_price_target_by_analyst_company(company: str, as_pandas: bool = True) -> Union[Series, SimpleNamespace]:
    url = f"{base_url_v4}price-target-analyst-company?company={company}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, f"Failed to fetch price target for {company}")
    json_data = response.json()
    data = json_data[0]
    data = convert_dict_keys_to_snake_case(data)
    if as_pandas:
        return Series(data)
    return SimpleNamespace(**data)


def get_price_target_consensus(symbol: str, as_pandas: bool = True) -> Union[Series, SimpleNamespace]:
    url = f"{base_url_v4}price-target-consensus?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, f"Failed to fetch price target for {symbol}")
    json_data = response.json()
    data = json_data[0]
    data = convert_dict_keys_to_snake_case(data)
    if as_pandas:
        return Series(data)
    return SimpleNamespace(**data)


def get_price_target_rss_feed(page: Union[str, int] = 0, as_pandas: bool = True):
    url = f"{base_url_v4}price-target-rss-feed?page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, f"Failed to fetch price target rss feed")
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        return df
    return json_data
