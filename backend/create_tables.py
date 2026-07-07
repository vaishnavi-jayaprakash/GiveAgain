from app.db.database import Base, engine

# Import all models so they get registered
import app.models

print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("Done!")