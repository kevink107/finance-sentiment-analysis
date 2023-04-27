import json
from sec_api import QueryApi
from sec_api.index import ExtractorApi 

# run in terminal: python3 test-api.py

# Get .htm file for TSLA
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


extractorApi = ExtractorApi("9b89bcb731e64037b4d25f6e44248e683ba5adb6e88412ad44631277158d7140")

filing_url = "https://www.sec.gov/Archives/edgar/data/1318605/000156459021004599/tsla-10k_20201231.htm"

section_text = extractorApi.get_section(filing_url, "1A", "text")
section_html = extractorApi.get_section(filing_url, "1A", "html")

print(section_text)
print(section_html)
