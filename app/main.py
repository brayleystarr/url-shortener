from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse,RedirectResponse, FileResponse
import app.db_schema as db_schema
from app.db_schema import engine, URL
from app.hash import crc32_hash
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import URLIn
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/")
async def home():
    return FileResponse("app/static/index.html")

@app.post("/shorten") 
async def shorten_URL(http_body : URLIn):
    """Add long URL to database and return it's short URL. 

    Args: 
        long_url: Original, long URL string. 

    Returns: 
        JSON containing the shortened URL string. 
    """
    # engine creates new session connection to database
    with Session(engine) as session: 
        # fetch long URL from http contents
        original_url = http_body.url

        # URL in database?
        short_url_exists = session.scalar(select(URL).where(URL.original_url == original_url))
        if short_url_exists:
            return JSONResponse(content={"hashed_url" : "http://localhost:8000/" + str(short_url_exists.hashed_url)}, status_code=status.HTTP_200_OK)
        
        # create URL hash
        hashed_url = str(crc32_hash(original_url)[:7])
        seed = "please_hire_me_😀!"
        stmt = select(URL).where(URL.hashed_url == hashed_url)
        extended_url = original_url

        # URL hash collision?
        while session.execute(stmt).all(): 
            extended_url = extended_url + seed 
            hashed_url = str(crc32_hash(extended_url)[:7])
            stmt = select(URL).where(URL.hashed_url == hashed_url)
            
        # push URL to table
        url_row = URL(original_url, hashed_url) 
        session.add(url_row)

        # commit changes
        session.commit()

        # communicate changes to frontend / client
        return JSONResponse(content={"hashed_url" : "http://localhost:8000/" + str(hashed_url)}, status_code=status.HTTP_201_CREATED)
    
@app.get("/{tiny_url}")
async def url_redirect(tiny_url : str):
    """Redirect short URL to long URL. 

    Args: 
        tiny_url : Hash of a normal URL.
    """
    # engine creates new session connection to database
    with Session(engine) as session: 
        # fetch corresponding URL record
        url_record = session.scalar(select(URL).where(URL.hashed_url == tiny_url))
        print(url_record)
        # shortened URL exist? 
        if not url_record:
            raise HTTPException(status_code=404, detail="Shortened URL not found.") 
    # redirect to long URL of interest     
    print(url_record.original_url)
    return RedirectResponse(url=url_record.original_url, status_code=301)

# mount static frontend home GUI
app.mount("/static", StaticFiles(directory="app/static"), name="static")