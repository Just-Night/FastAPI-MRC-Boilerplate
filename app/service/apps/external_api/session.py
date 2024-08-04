from aiohttp.client import ClientSession


class ExternalApiSession(ClientSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers.update({
            'Content-Type': 'application/json'
        })
