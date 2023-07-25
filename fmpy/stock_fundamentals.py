# Helper functions and API Key for the user
from .utils import *

import requests
import pandas as pd

from pandas import DataFrame, Series
from io import StringIO
from types import SimpleNamespace
from typing import List, Union, Any, IO, Optional
from os import PathLike

url_api = f"apikey={api_key}"

__author__ = 'Lukas Schröder'
__date__ = '2023-05-12'
__version__ = '0.1.0'
__rights__ = 'Copyright (c) 2023 Lukas Schröder'

__doc__ = """
This module is related to the stock fundamentals section of the financial modeling prep API endpoint and 
provides section specific python functions that can be used to retrieve the data easily and well processed.
"""

__all__ = ['get_financial_statements_list',
           'get_income_statement',
           'get_cashflow_statement',
           'get_balance_sheet_statement',
           'get_sec_filings',
           'get_company_notes',
           'get_shares_float_all',
           'get_shares_float_symbol',
           'get_earning_call_transcript',
           'get_revenue_geographic_by_segments',
           'get_sales_and_revenue_by_segments',
           'get_sec_rss_feed',
           'get_financial_reports_dates',
           'get_earning_call_transcript_dates',
           'get_reports_on_form_10k',
           'get_rss_feed_8k_forms']


def get_financial_statements_list() -> List:
    """
    This endpoint allows you to get a list of all companies for which the API has financial statements.
    We cover the New York Stock Exchange (NYSE), the New York Stock Exchange (NASDAQ),
    international exchanges, and more. Because we're growing all the time, this list will be updated on a regular basis.
    --------------------------------------------------------------------------------------------------------------------
    Returns:
        List: Returns a list of all symbols with available financial statements
    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: Request error returning status code and possible reason
    """
    category = 'financial-statement-symbol-lists'
    url = f"{base_url_v3}{category}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data: list = response.json()
    return json_data


def get_income_statement(symbol: str, limit: Union[int, str] = 120, period: str = 'quarter',
                         as_pandas: bool = True, as_reported: bool = False, *args, **kwargs) -> Union[
    DataFrame, Union[Any, dict]]:
    """
    Fetches the income statement data for a specific company, identified by its ticker symbol,
    from the Financial Modeling Prep API.
    An income statement, also known as a profit and loss statement,
    is a financial document that provides a snapshot of a company's financial performance
    over a specific period of time. It shows the company's revenues, costs, and expenses,
    which together can be used to calculate net income or loss.


    This method allows you to retrieve the income statement data in the form of a pandas DataFrame or a JSON object,
    depending on your preference.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        symbol (str): The ticker symbol of the company for which to retrieve the income statement.
                      This is a unique series of letters representing a particular company's stock.
        limit (Union[int, str], optional): The maximum number of income statement records to retrieve.
                                           This can either be an integer or the string 'max'. Defaults to 120.
        period (str, optional): The financial period for which to retrieve the income statement.
                                This can be either 'quarter' for quarterly data or 'annual' for yearly data.
                                Defaults to 'quarter'.
        as_pandas (bool, optional): A flag indicating whether to return the income statement data as a pandas DataFrame.
                                    If set to False, the data will be returned as a JSON object. Defaults to True.
        *args: Variable length argument list that will be passed to the
               `process_dataframe` function when 'as_pandas' is True. These arguments
               can be used to further customize the DataFrame processing.
        **kwargs: Arbitrary keyword arguments that will be passed to the `process_dataframe`
                  function when 'as_pandas' is True. These arguments can be used to further customize
                  the DataFrame processing.
                  One key that can be included is 'transpose_', which controls whether to transpose the DataFrame.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[DataFrame, Union[Any, dict]]: The income statement data. If 'as_pandas' is True,
        this will be a pandas DataFrame. If 'as_pandas' is False, this will be a JSON object.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_income_statement('AAPL', limit=10, period='annual', as_pandas=True)
        :param period:
        :param limit:
        :param symbol:
        :param as_pandas:
        :param as_reported:
    """
    statement = 'income-statement-as-reported' if as_reported else 'income-statement'
    url = f"{base_url_v3}{statement}/{symbol}?limit={limit}&period={period}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        transpose = kwargs.pop('transpose_', True)
        return process_dataframe(json_data, transpose_=transpose, *args, **kwargs)
    return json_data


