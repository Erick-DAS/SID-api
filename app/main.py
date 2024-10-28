from fastapi import FastAPI

import app.api.article as article_api
import app.api.user as user_api
import app.api.version as version_api

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
]

app = FastAPI(debug=True, openapi_tags=tags_metadata)

app.include_router(prefix="/users", router=user_api.app, tags=["Users"])
app.include_router(prefix="/articles", router=article_api.app, tags=["Articles"])
app.include_router(prefix="/versions", router=version_api.app, tags=["Versions"])
