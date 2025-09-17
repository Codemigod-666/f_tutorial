import os
# from supabase import create_client, Client
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL=os.getenv("EXTERNAL_DATABASE_URL")

Base = declarative_base()

# CREATE ENGINE
engine = create_engine(DATABASE_URL)

# create a session 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for fastAPI 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def get_supabase_client() -> Client:
#     """
#     Creates and returns a Supabase client. 

#     This function retrieves the Supabase URL and key from environment variables,
#     which is a best practice for handling sensitive credentials. 

#     Returns: 
#         Client: An instance of the Supabase client.
#     """

#     try:
#         url: str = os.environ.get("PROJECT_URL")
#         key: str = os.environ.get("API_KEY")
#         # print(url, key, "url and key")

#         if not url or not key:
#             raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set as environment variables.")
        
#         supabase_client: Client = create_client(url, key)
#         print(supabase_client, "client")
#         return supabase_client
    
#     except Exception as e:
#         print(f"Error creating Supabase client: {e}")
#         return None

