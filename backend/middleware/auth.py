"""JWT Authentication Middleware"""
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from jose import jwt
from config import settings

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/auth/"):
            return await call_next(request)
        
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse({"detail": "Missing authorization header"}, status_code=401)
        
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                return JSONResponse({"detail": "Invalid auth scheme"}, status_code=401)
            
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            user_id = payload.get("user_id")
            if not user_id:
                return JSONResponse({"detail": "Invalid token"}, status_code=401)
            
            request.state.user_id = user_id
        except Exception as e:
            return JSONResponse({"detail": str(e)}, status_code=401)
        
        return await call_next(request)
