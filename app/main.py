from fastapi import FastAPI

import app.api.search as search_api
import app.api.user as user_api

app = FastAPI()

app.include_router(user_api.app)
app.include_router(search_api.app)
