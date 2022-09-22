from typing import Optional

from fastapi.responses import Response
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from webvisualization_plots import plot_reported_cases_per_million
from webvisualization_plots import get_countries

# create app variable (FastAPI instance)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# mount one or more static directories,
# e.g. your auto-generated Sphinx documentation with html files
app.mount(
    # the URL where these files will be available
    "/static",
    StaticFiles(
        # the directory the files are in
        directory="static/",
        html=True,
    ),
    # an internal name for FastAPI
    name="static",
)


@app.get("/")
def plot_reported_cases_per_million_html(request: Request):
    """
    Root route for the web application.
    Handle requests that go to the path "/".
    """
    return templates.TemplateResponse(
        "plot_reported_cases_per_million.html",
        {
            "request": request,
            "countries": get_countries(),
            
            
        },
    )

@app.get("/plot.json")
def plot_json(country: Optional[str] = None,start: Optional[str] = None, end: Optional[str] = None):
    """
    Function is providing Json plot object based on query parameters recieved from HTML template.

    Args:
        country (String): country is a query param, a comma-separated list
        start (String): query start date 
        end (String): query end date
    Returns:
        chart plot object (JSON)    
    """
   
    # country is a query param, a comma-separated list
    if country:
        country = country.split(",")
    else:
        country = None  
        
    if start=="":
        start = None

    if end=="":
        end = None 

    chart = plot_reported_cases_per_million(country, start, end)
    return chart.to_dict()

def main():
    """Called when run as a script

    Should launch your web app
    """
    import uvicorn
    uvicorn.run(app)
    


if __name__ == "__main__":
    main()
