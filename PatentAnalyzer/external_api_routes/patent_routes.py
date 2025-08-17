import requests
import json
import time
import random
from typing import *

SLEEP_AFTER_429 = 0.1
SLEEP_BETWEEN_HTTP = 0
HTTP_RETRY = 5
MAX_FILES = 2
total_429 = 0
total_rate = 0
API_KEY = "zbncijprczprbxnvxksauznwwdxzot"
# API URL for searching patents
PATENT_SEARCH_URL = 'https://api.uspto.gov/api/v1/patent/applications/search'
# API URL for downloading patent document URL
PATENT_DOC_URL = 'https://api.uspto.gov/api/v1/patent/applications/'
DEFAULT_LIMIT = 100

# header for the US Patent API
headers = {
    'X-API-KEY': API_KEY,
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

# List of fields to return from the API. These are supplied to the JSON message in the JSON constructor method.
LIST_OF_FIELDS = [
    'applicationNumberText',
    'applicationMetaData.inventionTitle',
    'applicationMetaData.patentNumber',
    'applicationMetaData.smallEntityStatusIndicator',
    'applicationMetaData.nationalStageIndicator',
    'applicationMetaData.firstApplicantName',
    'applicationMetaData.firstInventorName',
    'applicationMetaData.applicationStatusDescriptionText',
    'applicationMetaData.applicationStatusCode',
    'applicationMetaData.applicationStatusDate',
    'applicationMetaData.filingDate',
    'applicationMetaData.applicationTypeCode',
    'applicationMetaData.applicationTypeLabelName',
    'applicationMetaData.applicationTypeCategory',
    'applicationMetaData.filingDate',
    'applicationMetaData.grantDate',
    'correspondenceAddressBag.geographicRegionName',
    'correspondenceAddressBag.cityName',
    'correspondenceAddressBag.countryName'
]

def create_json_payload(q: str = None, filing_start_date: Optional[str] = None, filing_end_date: Optional[str] = None,
                        offset: int = 0,limit: int = DEFAULT_LIMIT, sort: Optional[List] = None):
    """
    Constructs a JSON structure for a patent search query.

    Parameters:
        q (str, optional): The search query string.
        filters (list of dict, optional): List of filter dictionaries.
        range_filters (list of dict, optional): List of range filter dictionaries.
        offset (int, optional): Pagination offset, default is 0.
        limit (int, optional): Pagination limit, default is 100 which is the max allowable limit.
        sort (list of dict, optional): List of sorting criteria. The patents are sorted by the patent filing date.

    Returns:
        dict: JSON-compatible dictionary representing the patent search query.
    """

    query = {}

    if q:
        query["q"] = q
    # can use this to filter for cases that are either granted or under examination (it is currently filtering out patents that are rejected)
    query["filters"] = [
    {
      "name": "applicationMetaData.applicationStatusDescriptionText",
      "value": [
        "Patented Case",
        "Docketed New Case - Ready for Examination",
        "Non Final Action Mailed"
      ]
    }
    ]
    # range filters are used to filter by a filing date range.
    query["rangeFilters"] = [
     {
      "field": "applicationMetaData.filingDate",
      "valueFrom": filing_start_date, 
      "valueTo": filing_end_date
     }
    ]


    query["pagination"] = {
        "offset": offset,
        "limit": limit
    }

    query["sort"] = [
    {
      "field": "applicationMetaData.filingDate",
      "order": "desc"
    }
  ]

    query["fields"] = LIST_OF_FIELDS
    # return the final JSON message
    return query


def make_search_request(base_url, json_payload, retry=0):
    """This method is used to call the US Patent search API based on a provided JSON message"""
    global total_429
    response = requests.post(base_url, headers=headers, json=json_payload)
    if response.status_code == 429 and retry < HTTP_RETRY:
        time.sleep(SLEEP_AFTER_429)
        retry += 1
        total_429 += 1
        print(f"Got HTTP 429. Retry number: {retry}")
        return make_search_request(base_url, retry, json_payload=json_payload)
    else:
        print('Sorry maximum retries exceeded, server not available. Please try again later')
    return response


def get_patent_docs(base_url, application_number, retry=0):
    """This method is used to call the US Patent API for the documents associated to a specific patent application number"""
    global total_429
    doc_url = f'{base_url}{application_number}/documents'
    response = requests.get(doc_url, headers=headers)
    if response.status_code == 429 and retry < HTTP_RETRY:
        time.sleep(SLEEP_AFTER_429)
        retry += 1
        total_429 += 1
        print(f"Got HTTP 429. Retry number: {retry}")
        response = get_patent_docs(doc_url, application_number, retry)
    else:
        print('Sorry maximum retries exceeded, server not available. Please try again later')
    return response
