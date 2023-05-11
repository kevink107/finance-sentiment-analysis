import json
from sec_api import QueryApi
from sec_api.index import ExtractorApi 

# To run the program in terminal: python3 test-api.py

# API Keys
queryApi = QueryApi(api_key="d9154fab9f6819c42f9bb716dc24983cd9ca3bb322239596629b7dc05ca4ce78")
extractorApi = ExtractorApi("d9154fab9f6819c42f9bb716dc24983cd9ca3bb322239596629b7dc05ca4ce78")

query = {
        "query": { "query_string": {
            "query": "ticker: TSLA AND filedAt: {2022-01-01 TO 2022-06-01} AND formType:\"10-Q\""
          } },
        "from": "0",
        "size": "10",
        "sort"
        : [{ "filedAt": { "order": "desc" } }]
      }

filings_query = queryApi.get_filings(query)

file_path = "filings/TSLA_filings_10Q.json"

with open(file_path, "w") as filings_json_file:
    json.dump(filings_query, filings_json_file)

# Read filing JSON 
with open(file_path, "r") as filings_json_file:
    query_data = json.load(filings_json_file)

filing_url = ""

for l in range(0, len(query_data["filings"])):
    link = query_data["filings"][l]["formType"]
    if (link == "10-Q"): 
        filing_url = query_data["filings"][l]["linkToFilingDetails"]

print("Viewing URL: " + filing_url)

# Extract relevant sections in the filing
risk_factors_section = extractorApi.get_section(filing_url, "part2item1a", "text")
mda_section = extractorApi.get_section(filing_url, "part1item2", "text")

# Write new text files for the relevant sections
with open("risks/TSLA_risks_10Q_1", "w", encoding="utf-8") as f:
    f.write(risk_factors_section)

with open("mda/TSLA_mda_10Q_1", "w", encoding="utf-8") as f:
    f.write(mda_section)