from app.database import engine, Base, SessionLocal
from app.db_models import Building, Unit

# Create a session
session = SessionLocal()

# Clear ALL data from ALL tables
session.query(Unit).delete()
session.query(Building).delete()

# Recreate tables after dropping them (if needed)
Base.metadata.create_all(engine)

# Commit changes and close the session
session.commit()
session.close()
