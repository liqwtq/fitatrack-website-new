from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import logging
from datetime import datetime


logger = logging.getLogger(__name__)

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')


@app.post("/", response_class=HTMLResponse)
async def root(request: Request):
    this_year = datetime.now().year
    return templates.TemplateResponse("index.html", {"request": request, "year":this_year})