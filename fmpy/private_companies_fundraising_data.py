from .utils import *
import requests
from typing import Union

__author__ = 'Lukas Schröder'
__date__ = '2023-08-05'
__version__ = '0.1.0'

__doc__ = """
This module is related to the private companies fundraising data section of the financial modeling prep API endpoint and 
provides section specific python functions.
"""

__all__ = [
    'get_crowdfunding_offerings_rss_feed',
    'get_crowdfunding_offerings_by_cik',
    'get_crowdfunding_offerings_company_search',
    'get_equity_offerings_fundraising_rss_feed',
    'get_equity_fundraising_by_cik',
    'get_equity_offerings_fundraising_company_search'
]


@in_development
def get_crowdfunding_offerings_rss_feed(page: Union[str, int] = 0, as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v4}crowdfunding-offerings-rss-feed?page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


@in_development
def get_crowdfunding_offerings_company_search(name: str, as_pandas: bool = True, *args, **kwargs):
    url = f"{base_url_v4}crowdfunding-offerings/search?name={name}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


@in_development
def get_crowdfunding_offerings_by_cik(cik: str, as_pandas=True, *args, **kwargs):
    url = f"{base_url_v4}crowdfunding-offerings?cik={cik}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


def get_equity_offerings_fundraising_rss_feed(page: Union[int, str] = 0, as_pandas=True, *args, **kwargs):
    url = f"{base_url_v4}fundraising-rss-feed?page={page}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'cik')
        return process_dataframe(json_data, index_=index_ * args, **kwargs)
    return json_data


@in_development
def get_equity_offerings_fundraising_company_search(name: str, as_pandas=True, *args, **kwargs):
    url = f"{base_url_v4}fundraising/search?name={name}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


@in_development
def get_equity_fundraising_by_cik(cik: str, as_pandas=True, *args, **kwargs):
    url = f"{base_url_v4}fundraising?cik={cik}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data
