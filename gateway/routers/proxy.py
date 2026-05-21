import httpx
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse

from gateway.config import INTERNAL_API_URL
from gateway.middleware.rate_limit import limiter

router = APIRouter(prefix="/gateway/v1")


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
)
@limiter.limit("10/minute")
async def proxy(request: Request, path: str):
    internal_url = f"{INTERNAL_API_URL}/api/v1/{path}"

    headers = {
        k: v
        for k, v in request.headers.items()
        if k.lower() not in {"host", "content-length", "transfer-encoding"}
    }
    headers["X-User-Cedula"] = request.state.user_cedula

    body = await request.body()
    params = dict(request.query_params)

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            resp = await client.request(
                method=request.method,
                url=internal_url,
                headers=headers,
                content=body or None,
                params=params,
            )
            return Response(
                status_code=resp.status_code,
                content=resp.content,
                media_type=resp.headers.get("content-type"),
            )
        except httpx.RequestError:
            return JSONResponse(
                status_code=502,
                content={
                    "detail": "Error de conexión con el servicio interno",
                    "code": "BAD_GATEWAY",
                },
            )
