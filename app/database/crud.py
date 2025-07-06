from sqlalchemy.future import select
from .models import User
from .db import async_session

async def get_user_by_telegram_id(telegram_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).filter_by(telegram_id=telegram_id))
        scalars = await result.scalars()
        return scalars.first()

async def add_user(telegram_id: int, name: str):
    from .models import User
    from .db import async_session

    async with async_session() as session:
        user = User(telegram_id=telegram_id, name=name)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user