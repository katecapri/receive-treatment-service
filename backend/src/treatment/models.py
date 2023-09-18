from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.dialects import postgresql

from src.init_database import Base


class Treatment(Base):
    __tablename__ = 'treatments'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True,  server_default=text("gen_random_uuid()"))
    last_name = Column(String(), nullable=False)
    first_name = Column(String(), nullable=False)
    patronymic = Column(String(), nullable=False)
    phone = Column(String(), nullable=False)
    treatment = Column(String(), nullable=False)
    creation_date = Column(DateTime(), nullable=False, server_default=text('clock_timestamp()'))
