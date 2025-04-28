import logging
import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Serve static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    logger.info("Static files mounted successfully.")
except Exception as e:
    logger.error(f"Error mounting static files: {e}")

# Set up the templates directory
try:
    templates = Jinja2Templates(directory='templates')
    logger.info("Templates directory set up successfully.")
except Exception as e:
    logger.error(f"Error setting up templates directory: {e}")

@app.api_route("/", response_class=HTMLResponse, methods=['GET'])
async def root(request: Request):
    try:
        this_year = datetime.now().year
        return templates.TemplateResponse("index.html", {"request": request, "year": this_year})
    except Exception as e:
        logger.error(f"Error rendering template: {e}")
        raise e


@app.api_route("/sitemap", response_class=HTMLResponse, methods=['GET'])
async def root(request: Request):
    return templates.TemplateResponse("sitemap.xml", {"request": request})

# If running locally or in development, use uvicorn directly
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    try:
        uvicorn.run(app, host="0.0.0.0", port=port)
        logger.info("Uvicorn server running.")
    except Exception as e:
        logger.error(f"Error running Uvicorn: {e}")
