# Import all models and Base to ensure they are registered on Metadata for table creation
from app.database.connection import Base
from app.database.models.camera import Camera
from app.database.models.violation import Violation
from app.database.models.email_log import EmailLog
from app.database.models.evidence import Evidence
