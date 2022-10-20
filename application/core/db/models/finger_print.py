from application import db, marshmallow
from application.core.db.models.base import Base


class FingerPrintData(Base):
   client_id = db.Column(db.String(255))

class FingerPrintDataSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = FingerPrintData
        include_fk = True