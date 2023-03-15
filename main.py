import time

import uvicorn
import redis.asyncio as redis
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi_limiter import FastAPILimiter
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from src.database.db import get_db
from src.routes import auth, contacts, users
from src.config.config import settings


app = FastAPI()

origins = [
    "http://localhost:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')


@app.on_event("startup")
async def startup():
    """
    The startup function is called when the application starts.
    It's a good place to initialize things that are used by the app, such as databases or caches.
    Since we are making an async function so we need to add async keyword before the def keyword and
    we need to await the results of async tasks inside this function.

    :return: A dictionary with the following keys:
    """
    r = await redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
        encoding="utf-8",
        decode_responses=True
    )
    await FastAPILimiter.init(r)


@app.get("/", name="Main page")
def read_root():
    """
    The read_root function returns a dictionary with the key ;message&amp;quot; and value &amp;quot;Hello&amp;quot;.

    :return: A dictionary with the key ;message&amp;quot; and value &amp;quot;hello&amp;quot;
    """
    return {"message": "Hello! FastAPI Homework 2.12"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    The add_process_time_header function adds a header to the response called &quot;My-Process-Time&quot;
    that contains the time it took for this function to run. This is useful for debugging purposes.

    :param request: Request: Access the request object
    :param call_next: Call the next middleware in the chain
    :return: A response object with an additional header
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["My-Process-Time"] = str(process_time)
    return response


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    """
    The healthchecker function is a simple function that checks if the database is configured correctly.
    It does this by making a request to the database and checking if it returns any results. If it doesn't,
    it raises an HTTPException with status code 500 (Internal Server Error) and detail &quot;Database is not
    configured correctly&quot;. If there are no errors, then it returns {&quot;message&quot;: &quot;Hello! FastAPI Homework 2.12&quot;}.

    :param db: Session: Pass the database session to the function
    :return: A dictionary with the message &quot;hello! fastapi homework 2
    """
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        print(result)
        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Database is not configured correctly")
        return {"message": "Hello! FastAPI Homework 2.12"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error connecting to the database")


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)
