from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.config.config import settings
from src.schemas import UserDb

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_users_me function is a GET request that returns the current user's information.
        It requires authentication, and it uses the auth_service to get the current user.

    :param current_user: User: Get the current user from the database
    :return: The current_user object
    """
    return current_user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(
        file: UploadFile = File(),
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    """
    The update_avatar_user function updates the avatar of a user.
        Args:
            file (UploadFile): The file to be uploaded.
            current_user (User): The currently logged in user.  This is passed by the Depends decorator,
            which uses the auth_service module to get this information from an authorization token that was sent
            with a request header when making an API call to this function's endpoint URL.  If no valid token is found,
            then it will return None and raise HTTPException(status_code=HTTPStatusCode(401),
            detail=&quot;Unauthorized&quot;).
            db (Session): A database
    
    :param file: UploadFile: Upload the file to cloudinary
    :param current_user: User: Get the current user
    :param db: Session: Access the database
    :return: The updated user
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    cloudinary.uploader.upload(file.file, public_id=f'ContactsApp/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(
        f'ContactsApp/{current_user.username}').build_url(width=250, height=250, crop='fill'
                                                          )
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
