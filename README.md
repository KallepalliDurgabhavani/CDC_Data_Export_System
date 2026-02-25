# CDC Export System

## Run
```bash
docker-compose up --build

API

GET /health

POST /exports/full

POST /exports/incremental

POST /exports/delta

GET /exports/watermark

Tests
pytest --cov

---

# ✅ HOW TO RUN

```bash
docker-compose up --build

Test API:

curl http://localhost:8080/health

Full export:

curl -X POST http://localhost:8080/exports/full -H "X-Consumer-ID: consumer-1""# CDC_Data_Export_System" 
