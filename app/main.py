from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.routes import auth, fuel, qr, repayment
from app.core.config import settings

# Seed database tables (use Alembic for production migrations)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WesePlus Microloans API",
    description="Production-ready backend for fuel credit and QR systems",
    version="1.0.0"
)

# CORS Configuration
origins = settings.ALLOWED_ORIGINS.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(fuel.router)
app.include_router(qr.router)
app.include_router(repayment.router)

@app.get("/")
async def root():
    return {
        "app": "WesePlus Microloans Backend",
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/debug/reset")
async def reset_db(db: Session = Depends(get_db)):
    from sqlalchemy import text
    db.execute(text("TRUNCATE TABLE fuel_loans, qr_codes, transactions, vehicles, users CASCADE"))
    db.commit()
    return {"message": "Database cleared! You have a fresh start."}

# In production, use gunicorn to run the application