@check_arguments
def get_balance_sheet_statement(symbol: str, limit: Union[int, str] = 120, period: str = 'quarter',
                                as_pandas: bool = True, as_reported: bool = False,
                                *args, **kwargs) -> Union[DataFrame, Union[Any, dict]]:
    """
    Retrieves the balance sheet statement data for a given company ticker symbol from the Financial Modeling Prep API.

    A balance sheet statement is a snapshot of a company's financials at a given point in time, 
    detailing assets, liabilities, and shareholders' equity. This function fetches such data and 
    can return it as a JSON object or a pandas DataFrame.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        symbol (str): The ticker symbol of the company for which to retrieve the balance sheet statement.
        limit (Union[int, str], optional): The maximum number of records to fetch. Defaults to 120.
        period (str, optional): The time period for the balance sheet statement, either 'quarter' or 'annual'. 
                                Defaults to 'quarter'.
        as_pandas (bool, optional): If True, returns the data as a pandas DataFrame. If False,
                                    returns it as a JSON object. Defaults to True.
        *args: Variable length argument list to pass to the `process_dataframe` function.
        **kwargs: Arbitrary keyword arguments to pass to the `process_dataframe` function. Accepts 'transpose_'
                  as a key.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[DataFrame, Union[Any, dict]]: The balance sheet statement data as a pandas DataFrame (if as_pandas=True) 
                                            or a JSON object (if as_pandas=False).

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request is unsuccessful, it raises an error with the status code and potential 
                         reason for the failure.
        TypeError: If provided arguments do not match their expected types, enforced by the `check_arguments` decorator.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_balance_sheet_statement('AAPL', limit=10, period='annual', as_pandas=True)
    """
    statement = 'balance-sheet-statement-as-reported' if as_reported else 'balance-sheet-statement'
    url = f"{base_url_v3}{statement}/{symbol}?limit={limit}&period={period}&apikey={api_key}"
    response = requests.get(url)

    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        transpose = kwargs.pop('transpose_', True)
        return process_dataframe(json_data, transpose_=transpose, *args, **kwargs)
    return json_data


@check_arguments
def get_cashflow_statement(symbol: str, limit: Union[int, str] = 120, period: str = 'quarter',
                           as_pandas: bool = True, as_reported: bool = False, *args, **kwargs) -> Union[
    DataFrame, Union[Any, dict]]:
    """
    Fetches the cash flow statement data for a specific company, identified by its ticker symbol,
    from the Financial Modeling Prep API.
    A cash flow statement provides information about a company's cash inflows and outflows over a certain
    period of time,
    which helps in understanding its operating, investing, and financing activities.

    This method allows you to retrieve the cash flow statement data in the form of a pandas DataFrame or a JSON object,
    depending on your preference.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        symbol (str): The ticker symbol of the company for which to retrieve the cash flow statement.
                      This is a unique series of letters representing a particular company's stock.
        limit (Union[int, str], optional): The maximum number of cash flow statement records to retrieve.
                                           This can either be an integer or the string 'max'. Defaults to 120.
        period (str, optional): The financial period for which to retrieve the cash flow statement.
                                This can be either 'quarter' for quarterly data or 'annual' for yearly data.
                                Defaults to 'quarter'.
        as_pandas (bool, optional): A flag indicating whether to return the cash flow statement data
                                    as a pandas DataFrame.
                                    If set to False, the data will be returned as a JSON object. Defaults to True.
        *args: Variable length argument list that will be passed to the
               `process_dataframe` function when 'as_pandas' is True. These arguments
               can be used to further customize the DataFrame processing.
        **kwargs: Arbitrary keyword arguments that will be passed to the `process_dataframe`
                  function when 'as_pandas' is True. These arguments can be used to further customize
                  the DataFrame processing.
                  One key that can be included is 'transpose_', which controls whether to transpose the DataFrame.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[DataFrame, Union[Any, dict]]: The cash flow statement data. If 'as_pandas' is True,
        this will be a pandas DataFrame. If 'as_pandas' is False, this will be a JSON object.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_cashflow_statement('AAPL', limit=10, period='annual', as_pandas=True)
    """
    statement = 'cash-flow-statement-as-reported' if as_reported else 'cash-flow-statement'
    url = f"{base_url_v3}{statement}/{symbol}?limit={limit}&period={period}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        transpose = kwargs.pop('transpose_', True)
        return process_dataframe(json_data, transpose_=transpose, *args, **kwargs)
    return json_data


