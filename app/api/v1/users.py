from fastapi import APIRouter, Depends

from app.schemas.user import UserOut
from app.core.auth_deps import get_current_user

router = APIRouter()


@router.get("/profile", response_model=UserOut)
def get_profile(current_user = Depends(get_current_user)):
    return current_user
