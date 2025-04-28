import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Log all levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logger = logging.getLogger(__name__)

# Initialize the FastAPI app
app = FastAPI()

# Mount the static files directory
try:
    logger.info("Mounting static files...")
    app.mount("/static", StaticFiles(directory="static"), name="static")
    logger.info("Static files mounted successfully.")
except Exception as e:
    logger.error(f"Error mounting static files: {e}")
    raise

# Set up the templates directory
try:
    logger.info("Setting up the templates directory...")
    templates = Jinja2Templates(directory='templates')
    logger.info("Templates directory set up successfully.")
except Exception as e:
    logger.error(f"Error setting up templates directory: {e}")
    raise


@app.api_route("/", response_class=HTMLResponse, methods=['GET'])
async def root(request: Request):
    try:
        logger.info("Handling root request...")
        this_year = datetime.now().year
        logger.debug(f"Year for template: {this_year}")
        response = templates.TemplateResponse("index.html", {"request": request, "year": this_year})
        logger.info("Root request handled successfully.")
        return response
    except Exception as e:
        logger.error(f"Error handling root request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# If running locally or in development, use uvicorn directly
if __name__ == "__main__":
    try:
        port = int(os.getenv("PORT", 8000))
        logger.info(f"Starting uvicorn server on port {port}...")
        uvicorn.run(app, host="0.0.0.0", port=port)
        logger.info("Uvicorn server started successfully.")
    except Exception as e:
        logger.error(f"Error starting uvicorn server: {e}")
        raise
