from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.security import get_current_user

router = APIRouter(prefix="/votes", tags=["Votes"], dependencies=[Depends(get_current_user)])


@router.post("", response_model=schemas.VoteResponse, status_code=status.HTTP_201_CREATED)
def cast_vote(vote_in: schemas.VoteCreate, db: Session = Depends(get_db)):
    return crud.cast_vote(db, vote_in)


@router.get("/statistics", response_model=schemas.StatisticsResponse)
def statistics(db: Session = Depends(get_db)):
    return crud.get_statistics(db)


@router.get("", response_model=list[schemas.VoteResponse])
def list_votes(db: Session = Depends(get_db)):
    return crud.get_votes(db)
