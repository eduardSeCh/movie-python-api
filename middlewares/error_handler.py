from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, ) -> None:
        super().__init__(app)
    
    # detect errors
    async def dispatch(self, request: Request, call_next) -> Response or JSONResponse:
        try:
            return await call_next(request) #no hay error, pasa a siguiente llamada
        except Exception as e:
            return JSONResponse(status_code=500, content={'error': str(e)}) 