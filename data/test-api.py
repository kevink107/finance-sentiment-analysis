import json
from sec_api import QueryApi
from sec_api.index import ExtractorApi 

# To run the program in terminal: python3 test-api.py

# API Keys
queryApi = QueryApi(api_key="d9154fab9f6819c42f9bb716dc24983cd9ca3bb322239596629b7dc05ca4ce78")
extractorApi = ExtractorApi("d9154fab9f6819c42f9bb716dc24983cd9ca3bb322239596629b7dc05ca4ce78")

tickers = ["TSLA"]

with open("companies.json", "r") as companies_json_file: 
  data = json.load(companies_json_file)

companies = data["Companies"]
forms = data["Forms"]

for i in range(0, len(companies)):
  for j in range(0, len(forms)):
    companyName = companies[i]["companyName"]
    ticker = companies[i]["ticker"]
    formType = forms[j]["formType"]
    formDates = forms[j]["dates"]

    for k in range(0, len(formDates)):
      filedAt = formDates[k]["filedAt"]
      year = formDates[k]["year"]
      
      print(companyName + ": " + year + " " + " " + formType)

      query = {
        "query": { "query_string": {
            "query": "ticker:" + ticker + " AND filedAt:" + filedAt + " AND formType:\"" + formType + "\""
          } },
        "from": "0",
        "size": "10",
        "sort"
        : [{ "filedAt": { "order": "desc" } }]
      }

      filings_query = queryApi.get_filings(query)

      # Save SEC filing
      file_path = "filings/" + ticker + "_filings_" + year + ".json"
      with open(file_path, "w") as filings_json_file:
        json.dump(filings_query, filings_json_file)

      print("Filings saved to filings.json.")

      # Read filing JSON 
      with open(file_path, "r") as filings_json_file:
        query_data = json.load(filings_json_file)
          
      # Get the necessary URL for the filing
      filing_url = ""
      for l in range(0, len(query_data["filings"])):
        link = query_data["filings"][l]["formType"]
        if (link == formType): 
          filing_url = query_data["filings"][l]["linkToFilingDetails"]

      print("Viewing URL: " + filing_url)

      # Extract relevant sections in the filing
      risk_factors_section = extractorApi.get_section(filing_url, "1A", "text")
      mda_section = extractorApi.get_section(filing_url, "7", "text")

      # Write new text files for the relevant sections
      with open("risks/" + ticker + "_risks_" + year, "w", encoding="utf-8") as f:
        f.write(risk_factors_section)

      with open("mda/" + ticker + "_mda_" + year, "w", encoding="utf-8") as f:
        f.write(mda_section)
    
      print("\n")
