from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from app import settings

engine = create_engine(
    settings.POSTGRES_URL.replace("asyncpg", "psycopg2")
)

Base = automap_base()
Base.prepare(engine, reflect=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Company = Base.classes.companies
Cafe = Base.classes.cafes
Geodata = Base.classes.geodatas
Menu = Base.classes.menus
MenuEntry = Base.classes.menu_entries
Currency = Base.classes.currencies
