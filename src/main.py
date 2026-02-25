from fastapi import FastAPI
from api.v1.routers.api import api_router

app = FastAPI()

@app.get('/')
def welcome():
    return {'message': 'Welcome to my FastAPI application'}

app.include_router(api_router)
