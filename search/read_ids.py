import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()


engine = create_engine(os.environ['DB_CONNECTION_STRING'])

def read_collection_ids():
    with engine.connect() as connection:
        query = text("SELECT id FROM langchain_pg_embedding")
        result = connection.execute(query)

        return [row[0] for row in result]
    