from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.middleware.logging import setup_logging
import jwt
from conf import cnf

app = FastAPI(title="AI Resume Analysis", openapi_tags=[])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 鉴权中间件
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            r_dict = self.verify_jwt(credentials.credentials)
            if not r_dict.get("is_token_valid"):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return r_dict
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> dict:
        is_token_valid: bool = False
        user_uid = 0
        try:
            payload = jwt.decode(jwtoken, cnf.auth.jwt_secret, algorithms=["HS256"])
        except:
            payload = None

        # 如果token信息可以解，并且没有过期，那么token有效
        if payload:
            is_token_valid = True

        r = {
            "jwt_token": jwtoken,
            "is_token_valid": is_token_valid, 
            "user_uid": user_uid,
        }
        return r

setup_logging()
from src.actions.api.action import router as api_router
app.include_router(api_router, prefix="/api")
