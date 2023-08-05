from .utils import *
import requests

from pandas import DataFrame, Series
from types import SimpleNamespace
from typing import Union, Optional, Any

__author__ = 'Lukas Schröder'
__date__ = '2023-05-20'
__version__ = '0.1.0'

__doc__ = """
This module is related to the stock fundamentals Analysis section of the financial modeling prep API endpoint and 
provides section specific python functions.
"""

__all__ = ['get_company_financial_ratios',
           'get_company_rating',
           'get_company_key_metrics',
           'get_discounted_cash_flow',
           'get_cashflow_statement_growth',
           'get_company_enterprise_value',
           'get_company_financial_growth',
           'get_historical_discounted_cashflow',
           'get_income_statement_growth',
           'get_balance_sheet_statement_growth',
           ]



def get_company_financial_ratios(symbol: str, ttm: bool = True, period: str = 'quarter',
                                 limit: Optional[Union[str, int]] = None,
                                 as_pandas: bool = False,
                                 *args, **kwargs) -> Union[Union[Series, DataFrame], SimpleNamespace]:
    """
    Retrieves a company's financial ratios either for the trailing twelve months (TTM) or for a specified period.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        symbol (str): The stock symbol of the company to get financial ratios for.
        ttm (bool, optional): If True, gets the financial ratios for the trailing twelve months (TTM).
                              If False, gets the financial ratios for a specific period. Defaults to True.
        period (str, optional): The period for which to get financial ratios. Can be 'quarter' or 'annual'.
                                Defaults to 'quarter'.
        limit (Optional[Union[str, int]], optional): The maximum number of financial ratios to retrieve. Defaults to None.
        as_pandas (bool, optional): Determines whether the returned data is in a Pandas DataFrame or Series format
                                     (if as_pandas=True) or in a SimpleNamespace object (if as_pandas=False).
                                     Defaults to False.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[Union[Series, DataFrame], SimpleNamespace]: A DataFrame or Series (if as_pandas=True) or SimpleNamespace
                                                          object (if as_pandas=False) containing the financial ratios
                                                          data.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_company_financial_ratios(symbol='AAPL', ttm=True, period='quarter', limit=10, as_pandas=True)
    """
    url_ = f'{base_url_v3}ratios-ttm/{symbol}?{period}' if ttm else f'{base_url_v3}ratios/{symbol}?{period}'
    url_ += f'&apikey={api_key}'
    url = url_ + f'&{limit}' if limit is not None else url_
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = json_data[0] if ttm else json_data
    data = convert_dict_keys_to_snake_case(data) if ttm else data
    if as_pandas:
        return Series(data) if ttm else process_dataframe(data, *args, **kwargs)
    return SimpleNamespace(**data)



def get_score(symbol: str, as_pandas: bool = True):
    """
    Retrieves the score for a specified stock symbol.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        symbol (str): The stock symbol of the company to get the score for.
        as_pandas (bool, optional): Determines whether the returned data is in a Pandas DataFrame or Series format
                                     (if as_pandas=True) or in a SimpleNamespace object (if as_pandas=False).
                                     Defaults to True.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[Series, SimpleNamespace]: A Series (if as_pandas=True) or SimpleNamespace object (if as_pandas=False)
                                        containing the score data.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_score(symbol='AAPL', as_pandas=True)
    """
    url = f'{base_url_v4}score?symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = convert_dict_keys_to_snake_case(json_data[0])
    return Series(data) if as_pandas else SimpleNamespace(**data)