@check_arguments
def get_shares_float_symbol(symbol: Union[str, list], as_pandas: bool = True,
                            *args, **kwargs) -> Union[Union[Series, DataFrame], SimpleNamespace]:
    """
    Fetches the floating shares data for a specific company or a list of companies,
    identified by their ticker symbols, from the Financial Modeling Prep API.
    Floating shares are the number of shares available for trading of a particular stock.

    This method allows you to retrieve the floating shares' data in the form of a pandas Series or DataFrame,
    or a JSON-like object (SimpleNamespace), depending on your preference.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        symbol (Union[str, list]): The ticker symbol or a list of ticker symbols of the company(ies)
                                   for which to retrieve the floating shares data.
        as_pandas (bool, optional): A flag indicating whether to return the floating shares' data as a pandas object
                                    (Series or DataFrame). If set to False, the data will be returned
                                    as a SimpleNamespace object. Defaults to True.
        *args: Variable length argument list that will be passed to the `get_shares_float_all` function
               when 'symbol' is a list and 'as_pandas' is True. These arguments can be used to further customize
               the data processing.
        **kwargs: Arbitrary keyword arguments that will be passed to the `get_shares_float_all` function
                  when 'symbol' is a list and 'as_pandas' is True. These arguments can be used to further customize
                  the data processing.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[Union[Series, DataFrame], SimpleNamespace]: The floating shares data. If 'as_pandas' is True,
        this will be a pandas Series (for a single company) or DataFrame (for multiple companies). If 'as_pandas'
        is False, this will be a SimpleNamespace object.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_shares_float_symbol('AAPL', as_pandas=True)
        >>> get_shares_float_symbol(['AAPL', 'MSFT'], as_pandas=True)
    """
    if isinstance(symbol, list):
        data = get_shares_float_all(as_pandas=as_pandas, *args, **kwargs)
        if as_pandas:
            return data.loc[symbol]
        return data
    url = f'{base_url_v4}shares_float?symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = json_data[0]
    if as_pandas:
        data = convert_dict_keys_to_snake_case(data)
        return Series(data)
    return SimpleNamespace(**data)


@check_arguments
def get_shares_float_all(as_pandas: bool = True,
                         *args, **kwargs) -> Union[DataFrame, Any]:
    """
    Fetches the floating shares data for all companies from the Financial Modeling Prep API.
    Floating shares are the number of shares available for trading of a particular stock.

    This method allows you to retrieve the floating shares data in the form of a pandas DataFrame or a JSON object,
    depending on your preference.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        as_pandas (bool, optional): A flag indicating whether to return the floating shares data as a pandas DataFrame.
                                    If set to False, the data will be returned as a JSON object. Defaults to True.
        *args: Variable length argument list that will be passed to the `process_dataframe` function when 'as_pandas'
               is True. These arguments can be used to further customize the DataFrame processing.
        **kwargs: Arbitrary keyword arguments that will be passed to the `process_dataframe` function when 'as_pandas'
                  is True. These arguments can be used to further customize the DataFrame processing. A key that can be
                  included is 'index_', which controls the indexing of the DataFrame.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[DataFrame, Any]: The floating shares data. If 'as_pandas' is True, this will be a pandas DataFrame.
                               If 'as_pandas' is False, this will be a JSON object.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain a
                         message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_shares_float_all(as_pandas=True)
    """
    url = f'{base_url_v4}shares_float/all?apikey={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_, *args, **kwargs)
    return json_data


