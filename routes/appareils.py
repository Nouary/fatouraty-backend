from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Appareil
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AppareilCreate(BaseModel):
    batiment_id: UUID
    nom: str
    puissance_w: float
    heures_par_jour: float = 8.0
    actif: bool = True
    categorie: str

class AppareilResponse(BaseModel):
    id: UUID
    batiment_id: UUID
    nom: str
    puissance_w: float
    heures_par_jour: float
    actif: bool
    categorie: str

    model_config = ConfigDict(from_attributes=True)

@router.post("/appareils/", response_model=AppareilResponse)
def create_appareil(appareil: AppareilCreate, db: Session = Depends(get_db)):
    db_appareil = Appareil(**appareil.dict())
    db.add(db_appareil)
    db.commit()
    db.refresh(db_appareil)
    return db_appareil

@router.get("/appareils/", response_model=List[AppareilResponse])
def read_appareils(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appareils = db.query(Appareil).offset(skip).limit(limit).all()
    return appareils

@router.get("/appareils/{appareil_id}", response_model=AppareilResponse)
def read_appareil(appareil_id: UUID, db: Session = Depends(get_db)):
    appareil = db.query(Appareil).filter(Appareil.id == appareil_id).first()
    if appareil is None:
        raise HTTPException(status_code=404, detail="Appareil not found")
    return appareil