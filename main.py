from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import models
from database import engine, get_db
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date
from uuid import UUID
import uuid
from dotenv import load_dotenv

load_dotenv()  # Ensure .env is loaded
load_dotenv('.env.local')  # Load .env.local for overrides

# Crée les tables dans Neon si elles n'existent pas
try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Could not create tables on startup: {e}")

app = FastAPI()

# Pydantic response model for Facture
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

# Pydantic schema for OnboardingRequest
class ApplianceOnboarding(BaseModel):
    name: str
    power: float

class OnboardingRequest(BaseModel):
    google_id: str
    email: str
    city: str
    primary_goal: str
    selected_appliances: List[ApplianceOnboarding]
    weekend_habits: bool  # surconso_weekend
    alert_preferences: bool  # alerte_smart_active

@app.get("/")
def home():
    return {"status": "Fatouraty API is Online"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Test database connectivity"""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

@app.get("/factures", response_model=List[FactureResponse])
def get_factures(db: Session = Depends(get_db)):
    try:
        factures = db.query(models.Facture).all()
        return factures
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/users/onboarding")
def onboarding(request: OnboardingRequest, db: Session = Depends(get_db)):
    try:
        # Find or create user
        user = db.query(models.User).filter(models.User.google_id == request.google_id).first()
        if not user:
            user = models.User(
                email=request.email,
                google_id=request.google_id,
                password_hash="",  # Placeholder, since auth not implemented
                nom="",  # Can be updated later
                ville=request.city,
                objectif_principal=request.primary_goal,
                surconso_weekend=request.weekend_habits,
                alerte_smart_active=request.alert_preferences,
                suggestion_heures_creuses=True  # Default
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # Update existing user
            user.ville = request.city
            user.objectif_principal = request.primary_goal
            user.surconso_weekend = request.weekend_habits
            user.alerte_smart_active = request.alert_preferences
            db.commit()

        # Get or create batiment
        batiment = db.query(models.Batiment).filter(models.Batiment.user_id == user.id).first()
        if not batiment:
            batiment = models.Batiment(
                user_id=user.id,
                nom="Maison principale",
                adresse="",
                surface_m2=100,  # Default
                objectif_mensuel_dh=500  # Default
            )
            db.add(batiment)
            db.commit()
            db.refresh(batiment)

        # Bulk insert appliances
        appliances = []
        for app in request.selected_appliances:
            appliance = models.Appareil(
                batiment_id=batiment.id,
                nom=app.name,
                puissance_w=app.power,
                heures_par_jour=8,  # Default
                actif=True,
                categorie="autre",
                est_ignorable=False
            )
            appliances.append(appliance)
        db.add_all(appliances)
        db.commit()

        # Calculate projected saving
        last_facture = db.query(models.Facture).filter(models.Facture.batiment_id == batiment.id).order_by(models.Facture.periode_mois.desc()).first()
        projected_saving = 0
        if last_facture and request.alert_preferences:
            projected_saving = last_facture.montant_dh * 0.2

        return {"projected_saving": projected_saving}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Include routers
from routes import factures, appareils
app.include_router(factures.router)
app.include_router(appareils.router)

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )