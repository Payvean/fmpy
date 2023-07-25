from .utils import *
import requests


@check_arguments
def get_historical_number_of_employees(symbol: str, as_pandas: bool = True,
                                       *args, **kwargs):
    url = f"{base_url_v4}historical/employee_count?symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise APIRequestError(response.status_code)
    json_data = response.json()
    return process_dataframe(json_data, *args, **kwargs) if as_pandas else json_data
