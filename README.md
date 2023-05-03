# Building Chartstrings
```bash
python3.8 -m venv venv
source venv/bin/activate
```

## Setup .env:
```bash
export PLN_URL=https://facilities-***.dartmouth.edu/nyx/services
export PLN_USR=f003v3f
export PLN_PWD=$(pass planon/f003v3f/local)
export LOG_LEVEL="INFO"
```
## Description:
FOM_update_with_client :
    Loops through all building in Planon and pre-pends a semicolon if length of Chartstring == 30
FOM_update_with_CSV :
    Loops through buildings mentioned in CSV file and compares it with Planon. If match is found , then updates the Chart String. This can also be used to reset values in Planon , in case Bulk_upload goes wrong.
    special case properties- properties with 5 segments where len(CS)==25

 ## Adding FreeString45 under Field definer>Properties>Extensions:
chartString=FreeString45
baseURL=https://api.dartmouth.edu
path=/api/general_ledger/accounts/
scopeParam=
segmentsLimit=6
error=Error occurred while calling webservice to validate the chart string
apiKey=****
error.unauthorized=security credentials invalid
error.invalid.accountString=Please give the valid chart string
error.invalid.url=The request URL and/or parameters are improperly formatted
error.server=Server encountered a problem

# Add steps & sequence of event under Extensions:
BI>15 & BU>25 
