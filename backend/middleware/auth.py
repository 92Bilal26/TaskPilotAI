"""JWT authentication middleware"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from config import settings
import logging

logger = logging.getLogger(__name__)


class JWTAuthMiddleware(BaseHTTPMiddleware):
    """Middleware to verify JWT tokens in Authorization header"""

    async def dispatch(self, request: Request, call_next):
        """Process request and verify JWT token"""
        public_routes = ["/docs", "/openapi.json", "/health", "/auth/signup", "/auth/signin"]
        
        if request.url.path in public_routes:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Missing authorization header")

        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=401, detail="Invalid authorization scheme")

            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            request.state.user_id = payload.get("user_id")

        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid authorization header")

        return await call_next(request)
