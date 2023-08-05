from .utils import *
import requests
import datetime

from pandas import DataFrame, Series
from typing import Union, Any

__author__ = 'Lukas Schröder'
__date__ = '2023-05-29'
__version__ = '0.1.0'

__doc__ = """
This module is related to the economics section of the financial modeling prep API endpoint and 
provides section specific python functions.
"""

__all__ = ['get_market_risk_premium',
           'get_treasury_rates',
           'get_economic_indicator']


def get_market_risk_premium(as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v4}market_risk_premium?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'country')
        return process_dataframe(json_data, index_=index_, *args, **kwargs)
    return json_data


def get_treasury_rates(from_: Union[str, datetime.datetime] = '2008-01-01',
                       to_: Union[str, datetime.datetime] = str(datetime.date.today()),
                       as_pandas: bool = True, *args, **kwargs) -> Union[DataFrame, Any]:
    url = f"{base_url_v4}treasury?from={from_}&to={to_}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data


def get_economic_indicator(name: str, from_: Union[str, datetime.datetime] = '2008-01-01',
                           to_: Union[str, datetime.datetime] = str(datetime.date.today()),
                           as_pandas: bool = True, *args, **kwargs) -> Union[Series, Any]:
    """
    All economic indicators are:
    GDP | realGDP | nominalPotentialGDP | realGDPPerCapita |
    | federalFunds | CPI | inflationRate | inflation |
    | retailSales | consumerSentiment | durableGoods | unemploymentRate |
    | totalNonfarmPayroll | initialClaims | industrialProductionTotalIndex |
    | newPrivatelyOwnedHousingUnitsStartedTotalUnits | totalVehicleSales |
    | retailMoneyFunds | smoothedUSRecessionProbabilities |
    | 3MonthOr90DayRatesAndYieldsCertificatesOfDeposit |
    commercialBankInterestRateOnCreditCardPlansAllAccounts |
    30YearFixedRateMortgageAverage |
    15YearFixedRateMortgageAverage
    Historical GDP data for specified period of time
    """
    url = f"{base_url_v4}economic?name={name}&from={from_}&to={to_}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        df = process_dataframe(json_data, *args, **kwargs)
        return Series(df.value.values, index=df.index, name=name)
    return json_data
