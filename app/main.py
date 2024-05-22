from fastapi import FastAPI

from app.core.db.db import DB
from app.api.http import v1

app = FastAPI()
setattr(app.state, "db", DB())
setattr(app.state, "transactions", {})

app.include_router(v1)
