from .utils import *

import requests
import pandas as pd
from typing import Union, Optional


exchanges = ['ETF', 
             'MUTUAL_FUND',
             'COMMODITY', 
             'INDEX', 
             'CRYPTO', 
             'FOREX', 
             'TSX', 
             'AMEX', 
             'NASDAQ',
             'NYSE',
             'EURONEXT',
             'XETRA',
             'NSE',
             'LSE']

@check_arguments
def get_company_search(query: str, exchange: str = 'ALL',
                       limit: Union[int, str] = 10, as_pandas=True,
                       options: Optional[dict] = None, *args, **kwargs):
    dataframes = []
    dictionaries = {}
    if exchange == 'ALL':
        for exchange_ in exchanges:
            if as_pandas:
                df = get_company_search_(query, exchange_, limit, as_pandas, options, *args, **kwargs)
                dataframes.append(df)
            else:
                data = get_company_search_(query, exchange_, limit, as_pandas, options, *args, **kwargs)
                dictionaries.update(data)
        return pd.concat(dataframes, axis=0)
    return get_company_search_(query, exchange, limit, as_pandas, options, *args, **kwargs)

@check_arguments
def get_company_search_(query: str, exchange: str,
                       limit: Union[int, str] = 10, as_pandas=True,
                       options: Optional[dict] = None, *args, **kwargs):
    """
    Search via ticker or company name.
    Values for exchange parameter are: | ALL | ETF | MUTUAL_FUND | COMMODITY
    | INDEX | CRYPTO | FOREX | TSX | AMEX | NASDAQ | NYSE | 
    EURONEXT | XETRA | NSE | LSE
    """
    if options is None:
        options = {'ticker': True, 'name': True}
    if not options['ticker'] and not options['name']:
        raise AssertionError("At least ticker or name must be True within options parameter")
    if options['ticker'] and options['name']:
        local_base = 'search'
    elif not options['ticker'] and options['name']:
        local_base = 'search-name'
    else:
        local_base = 'search-ticker'
    url = f"{base_url_v3}{local_base}?query={query}&limit={limit}&exchange={exchange}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    if as_pandas:
        index_ = kwargs.pop('index_', 'symbol')
        df: DataFrame =  process_dataframe(json_data, index_, *args, **kwargs)
        if df.empty:
            print(f"Couldn't find any match in exchange: {exchange} for query {query}")
        return df
    return json_data


def stock_screener():
    """
    Stock screener is a more advanced way to search for stocks. 
    Unlike our search endpoint, there is no query parameter, but there are numerous parameters 
    such as market cap, price, volume, beta, sector, country, and so on. 
    For example, you can use this endpoint to find NASDAQ-listed software companies that 
    pay dividends and have good liquidity.

    Params
    --------------------

    market_cap_more_than: 
    market_cap_lower_than
    price_more_than
    price_lower_than
    beta_more_than
    beta_lower_than
    volume_more_than
    volume_lower_than
    dividend_more_than
    dividend_lower_than
    is_etf
    is_actively_trading
    sector
    industry
    country
    exchange
    limit
    """
    pass


def get_list_of_countries():
    url = f"{base_url_v3}get-all-countries?apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code, "Failed to fetch country list")
    return response.json()


