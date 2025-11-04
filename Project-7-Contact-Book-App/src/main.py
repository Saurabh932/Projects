from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from src.db.main import init_db
from src.contacts.routes import router


# Define app lifespan  (Startup and shutdown logic)
async def lifespan(app: FastAPI):
    print("🚀 Starting Contact Book API...")
    await init_db()  # Create tables if they don't exists
    yield
    print("🛑 Shutting down Contact Book API ...")


# Initializing Fastapi app
app = FastAPI(
    title="Contact Book App",
    description="An async contact management API with PostgreSQL",
    version="1.2.0",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Register routes
# app.include_router(router, prefix="/api/v2/contact", tags=["Contact"])
app.include_router(router)