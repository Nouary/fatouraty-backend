# FastAPI Fatouraty - Configuration Guide

## ✅ Fixed Issues

### 1. **500 Internal Server Error on /factures endpoint**
   - **Root Cause**: Network timeout connecting to Neon PostgreSQL server
   - **Solution**: Added SQLite support for local development

### 2. **Database Connection Timeout**
   - The system cannot connect to the Neon database server at `ep-mute-brook-alzeriuq-pooler.c-3.eu-central-1.aws.neon.tech`
   - This could be due to:
     - Firewall/ISP blocking connections to the EU-Central region
     - Geographic restrictions
     - Network connectivity issues

## 📋 Current Configuration

### Development (SQLite)
- **Default Mode**: SQLite (set in `.env`)
- **Database File**: `fatouraty.db`
- **No external dependencies needed**
- Perfect for local development and testing

### Production (Neon PostgreSQL)
- **Configuration File**: `.env.local` 
- **To Enable**: Set `DATABASE_MODE=neon` in `.env.local` ✓
- **Connection String**: Already configured with your Neon credentials

## 🚀 Running the Application

### Start the Server
```bash
uvicorn main:app --reload
```

### Test Endpoints
```bash
# Root endpoint
curl http://127.0.0.1:8000/

# Get all factures (empty list initially)
curl http://127.0.0.1:8000/factures

# API documentation
http://127.0.0.1:8000/docs
```

## 📊 Database Schema

### Facture (Invoice) Table
- `id` - Integer (Primary Key)
- `batiment_nom` - String (Building name, e.g., "Villa 1")
- `consommation_kwh` - Float (Energy consumption)
- `montant_ht` - Float (Invoice amount)
- `date_facture` - String (Invoice date, e.g., "2024-03")
- `zone_geo` - String (Geographic zone, e.g., "Fès-Meknès")

### Appareil (Device) Table
- `id` - Integer (Primary Key)
- `nom` - String (Device name)
- `type_appareil` - String (Device type)
- `numero_serie` - String (Serial number)
- `date_achat` - DateTime (Purchase date)

## 🔄 Switching Between SQLite and Neon

### Use SQLite (Development)
Edit `.env.local`:
```
DATABASE_MODE=sqlite
```

### Use Neon (Production)
Edit `.env.local`:
```
DATABASE_MODE=neon
NEON_DATABASE_URL=postgresql://neondb_owner:npg_lMb7pQ1WYdns@ep-mute-brook-alzeriuq-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require
```

## ⚠️ Troubleshooting Neon Connection Issues

If you encounter connection timeouts when using Neon:

1. **Check Network Connectivity**
   ```bash
   # Test if the Neon server is reachable
   ping ep-mute-brook-alzeriuq-pooler.c-3.eu-central-1.aws.neon.tech
   ```

2. **Check Firewall Settings**
   - Ensure port 5432 (PostgreSQL) is not blocked
   - Some ISPs or networks may block cloud database connections

3. **Verify Credentials**
   - Check that the connection string in `.env.local` is correct
   - Ensure no extra spaces or characters

4. **Use VPN**
   - If the server is unreachable, try connecting through a VPN

5. **Contact Neon Support**
   - Verify your database is running in Neon dashboard
   - Check if there are any access restrictions

## 📦 Project Dependencies
All dependencies are listed in `requirements.txt`:
- fastapi
- uvicorn[standard]
- sqlalchemy
- pydantic
- python-dotenv
- psycopg2-binary

## 🎯 API Endpoints

### Health Check
```
GET /health
```
Response: `{"status": "healthy", "database": "connected"}`

### Root
```
GET /
```
Response: `{"status": "Fatouraty API is Online"}`

### Get All Factures
```
GET /factures
```
Response: List of facture objects

### Interactive API Documentation
```
GET /docs
```
Opens Swagger UI for testing all endpoints

