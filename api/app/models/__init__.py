from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import Base

from .client import Client
from .provider import Provider
from .task import Task
from .category import Category
from .user import User