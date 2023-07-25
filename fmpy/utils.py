import json
import os
import pandas as pd
from pandas import DataFrame

with open("../config.json") as config:
    data = json.load(config)

api_key = data['api_key']

base_url_v3 = "https://financialmodelingprep.com/api/v3/"
base_url_v4 = "https://financialmodelingprep.com/api/v4/"
output_path = None


class APIRequestError(Exception):

    def __init__(self, status_code):
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self):
        return f"APIRequestError: [Status Code: {self.status_code}] {self.message}"

    @property
    def message(self):
        if self.status_code == 401:
            return 'Invalid API KEY. Please retry or visit our documentation to create one ' \
                   'FREE https://site.financialmodelingprep.com/developer/docs'
        elif self.status_code == 403:
            return 'This endpoint is only for users with Professional or Enterprise plan ' \
                   'please visit our subscription page to upgrade your plan' \
                   ' at https://financialmodelingprep.com/developer/docs/pricing'
        else:
            return 'Unable to fetch the request'


def check_arguments(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def to_snake_case_ttm(column_name):
    result = []
    i = 0
    while i < len(column_name):
        char = column_name[i]
        if char == 'T' and column_name[i:i + 3] == 'TTM':
            result.append('_ttm')
            i += 3
        else:
            if char.isupper():
                result.append('_')
            result.append(char.lower())
            i += 1
    return ''.join(result)


def to_snake_case(column_name):
    result = []
    i = 0
    while i < len(column_name):
        char = column_name[i]
        if char.isupper():
            # Check if there are two or more consecutive uppercase characters
            j = i + 1
            while j < len(column_name) and column_name[j].isupper():
                j += 1
            if j - i > 1:
                result.append('_')
                result.append(column_name[i:j - 1].lower())  # Exclude the last uppercase character
                i = j - 1  # Set i to the index of the last uppercase character
            else:
                if i > 0:  # Add an underscore if it's not the first character
                    result.append('_')
                result.append(char.lower())
                i += 1
        else:
            result.append(char)
            i += 1
    return ''.join(result)


def convert_columns_to_snake_case(df, is_ttm=False):
    if is_ttm:
        df.columns = [to_snake_case_ttm(col) for col in df.columns]
        return df
    df.columns = [to_snake_case(col) for col in df.columns]
    return df


def remove_timestamp_from_date_cols(df: pd.DataFrame, date_cols: list, as_string: bool = True):
    """
    Parameters
    ----------
    df: Ledger Table as pandas DataFrame
    date_cols: (list) of the date column names
    as_string: (bool) is used to convert datetime objects to string
    """
    # Convert all rows of a date column to datetime objects without a timestamp
    df = df.assign(**{col: pd.to_datetime(df[col]).dt.date for col in date_cols})

    # Convert adjusted date columns to string type
    if as_string:
        df[date_cols] = df[date_cols].applymap(lambda x: str(x))
    return df


def convert_dict_keys_to_snake_case(d: dict) -> dict:
    return {to_snake_case(key): value for key, value in d.items()}


def count_string_chars(string, char=','):
    num = 0
    for x in string:
        if x == char:
            num += 1
    return num


def flatten_data(data):
    return [{'date': date, **values} for d in data for date, values in d.items()]


def reverse_date_order(df):
    # Check if the DataFrame is currently sorted in ascending order
    if df.index.is_monotonic_increasing:
        # If it's in ascending order, sort it in descending order
        df_sorted = df.sort_index(ascending=False)
    else:
        # If it's not in ascending order, sort it in ascending order
        df_sorted = df.sort_index(ascending=True)

    return df_sorted


def process_dataframe(data, index_=None, ignore_=None, transpose_: bool = False,
                      save_=False, datatype_='csv', output_path_=None, filename_=None,
                      format_=None, to_datetime: bool = True, reversed_: bool = False):
    if output_path_ is None:
        output_path_ = output_path
    df = DataFrame(data)
    df = convert_columns_to_snake_case(df)
    if 'filling_date' in df.columns:
        df.rename(columns={'filling_date': 'filing_date'}, inplace=True)
    if index_ is not None:
        if df.empty:
            return df
        if index_ not in df.columns:
            raise AttributeError(f"Couldn't find {index_} in data columns")
        df.set_index(index_, inplace=True)
        if to_datetime and 'date' in index_:
            df.index = pd.to_datetime(df.index)
    else:
        if 'date' in df.columns:
            df.set_index('date', inplace=True)
            df.index = pd.to_datetime(df.index) if to_datetime else df.index
        else:
            for col in df.columns:
                if 'date' in col:
                    df.set_index(col, inplace=True)
                    df.index = pd.to_datetime(df.index) if to_datetime else df.index

    if ignore_ is not None:
        df.drop(ignore_, axis=1, inplace=True)
    if transpose_:
        df = df.T
    if format_ is not None:
        df = format_number(df, format_)
    if reversed_:
        df = reverse_date_order(df)
    if save_:
        _save_frame(df, datatype_, output_path_, filename_)
    return df


def _save_frame(df: DataFrame, datatype, output_path_, filename_):
    output_path_ = os.path.join(output_path_, filename_ + '.' + datatype)
    if datatype == 'csv':
        df.to_csv(output_path_, index=False)
        print("Saved table as 'csv' to {}".format(output_path_))

    elif datatype == 'xlsx':
        df.to_excel(output_path_, index=False, engine='openpyxl')
        print("Saved table as 'xlsx' to {}".format(output_path_))

    elif datatype == 'html':
        df.to_html(output_path_, index=False)
        print("Saved table as 'html' to {}".format(output_path_))
    else:
        raise TypeError(f"Invalid datatype {datatype}. Valid types are 'csv', 'xlsx', 'html'")


def format_number(df, format_='mil'):
    for index in df.index:
        for col in df.columns:
            val = df.at[index, col]
            if isinstance(val, (int, float)):
                if format_ == 'M' or 'mil':
                    df.at[index, col] = f'{val / 1e6:.1f}'
                elif format_ == 'B' or 'bil':
                    df.at[index, col] = f'{val / 1e9:.1e}'
                if df.at[index, col].endswith('0'):
                    df.at[index, col] = int(float(df.at[index, col]))
                else:
                    df.at[index, col] = float(df.at[index, col])
    return df
