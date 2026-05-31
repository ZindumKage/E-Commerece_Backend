from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import engine, Base
from app.routes.product import router as product_router
from app.routes.auth import router as auth_router
from app.routes.order import router as order_router
from app.routes.payment import router as payment_router
from app.routes.webhook import router as webhook_router

from config.settings import settings
from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        connection = engine.connect()

        logger.info("Database connected successfully")

        connection.close()

    except Exception as e:
        logger.error(f"Database connection failed: {e}")

    yield

    logger.info("Application shutting down")


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
)

# Temporary during development, replace with Alembic later
Base.metadata.create_all(bind=engine)

app.include_router(product_router)
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(webhook_router)

@app.get("/")
def root():
    logger.info("Root endpoint accessed")

    return {"message": "Hello BuildLabs!"}
