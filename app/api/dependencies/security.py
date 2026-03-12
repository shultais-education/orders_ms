from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from typing import TypeAlias, Annotated
import jwt
from app.core.config import settings


security = HTTPBearer()

HTTPAuthorizationCredentialsDep: TypeAlias = Annotated[HTTPAuthorizationCredentials, Depends(security)]

def verify_token(credentials: HTTPAuthorizationCredentialsDep):
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": True, "verify_signature": True}
        )
        return payload
    except jwt.PyJWTError:
       raise HTTPException(status_code=401, detail="Invalid token")

JWTDep: TypeAlias = Annotated[dict, Depends(verify_token)]
