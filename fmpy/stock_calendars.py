# Helper functions and API Key for the user
from .utils import *
import requests
from pandas import DataFrame
from typing import List, Union, Any, IO, Optional
from datetime import datetime, date

url_api = f"apikey={api_key}"

__author__ = 'Lukas Schröder'
__date__ = '2023-05-22'
__version__ = '0.1.0'

__doc__ = """
This module is related to the stock calendars section of the financial modeling prep API endpoint and 
provides section specific python functions.
"""

__all__ = ['get_earnings_calendar',
           'get_ipo_calendar',
           'get_historical_dividends',
           'get_dividend_calendar',
           'get_economic_calendar',
           'get_stock_split_calendar',
           'get_earnings_calendar_confirmed',
           'get_historical_earning_calendar',
           'get_ipo_calendar_confirmed',
           'get_ipo_calendar_with_prospectus',
           ]

def get_earnings_calendar(as_pandas: bool = True,
                          from_: Optional[Union[str, datetime, date]]=None,
                          to_=None, *args, **kwargs) -> Union[DataFrame, Any]:
    """
    Fetches the earnings calendar from the Financial Modeling Prep API.

    An earnings calendar is a schedule of earnings release dates for publicly traded companies.
    It shows when companies will release their quarterly or annual earnings reports, which can significantly
    impact their stock prices.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        as_pandas (bool, optional): A flag indicating whether to return the earnings calendar as a pandas DataFrame.
                                    If set to False, the data will be returned as a JSON object. Defaults to True.
        from_ (Optional[Union[str, datetime]], optional): The start date for the earnings calendar.
                                                          This can either be a string in the format 'YYYY-MM-DD'
                                                          or a datetime object. If not provided, the earnings calendar
                                                          will start from the current date.
        to_ (Optional[Union[str, datetime]], optional): The end date for the earnings calendar.
                                                        This can either be a string in the format 'YYYY-MM-DD'
                                                        or a datetime object. If not provided, the earnings calendar
                                                        will end at the current date.
        *args: Variable length argument list that will be passed to the `process_dataframe` function when
               'as_pandas' is True. These arguments can be used to further customize the DataFrame processing.
        **kwargs: Arbitrary keyword arguments that will be passed to the `process_dataframe` function when
                  'as_pandas' is True. These arguments can be used to further customize the DataFrame processing.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[DataFrame, Any]: The earnings calendar data. If 'as_pandas' is True, this will be a pandas DataFrame.
                               If 'as_pandas' is False, this will be a JSON object.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_earnings_calendar(as_pandas=True, from_='2023-01-01', to_='2023-12-31')
    """
    url = f"{base_url_v3}earning_calendar?apikey={api_key}"
    url = url + f"&from={from_}" if from_ is not None else url
    url = url + f"&to={to_}" if to_ is not None else url
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data



