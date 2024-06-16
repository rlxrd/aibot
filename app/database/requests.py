from app.database.models import async_session
from app.database.models import (User, Admin,
                                 ModelType, ModelCompany, ModelVariant, DefaultModel,
                                 History, Order)
from sqlalchemy import select, update, delete, desc


def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner


@connection
async def set_user(session, tg_id):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))

    if not user:
        user = User(tg_id=tg_id)
        session.add(user)
        await session.flush()

        models = await session.scalars(select(ModelVariant).where(ModelVariant.default.is_(True)))
        for model in models:
            session.add(DefaultModel(user=user.id, model_type=model.model_type, model_variant=model.id))

        await session.commit()


@connection
async def get_user(session, tg_id):
    return await session.scalar(select(User).where(User.tg_id == tg_id))


@connection
async def user_text(session, tg_id, ):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    model_type = await session.scalar(select(ModelType).where(ModelType.name == 'text'))
    default = await session.scalar(select(DefaultModel).where(DefaultModel.user == user.id,
                                                              DefaultModel.model_type == model_type.id))
    model = await session.scalar(select(ModelVariant).where(ModelVariant.id == default.model_variant))
    company = await session.scalar(select(ModelCompany).where(ModelCompany.id == model.model_company))
    return {'user': user.id, 'model_variant': model, 'company': company}
