from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = Field(..., alias="DATABASE_URL")
    
    # Security
    SECRET_KEY: str = Field(..., alias="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    ALLOWED_ORIGINS: str = Field("*", alias="ALLOWED_ORIGINS")
    
    # Firebase
    FIREBASE_CREDENTIALS_PATH: str = Field(..., alias="FIREBASE_CREDENTIALS_PATH")
    
    # Business Rules
    PRICE_PER_LITRE: float = 2.50
    MAX_LITRES_PER_DAY: int = 10
    QR_EXPIRY_HOURS: int = 2
    SERVICE_FEE_PERCENTAGE: float = 0.10

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
