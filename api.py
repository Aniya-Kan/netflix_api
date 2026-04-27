from fastapi import FastAPI, HTTPException
import pandas as pd
from sqlalchemy import create_engine, text
from passlib.context import CryptContext

app = FastAPI(title="Netflix API")


engine = create_engine("postgresql://aniya:root1234@localhost:5432/netflix_data")

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
    """))
    conn.commit()

@app.get("/")
def read_root():
    return {"message": "NETFLIX API"}


@app.get("/shows/search")
def search_movies(title: str = None, type: str = None, rating: str = None):
    query = "SELECT * FROM netflix_movies WHERE 1=1"
    params = {}

    if title:
        query += " AND title ILIKE :title"
        params["title"] = f"%{title}%"

    if type:
        query += " AND type = :type"
        params["type"] = type

    if rating:
        query += " AND rating = :rating"
        params["rating"] = rating

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn, params=params)

    return df.to_dict(orient="records")

@app.post("/register")
def register(username: str, password: str):
    hashed_password = pwd_context.hash(password)

    query = text("""
        INSERT INTO users (username, password_hash)
        VALUES (:username, :password_hash)
    """)

    try:
        with engine.connect() as conn:
            conn.execute(query, {
                "username": username,
                "password_hash": hashed_password
            })
            conn.commit()

        return {"message": "User registered successfully"}

    except Exception:
        raise HTTPException(status_code=400, detail="User already exists")


@app.post("/login")
def login(username: str, password: str):
    query = text("SELECT * FROM users WHERE username = :username")

    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"username": username})

    if df.empty:
        raise HTTPException(status_code=400, detail="Wrong username or password")

    stored_hash = df.loc[0, "password_hash"]

    if pwd_context.verify(password, stored_hash):
        return {"message": "Welcome"}
    else:
        raise HTTPException(status_code=400, detail="Wrong username or password")