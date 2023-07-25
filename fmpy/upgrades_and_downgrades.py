from .utils import *

import requests
import pandas as pd
from types import SimpleNamespace
from typing import Union

def get_upgrades_and_downgrades(symbol: str, as_pandas=True):
    url = f"{base_url_v4}upgrades-downgrades?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df['published_date'] = df['published_date'].apply(lambda x: x[0:10])
        df.drop(['news_ur_l'], axis=1, inplace=True)
        return df
    return json_data


def get_upgrades_and_downgrades_rss_feed(page: Union[str, int] = 0, as_pandas=True):
    url = f"{base_url_v4}upgrades-downgrades-rss-feed?page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df['published_date'] = df['published_date'].apply(lambda x: x[0:10])
        df.drop(['news_ur_l'], axis=1, inplace=True)
        return df
    return json_data


def get_upgrades_and_downgrades_consensus(symbol: str, as_pandas=True):
    url = f"{base_url_v4}upgrades-downgrades-consensus?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = convert_dict_keys_to_snake_case(json_data[0])
    if as_pandas:
        return pd.Series(data)
    return SimpleNamespace(**data)


def get_upgrades_and_downgrades_by_company(company: str, as_pandas=True):
    url = f"{base_url_v4}upgrades-downgrades-grading-company?company={company}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df['published_date'] = df['published_date'].apply(lambda x: x[0:10])
        df.drop(['news_ur_l'], axis=1, inplace=True)
        return df
    return json_data
