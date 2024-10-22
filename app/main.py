from fastapi import FastAPI

import app.api.article as article_api
import app.api.user as user_api

app = FastAPI()

app.include_router(user_api.app)
app.include_router(article_api.app)
