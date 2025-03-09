from fastapi import FastAPI, Depends, HTTPException
from external_api_routes.patent_routes import *
from external_api_routes.gemeni_routes import *
import pandas as pd
import numpy as np
from datetime import datetime
from database import *
from state_abbreviations import st_abr_dic

# Initialize FastAPI
app = FastAPI()
app.db = DataBase()

@app.get("/search_patents")
def store_patents(search_all: str = "", filing_start_date: str = "", filing_end_date: str = "", grant_date: str = "",
                  patent_number: str = "", inventor_name: str = "", invention_title: str = "", applicant_name: str = "", city: str = "", state: str = ""):
    """This is the primary function which downloads the patent data from the US Patent Office API. The API has a limit of only 100 records at a time 
    so it requires paginating and calling the API multiple times. All of the records are then stored in the Database object for easy retrieval for subsequent functions."""
    search_results = dict()
    # construct the query term necessary to pass into the JSON based on whether fields are filled out or now
    q= ''
    # the following if statements are used to construct and pass the appropriate message to the JSON construction helper method in the external_api_routes module. 
    if search_all:
        if not q == '':
            q = q + ' AND "' + search_all + '"'
        else:
            q = '"' + search_all + '"'

    if patent_number:
        if not q == '':
            q = q + ' AND ' + 'applicationMetaData.patentNumber:"' + patent_number + '"'
        else:
            q = 'applicationMetaData.patentNumber:"' + patent_number + '"'
    
    if applicant_name:
        if not q == '':
            q = q + ' AND ' + 'applicationMetaData.firstApplicantName:"' + applicant_name + '"'
        else:
            q = 'applicationMetaData.firstApplicantName:"' + applicant_name + '"'
    
    if inventor_name:
        if not q == '':
            q = q + ' AND ' + 'applicationMetaData.firstInventorName:"' + inventor_name + '"'
        else:
            q = 'applicationMetaData.firstInventorName:"' + inventor_name + '"'
    if invention_title:
        if not q == '':
            q = q + ' AND ' + 'applicationMetaData.inventionTitle:"' + invention_title + '"'
        else:
            q = 'applicationMetaData.inventionTitle:"' + invention_title + '"'
    if city:
        if not q == '':
            q = q + ' AND ' + 'correspondenceAddressBag.cityName:"' + city + '"'
        else:
            q = 'correspondenceAddressBag.cityName:"' + city + '"'
    if state:
        if not q == '':
            q = q + ' AND ' + 'correspondenceAddressBag.geographicRegionName:"' + state + '"'
        else:
            q = 'correspondenceAddressBag.geographicRegionName:"' + state + '"'
    # create the JSON payload based on the data passed from the user on the streamlit front end.
    json_payload = create_json_payload(q=q, filing_start_date=filing_start_date, filing_end_date= filing_end_date)
    # create a response using the make_search_request function by passing in the constructed JSON.
    resp = make_search_request(PATENT_SEARCH_URL, json_payload=json_payload)
    # this is used to track the number of API calls that are made since multiple requests need to be made whenever the number of records from the query is greater than 100
    api_call_number = 0
    search_results["count"] = resp.json()["count"]
    # store the results from the initial 100 records in a temporary dictionary called search_results.
    search_results[f"attempt{api_call_number}"] = resp.json()["patentFileWrapperDataBag"]
    if resp.json()["count"] > 100:
        # The API call limit is used cap the total number of API calls that are made for a single query.
        # I am setting to a conservative limit of 10 to reduce likelihood of hitting weekly limit for testing purposes. Currently, up to 1100 records will be returned.
        # Can make this bigger in a production environmment
        api_call_limit = 10
        # the offset parameter is used to control the starting entry of the pagination of 100 records
        offset = 0
        # stop requesting from the Patent API if either the API call limit is reached or all records have been received 
        while search_results["count"] - (offset + 100) >= 0 and api_call_number < api_call_limit:
            offset = offset + 100
            json_payload2 = create_json_payload(q=q, filing_start_date=filing_start_date, filing_end_date= filing_end_date, offset = offset)
            resp2 = make_search_request(PATENT_SEARCH_URL, json_payload=json_payload2)
            api_call_number += 1
            search_results[f"attempt{api_call_number}"] = resp2.json()["patentFileWrapperDataBag"]
    # for every key in the search_results dictionary, check if the key value is count, if it is then skip.
    for x in search_results:
        if x == "count":
            continue
        else:
            # if the key value is not count then download all of the patent records associated with that request attempt.
            for y in search_results[x]:
                if y == "count":
                    continue
                else:
                    try:
                        application_number = y['applicationNumberText']
                    except:
                        continue
                    else:
                        # store the records in the database.
                        application_number = y['applicationNumberText']
                        concat_dict =  y['applicationMetaData'] | y['correspondenceAddressBag'][0] | {"applicationNumberText":y['applicationNumberText']}
                        app.db.put(application_number, concat_dict)
    return app.db.all()

