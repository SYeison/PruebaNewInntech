from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Voter(Base):
    __tablename__ = "voters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    has_voted = Column(Boolean, default=False, nullable=False)

    vote = relationship("Vote", back_populates="voter", uselist=False, cascade="all, delete-orphan")


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    party = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=True, index=True)
    votes = Column(Integer, default=0, nullable=False)

    received_votes = relationship("Vote", back_populates="candidate", cascade="all, delete-orphan")


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    voter_id = Column(Integer, ForeignKey("voters.id"), unique=True, nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)

    voter = relationship("Voter", back_populates="vote")
    candidate = relationship("Candidate", back_populates="received_votes")
