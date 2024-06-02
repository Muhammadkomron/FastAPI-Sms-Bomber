from fastapi import APIRouter, HTTPException

from app import crud, schemas

router = APIRouter()


@router.post('/users/', response_model=schemas.User)
async def create_user(user: schemas.UserCreateUpdate):
    user = await crud.get_user_by_username(username=user.username)
    if user:
        raise HTTPException(status_code=400, detail='Username already registered')
    return await crud.create_user(user)


@router.get('/users/', response_model=list[schemas.User])
async def read_users(offset: int = 0, limit: int = 10):
    return await crud.get_users(offset=offset, limit=limit)
