from sqlmodel import create_engine

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/web_fitness"


engine = create_engine(DATABASE_URL, echo=True)
