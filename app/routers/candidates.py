from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.security import get_current_user

router = APIRouter(
    prefix="/candidates", tags=["Candidates"], dependencies=[Depends(get_current_user)]
)


@router.post("", response_model=schemas.CandidateResponse, status_code=status.HTTP_201_CREATED)
def create_candidate(candidate_in: schemas.CandidateCreate, db: Session = Depends(get_db)):
    return crud.create_candidate(db, candidate_in)


@router.get("", response_model=list[schemas.CandidateResponse])
def list_candidates(db: Session = Depends(get_db)):
    return crud.get_candidates(db)


@router.get("/{candidate_id}", response_model=schemas.CandidateResponse)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    return crud.get_candidate(db, candidate_id)


@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    crud.delete_candidate(db, candidate_id)
