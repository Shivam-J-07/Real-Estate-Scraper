from sqlalchemy.orm import Session
from datetime import datetime

from backend.db_models import Unit

def delete_units_by_timestamp(db: Session, timestamp: datetime):
    try:
        db.query(Unit).filter(Unit.timestamp == timestamp).delete()
        db.commit()
    except Exception as e:
        print(f"An error occurred while deleting units by timestamp: {e}")
