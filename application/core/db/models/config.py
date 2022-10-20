from application import db, marshmallow
from application.core.db.models.base import Base


class Config(Base):
   access_token = db.Column(db.String(255))

class ConfigSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Config
        include_fk = True