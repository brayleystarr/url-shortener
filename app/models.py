from pydantic import BaseModel

class URLIn(BaseModel):
    """Deserialize long URL input from HTTP JSON payload."""
    url : str


