from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware

from app.core.rate_limit import limiter
from app.api.v1.auth import router as auth_router
from app.api.v1.users import user_router as user_router
app = FastAPI()
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
)

app.include_router(
    user_router,
    prefix = "/api/v1/users"
)