# Return all stored patent data. This API is used frequently to return data to the front end table, line chart, and heatmap.
@app.get("/all_patents")
def return_all_patents():
    return app.db.all()
    

# download patent spec document
@app.get("/download_patent")
def download_patent(application_number):
    response = get_patent_docs(PATENT_DOC_URL, application_number=application_number)
    """This function is used to download the patent specification document for a specific patent application number"""
    #helper function to get the download URL of the selected patent
    def find_pdf_spec_url(data):
        for document in data.get('documentBag', []):
            if document.get('documentCode') == 'SPEC':
                for download in document.get('downloadOptionBag', []):
                    if download.get('mimeTypeIdentifier') == 'PDF':
                        return download.get('downloadUrl')
        return None
    pdf_url = find_pdf_spec_url(response.json())
    if pdf_url:
        # request downloading the patent spec file from the US Patent Office API
        response2 = requests.get(pdf_url, headers=headers)
        if response2.status_code == 200:
            # download and save the patent spec in the contents directory of the application repo. 
            with open("./contents/PatentSpec.pdf", 'wb') as file:
                file.write(response2.content)
            return 'File downloaded successfully'
        else:
            return 'Failed to download file'
        
def process_patent_dates(data):
    """This function is used to take all of the records in the database and count the number of patents filed in a given date"""
    patents_by_date = {}
    for x in data:
        # for every record in the database extract the filing date and format it as Month/Year
        date = datetime.strptime(data[x]['filingDate'],'%Y-%m-%d').strftime('%m/%Y')
        # if the key exists in the patents_by_date dictionary, then increment the count by 1.
        if date in patents_by_date:
            patents_by_date[date] += 1
        else:
            # if it is a new key in the patents_by_date dictionary then initialize the count as 1.
            patents_by_date[date] = 1
    return patents_by_date

# Generate line chart data
@app.get("/line_chart")
def generate_line_chart():
    # call and return process patent dates function
    return process_patent_dates(app.db.all())


def process_heatmap_data(data):
    """This method is used to process data in the database and format it for the plotly US Chropleth graph"""
    patents_by_state = {}
    for x in data:
        #for every record in the database extract the statename
        state = data[x]['geographicRegionName'].lower()
        try:
            #Check if the statename exists in the abbreviated state dictionary. If it does, return the abbreviated statename.
            state_abb = st_abr_dic[state]
        except:
            #if the statename doesn't exist (this occurs for any patents outside the US) then skip the record.
            continue
        else:
            #If the state abbreviation exists, then increment the count by 1.
            if state_abb in patents_by_state:
                patents_by_state[state_abb] += 1
            else:
                # if the state abbreviation does not exist, then initialize with a count of 1.
                patents_by_state[state_abb] = 1
    return patents_by_state


# Generate heatmap data
@app.get("/heatmap")
def generate_heatmap():
    # return the reformatted data for the heatmap.
    return process_heatmap_data(app.db.all())

@app.delete("/clear_db")
# method to clear all entries in the database.
def clear_db_table():
    return app.db.clear_all()
