from pydantic import BaseModel

class URLIn(BaseModel):
    url : str

class URLOut(URLIn):
    pass
