from fastapi import  Depends, APIRouter, HTTPException, status, Request
from utils.utils import authenticate_and_get_user
router = APIRouter()

@router.get("/me")
def get_me(request: Request):
    try:
        user_details = authenticate_and_get_user(request)
        user = user_details.get("user_id")
        return {"user": user}
    except Exception as error:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))
    


@router.get('/user_profile')
def user_profile(request: Request):
    pass