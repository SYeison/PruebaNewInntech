from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas


def _name_matches(a: str, b: str) -> bool:
    return a.strip().lower() == b.strip().lower()


# ---------- Voter ----------

def create_voter(db: Session, voter_in: schemas.VoterCreate) -> models.Voter:
    if db.query(models.Voter).filter(models.Voter.email == voter_in.email).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "Ya existe un votante con ese email")

    candidates = db.query(models.Candidate).all()
    for candidate in candidates:
        if _name_matches(candidate.name, voter_in.name) or (
            candidate.email and candidate.email == voter_in.email
        ):
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "Esta persona ya está registrada como candidato; no puede ser también votante",
            )

    voter = models.Voter(name=voter_in.name, email=voter_in.email)
    db.add(voter)
    db.commit()
    db.refresh(voter)
    return voter


def get_voters(db: Session) -> list[models.Voter]:
    return db.query(models.Voter).all()


def get_voter(db: Session, voter_id: int) -> models.Voter:
    voter = db.query(models.Voter).filter(models.Voter.id == voter_id).first()
    if not voter:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Votante no encontrado")
    return voter


def delete_voter(db: Session, voter_id: int) -> None:
    voter = get_voter(db, voter_id)
    db.delete(voter)
    db.commit()


# ---------- Candidate ----------

def create_candidate(db: Session, candidate_in: schemas.CandidateCreate) -> models.Candidate:
    if candidate_in.email:
        if db.query(models.Candidate).filter(models.Candidate.email == candidate_in.email).first():
            raise HTTPException(status.HTTP_409_CONFLICT, "Ya existe un candidato con ese email")

    voters = db.query(models.Voter).all()
    for voter in voters:
        if _name_matches(voter.name, candidate_in.name) or (
            candidate_in.email and voter.email == candidate_in.email
        ):
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "Esta persona ya está registrada como votante; no puede ser también candidato",
            )

    candidate = models.Candidate(
        name=candidate_in.name, party=candidate_in.party, email=candidate_in.email
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate


def get_candidates(db: Session) -> list[models.Candidate]:
    return db.query(models.Candidate).all()


def get_candidate(db: Session, candidate_id: int) -> models.Candidate:
    candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Candidato no encontrado")
    return candidate


def delete_candidate(db: Session, candidate_id: int) -> None:
    candidate = get_candidate(db, candidate_id)
    db.delete(candidate)
    db.commit()


# ---------- Vote ----------

def cast_vote(db: Session, vote_in: schemas.VoteCreate) -> models.Vote:
    voter = get_voter(db, vote_in.voter_id)
    candidate = get_candidate(db, vote_in.candidate_id)

    if voter.has_voted:
        raise HTTPException(status.HTTP_409_CONFLICT, "Este votante ya emitió su voto")

    vote = models.Vote(voter_id=voter.id, candidate_id=candidate.id)
    voter.has_voted = True
    candidate.votes += 1

    db.add(vote)
    db.add(voter)
    db.add(candidate)
    db.commit()
    db.refresh(vote)
    return vote


def get_votes(db: Session) -> list[models.Vote]:
    return db.query(models.Vote).all()


def get_statistics(db: Session) -> schemas.StatisticsResponse:
    candidates = db.query(models.Candidate).all()
    total_votes = sum(c.votes for c in candidates)
    total_voters_voted = db.query(func.count(models.Voter.id)).filter(
        models.Voter.has_voted.is_(True)
    ).scalar()

    results = [
        schemas.CandidateStat(
            candidate_id=c.id,
            name=c.name,
            votes=c.votes,
            percentage=round((c.votes / total_votes * 100), 2) if total_votes > 0 else 0.0,
        )
        for c in candidates
    ]

    return schemas.StatisticsResponse(
        total_votes=total_votes,
        total_voters_voted=total_voters_voted,
        results=results,
    )
