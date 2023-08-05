from .utils import *

import requests
import pandas as pd

__author__ = 'Lukas Schröder'
__date__ = '2023-08-05'
__version__ = '0.1.0'

__doc__ = """This module is related to the esg_score data section of the financial modeling 
prep API endpoint and provides section specific python functions."""

__all__ = [
    'get_esg_score',
    'get_company_esg_risk_ratings',
    'get_esg_benchmarking_by_sector_and_year',
]

def get_esg_score(symbol, as_pandas=True, *args, **kwargs):
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


def get_company_esg_risk_ratings(symbol, as_pandas=True, *args, **kwargs):
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


def get_esg_benchmarking_by_sector_and_year(year, as_pandas=True, *args, **kwargs):
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
