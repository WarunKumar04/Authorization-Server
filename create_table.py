# create_tables.py
from app.database import Base, engine

Base.metadata.create_all(bind=engine)
print("✅ MySQL users table created.")
