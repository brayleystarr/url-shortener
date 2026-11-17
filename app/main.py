from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse
import app.db_schema as db_schema 
from app.db_schema import engine, URL
from app.hash import crc32_hash
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import URLIn

app = FastAPI()

@app.post("/shorten", status_code=status.HTTP_201_CREATED) 
async def shorten_URL(http_body : URLIn):
    """Add long URL instance to database. 

    Args: 
        long_url: Original URL string. 

    Returns: 
        Shortened URL string. 
    """
    
    # engine creates new session connection to database
    with Session(engine) as session: 
        original_url = http_body.url

        # URL exists in database, redirect!
        if session.execute(select(URL).where(URL.original_url == original_url)).all():
            short_url = session.scalars(select(URL).where(URL.original_url == original_url)).all()[0].hashed_url
            return JSONResponse(content=None, status_code=301, headers={"Location" : "https://localhost:8000/" + short_url}) # TODO: THIS WILL LIKELY BE CHANGED BEFORE FINAL PUSH

        hashed_url = str(crc32_hash(original_url)[:7])
        seed = "please_hire_me_😀!"
        stmt = select(URL).where(URL.hashed_url == hashed_url)
        extended_url = original_url

        # collision?
        while session.execute(stmt).all(): 
            extended_url = extended_url + seed 
            hashed_url = str(crc32_hash(extended_url)[:7])
            stmt = select(URL).where(URL.hashed_url == hashed_url)
            
        # add URL record to table
        url_row = URL(original_url, hashed_url) 
        session.add(url_row)

        # commit changes
        session.commit()

        # communicate changes to frontend / client
        return {"hashed_url" : "https://localhots:8000/" + str(hashed_url)}



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
