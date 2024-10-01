from fastapi import FastAPI

import app.api.user as user_api

app = FastAPI()

app.include_router(user_api.app)
