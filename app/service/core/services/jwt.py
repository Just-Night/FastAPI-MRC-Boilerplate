from functools import wraps

from apps.auth.service import JWTToken
from fastapi import HTTPException, Request, WebSocket, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from apps.user.service import UserService

security = HTTPBearer()


def need_jwt(func):

    @wraps(func)
    async def decorated_function(request: Request, *args, **kwargs):
        credentials: HTTPAuthorizationCredentials = await security(request)

        token = credentials.credentials
        payload = await JWTToken.verify_access_token(token)

        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

        if await UserService.get_user_by_id(telegram_id=payload.get('user_uuid')) is False:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")

        request.state.payload = payload

        return await func(request, *args, **kwargs)

    return decorated_function


def ws_need_jwt(func):
    @wraps(func)
    async def decorated_function(websocket: WebSocket, *args, **kwargs):
        try:
            authorization: str = websocket.query_params.get('token')
            if not authorization:
                raise HTTPException(status_code=401, detail="Token is required")

            credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=authorization)
            token = credentials.credentials
            payload = await JWTToken.verify_access_token(token)

            if not payload:
                raise HTTPException(status_code=401, detail="Invalid or expired token")

            websocket.state.payload = payload

            return await func(websocket, *args, **kwargs)

        except HTTPException as http_exc:
            await websocket.close(code=http_exc.status_code)
            raise http_exc

        except Exception as exc:
            await websocket.close(code=1011)  # Internal Error
            raise exc

    return decorated_function
