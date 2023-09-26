from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import exc, func
from sqlalchemy import select
from fastapi_async_sqlalchemy import db
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        :param model: A SQLAlchemy model class
        """
        self.model = model
        self.db = db

    def get_db(self):
        return self.db

    async def get(self, _id: Any, db_session: AsyncSession | None = None) -> Optional[ModelType]:
        db_session = db_session or self.db.session
        query = select(self.model).where(self.model.id == _id)
        response = await db_session.execute(query)
        return response.scalar_one_or_none()

    async def get_multi(
            self,
            *,
            skip: int = 0,
            limit: int = 100,
            db_session: AsyncSession | None = None
    ) -> List[ModelType]:
        db_session = db_session or self.db.session
        query = select(self.model).offset(skip).limit(limit).order_by(self.model.id)
        response = await db_session.execute(query)
        return response.scalars().all()

    async def get_count(
            self, db_session: AsyncSession | None = None
    ) -> ModelType | None:
        db_session = db_session or self.db.session
        response = await db_session.execute(
            select(func.count()).select_from(select(self.model).subquery())
        )
        return response.scalar_one()

    async def create(
            self,
            *,
            obj_in: CreateSchemaType,
            db_session: AsyncSession | None = None
    ) -> ModelType:
        db_session = db_session or self.db.session
        db_obj = self.model.from_orm(obj_in)  # type: ignore

        try:
            db_session.add(db_obj)
            await db_session.commit()
        except exc.IntegrityError:
            await db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Resource already exists",
            )
        await db_session.refresh(db_obj)

        return db_obj

    async def update(
        self,
        *,
        obj_current: ModelType,
        obj_new: Union[UpdateSchemaType, Dict[str, Any]],
        db_session: AsyncSession | None = None
    ) -> ModelType:
        db_session = db_session or self.db.session

        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            update_data = obj_new.model_dump(
                exclude_unset=True
            )  # This tells Pydantic to not include the values that were not sent
        for field in update_data:
            setattr(obj_current, field, update_data[field])

        db_session.add(obj_current)
        await db_session.commit()
        await db_session.refresh(obj_current)

        return obj_current

    async def remove(self, *, _id: int, db_session: AsyncSession | None = None) -> ModelType:
        db_session = db_session or self.db.session
        query = select(self.model).where(self.model.id == _id)
        response = await db_session.execute(query)
        obj = response.scalar_one()
        await db_session.delete(obj)
        await db_session.commit()

        return obj
