#APIKEY:AIzaSyBfOLl57ibOiXm6Zvb39OXZuGR1hJY5tmo
#Project Number: 367827059802
from google import genai
from google.genai import types
import pathlib as pl
import httpx




def gemini_wrapper():
    """Wrapper function to make a call to the Google Gemini API. The function uploads the PDF file, supplies it to the Google Gemini 2.0 Flash Lite model."""
    client = genai.Client(api_key="AIzaSyBfOLl57ibOiXm6Zvb39OXZuGR1hJY5tmo")

    # Get the current path
    current_path = pl.Path.cwd()
    # Location of the PDF
    file_path = current_path.joinpath(pl.Path('./contents/PatentSpec.pdf')).resolve()

    # Upload the PDF using the File API
    sample_file = client.files.upload(
    file=file_path,
    )
    # prompt to summarize the patent spec, identify risks and limitations, potential customers, and competitors.
    prompt = "You are an expert in patent analysis and technology evaluation. Given the full text of a patent document, analyze it and provide the following structured insights: \
    Summary (5 sentences maximum): Provide a concise summary of the patent, focusing on its key objectives, core technological innovation, and intended use cases. \
    Limitations: Identify any technical, operational, or scalability limitations of the described technology. Consider constraints related to feasibility, cost, performance, regulatory challenges, or adoption barriers. \
    Competing and Emerging Technologies: List existing and emerging technologies that serve a similar purpose. Briefly compare them to the patented technology, highlighting differences in approach, efficiency, market adoption, or potential advantages and disadvantages. \
    Market Opportunity: Provide a rough outline of the market opportunity including current market size, expected market growth, number of competitors, and prospective customers. \
    Ensure the response is clear, objective, and well-structured for easy interpretation. "

    response = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents=[sample_file, prompt])
    return response

