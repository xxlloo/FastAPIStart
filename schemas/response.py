from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse


class SuccessResponse(BaseModel):
    message: str


def success_response(
    message: str, status_code: int = status.HTTP_200_OK
) -> JSONResponse:
    """
    封装一个统一的成功无数据返回的接口
    :param message: 返回的消息内容
    :param status_code: HTTP 状态码，默认为 200
    :return: 返回一个 FastAPI 的 JSONResponse 对象
    """
    return JSONResponse(status_code=status_code, content={"message": message})
