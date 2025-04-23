import uvicorn

from fastapi.exceptions import HTTPException, RequestValidationError
from pydantic import BaseModel
from starlette.responses import JSONResponse

from main import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
