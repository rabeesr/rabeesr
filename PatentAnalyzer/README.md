# PatentAnalyzer
Final Project for MPCS Python Programming


# Note to Graders

To run the application simply type ./setup.sh in the terminal after changing the working directory to whereever the app repo was downloaded. 

The patent app requires ports 8000 and ports 8501 to be clear of any processes. If there are existing processes then users will get an error. To correct the issue, run the command lsof -i :8000 (for port 8000) or lsof -i :8501 (for port 8501). Use the PID that is returned from that command and type in kill -9 {PID Number here}. This will kill the process.

As another note, if this is your first time using streamlit, it will ask you to enter an email before the app is started. Simply press enter to skip this step.

Finally, if there are any other issues please feel free to reach out to Rabees via slack. 

**Project Description**
I would like to develop an application which allows users to analyze information from the US Patent Office. The application will allow users to interact with it via the command line to support the following methods/actions. I will use the Patent search API developed in partnership with the US Patents Office found here: https://data.uspto.gov/apis/patent-file-wrapper/search.

Here are some preliminary methods that I would like to develop. I am not going to limit myself to these methods and will continuosuly refine the features based upon feasibility and end user value.

**Potential Features**

    * Provide analysis on the number of patents filed within a designated date period
    * Allow the user to search patents by keywords or strings or across a combination of fields (i.e. combinations of attributes such as inventor, filing date, keyword, geography, etc.)
    * Allow the user to search the patent by different market sectors (i.e. healthcare, tech, etc.)
    * Allow the user to check on the status of a patent by providing the patent API
    * I would like to see if I can collate all the information returned from the query and send it to an LLM to summarize and identify key points from.


### Patent Analyzer Project Plan

    - [X] By end of week 4, confirm the availability of the API and perform a simple "Get" HTTPS request and ingest JSON message. If the aforementioned API is not supported then identify alternative sources of Patent Data.
    - [X] By end of week 5, design a simple webpage for users to interact with the data and host it on a local port.
    - [X] By end of week 6, finalize the list of interesting analytics/KPIs that would be interesting to inventors and begin developing methods to analyze patent data (i.e. # of patents filed within a given period, # of patents in particular sectors, identify soon-to-expire patents that may be available for licensing, etc.).
    - [X] By end of week 7, develop the UI/UX and functions which will allow users to query the US Patent Database by different patent attributes such as: filing entity, company, keywords, dates, status, sector, etc.
    - [X] By end of week 8, develop a prompt and method which takes the patent that are returned and summarizes them using an LLM such as LLAMA, ChatGPT, etc. Validate the responses and try to add functionality to where users can select from a set of preconceived prompts (I.e. summarize the patents, identify competing technology for each returned patent, etc.)
    - [X] By week 9, finalize the application, perform testing and add nice to have features such as graphics and charts which will allow users to identify trends. 2 examples of charts may be: a time series graph of patent filings within a specified date range. Heatmaps of patent filings by geography (i.e. states, cities, etc.)
    


