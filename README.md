# Fmpy 


## Overview
This project provides a software development kit (SDK) 
for the API endpoints from Financial Modeling Prep.
All endpoints listed on the financial modeling preps' 
documentation page are included 
https://site.financialmodelingprep.com/developer/docs/ .
This SDK allows to retrieve processed data in kind of
pandas dataframes and also allows to return the raw json
data.


## Installation

### Dependencies
To install this project make sure to install the package
requirements you can find within the `requirements.txt`
file at the projects' root.
You can install the requirements by running
```shell
pip install -r requirements.txt
```
if you are working with `pip3` you might use
```shell
pip3 install -r requirements.txt
```
instead.

### Set-Up API-Key

within the root directory you are required to create a 
`config.json` file where you set up your personal 
API-key of Financial Modeling Prep.
The file should look like this:
```json
{
  "api_key": "<your api key>"
}
```
After following the steps above you will be able to use 
all endpoints provided by this version with no further
preparations. **Enjoy!**