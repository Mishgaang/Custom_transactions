from fastapi import FastAPI

from app.core.db.db import DB
from app.api.http import v1

app = FastAPI()
setattr(app.state, "db", DB())
setattr(app.state, "transactions", {})

app.include_router(v1)


import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host='0.0.0.0', port=8082, reload=True)
