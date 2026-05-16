from fastapi import FastAPI
from app.database import engine, Base
from app.routes.product import router as product_router
from app.routes.auth import router as auth_router
from config.settings import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)


app.include_router(product_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Hello BuildLabs!"}

try: 
    connection = engine.connect()
    print("Database connection successful, Test complete!")
    connection.close()
except Exception as e:
    print(f"Database connection failed: {e}")
