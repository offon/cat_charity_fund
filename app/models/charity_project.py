from sqlalchemy import Column, String, Text

from app.core.db import Base, ProjectDonation


class CharityProject(Base, ProjectDonation):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