def get_owner_earnings(symbol: str, as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    """
    Retrieves the owner earnings for a specified stock symbol.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        symbol (str): The stock symbol of the company to get the owner earnings for.
        as_pandas (bool, optional): Determines whether the returned data is in a Pandas DataFrame format
                                     (if as_pandas=True) or in a raw JSON format (if as_pandas=False).
                                     Defaults to True.
        *args: Additional positional arguments passed to the `process_dataframe` function (only applicable if
               as_pandas=True).
        **kwargs: Additional keyword arguments passed to the `process_dataframe` function (only applicable if
                  as_pandas=True).

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[DataFrame, Any]: A DataFrame (if as_pandas=True) or a raw JSON object (if as_pandas=False)
                               containing the owner earnings data.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_owner_earnings(symbol='AAPL', as_pandas=True)
    """
    url = f'{base_url_v4}owner_earnings?symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data



def get_company_enterprise_value(symbol: str, period: str = 'quarter',
                                 limit: Optional[Union[str, int]] = None,
                                 as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    """
    Retrieves the enterprise value for a specified stock symbol.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        symbol (str): The stock symbol of the company to get the enterprise value for.
        period (str, optional): The period of the financials. Accepted values are 'quarter', 'annual'.
                                Defaults to 'quarter'.
        limit (Union[str, int], optional): Maximum number of results to return. Defaults to None.
        as_pandas (bool, optional): Determines whether the returned data is in a Pandas DataFrame format
                                     (if as_pandas=True) or in a raw JSON format (if as_pandas=False).
                                     Defaults to True.
        *args: Additional positional arguments passed to the `process_dataframe` function (only applicable if
               as_pandas=True).
        **kwargs: Additional keyword arguments passed to the `process_dataframe` function (only applicable if
                  as_pandas=True).

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[DataFrame, Any]: A DataFrame (if as_pandas=True) or a raw JSON object (if as_pandas=False)
                               containing the enterprise value data.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_company_enterprise_value(symbol='AAPL', period='quarter', as_pandas=True)
    """
    url = f'{base_url_v3}enterprise-values/{symbol}?apikey={api_key}&period={period}'
    url = url + f'&limit={limit}' if limit is not None else url
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data



def get_income_statement_growth(symbol: str, limit: Optional[Union[str, int]] = None,
                                as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    url = f'{base_url_v3}income-statement-growth/{symbol}?apikey={api_key}'
    url = url + f'&limit={limit}' if limit is not None else url
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data



def get_balance_sheet_statement_growth(symbol: str, limit: Optional[Union[str, int]] = None,
                                       as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    url = f'{base_url_v3}balance-sheet-statement-growth/{symbol}?apikey={api_key}'
    url = url + f'&limit={limit}' if limit is not None else url
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data



def get_cashflow_statement_growth(symbol: str, limit: Optional[Union[str, int]] = None,
                                  as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    url = f'{base_url_v3}cash-flow-statement-growth/{symbol}?apikey={api_key}'
    url = url + f'&limit={limit}' if limit is not None else url
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data



def get_company_key_metrics(symbol: str, ttm: bool = True, period: str = 'quarter',
                            limit: Optional[Union[str, int]] = None, as_pandas: bool = True,
                            *args, **kwargs) -> Union[Union[Series, DataFrame], Any]:
    url_ = f'{base_url_v3}key-metrics-ttm/{symbol}?period={period}' if ttm else f'{base_url_v3}key-metrics/{symbol}?period={period}'
    url_ += f'&apikey={api_key}'
    url = url_ + f'&limit={limit}' if limit is not None else url_
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = json_data[0] if ttm else json_data
    data = convert_dict_keys_to_snake_case(data) if ttm else data
    if as_pandas:
        return Series(data) if ttm else process_dataframe(json_data, *args, **kwargs)
    return SimpleNamespace(**data)



def get_company_financial_growth(symbol: str, period: str = 'quarter',
                                 limit: Optional[Union[str, int]] = None,
                                 as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    url = f'{base_url_v3}financial-growth/{symbol}?apikey={api_key}&period={period}'
    url = url + f'limit={limit}' if limit is not None else url
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data



def get_company_rating(symbol: str, historical: bool = False,
                       limit: Optional[Union[str, int]] = None,
                       as_pandas: bool = True, *args, **kwargs):
    url_ = f'{base_url_v3}rating/{symbol}' if not historical else f'{base_url_v3}historical-rating/{symbol}'
    url_ += f'?apikey={api_key}'
    url = url_ + f'&limit={limit}' if limit is not None else url_
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if not historical:
        data = json_data[0] if len(json_data) > 0 else {'data': 'EmptyData'}
        data = convert_dict_keys_to_snake_case(data)
        if as_pandas:
            return Series(data)
        return SimpleNamespace(**data)
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data



def get_discounted_cash_flow(symbol: str, advanced: bool = False,
                             levered: bool = False, as_pandas: bool = True,
                             *args, **kwargs) -> Union[DataFrame, Any, float]:
    if advanced:
        url = f'{base_url_v4}advanced_levered_discounted_cash_flow?' if levered else f'{base_url_v4}advanced_discounted_cash_flow?'
        url += f'symbol={symbol}&apikey={api_key}'
        response = requests.get(url)
        if response.status_code != 200:
            raise APIRequestError(response.status_code)
        json_data = response.json()
        index_ = kwargs.pop('index_', 'year')
        return process_dataframe(json_data, index_=index_, *args, **kwargs) if as_pandas else json_data
    else:
        url = f'{base_url_v3}discounted-cash-flow/{symbol}?apikey={api_key}'
        response = requests.get(url)
        if response.status_code != 200:
            raise APIRequestError(response.status_code)
        json_data = response.json()
        data = json_data[0] if len(json_data) > 0 else {'dcf': 'no_data_found'}
        return data['dcf']


def get_historical_discounted_cashflow(symbol: str, as_pandas: bool = True,
                                       period: str = 'daily',
                                       limit: Optional[Union[str, int]] = None,
                                       *args, **kwargs) -> Union[DataFrame, Any]:
    base_param_daily = 'historical-daily-discounted-cash-flow'
    base_param_p = 'historical-discounted-cash-flow-statement'
    if period == 'daily':
        url = f'{base_url_v3}{base_param_daily}/{symbol}'
        url += f'?apikey={api_key}&limit={limit}' if limit is not None else f"?apikey={api_key}"
    else:
        url = f'{base_url_v3}{base_param_p}/{symbol}'
        url += f'?apikey={api_key}&period={period}&limit={limit}' if limit is not None else f"?apikey={api_key}"

    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data
