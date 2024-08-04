from abc import abstractmethod, ABC
from urllib.parse import urljoin

from aiohttp.client import ClientSession

from apps.external_api import session


class BaseExternalApiRequestInterface(ABC):
    METHOD: str
    SESSION: ClientSession
    HOST: str
    ENDPOINT: str

    @property
    def url(self) -> str:
        url = urljoin(self.HOST, self.ENDPOINT)
        return url

    @abstractmethod
    async def _execute_request(self) -> tuple[int, dict]:
        raise NotImplementedError('"_execute_request" method has to be implemented')

    async def run(self) -> tuple[int, dict]:
        return await self._execute_request()


class BaseExternalPayloadApiRequest(BaseExternalApiRequestInterface):
    SESSION: ClientSession = session.ExternalApiSession

    def __init__(self, payload: dict = None, params: dict = None, path_params: dict = None):
        self.payload = payload
        self.params = params
        self.path_params = path_params

    @property
    def url(self) -> str:
        url = urljoin(self.HOST, self.ENDPOINT)
        if self.path_params:
            url = url.format(**self.path_params)
        return url

    async def _execute_request(self):
        async with self.SESSION() as s:
            resp = await s.request(
                method=self.METHOD,
                url=self.url,
                json=self.payload,
                params=self.params
            )
            return resp.status, await resp.json()
