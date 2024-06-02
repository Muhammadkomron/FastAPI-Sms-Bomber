from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.sql.functions import count

from app import schemas
from app.database import get_async_session
from app.models import Log, Student, User
from app.security import hash_password


async def get_user_by_id(user_id: str) -> Optional[User]:
    async with get_async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()


async def get_user_by_username(username: str) -> Optional[User]:
    async with get_async_session() as session:
        result = await session.execute(select(User).where(User.username == username))
        return result.scalars().first()


async def get_users(offset: int = 0, limit: int = 10) -> List[User]:
    async with get_async_session() as session:
        result = await session.execute(select(User).offset(offset).limit(limit))
        return result.all()


async def create_user(user: schemas.UserCreateUpdate) -> User:
    async with get_async_session() as session:
        db_user = User()
        for var, value in vars(user).items():
            print(var, value)
            setattr(db_user, var, hash_password(value) if var == 'password' else value)
        session.add(db_user)
        await session.commit()
        return db_user


async def update_user(db_user: User, user: schemas.UserBase) -> User:
    async with get_async_session() as session:
        for var, value in vars(user).items():
            setattr(db_user, var, value)
        session.add(db_user)
        await session.commit()
        return db_user


async def get_student_by_phone_number(phone_number: str) -> Optional[Student]:
    async with get_async_session() as session:
        result = await session.execute(select(Student).where(Student.phone_number == phone_number))
        return result.scalars().first()


async def get_students(offset: int = 0, limit: int = 10) -> List[Student]:
    async with get_async_session() as session:
        result = await session.execute(select(Student).offset(offset).limit(limit))
        return result.scalars().all()


async def get_students_count() -> int:
    async with get_async_session() as session:
        result = await session.execute(select(count(Student.id)))
        return result.scalars()


async def create_student(student: schemas.StudentCreateUpdate) -> Student:
    async with get_async_session() as session:
        db_student = Student()
        for var, value in vars(student).items():
            setattr(db_student, var, value)
        session.add(db_student)
        await session.commit()
        return db_student


async def update_student(db_student: Student, student: schemas.StudentCreateUpdate) -> Student:
    async with get_async_session() as session:
        for var, value in vars(student).items():
            setattr(db_student, var, value)
        session.add(db_student)
        await session.commit()
        return db_student


async def create_or_update_student(student: schemas.StudentCreateUpdate) -> Student:
    db_student = await get_student_by_phone_number(student.phone_number)
    if db_student:
        return await update_student(db_student, student)
    return await create_student(student)


async def get_or_create_student(student: schemas.StudentCreateUpdate) -> Student:
    db_student = await get_student_by_phone_number(student.phone_number)
    if db_student:
        return db_student
    return await create_student(student)


async def create_log(log: schemas.LogBase) -> Log:
    async with get_async_session() as session:
        db_log = Log()
        for var, value in vars(log).items():
            setattr(db_log, var, value)
        session.add(db_log)
        await session.commit()
        return db_log
