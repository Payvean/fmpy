from .utils import *

warnings.warn("This module is currently not implemented at all")

__author__ = 'Lukas Schröder'
__date__ = '2023-08-05'
__version__ = '0.1.0'

__doc__ = """
This module is related to the institutional stock ownership section of the financial modeling prep API endpoint and 
provides section specific python functions.
"""

__all__ = [
    'get_institutional_stock_ownership',
    'get_institutional_ownership_by_holder',
    'get_institutional_holdings_portfolio_positions_summary',
    'get_institutional_holder_rss_feed',
    'get_institutional_holders_list',
]

@not_implemented
def get_institutional_stock_ownership(symbol):
    pass

@not_implemented
def get_institutional_ownership_by_holder(symbol):
    pass

@not_implemented
def get_institutional_holdings_portfolio_positions_summary(symbol):
    pass

@not_implemented
def get_institutional_holder_rss_feed(symbol):
    pass

@not_implemented
def get_institutional_holders_list():
    pass

@not_implemented
def search_institutional_holders(name):
    pass
