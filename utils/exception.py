from fastapi.exceptions import HTTPException, RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from main import app


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details = []
    for error in exc.errors():
        field = error.get("loc")[-1]  # 错误字段
        msg = error.get("msg")  # 错误信息

        if "gt" in error.get("ctx", {}):
            msg = f"{field} should be greater than {error['ctx']['gt']}"

        error_details.append({"field": field, "message": msg})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"code": 422, "detail": error_details},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
        headers=exc.headers,
    )
