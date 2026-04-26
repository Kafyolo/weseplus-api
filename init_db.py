import warnings
# Suppress SQLAlchemy 2.0 warnings for clean output
warnings.filterwarnings("ignore")

import sys
from app.core.database import Base, engine
from app.models import user, vehicle, loan, coupon, transaction, audit

def init_db():
    print("Connecting to Supabase and establishing schema...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Success! All tables have been created in the remote Supabase PostgreSQL instance.")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_db()
