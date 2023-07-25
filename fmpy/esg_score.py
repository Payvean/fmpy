from .utils import *

import requests
import pandas as pd


@check_arguments
def get_esg_score(symbol, as_pandas=True):
    url = f"{base_url_v4}esg-environmental-social-governance-data?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df = convert_columns_to_snake_case(df)
        df.index = df.date
        df.drop(['symbol', 'date', 'cik', 'url', 'company_name'], axis=1, inplace=True)
        df.index.name = 'date'
        return df
    return json_data


@check_arguments
def get_company_esg_risk_ratings(symbol, as_pandas=True):
    local_base = 'esg-environmental-social-governance-data-ratings'
    url = f"{base_url_v4}{local_base}?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df.index = df.year
        df = convert_columns_to_snake_case(df)
        df.drop(['symbol', 'cik', 'company_name', 'year'], axis=1, inplace=True)
        df.index.name = 'year'
        return df
    return json_data


@check_arguments
def get_esg_benchmarking_by_sector_and_year(year, as_pandas=True):
    local_base = 'esg-environmental-social-governance-sector-benchmark'
    url = f"{base_url_v4}{local_base}?year={year}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = pd.DataFrame(json_data)
        df.index = df.year
        df = convert_columns_to_snake_case(df)
        df.drop(['year'], axis=1, inplace=True)
        df.index.name = 'year'
        return df
    return json_data
