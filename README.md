# MACE
Mining Automated Compliance Execution

# Installation process

 1. Install Visual Studio Code
 2. Install Docker Desktop and run it
 3. Install Git
 4. Clone the repository and open in Visual Studio Code
 5. Click on "Open In Container" if no pop-up appears use Ctrl + Shift + P and search "Rebuild dev container clear cache"


# Quick verification checklist

## Python dependency sanity
python3 -m pip check

## Node dependency sanity
npm ls --depth=0

## Port listeners
ss -tulnp | egrep ':(8000|5173|5432)'

## Backend health
curl http://localhost:8000/docs

## Frontend health
curl http://localhost:5173

## Database health
pg_isready -h localhost -p 5432


# Development Must Dos
Switch to "development" branch when writing code, do not push/merge in "main" branch.
