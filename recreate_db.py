#!/usr/bin/env python3

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import fresh
from database import engine
from models import Base

# Drop all tables first
Base.metadata.drop_all(bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)

print("Database recreated successfully")

# Verify
from models import Facture
print(f"Facture columns: {[c.name for c in Facture.__table__.columns]}")