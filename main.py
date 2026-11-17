from fastapi import FastAPI, Depends, status
import db_schema 
from db_schema import engine, URL
from hash import crc32_hash
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import URLIn, URLOut


app = FastAPI()

@app.post("/shorten", response_model=URLOut, status_code=status.HTTP_201_CREATED) 
async def shorten_URL(http_body : URLIn):
    """Add long URL instance to database. 

    Args: 
        long_url: Original URL string. 
    """
    
    # use engine to create new session connection with database
    with Session(engine) as session: 
        long_url = http_body.url
        hashed_url = crc32_hash(long_url)[:7]
        seed = "please_hire_me!"
        stmt = select(URL).where(URL.hashed_url == hashed_url)

        # collision?
        while session.execute(stmt): # TODO: claude is saying that this while loop will never exit
            long_url = long_url + seed 
            hashed_url = crc32_hash(long_url)[:7] 
            stmt = select(URL).where(URL.hashed_url == hashed_url)
            print(session.execute(stmt))

        # add URL record to table
        url_row = URL(long_url, hashed_url) 
        session.add(url_row)

        # commit changes
        session.commit()



