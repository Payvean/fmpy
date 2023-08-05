# Fmpy

## Overview
Hello, welcome to Fmpy!
Fmpy is a hobby project intended to provide a user-friendly, unofficial Python Software
Development Kit (SDK) for the API endpoints from Financial Modeling Prep (FMP) 
https://site.financialmodelingprep.com/developer/docs/.

Although most of FMP's endpoints are already included and are expected to work,
this project is still in development and at a relatively early stage.
I'm not a professional software developer,
so you may encounter inconsistencies or other unexpected behavior in the current version.
I hope to learn from the community, and I appreciate any advice!

This SDK retrieves processed data as pandas dataframes,
post-processed to provide a well-organized representation of the data.
All functions also allow retrieving the data in JSON format if no pandas output is desired.

**Note**
Financial Modeling Prep requires you to have an account and an API key to use their endpoints.
You can set up a free account on https://site.financialmodelingprep.com/register
to retrieve an API key with limited access.
Some endpoints require a higher plan.
For further information about setting up that key, please refer to their webpage.

## Installation

### Dependencies
To install this project make sure to install the package
requirements that you can find within the `requirements.txt`
file at the projects' root.
You can install the requirements by running
```shell
pip install -r requirements.txt
```
in the terminal.
if you are working with `pip3` you might use
```shell
pip3 install -r requirements.txt
```
instead.

### Set up the API-Key

Within the root directory,
you need to create a config.json file where you set up your personal API key from Financial Modeling Prep.
The file should look like this:
```json
{
  "api_key": "<your api key>"
}
```
After following the steps above, you will be able to use all endpoints provided
by this version with no further preparations.

#### Add an optional output path
You can set up a default output path if you want to save data directly there.
To set your default path, simply add the respective path to the config.json.
```json
{
  "api_key": "<your api key>",
  "output_path": "<your output path>"
}
```
## Usage
The use of the SDK is intended to be straight forward.
Within the root directory you will find an `example` notebook that
showcases how to use this project to access processed data.

### Naming conventions
This project aims
to stick with the same naming conventions and structure as the Financial Modeling Prep 
documentation page for their endpoints.
The idea is to provide a simple way to easily transfer their documentation to the usage of this project.
Within the fmpy package, all listed modules correspond to the headers of FMP's structure.
Each function in the modules refers to a specific endpoint of the header and is prefixed with a 'get_'
to clarify that this function will retrieve the respective endpoint.

## Contribution
I appreciate any interest in the project.
If you are interested in giving specific advice or in gaining access and being part of this development,
feel free to write me an email.
I appreciate any kind of support!
Thank you for your interest in Fmpy!



## Contact
If you want to contact me you can reach me at 
[lukaspythonmail@gmail.com](mailto:lukaspythonmail@gmail.com)

**Thank you and Enjoy!**