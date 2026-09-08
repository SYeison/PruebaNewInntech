from pydantic import BaseModel, ConfigDict, EmailStr


# ---------- Auth ----------

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Voter ----------

class VoterCreate(BaseModel):
    name: str
    email: EmailStr


class VoterResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    has_voted: bool

    model_config = ConfigDict(from_attributes=True)


# ---------- Candidate ----------

class CandidateCreate(BaseModel):
    name: str
    party: str | None = None
    email: EmailStr | None = None


class CandidateResponse(BaseModel):
    id: int
    name: str
    party: str | None
    email: EmailStr | None
    votes: int

    model_config = ConfigDict(from_attributes=True)


# ---------- Vote ----------

class VoteCreate(BaseModel):
    voter_id: int
    candidate_id: int


class VoteResponse(BaseModel):
    id: int
    voter_id: int
    candidate_id: int

    model_config = ConfigDict(from_attributes=True)


# ---------- Statistics ----------

class CandidateStat(BaseModel):
    candidate_id: int
    name: str
    votes: int
    percentage: float


class StatisticsResponse(BaseModel):
    total_votes: int
    total_voters_voted: int
    results: list[CandidateStat]