def get_historical_earning_calendar(symbol: str,
                                    limit: Union[int, str] = 80,
                                    as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    """
    Retrieves historical earnings calendar data for a specific company, identified by its ticker symbol,
    from the Financial Modeling Prep API.

    The historical earnings calendar shows the dates on which a particular company has released its earnings reports
    in the past, as well as the earnings per share (EPS) reported on each date.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        symbol (str): The ticker symbol of the company for which to retrieve the historical earnings calendar.
                      This is a unique series of letters representing a particular company's stock.
        limit (Union[int, str], optional): The maximum number of historical earnings calendar records to retrieve.
                                           This can either be an integer or the string 'max'. Defaults to 80.
        as_pandas (bool, optional): A flag indicating whether to return the historical earnings calendar data
                                    as a pandas DataFrame. If set to False, the data will be returned as a JSON object.
                                    Defaults to True.
        *args: Variable length argument list that will be passed to the `process_dataframe` function when
               'as_pandas' is True. These arguments can be used to further customize the DataFrame processing.
        **kwargs: Arbitrary keyword arguments that will be passed to the `process_dataframe` function when
                  'as_pandas' is True. These arguments can be used to further customize the DataFrame processing.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[DataFrame, Any]: The historical earnings calendar data. If 'as_pandas' is True, this will be a pandas DataFrame.
                               If 'as_pandas' is False, this will be a JSON object.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_historical_earning_calendar('AAPL', limit=20, as_pandas=True)
    """
    url = f"{base_url_v3}historical/earning_calendar/{symbol}?limit={limit}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        return process_dataframe(json_data, *args, **kwargs)
    return json_data



def get_earnings_calendar_confirmed(as_pandas: bool = True,
                                    from_: Optional[Union[str, datetime, date]] = None,
                                    to_: Optional[Union[str, datetime, date]] = None,
                                    *args, **kwargs) -> Union[DataFrame, Any]:
    """
    Retrieves confirmed earnings calendar data for all companies from the Financial Modeling Prep API.

    The confirmed earnings calendar includes upcoming dates when companies have confirmed they will be releasing
    their earnings reports.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        as_pandas (bool, optional): A flag indicating whether to return the confirmed earnings calendar data
                                    as a pandas DataFrame. If set to False, the data will be returned as a JSON object.
                                    Defaults to True.
        from_ (Union[str, datetime], optional): The start date for the time range from which to retrieve earnings
                                                calendar data. Defaults to None, which means that data will be retrieved
                                                from the earliest available date.
        to_ (Union[str, datetime], optional): The end date for the time range from which to retrieve earnings calendar
                                              data. Defaults to None, which means that data will be retrieved up to
                                              the latest available date.
        *args: Variable length argument list that will be passed to the `process_dataframe` function when
               'as_pandas' is True. These arguments can be used to further customize the DataFrame processing.
        **kwargs: Arbitrary keyword arguments that will be passed to the `process_dataframe` function when
                  'as_pandas' is True. These arguments can be used to further customize the DataFrame processing.

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[DataFrame, Any]: The confirmed earnings calendar data. If 'as_pandas' is True, this will be a pandas
                               DataFrame.
                               If 'as_pandas' is False, this will be a JSON object.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_earnings_calendar_confirmed(as_pandas=True, from_="2023-01-01", to_="2023-12-31")
    """
    url = f"{base_url_v4}earning-calendar-confirmed?apikey={api_key}"
    url = url + f"&from={from_}" if from_ is not None else url
    url = url + f"&to={to_}" if to_ is not None else url
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        return process_dataframe(json_data, *args, **kwargs)
    return json_data



def get_ipo_calendar(as_pandas: bool = True,
                     from_: Optional[Union[str, datetime, date]] = None,
                     to_: Optional[Union[str, datetime, date]] = None,
                     *args, **kwargs) -> Union[DataFrame, Any]:
    """
    Retrieves the initial public offerings (IPO) calendar for a specified date range.

    --------------------------------------------------------------------------------------------------------------------
    Parameters:
        as_pandas (bool, optional): Determines whether the returned data is in a Pandas DataFrame format 
                                     (if as_pandas=True) or in a raw JSON format (if as_pandas=False). 
                                     Defaults to True.
        from_ (Union[str, datetime, date], optional): The start date for the IPO calendar. It can be a string 
                                                      in the format 'YYYY-MM-DD', or a datetime or date object. 
                                                      Defaults to None.
        to_ (Union[str, datetime, date], optional): The end date for the IPO calendar. It can be a string 
                                                    in the format 'YYYY-MM-DD', or a datetime or date object. 
                                                    Defaults to None.
        *args: Additional positional arguments passed to the `process_dataframe` function (only applicable if 
               as_pandas=True).
        **kwargs: Additional keyword arguments passed to the `process_dataframe` function (only applicable if 
                  as_pandas=True).

    --------------------------------------------------------------------------------------------------------------------
    Returns:
        Union[DataFrame, Any]: A DataFrame (if as_pandas=True) or a raw JSON object (if as_pandas=False) 
                               containing the IPO calendar data.

    --------------------------------------------------------------------------------------------------------------------
    Raises:
        APIRequestError: If the API request does not return a 200 status code. The raised exception will contain
                         a message with details about the error.
        TypeError: If any of the provided arguments do not match the expected types. This is enforced by the
                   `check_arguments` decorator, which performs runtime type checking.

    --------------------------------------------------------------------------------------------------------------------
    Example:
        >>> get_ipo_calendar(as_pandas=True, from_='2023-01-01', to_='2023-12-31')
    """
    url = f"{base_url_v3}ipo_calendar?apikey={api_key}"
    url = url + f"&from={from_}" if from_ is not None else url
    url = url + f"&to={to_}" if to_ is not None else url
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data



def get_ipo_calendar_with_prospectus(as_pandas: bool = True,
                                     from_: Optional[Union[str, datetime, date]] = None,
                                     to_: Optional[Union[str, datetime, date]] = None,
                                     *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v4}ipo-calendar-prospectus?apikey={api_key}"
    url = url + f"&from={from_}" if from_ is not None else url
    url = url + f"&to={to_}" if to_ is not None else url
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_ipo_calendar_confirmed(as_pandas: bool = True,
                               from_: Optional[Union[str, datetime, date]] = None,
                               to_: Optional[Union[str, datetime, date]] = None,
                               *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v4}ipo-calendar-confirmed?apikey={api_key}"
    url = url + f"&from={from_}" if from_ is not None else url
    url = url + f"&to={to_}" if to_ is not None else url
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_stock_split_calendar(as_pandas: bool = True,
                             from_: Optional[Union[str, datetime, date]] = None,
                             to_: Optional[Union[str, datetime, date]] = None,
                             *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v3}stock_split_calendar?apikey={api_key}"
    url = url + f"&from={from_}" if from_ is not None else url
    url = url + f"&from={to_}" if to_ is not None else url
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_dividend_calendar(as_pandas: bool = True,
                          from_: Optional[Union[str, datetime, date]] = None,
                          to_: Optional[Union[str, datetime, date]] = None,
                          *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v3}stock_dividend_calendar?apikey={api_key}"
    url = url + f"&from={from_}" if from_ is not None else url
    url = url + f"&from={to_}" if to_ is not None else url
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_historical_dividends(symbol: str, as_pandas: bool = True,
                             *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v3}historical-price-full/stock_dividend/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    data = json_data['historical']
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


def get_economic_calendar(as_pandas: bool = True,
                          from_: Optional[Union[str, datetime, date]] = None,
                          to_: Optional[Union[str, datetime, date]] = None,
                          *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v3}economic_calendar?apikey={api_key}"
    url = url + f"&from={from_}" if from_ is not None else url
    url = url + f"&to={to_}" if to_ is not None else url
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data

