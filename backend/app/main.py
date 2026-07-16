from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware

from app.core.rate_limit import limiter
from app.api.v1.auth import router as auth_router

app = FastAPI()
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.include_router(
    auth_router,
    prefix="/api/v1",
)
