from fastapi import FastAPI
from database import engine
from models import Base
from routers import urls
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(urls.router)

