from typing import Any, List, Optional
from pydantic import BaseModel
import aiohttp
from config import IS_MAINNET, TONAPI_KEY


headers = {"Authorization": f"Bearer {TONAPI_KEY}"}


class TvmStackRecord(BaseModel):
    type: str
    num: Optional[str] = None
    cell: Optional[str] = None
    slice: Optional[str] = None
    tuple: Optional[List['TvmStackRecord']] = None


class MethodExecutionResult(BaseModel):
    success: bool
    exit_code: int
    stack: List[TvmStackRecord]
    decoded: Optional[Any] = None


class Tonapi:
    def __init__(self):
        self.base_url = f"https://{'testnet.' if not IS_MAINNET else ''}tonapi.io"

    async def execute_get_method(
        self,
        account_id: str,
        method_name: str,
        *args: Optional[str],
    ) -> MethodExecutionResult:
        """
        Execute get method for account.

        :param account_id: account ID
        :param method_name: contract get method name
        :param args: contract get method args
        :return: :class:`MethodExecutionResult`
        """
        method = f"/v2/blockchain/accounts/{account_id}/methods/{method_name}"
        query_params = "&".join(f"args={arg}" for arg in args)

        url = self.base_url + method
        if query_params:
            url += f"?{query_params}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    print(f"Error response: {await response.text()}")
                    raise Exception(
                        f"API request failed with status {response.status}")

                data = await response.json()
                return MethodExecutionResult(**data)
