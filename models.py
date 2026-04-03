from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Boolean, Date, CheckConstraint, UniqueConstraint, Index, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    nom = Column(String)
    ville = Column(String, default="Fès")
    type_client = Column(String, default="particulier")
    objectif_principal = Column(String)
    surconso_weekend = Column(Boolean, default=False)
    alerte_smart_active = Column(Boolean, default=True)
    suggestion_heures_creuses = Column(Boolean, default=True)
    google_id = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=func.now())

    __table_args__ = (
        CheckConstraint("type_client IN ('particulier', 'pme')"),
    )

class Batiment(Base):
    __tablename__ = "batiments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    nom = Column(String, nullable=False)
    adresse = Column(String)
    surface_m2 = Column(Numeric(8, 2))
    objectif_mensuel_dh = Column(Numeric(10, 2), default=0)
    created_at = Column(DateTime, default=func.now())

class Facture(Base):
    __tablename__ = "factures"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batiment_id = Column(UUID(as_uuid=True), ForeignKey("batiments.id", ondelete="CASCADE"), nullable=False)
    periode_mois = Column(Date, nullable=False)
    montant_dh = Column(Numeric(10, 2), nullable=False)
    consommation_kwh = Column(Numeric(10, 2))
    prix_kwh = Column(Numeric(6, 4))
    source = Column(String, default="manuel")
    ocr_texte_brut = Column(String)
    created_at = Column(DateTime, default=func.now())

    __table_args__ = (
        CheckConstraint("source IN ('manuel', 'ocr', 'pdf')"),
        UniqueConstraint('batiment_id', 'periode_mois'),
        Index('idx_factures_batiment_date', 'batiment_id', 'periode_mois'),
    )

class Appareil(Base):
    __tablename__ = "appareils"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batiment_id = Column(UUID(as_uuid=True), ForeignKey("batiments.id", ondelete="CASCADE"), nullable=False)
    nom = Column(String, nullable=False)
    puissance_w = Column(Numeric(8, 2), nullable=False)
    heures_par_jour = Column(Numeric(4, 2), default=8)
    actif = Column(Boolean, default=True)
    categorie = Column(String)
    est_ignorable = Column(Boolean, default=False)

    __table_args__ = (
        CheckConstraint("categorie IN ('climatisation', 'chauffage', 'eclairage', 'refrigeration', 'production', 'autre')"),
        Index('idx_appareils_batiment', 'batiment_id'),
    )

class Alerte(Base):
    __tablename__ = "alertes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batiment_id = Column(UUID(as_uuid=True), ForeignKey("batiments.id", ondelete="CASCADE"), nullable=False)
    type_alerte = Column(String, nullable=False)
    message = Column(String, nullable=False)
    valeur_actuelle = Column(Numeric(10, 2))
    valeur_seuil = Column(Numeric(10, 2))
    lue = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    __table_args__ = (
        Index('idx_alertes_batiment_lue', 'batiment_id', 'lue'),
    )

class VilleSolaire(Base):
    __tablename__ = "villes_solaire"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ville = Column(String, unique=True, nullable=False)
    irradiation_kwh_m2 = Column(Numeric(5, 2))
    score_solaire = Column(Integer)
    roi_annees = Column(Numeric(4, 1))
    region = Column(String)

    __table_args__ = (
        CheckConstraint("score_solaire BETWEEN 0 AND 100"),
    )