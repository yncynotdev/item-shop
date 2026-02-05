import jwt
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config.env import (
    BETTER_AUTH_URL,
    JWKS_URL,
    JWT_ALGORITHM
)


router = APIRouter()


@router.get("/api/auth/verify")
def verify_auth(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    jwk_url = f"{BETTER_AUTH_URL}/{JWKS_URL}"

    token = credentials.credentials
    jwk = jwt.PyJWKClient(jwk_url)

    signing_key = jwk.get_signing_key_from_jwt(token).key

    try:
        payload = jwt.decode(
            jwt=token,
            key=signing_key,
            algorithms=[JWT_ALGORITHM],
            audience=[BETTER_AUTH_URL]
        )

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user id"
            )
        return {"user_id": user_id, "payload": payload}

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        print(f"DEBUG JWT Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
