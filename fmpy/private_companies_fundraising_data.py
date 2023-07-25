
from .utils import *

import requests
import pandas as pd
from typing import Union, List

@check_arguments
def get_crowdfunding_offerings_rss_feed(page: Union[str, int] = 0, as_pandas: bool = True):
    url = f"{base_url_v4}crowdfunding-offerings-rss-feed?page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df['filling_date'] = df['filling_date'].apply(lambda x: x[0:10])
        df.index = df.filling_date
        df.drop(['cik', 'company_name', 'filling_date'], axis=1, inplace=True)
        df.index.name = 'filling_date'
        return df
    return json_data


@check_arguments
def get_crowdfunding_offerings_company_search(name: str, as_pandas: bool = True):
    url = f"{base_url_v4}crowdfunding-offerings/search?name={name}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        if len(df) == 0:
            return f"No funding's detected for {name}"
        df.index = df.date
        df.drop(['date'], axis=1, inplace=True)
        df.index.name = 'date'
        return df
    return json_data


@check_arguments
def get_crowdfunding_offerings_by_cik(cik: str, as_pandas=True):
    url = f"{base_url_v4}crowdfunding-offerings?cik={cik}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        if len(df) == 0:
            return f"No funding's detected for {cik}"
        return df
    return json_data


@check_arguments
def get_equity_offerings_fundraising_rss_feed(page: Union[int, str] = 0, as_pandas=True):
    url = f"{base_url_v4}fundraising-rss-feed?page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.index = df.cik
        df.drop(['cik'], axis=1, inplace=True)
        df.index.name = 'cik'
        return df
    return json_data


@check_arguments
def get_equity_offerings_fundraising_company_search(name: str, as_pandas=True):
    url = f"{base_url_v4}fundraising/search?name={name}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        if len(df) == 0:
            return f"No funding's detected for {name}"
        df.index = df.date
        df.drop(['date'], axis=1, inplace=True)
        df.index.name = 'date'
        return df
    return json_data


@check_arguments
def get_equity_fundraising_by_cik(cik: str, as_pandas=True):
    url = f"{base_url_v4}fundraising?cik={cik}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        if len(df) == 0:
            return f"No funding's detected for {cik}"
        return df
    return json_data
