from fastapi import FastAPI, Response, status

app = FastAPI(
    title="Johnny's-FastAPI",
    description="This is the swagger spec for the FastApi workshop",
    version='1.0.0'
)


@app.get("/", tags=['welcome'], response_description="Displays welcome message")
async def welcome(response: Response):
    response.status_cod = status.HTTP_200_OK
    return{"message": "Hello, welcome to Autobots FastAPI bootcamp"}
