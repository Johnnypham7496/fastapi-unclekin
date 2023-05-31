from fastapi import FastAPI, Response, status
from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=['welcome'], response_description="Displays welcome message")
async def welcome(response: Response):
    response.status_cod = status.HTTP_200_OK
    return{"message": "Hello, welcome to Autobots FastAPI bootcamp"}



@router.get("/health", tags=['health'], response_description="Retrives heatlh status of this application")
async def heatlh(response: Response):
    response.status_code = status.HTTP_200_OK
    return{"status": "OK"}