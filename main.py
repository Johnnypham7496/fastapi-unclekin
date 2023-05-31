from fastapi import FastAPI, Response, status

app = FastAPI()


@app.get("/", tags=['welcome'], response_description="Displays welcome message")
async def welcome(response: Response):
    response.status_cod = status.HTTP_200_OK
    return{"message": "Hello, welcome to Autobots FastAPI bootcamp"}
