from .utils import *
import requests
from pandas import DataFrame
from typing import Any, Union

__author__ = 'Lukas Schröder'
__date__ = '2023-08-05'
__version__ = '0.1.0'

__doc__ = """
This module is related to the historical number of employees section of the financial modeling prep API endpoint and 
provides section specific python functions.
"""

__all__ = [
    'get_historical_number_of_employees'
]


def get_historical_number_of_employees(symbol: str, as_pandas: bool = True,
                                       *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v4}historical/employee_count?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data
