from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from gateway.middleware.auth import AuthMiddleware
from gateway.middleware.enforce_https import HTTPSEnforceMiddleware
from gateway.middleware.rate_limit import limiter
from gateway.middleware.verify_user import VerifyUserMiddleware
from gateway.routers.proxy import router as proxy_router

app = FastAPI(title="API Gateway - Sistema de Gestión de Adopciones de Mascotas")

app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def _rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Demasiadas solicitudes. Intente nuevamente en 1 minuto.",
            "code": "RATE_LIMIT_EXCEEDED",
        },
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(HTTPSEnforceMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(VerifyUserMiddleware)

app.include_router(proxy_router)
