import uuid
from fastapi import FastAPI, HTTPException, status, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

"""
Import our tools
This is the database connection file
"""
from db import engine
from config import settings

from models.users import User, UserCreate, UserRead, UserUpdate, auth_backend, current_active_user, fastapi_users

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

"""
Setup our origins...
...for now it's just our local environments
"""
origins = [
    "http://localhost:5173"
]

"""
Add the CORS middleware, it will pass the proper CORS headers
- https://fastapi.tiangolo.com/tutorial/middleware/
- https://fastapi.tiangolo.com/tutorial/cors/
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""
FastAPI Users is going to give us all of our auth routes,
The `prefix` is the url that will precede each url.

These settings will generate these routes:
- auth/register
- auth/login
- auth/logout
"""
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

"""
We now return you to your regular routes.
"""
@app.get("/")
def home():
    return {"message": "Root Route"}


"""
This is a demo protected route, it will only
return the response if a user is authenticated.
"""
@app.get("/authenticated-route-demo")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


