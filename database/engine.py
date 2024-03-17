from sqlalchemy.ext.asyncio import create_async_engine

import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
