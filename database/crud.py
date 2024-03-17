from sqlalchemy import delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from .models import Config, User, Vacancy
from .session import AsyncSessionLocal


async def create_user(**kwargs):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            existing_user = await get_user(user_id=kwargs.get("user_id"))
            if existing_user:
                return existing_user
            new_user = User(**kwargs)
            session.add(new_user)
            await session.commit()
            return new_user


async def get_user(user_id: int):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            statement = select(User).where(User.id == user_id)
            result = await session.execute(statement)
            try:
                return result.scalar_one()
            except NoResultFound:
                return None


async def update_user(user_id: int, **kwargs):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            statement = select(User).where(User.id == user_id)
            result = await session.execute(statement)
            try:
                user_to_update = result.scalar_one()
                for key, value in kwargs.items():
                    setattr(user_to_update, key, value)
                await session.commit()
                return user_to_update
            except NoResultFound:
                return None


async def get_user_configs(user_id: int):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            statement = select(Config).where(Config.user_id == user_id)
            result = await session.execute(statement)
            configs = result.scalars().all()
            return configs


async def delete_all_user_configs(user_id: int):
    async with AsyncSessionLocal() as session:
        await session.execute(delete(Config).where(Config.user_id == user_id))
        await session.commit()


async def create_config(**kwargs):
    async with AsyncSessionLocal() as session:
        query = select(Config).filter_by(**kwargs)
        result = await session.execute(query)
        existing_config = result.scalars().first()
        if existing_config:
            return existing_config

        new_config = Config(**kwargs)
        session.add(new_config)
        await session.commit()
        await session.refresh(new_config)
        return new_config


async def get_config(config_id):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            statement = select(Config).options(selectinload(Config.vacancies)).where(Config.id == config_id)

            result = await session.execute(statement)
            try:
                return result.scalar_one()
            except NoResultFound:
                return None


async def update_config(config_id, **kwargs):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            statement = select(Config).where(Config.id == config_id)
            result = await session.execute(statement)
            try:
                config_to_update = result.scalar_one()
                for key, value in kwargs.items():
                    setattr(config_to_update, key, value)
                await session.commit()
                return config_to_update
            except NoResultFound:
                return None


async def delete_config(config_id):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            statement = select(Config).where(Config.id == int(config_id))
            result = await session.execute(statement)
            try:
                config_to_delete = result.scalar_one()
                await session.delete(config_to_delete)
                await session.commit()
            except NoResultFound:
                return None


async def create_vacancy(**kwargs):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            existing_vacancy = await session.execute(select(Vacancy).where(Vacancy.url == kwargs.get("url")))
            vacancy = existing_vacancy.scalars().first()

            if vacancy:
                return vacancy.id
            else:
                new_vacancy = Vacancy(**kwargs)
                session.add(new_vacancy)

        await session.commit()
        return new_vacancy.id


async def get_vacancy(vacancy_id):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            statement = select(Vacancy).where(Vacancy.id == vacancy_id)
            result = await session.execute(statement)
            try:
                return result.scalar_one()
            except NoResultFound:
                return None


async def update_vacancy(vacancy_id, **kwargs):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            statement = select(Vacancy).where(Vacancy.id == vacancy_id)
            result = await session.execute(statement)
            try:
                vacancy_to_update = result.scalar_one()
                for key, value in kwargs.items():
                    setattr(vacancy_to_update, key, value)
                await session.commit()
                return vacancy_to_update
            except NoResultFound:
                return None


async def delete_vacancy(vacancy_id):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            statement = select(Vacancy).where(Vacancy.id == vacancy_id)
            result = await session.execute(statement)
            try:
                vacancy_to_delete = result.scalar_one()
                await session.delete(vacancy_to_delete)
                await session.commit()
            except NoResultFound:
                return None


async def assign_vacancy_to_config(vacancy_id, config_id):
    async with AsyncSessionLocal() as session:
        try:
            config = await session.get(Config, config_id, options=[selectinload(Config.vacancies)])
            vacancy = await session.get(Vacancy, vacancy_id)
        except NoResultFound:
            raise ValueError("Config or Vacancy not found in the database.")

        if vacancy not in config.vacancies:
            config.vacancies.append(vacancy)
            await session.commit()
            return True
        else:
            return False
