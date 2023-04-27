import json
from sec_api import QueryApi

# run in terminal: python3 test-api.py

queryApi = QueryApi(api_key="9b89bcb731e64037b4d25f6e44248e683ba5adb6e88412ad44631277158d7140")

query = {
  "query": { "query_string": {
      "query": "ticker:TSLA AND filedAt:{2020-01-01 TO 2020-12-31} AND formType:\"10-Q\""
    } },
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
}

filings = queryApi.get_filings(query)

with open("filings.json", "w") as json_file:
    json.dump(filings, json_file)

print("Filings saved to filings.json.")