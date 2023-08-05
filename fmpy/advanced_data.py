from .utils import *
import requests
from pandas import DataFrame, Series
from types import SimpleNamespace
from typing import Union, Optional, Any

__author__ = 'Lukas Schröder'
__date__ = '2023-05-14'
__version__ = '0.1.0'

__doc__ = """
This module is related to the advanced data section of the financial modeling prep API endpoint and 
provides section specific python functions.
"""

__all__ = ['get_standard_industrial_classification',
           'get_standard_industrial_classification_list',
           'get_commitment_of_traders_analysis',
           'get_commitment_of_traders_report',
           'get_cod_trading_symbols_list']


def get_standard_industrial_classification(symbol: Optional[str] = None, cik: Optional[str] = None,
                                           sic_code: Optional[str] = None, as_pandas: bool = True,
                                           *args, **kwargs) -> Union[
    Union[Series, DataFrame], Union[SimpleNamespace, Any]]:
    """
    Retrieves the Standard Industrial Classification (SIC) code and details for a specific
    company or for all companies from the Financial Modeling Prep API. SIC is a system for
    classifying industries by a four-digit code.

    This function allows you to fetch data by symbol, CIK (Central Index Key, a unique
    identifier assigned by the SEC to each company), or SIC code. If no identifier is provided,
    it fetches data for all companies.

    Parameters:
    symbol (str, optional): The ticker symbol of the company to fetch the SIC for. Defaults to None.
    cik (str, optional): The CIK of the company to fetch the SIC for. Defaults to None.
    sic_code (str, optional): The SIC code to fetch the details for. Defaults to None.
    as_pandas (bool): If True, the function will return the fetched data as a pandas DataFrame or Series.
                     If False, it will return the raw JSON data or a SimpleNamespace object. Defaults to True.
    *args, **kwargs: Additional arguments to pass to the 'process_dataframe' function.

    Returns:
    Union[Union[Series, DataFrame], Union[SimpleNamespace, Any]]:
        If 'as_pandas' is True and only one company's data is fetched,
        returns a pandas Series with the fetched data.
        If 'as_pandas' is True and multiple companies' data are fetched,
        returns a pandas DataFrame with the fetched data.
        If 'as_pandas' is False and only one company's data is fetched,
        returns a SimpleNamespace object with the fetched data.
        If 'as_pandas' is False and multiple companies' data are fetched,
        returns the raw JSON data.
        If the API call fails, it returns an instance of the APIRequestError exception.

    Raises:
    APIRequestError: If the request to the Financial Modeling Prep API fails.
    """
    get_all = (symbol is None and cik is None and sic_code is None)
    local_base = f"{base_url_v4}standard_industrial_classification"
    if get_all:
        url = f"{local_base}/all?apikey={api_key}"
    elif symbol:
        url = f"{local_base}?symbol={symbol}&apikey={api_key}"
    elif cik:
        url = f"{local_base}?cik={cik}&apikey={api_key}"
    else:
        url = f"{local_base}?sicCode={sic_code}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        if not get_all:
            data = convert_dict_keys_to_snake_case(json_data[0])
            return Series(data)
        return process_dataframe(json_data, *args, **kwargs)
    if not get_all:
        data = convert_dict_keys_to_snake_case(json_data[0])
        return SimpleNamespace(**data)
    return json_data


def get_standard_industrial_classification_list(as_pandas: bool = True,
                                                industry_title: Optional[str] = None,
                                                sic_code: Optional[str] = None,
                                                *args, **kwargs) -> Union[DataFrame, Any]:
    """
    Retrieves the standard industrial classification (SIC) list from the Financial Modeling Prep API.

    The SIC is a system for classifying industries by a four-digit code. It is being supplanted by the 
    six-digit North American Industry Classification System (NAICS code), but certain government departments 
    and agencies still use the SIC codes.

    Parameters: as_pandas (bool): If True, the function will return a pandas DataFrame. If False, it will return JSON
    data. Defaults to True. industry_title (str, optional): The title of the industry to filter the SIC list. If
    provided, the function will return only the SIC codes for this industry. Defaults to None. sic_code (str,
    optional): A specific SIC code. If provided, the function will return only the data for this SIC code. Defaults
    to None. *args (tuple): Additional positional arguments passed to the 'process_dataframe' function. **kwargs (
    dict): Additional keyword arguments passed to the 'process_dataframe' function. The following keyword arguments
    are recognized: - 'index_': The column to use as index in the DataFrame. If not provided, defaults to 'sic_code'.
    - 'ignore_': A column or a list of columns to be dropped from the DataFrame. - 'datatype_': The format to save
    the DataFrame. It can be 'csv', 'xlsx', or 'html'. - 'output_path_': The location to save the DataFrame. If not
    provided, a default location will be used.

    Returns:
    Union[DataFrame, Any]: If 'as_pandas' is True, returns a pandas DataFrame with the SIC list data. If 'as_pandas' 
                           is False, returns JSON data as returned by the API.

    Raises:
    APIRequestError: If the request to the Financial Modeling Prep API fails.
    """
    url = f"{base_url_v4}standard_industrial_classification_list?apikey={api_key}"
    if industry_title is not None:
        url += f"&{industry_title}"
    elif sic_code is not None:
        url += f"&{sic_code}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'sic_code')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_cod_trading_symbols_list(as_pandas: bool = True,
                                 *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v4}commitment_of_traders_report/list?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'trading_symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


@not_implemented
def get_commitment_of_traders_report():
    pass


@not_implemented
def get_commitment_of_traders_analysis():
    pass
