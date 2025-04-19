# clients/http_client.py

import time
from typing import Dict, Optional, Tuple, Union

import backoff
import httpx

from utils.logger import logger


def default_backoff():
    return backoff.on_exception(
        backoff.expo,
        httpx.RequestError,
        max_tries=3,
    )


class HttpClient:
    def __init__(
        self,
        timeout: float = 10.0,
        base_url: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        auth: Optional[Tuple[str, str]] = None,
        log_response_length: int = 200,
    ):
        self.client = httpx.AsyncClient(
            timeout=timeout,
            base_url=base_url or "",
            headers=headers,
            cookies=cookies,
            auth=auth,
        )
        self.log_response_length = log_response_length

    @staticmethod
    def _log_request(method: str, url: str, **kwargs):
        logger.debug(f"➡️ Request: {method.upper()} {url}")
        for key in ["params", "data", "json", "headers"]:
            if key in kwargs:
                logger.debug(f"{key.capitalize()}: {kwargs[key]}")

    def _log_response(self, response: httpx.Response, elapsed: float):
        logger.debug(f"⬅️ Response [{response.status_code}] in {elapsed:.2f}s")
        logger.debug(f"Response Text: {response.text[:self.log_response_length]}")

    async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        self._log_request(method, url, **kwargs)
        start = time.time()
        response = None
        try:
            response = await self.client.request(method, url, **kwargs)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"❌ {method.upper()} 请求失败: {e}")
            raise
        finally:
            if response:
                self._log_response(response, time.time() - start)
        return response

    @default_backoff()
    async def get(self, url: str, **kwargs) -> httpx.Response:
        return await self._request("GET", url, **kwargs)

    @default_backoff()
    async def post(self, url: str, **kwargs) -> httpx.Response:
        return await self._request("POST", url, **kwargs)

    async def upload_file(
        self,
        url: str,
        files: Dict[str, Union[Tuple[str, bytes], Tuple[str, bytes, str]]],
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        self._log_request("POST FILE", url, files=files, headers=headers)
        start = time.time()
        response = None
        try:
            response = await self.client.post(url, files=files, headers=headers)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"❌ 文件上传失败: {e}")
            raise
        finally:
            if response:
                self._log_response(response, time.time() - start)
        return response

    async def close(self):
        await self.client.aclose()