@check_arguments
def get_earning_call_transcript_dates(symbol: str) -> List[list]:
    """
    Fetches the dates of earning call transcripts for a specific company, identified by its ticker symbol,
    from the Financial Modeling Prep API. An earnings call is a teleconference, or webcast,
    in which a public company discusses the financial results of a reporting period ("earnings guidance").

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        symbol (str): The ticker symbol of the company for which to retrieve the earning call transcript dates.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        List[list]: A list of lists, where each inner list represents a date and corresponding transcript data.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain a
                         message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_earning_call_transcript_dates('AAPL')
    """
    url = f'{base_url_v4}earning_call_transcript?symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    return response.json()


@check_arguments
def get_earning_call_transcript(symbol: str, quarter: Union[int, str] = 1,
                                year: Union[int, str] = 2023, content: bool = True,
                                batch: bool = False, as_pandas: bool = True,
                                *args, **kwargs) -> Union[str, SimpleNamespace, DataFrame]:
    """
    Fetches the transcript of the earnings call for a specific company and a specific quarter and year,
    identified by its ticker symbol, from the Financial Modeling Prep API.

    An earnings call is a teleconference, or webcast, in which a public company discusses the financial results
    of a reporting period.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        symbol (str): The ticker symbol of the company for which to retrieve the earning call transcript.
        quarter (Union[int, str], optional): The financial quarter for which to retrieve the transcript.
                                             Defaults to 1.
        year (Union[int, str], optional): The year for which to retrieve the transcript. Defaults to 2023.
        content (bool, optional): A flag indicating whether to return just the content of the transcript
                                  (as a string) or the whole transcript data (as a SimpleNamespace object).
                                  Defaults to True.
        batch (bool, optional): A flag indicating whether to retrieve transcripts for all quarters of the specified
                                year. If set to True, 'quarter' parameter is ignored. Defaults to False.
        as_pandas (bool, optional): A flag indicating whether to return the transcript data as a pandas DataFrame
                                    when 'batch' is True. If set to False, the data will be returned as a JSON object.
                                    Defaults to True.
        *args: Variable length argument list that will be passed to the `process_dataframe` function when 'batch'
               and 'as_pandas' are True. These arguments can be used to further customize the DataFrame processing.
        **kwargs: Arbitrary keyword arguments that will be passed to the `process_dataframe` function when 'batch'
                  and 'as_pandas' are True. These arguments can be used to further customize the DataFrame processing.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[str, SimpleNamespace, DataFrame]: The earnings call transcript. If 'content' is True, this will be
        a string containing the content of the transcript. If 'content' is False, this will be a SimpleNamespace
        object containing all transcript data. If 'batch' is True, this will be a pandas DataFrame (if 'as_pandas'
        is True) or a JSON object (if 'as_pandas' is False) containing all transcripts for the specified year.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain a
                         message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_earning_call_transcript('AAPL', quarter=2, year=2022, content=True)
    """
    url = f'{base_url_v3}earning_call_transcript/{symbol}?quarter={str(quarter)}&year={str(year)}&apikey={api_key}'
    if batch:
        url = f'{base_url_v4}batch_earning_call_transcript/{symbol}?year={str(year)}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if batch:
        return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data
    data = json_data[0]
    if content:
        return SimpleNamespace(**data).content.replace('/n', ' ')
    return SimpleNamespace(**data)


@check_arguments
def get_sec_filings(symbol: str, as_pandas: bool = True, type_: Optional[str] = None,
                    page: Optional[Union[int, str]] = None,
                    limit: Optional[Union[int, str]] = None, *args, **kwargs) -> Union[DataFrame, Any]:
    """
    Fetches the SEC filings for a specific company, identified by its ticker symbol,
    from the Financial Modeling Prep API.

    The SEC, or Securities and Exchange Commission, is a U.S. government oversight agency responsible for
    regulating the securities industry, which includes stocks and options exchanges.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        symbol (str): The ticker symbol of the company for which to retrieve the SEC filings.
        as_pandas (bool, optional): A flag indicating whether to return the SEC filings as a pandas DataFrame.
                                    If set to False, the data will be returned as a JSON object. Defaults to True.
        type_ (Optional[str], optional): The type of SEC filing to retrieve. If not specified, all types of filings
                                         are retrieved.
        page (Optional[Union[int, str]], optional): The page of the API results to retrieve. This parameter can be
                                                    used for pagination.
        limit (Optional[Union[int, str]], optional): The maximum number of SEC filing records to retrieve.
        *args: Variable length argument list that will be passed to the `process_dataframe` function when
               'as_pandas' is True. These arguments can be used to further customize the DataFrame processing.
        **kwargs: Arbitrary keyword arguments that will be passed to the `process_dataframe` function when
                  'as_pandas' is True. These arguments can be used to further customize the DataFrame processing.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[DataFrame, Any]: The SEC filings data. If 'as_pandas' is True, this will be a pandas DataFrame.
                               If 'as_pandas' is False, this will be a JSON object.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_sec_filings('AAPL', type_='10-K', page=1, limit=10, as_pandas=True)
    """
    url = f'{base_url_v3}sec_filings/{symbol}?apikey={api_key}'
    url = url + f'&page={page}' if page is not None else url
    url = url + f'&type={type_}' if type_ is not None else url
    url = url + f'&limit={limit}' if limit is not None else url

    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()

    if as_pandas:
        index_ = kwargs.pop('index_', 'filing_date')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


