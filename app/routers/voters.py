from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.security import get_current_user

router = APIRouter(prefix="/voters", tags=["Voters"], dependencies=[Depends(get_current_user)])


@router.post("", response_model=schemas.VoterResponse, status_code=status.HTTP_201_CREATED)
def create_voter(voter_in: schemas.VoterCreate, db: Session = Depends(get_db)):
    return crud.create_voter(db, voter_in)


@router.get("", response_model=list[schemas.VoterResponse])
def list_voters(db: Session = Depends(get_db)):
    return crud.get_voters(db)


@router.get("/{voter_id}", response_model=schemas.VoterResponse)
def get_voter(voter_id: int, db: Session = Depends(get_db)):
    return crud.get_voter(db, voter_id)


@router.delete("/{voter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_voter(voter_id: int, db: Session = Depends(get_db)):
    crud.delete_voter(db, voter_id)
