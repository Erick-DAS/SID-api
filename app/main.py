from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.api.article as article_api
import app.api.user as user_api
import app.api.version as version_api
import app.api.data as data_api

tags_metadata = [
    {
        "name": "Users",
        "description": "_Manage users_",
    },
    {
        "name": "Articles",
        "description": "_Manage articles_",
    },
    {
        "name": "Versions",
        "description": "_Manage article versions_",
    },
    {
        "name": "Data",
        "description": "_Access external data_",
    },
]

origins = [
    "https://sid-webpage.vercel.app",
    "http://localhost",
    "http://localhost:3000",
]

app = FastAPI(debug=True, openapi_tags=tags_metadata)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use origins=origins to allow only the specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow every HTTP method
    allow_headers=["*"],
)

app.include_router(prefix="/users", router=user_api.app, tags=["Users"])
app.include_router(prefix="/articles", router=article_api.app, tags=["Articles"])
app.include_router(prefix="/versions", router=version_api.app, tags=["Versions"])
app.include_router(prefix="/data", router=data_api.app, tags=["Data"])
