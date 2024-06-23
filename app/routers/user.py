from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import get_all_users, create_user
from app.db.session import AsyncSessionLocal
from app.schemas.user import UserCreate

router = APIRouter()


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/users/")
async def read_users(session: AsyncSession = Depends(get_session)):
    users = await get_all_users(session)
    return users


@router.post("/users/")
async def create_new_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    new_user = await create_user(session, user)
    return new_user


@router.get("/")
async def read_users():
    return [{"username": "user1"}, {"username": "user2"}]
