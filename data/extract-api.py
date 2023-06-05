'''
Authors:
- Arijeet Grewal (arijeet.s.grewal.23@dartmouth.edu)
- Kevin King (kevin.m.king.24@dartmouth.edu)
- Seamus O'Connell (seamus.c.o'connell.23@dartmouth.edu)

For the Dartmouth College course COSC72 Final Project

Description:
- This program extracts the risk factors and MD&A sections from the 10-K and 10-Q filings of the companies in the S&P 500.
'''

import json
from sec_api import QueryApi
from sec_api.index import ExtractorApi 

# To run the program in terminal: python3 test-api.py

# API Keys
queryApi = QueryApi(api_key="5ab252d05f9a151b9b4749a085c9780fb74380b8d048d8b5ccfa38e8df652808")
extractorApi = ExtractorApi("5ab252d05f9a151b9b4749a085c9780fb74380b8d048d8b5ccfa38e8df652808")


with open("companies_2020.json", "r") as companies_json_file: 
  data = json.load(companies_json_file)

companies = data["Companies"]
forms = data["Forms"]

for i in range(0, len(companies)):
  for j in range(0, len(forms)):
    # companyName = companies[i]["companyName"]
    ticker = companies[i]["ticker"]
    formType = forms[j]["formType"]
    formDates = forms[j]["dates"]

    quarter = 1
    for k in range(0, len(formDates)):
      filedAt = formDates[k]["filedAt"]
      year = formDates[k]["year"]

      # print(companyName + ": " + year + " " + " " + formType)

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

      file_path = "filings/2020/" + ticker + "_filings_" + formType + "_" + year + ".json"
      with open(file_path, "w") as filings_json_file:
        json.dump(filings_query, filings_json_file)

      print(str(ticker) + ": Filings saved to filings.json.")

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

      risk_file_path = ""
      mda_file_path = ""

      # Extract relevant sections in the filing
      if (formType == "10-K"): 
        risk_factors_section = extractorApi.get_section(filing_url, "1A", "text")
        risk_file_path = "risks_2020/" + ticker + "_risks_" + year
        mda_section = extractorApi.get_section(filing_url, "7", "text")
        mda_file_path = "mda_2020/" + ticker + "_mda_" + year
      
      # elif (formType == "10-Q"): 
      #   risk_factors_section = extractorApi.get_section(filing_url, "part2item1a", "text")
      #   risk_file_path = "risks/" + ticker + "_risks+" + year + "_q" + str(quarter)
      #   mda_section = extractorApi.get_section(filing_url, "part1item2", "text")
      #   mda_file_path = "mda/" + ticker + "_mda+" + year + "_q" + str(quarter)
      #   quarter += 1

      # Write new text files for the relevant sections
      with open(risk_file_path, "w", encoding="utf-8") as f:
        f.write(risk_factors_section)

      with open(mda_file_path, "w", encoding="utf-8") as f:
        f.write(mda_section)

      print("\n")
