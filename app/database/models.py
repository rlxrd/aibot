from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from datetime import datetime

from config import DB_URL

engine = create_async_engine(url=DB_URL, echo=False)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    balance: Mapped[str] = mapped_column(String(15), default='0')


class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))


class ModelType(Base):
    __tablename__ = 'model_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class ModelCompany(Base):
    __tablename__ = 'model_companies'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    sys_name: Mapped[str] = mapped_column(String(50))
    model_type: Mapped[int] = mapped_column(ForeignKey('model_types.id'))


class ModelVariant(Base):
    __tablename__ = 'model_variants'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    sys_name: Mapped[str] = mapped_column(String(50))
    price: Mapped[str] = mapped_column(String(15))
    model_type: Mapped[int] = mapped_column(ForeignKey('model_types.id'))
    model_company: Mapped[int] = mapped_column(ForeignKey('model_companies.id'))
    default: Mapped[bool] = mapped_column(default=False)


class DefaultModel(Base):
    __tablename__ = 'default_models'

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    model_type: Mapped[int] = mapped_column(ForeignKey('model_types.id'))
    model_variant: Mapped[int] = mapped_column(ForeignKey('model_variants.id'))


class History(Base):
    __tablename__ = 'history'

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    aimodel: Mapped[int] = mapped_column(ForeignKey('model_types.id'))
    tokens: Mapped[str] = mapped_column(String(15))
    price: Mapped[str] = mapped_column(String(15))
    request: Mapped[str] = mapped_column(String(4096))
    created_ad: Mapped[datetime] = mapped_column()


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(15))
    order: Mapped[str] = mapped_column(String(40))
    value: Mapped[str] = mapped_column(String(5))
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_ad: Mapped[datetime] = mapped_column()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
