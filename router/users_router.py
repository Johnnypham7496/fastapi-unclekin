from fastapi import FastAPI, Response, status, APIRouter, Depends, HTTPException
from repository import user_repository
from sqlalchemy.orm import Session
from db_config import get_db
from schemas import UserModel, MessageModel


router = APIRouter(
    prefix="/users/v1",
    tags=["users"]
)


@router.get("/", response_description="Display all users", description="Retrieves all users", response_model=list[UserModel])
def get_users(response: Response, db: Session = Depends(get_db)):
    return_value = user_repository.get_all_users(db)
    response.status_code = status.HTTP_200_OK
    return return_value


@router.get("/{username}", response_description="Display user by username", description="Retrieves user by username", response_model=UserModel,
            responses={404: {"model": MessageModel}})
def get_by_username(username: str, reponse: Response, db: Session = Depends(get_db)):
    return_value = user_repository.get_by_username(db, username)

    if return_value == None:
        reponse_text = "username not found. Please check your parameter and try again"
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=reponse_text)

    reponse.status_code = status.HTTP_200_OK
    return return_value