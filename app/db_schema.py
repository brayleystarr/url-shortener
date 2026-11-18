from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine, String 

print("\033[31mINFO:     URL Database Initialized.\033[0m")

class Base(DeclarativeBase):
    pass

class URL(Base):
    """URL database table schema."""

    __tablename__ = "urls"

    url_id : Mapped[int] = mapped_column(primary_key=True)
    original_url : Mapped[str] = mapped_column(String(2048), unique=True, index=True)
    hashed_url : Mapped[str] = mapped_column(String(7), unique=True)

    def __init__(self, original_url, hashed_url):
        self.original_url = original_url
        self.hashed_url = hashed_url

engine = create_engine("postgresql+psycopg://brayley:shortener_pw@localhost:5433/shortener") 
Base.metadata.create_all(bind=engine) 



