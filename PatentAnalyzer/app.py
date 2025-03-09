import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
from external_api_routes.gemeni_routes import *
import plotly.graph_objects as go

BASE_URL = "http://localhost:8000"


st.title("Patent Analysis Tool by Rabees R")

# --- 1. Query Form ---
st.subheader("Search Patents")
search_all = st.text_input("Search All")
start_date = st.date_input("Filing Start Date", value = datetime.today() - relativedelta(years = 50))
end_date = st.date_input("Filing End Date")
patent_number = st.text_input("Patent Number")
inventor_name = st.text_input("Inventor Name")
invention_title = st.text_input("Invention Title")
applicant_name = st.text_input("Applicant Name")
city = st.text_input("City")
state = st.text_input("State")

a = st.button("Run Query")
if a:
    params = {
        "search_all": search_all,
        "filing_start_date": start_date.strftime("%Y-%m-%d") if start_date else "",
        "filing_end_date": end_date.strftime("%Y-%m-%d") if end_date else "",
        "patent_number": patent_number,
        "inventor_name": inventor_name,
        "invention_title": invention_title,
        "applicant_name": applicant_name,
        "city" : city,
        "state" : state
    }
    response = requests.get(f"{BASE_URL}/search_patents", params=params)
    if response.status_code == 200:
        st.success(f"Patents fetched and stored successfully!")
    else:
        st.error("Failed to fetch patents.")

b = st.button("Clear Database")
if b:
    response = requests.delete(f"{BASE_URL}/clear_db")


if requests.get(f"{BASE_URL}/all_patents").json() != {}:
    # --- Line Chart ---
    st.subheader("Patent Trends Over Time")
    response3 = requests.get(f"{BASE_URL}/line_chart")
    chart_data = response3.json()
    # Convert keys (dates) to datetime format and sort
    sorted_data = sorted(chart_data.items(), key=lambda x: datetime.strptime(x[0], "%m/%Y"))
    # Extract sorted x and ynvalues
    sorted_x = [item[0] for item in sorted_data]
    sorted_y = [item[1] for item in sorted_data] 
    # Create the line chart
    fig = px.line(x=sorted_x, y=sorted_y, labels={"x": "Date", "y": "Patent Application Count"}, 
                markers=True, title="Patent Filing Trends")
    st.plotly_chart(fig)
    if response3.status_code != 200:
        st.error(f"There was an error generating the line chart with response code {response.status_code}. This may be due to anamolous data returned from the Patent API")
    # --- Heatmap ---
    response4 = requests.get(f"{BASE_URL}/heatmap")
    heatmap_data = response4.json()
    fig2 = go.Figure(data=go.Choropleth(
        locations=list(heatmap_data.keys()), # Spatial coordinates
        z = list(heatmap_data.values()), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Reds',
        colorbar_title = "Count of Patents",
    ))
    fig2.update_layout(
        title_text = 'US Patent Applications by State',
        geo_scope='usa', # limite map scope to USA
    )
    st.plotly_chart(fig2)

# --- 2. Display Stored Patent Data ---
st.subheader("Stored Patent Data")
response = requests.get(f"{BASE_URL}/all_patents")
if response.status_code == 200:
    data = pd.DataFrame(response.json()).transpose()
    event = st.dataframe(
    data,
    column_order = ['patentNumber','filingDate', 'grantDate', 'inventionTitle', 
                    'firstInventorName', 'firstApplicantName', 'applicationStatusDate', 'cityName', 'geographicRegionName', 'applicationNumberText'],

    column_config = {'filingDate': "Filing Date", 'grantDate': "Grant Date", 'inventionTitle': "Invention Title",
                    'firstInventorName': "Inventor Name", 'firstApplicantName': "Applicant Name",
                    'applicationStatusDate' : "Application Status Date", "cityName": "City", 'geographicRegionName': "State",
                    'applicationNumberText': "Application Number"
                    },
    selection_mode = ["single-row"],
    on_select = "rerun",
    hide_index=False
)
        
try:
    event.selection.rows[0]
except:
    pass
else:
    st.subheader("You have selected the following patent record")
    selected_data = data.iloc[int(event.selection.rows[0])]
    st.table(selected_data)
    st.subheader("Pressing Confirm will download the Patent Spec PDF and summarize it using an LLMs")
    if st.button("Confirm Selection and Summarize Patent Spec"):
        st.info(f"Please wait while the patent file for apllication number: {selected_data.applicationNumberText} is downloaded. This may take up to a few minutes for large files.")
        params = {
            "application_number" : selected_data.applicationNumberText
        }
        response = requests.get(f"{BASE_URL}/download_patent", params=params)
        if response.status_code == 200:
            st.info('Download Successful. Please wait while the document is being summarized...')
            try:
                summary = gemini_wrapper()
            except:
                st.error("Sorry there was an error in summarizing the patent. Google Gemini API limit may have been reached.")
            else:
                st.markdown(summary.text)
        else:
            st.error('Failed to download file. Download API limit may have been exceeded. Please try again later.')