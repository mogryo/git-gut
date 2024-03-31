"""ORM classes for GitStat"""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Integer, String, Float
from orm.base import Base


# pylint: disable = too-few-public-methods
class GitStat(Base):
    """Table containing all columns information for printing to user"""
    __tablename__ = "GitStat"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, nullable=False, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(), nullable=True)
    commitcount: Mapped[int] = mapped_column(Integer(), nullable=True)
    mfauthor: Mapped[str] = mapped_column(String(), nullable=True)
    maauthor: Mapped[str] = mapped_column(String(), nullable=True)
    mdauthor: Mapped[str] = mapped_column(String(), nullable=True)
    daratio: Mapped[float] = mapped_column(Float(), nullable=True)
    linecount: Mapped[int] = mapped_column(Integer(), nullable=True)