@check_arguments
def get_company_notes(symbol: str, as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    """
    Retrieves company notes data for a specific company from the Financial Modeling Prep API.

    Company notes provide specific remarks or observations about a company, which can provide valuable
    insights into a company's operations, strategies, and financial condition.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        symbol (str): The ticker symbol of the company for which to retrieve the company notes.
                      This is a unique series of letters representing a particular company's stock.
        as_pandas (bool, optional): A flag indicating whether to return the company notes data as a pandas DataFrame.
                                    If set to False, the data will be returned as a JSON object. Defaults to True.
        *args: Variable length argument list that will be passed to the `process_dataframe` function when
               'as_pandas' is True. These arguments can be used to further customize the DataFrame processing.
        **kwargs: Arbitrary keyword arguments that will be passed to the `process_dataframe` function when
                  'as_pandas' is True. These arguments can be used to further customize the DataFrame processing.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[DataFrame, Any]: The company notes data. If 'as_pandas' is True, this will be a pandas DataFrame.
                               If 'as_pandas' is False, this will be a JSON object.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_company_notes('AAPL', as_pandas=True)
    """
    url = f'{base_url_v4}company-notes?symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


@check_arguments
def get_sales_and_revenue_by_segments(symbol: str, period: str = 'quarter', structure: str = 'flat',
                                      as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    """
    Retrieves the sales and revenue data by segments for a specific company from the Financial Modeling Prep API.

    The segmentation provides an insight into the revenue streams of a company. It gives a detailed report
    of revenue generated by each segment within a specific period of time.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        symbol (str): The ticker symbol of the company for which to retrieve the sales and revenue data.
                      This is a unique series of letters representing a particular company's stock.
        period (str, optional): The financial period for which to retrieve the sales and revenue data.
                                This can be either 'quarter' for quarterly data or 'annual' for yearly data.
                                Defaults to 'quarter'.
        structure (str, optional): The structure of the data returned by the API. This can be either 'flat' for a flat
                                   structure, or any other value for a nested structure. Defaults to 'flat'.
        as_pandas (bool, optional): A flag indicating whether to return the data as a pandas DataFrame.
                                    If set to False, the data will be returned as a JSON object. Defaults to True.
        *args: Variable length argument list that will be passed to the `process_dataframe` function when
               'as_pandas' is True. These arguments can be used to further customize the DataFrame processing.
        **kwargs: Arbitrary keyword arguments that will be passed to the `process_dataframe` function when
                  'as_pandas' is True. These arguments can be used to further customize the DataFrame processing.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[DataFrame, Any]: The sales and revenue data by segments. If 'as_pandas' is True, this will be
                               a pandas DataFrame. If 'as_pandas' is False, this will be a JSON object.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_sales_and_revenue_by_segments('AAPL', period='annual', structure='flat', as_pandas=True)
    """
    url = f"{base_url_v4}revenue-product-segmentation?symbol={symbol}&period={period}&structure={structure}&{url_api}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        data = flatten_data(json_data)
        if structure != 'flat':
            print("When structure is not set to flat it is recommended to set as_pandas to False")
        return process_dataframe(data, *args, **kwargs)
    return json_data


@check_arguments
def get_revenue_geographic_by_segments(symbol: str, period: str = 'quarter', structure: str = 'flat',
                                       as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    """
    Retrieves the geographic revenue data by segments for a specific company from the Financial Modeling Prep API.

    Geographic segmentation provides insight into a company's revenue streams from various geographic locations. This
    function gives a detailed report of revenue generated by each geographic segment within a specific period of time.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        symbol (str): The ticker symbol of the company for which to retrieve the geographic revenue data.
                      This is a unique series of letters representing a particular company's stock.
        period (str, optional): The financial period for which to retrieve the geographic revenue data.
                                This can be either 'quarter' for quarterly data or 'annual' for yearly data.
                                Defaults to 'quarter'.
        structure (str, optional): The structure of the data returned by the API. This can be either 'flat' for a flat
                                   structure, or any other value for a nested structure. Defaults to 'flat'.
        as_pandas (bool, optional): A flag indicating whether to return the data as a pandas DataFrame.
                                    If set to False, the data will be returned as a JSON object. Defaults to True.
        *args: Variable length argument list that will be passed to the `process_dataframe` function when
               'as_pandas' is True. These arguments can be used to further customize the DataFrame processing.
        **kwargs: Arbitrary keyword arguments that will be passed to the `process_dataframe` function when
                  'as_pandas' is True. These arguments can be used to further customize the DataFrame processing.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[DataFrame, Any]: The geographic revenue data by segments. If 'as_pandas' is True, this will be
                               a pandas DataFrame. If 'as_pandas' is False, this will be a JSON object.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_revenue_geographic_by_segments('AAPL', period='annual', structure='flat', as_pandas=True)
    """
    local_base = 'revenue-geographic-segmentation'
    url = f'{base_url_v4}{local_base}?symbol={symbol}&structure={structure}&period={period}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        data = flatten_data(json_data)
        if structure != 'flat':
            print("When structure is not set to flat it is recommended to set as_pandas to False")
        return process_dataframe(data, *args, **kwargs)
    return json_data


@check_arguments
def get_financial_reports_dates(symbol: str, as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    """
    Retrieves the dates of financial reports for a specific company from the Financial Modeling Prep API.

    This function provides the dates when financial reports of a company are published. These reports are critical
    for analysts and investors to understand the financial health and performance of the company.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        symbol (str): The ticker symbol of the company for which to retrieve the financial reports dates.
                      This is a unique series of letters representing a particular company's stock.
        as_pandas (bool, optional): A flag indicating whether to return the data as a pandas DataFrame.
                                    If set to False, the data will be returned as a JSON object. Defaults to True.
        *args: Variable length argument list that will be passed to the `process_dataframe` function when
               'as_pandas' is True. These arguments can be used to further customize the DataFrame processing.
        **kwargs: Arbitrary keyword arguments that will be passed to the `process_dataframe` function when
                  'as_pandas' is True. These arguments can be used to further customize the DataFrame processing.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[DataFrame, Any]: The dates of financial reports. If 'as_pandas' is True, this will be a pandas DataFrame.
                               If 'as_pandas' is False, this will be a JSON object.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_financial_reports_dates('AAPL', as_pandas=True)
    """
    url = f'{base_url_v4}financial-reports-dates?symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


@check_arguments
def get_sec_rss_feed(page: Union[int, str] = 0, limit: Union[str, int] = 50,
                     type_: Optional[str] = None, from_: Optional[str] = None,
                     to_: Optional[str] = None, is_done: Optional[str] = None,
                     as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    """
    Retrieves the RSS feed data from the Securities and Exchange Commission (SEC) API.

    This function provides access to the latest company filings submitted to the SEC. The data can be used to track
    updates about a company's financial situation, including its quarterly and annual reports (10-Q and 10-K),
    insider trading activities (Forms 3, 4, and 5), and other relevant documents.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        page (Union[int, str], optional): The page number to retrieve from the RSS feed. Defaults to 0.
        limit (Union[str, int], optional): The maximum number of items to return from the RSS feed. Defaults to 50.
        type_ (Optional[str], optional): The type of SEC filing to retrieve. If None, all filing types are retrieved.
        from_ (Optional[str], optional): The start date for the RSS feed data, formatted as 'yyyy-mm-dd'. If None, all
                                         dates are retrieved.
        to_ (Optional[str], optional): The end date for the RSS feed data, formatted as 'yyyy-mm-dd'. If None, all
                                       dates are retrieved.
        is_done (Optional[str], optional): Whether the filing has been processed. This can be 'true' or 'false'. If None,
                                           all filings are retrieved.
        as_pandas (bool, optional): A flag indicating whether to return the data as a pandas DataFrame.
                                    If set to False, the data will be returned as a JSON object. Defaults to True.
        *args: Variable length argument list that will be passed to the `process_dataframe` function when
               'as_pandas' is True. These arguments can be used to further customize the DataFrame processing.
        **kwargs: Arbitrary keyword arguments that will be passed to the `process_dataframe` function when
                  'as_pandas' is True. These arguments can be used to further customize the DataFrame processing.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[DataFrame, Any]: The RSS feed data from the SEC. If 'as_pandas' is True, this will be a pandas DataFrame.
                               If 'as_pandas' is False, this will be a JSON object.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_sec_rss_feed(page=1, limit=10, as_pandas=True)
    """
    url = f"{base_url_v3}rss_feed?page={page}&limit={limit}"
    url = url + f"&type={type_}" if type_ is not None else url
    url = url + f"&from={from_}" if from_ is not None else url
    url = url + f"&to={to_}" if to_ is not None else url
    url = url + f"&isDone={is_done}" if is_done is not None else url
    url += f"&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


@check_arguments
def get_reports_on_form_10k(symbol: str, year: Union[int, str] = 2023, quarter_period: str = 'FY') -> Any:
    """
    Retrieves financial report data for a specific company from the Form 10-K filings.

    Form 10-K is a comprehensive report that public companies in the U.S. are required to file annually with the 
    Securities and Exchange Commission (SEC). It contains detailed information about a company's operational and 
    financial condition, including audited financial statements, a discussion of the company's financial results, 
    a description of the company's business, and other relevant details.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        symbol (str): The ticker symbol of the company for which the Form 10-K data will be retrieved.
        year (Union[int, str], optional): The year of the Form 10-K to retrieve. Defaults to 2023.
        quarter_period (str, optional): The financial period to retrieve. 'FY' represents a full year. Defaults to 'FY'.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Any: A JSON object containing the Form 10-K data for the specified company, year, and period.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_reports_on_form_10k('AAPL', 2023, 'FY')
    """
    url = f"{base_url_v4}financial-reports-json?symbol={symbol}&year={year}&period={quarter_period}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    return response.json()


@check_arguments
def get_rss_feed_8k_forms(page: Union[int, str] = 0, from_: Optional[str] = None,
                          to_: Optional[str] = None, has_financial: Optional[str] = None,
                          as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    """
    Retrieves RSS feed data for Form 8-K filings.

    Form 8-K is a report required to be filed by public companies in the U.S. to provide current information
    about significant events that shareholders should know about. The form includes a wide range of events,
    from a change in directors or executives to a bankruptcy filing.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        page (Union[int, str], optional): The page number for pagination. Defaults to 0.
        from_ (Optional[str], optional): The start date for the data retrieval in YYYY-MM-DD format.
                                          Defaults to None.
        to_ (Optional[str], optional): The end date for the data retrieval in YYYY-MM-DD format.
                                        Defaults to None.
        has_financial (Optional[str], optional): Indicates whether the form has financial data. Defaults to None.
        as_pandas (bool, optional): Determines whether the returned data is in a Pandas DataFrame format or in JSON.
                                     Defaults to True.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[DataFrame, Any]: A DataFrame (if as_pandas=True) or JSON object (if as_pandas=False) containing the
                               Form 8-K data.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_rss_feed_8k_forms(page=1, from_='2023-01-01', to_='2023-12-31', has_financial='True')
    """
    url = f"{base_url_v4}rss_feed_8k?page={page}&apikey={api_key}"
    url = url + f"&from={from_}" if from_ is not None else url
    url = url + f"&to={to_}" if to_ is not None else url
    url = url + f"&hasFinancial={has_financial}" if has_financial is not None else url
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data
