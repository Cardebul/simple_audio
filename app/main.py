from fastapi import FastAPI

from app.routers import audio, auth, su_router, users

app = FastAPI()

app.include_router(audio.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(su_router.router)
