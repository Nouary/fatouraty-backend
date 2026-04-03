from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Facture
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date
from uuid import UUID

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class FactureCreate(BaseModel):
    batiment_id: UUID
    periode_mois: date
    montant_dh: float
    consommation_kwh: Optional[float] = None
    prix_kwh: Optional[float] = None
    source: str = "manuel"
    ocr_texte_brut: Optional[str] = None

class FactureResponse(BaseModel):
    id: UUID
    batiment_id: UUID
    periode_mois: date
    montant_dh: float
    consommation_kwh: Optional[float]
    prix_kwh: Optional[float]
    source: str
    ocr_texte_brut: Optional[str]
    created_at: Optional[str]

    model_config = ConfigDict(from_attributes=True)

@router.post("/factures/", response_model=FactureResponse)
def create_facture(facture: FactureCreate, db: Session = Depends(get_db)):
    db_facture = Facture(**facture.dict())
    db.add(db_facture)
    db.commit()
    db.refresh(db_facture)
    return db_facture

@router.get("/factures/", response_model=List[FactureResponse])
def read_factures(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    factures = db.query(Facture).offset(skip).limit(limit).all()
    return factures

@router.get("/factures/{facture_id}", response_model=FactureResponse)
def read_facture(facture_id: UUID, db: Session = Depends(get_db)):
    facture = db.query(Facture).filter(Facture.id == facture_id).first()
    if facture is None:
        raise HTTPException(status_code=404, detail="Facture not found")
    return facture