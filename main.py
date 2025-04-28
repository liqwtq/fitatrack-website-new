import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up the templates directory
templates = Jinja2Templates(directory='templates')


@app.api_route("/", response_class=HTMLResponse, methods=['GET'])
async def root(request: Request):
    this_year = datetime.now().year
    return templates.TemplateResponse("index.html", {"request": request, "year": this_year})


# If running locally or in development, use uvicorn directly
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
