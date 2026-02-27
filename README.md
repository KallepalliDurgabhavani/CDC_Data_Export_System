CDC Incremental Export System (Production-Ready)

👤 Author: Kallepalli Durga Bhavani
💼 Backend Development | Data Engineering

🧠 Project Overview

This project implements a production-ready, containerized Change Data Capture (CDC) export system that efficiently synchronizes large datasets using timestamp-based watermarking.

Instead of exporting the full database repeatedly, the system exports only new or updated records using incremental and delta export strategies — a common real-world data pipeline pattern.

The system includes:

✔ Incremental & Delta export strategies

✔ Per-consumer watermark tracking

✔ Asynchronous export jobs

✔ Structured logging

✔ Automated seeding of 100,000+ records

✔ Fully containerized deployment using Docker

⚙️ Tech Stack
Category	Tools
Backend	FastAPI (Python)
Database	PostgreSQL
ORM	SQLAlchemy
Containerization	Docker, Docker Compose
Data Processing	Pandas
Testing	Pytest
Logging	Python Logging (Structured JSON-style logs)
🏗️ System Architecture
Client 
   ↓
FastAPI API
   ↓
Background Export Worker
   ↓
PostgreSQL
   ↓
CSV Export Files (Docker Volume Mounted)
Key Components

users table → Stores user data with CDC metadata

watermarks table → Tracks last exported timestamp per consumer

Async export jobs → Prevent API blocking

Docker volume → Persists exported CSV files

📂 Project Structure
cdc-export-system/
│
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── export_service.py
│   ├── database.py
│   ├── models.py
│
├── seeds/
│   ├── schema.sql
│   ├── seed.py
│   ├── seed.sh
│
├── tests/
│   ├── test_health.py
│
├── output/               # Exported CSV files (gitignored)
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
🚀 Setup Instructions
1️⃣ Clone Repository
git clone <your-repo-url>
cd cdc-export-system
2️⃣ Create .env File
cp .env.example .env
3️⃣ Run with Docker
docker compose up --build

The system will:

Start PostgreSQL

Create tables automatically

Seed 100,000+ users

Start FastAPI server on port 8080

🌐 API Endpoints
✅ Health Check

GET /health

{
  "status": "ok",
  "timestamp": "2026-02-25T10:00:00Z"
}
📤 Full Export

POST /exports/full
Header: X-Consumer-ID: consumer-1

{
  "jobId": "uuid",
  "status": "started",
  "exportType": "full",
  "outputFilename": "full_consumer-1_20260225.csv"
}
🔁 Incremental Export

POST /exports/incremental
Header: X-Consumer-ID: consumer-1

Exports rows where:

updated_at > last_exported_at
🔄 Delta Export

POST /exports/delta
Header: X-Consumer-ID: consumer-1

CSV includes additional column:

operation = INSERT | UPDATE | DELETE
🧭 Get Watermark

GET /exports/watermark
Header: X-Consumer-ID: consumer-1

{
  "consumerId": "consumer-1",
  "lastExportedAt": "2026-02-25T10:05:00Z"
}
📁 Export Output

Exported files are stored in:

./output/

Example files:

full_consumer-1_20260225.csv
incremental_consumer-1_20260225.csv
delta_consumer-1_20260225.csv
🗄️ Database Schema
users table
Column	Type
id	BIGSERIAL PRIMARY KEY
name	VARCHAR
email	UNIQUE
created_at	TIMESTAMP
updated_at	TIMESTAMP
is_deleted	BOOLEAN

Index:

CREATE INDEX idx_users_updated_at ON users(updated_at);
watermarks table
Column	Type
id	SERIAL
consumer_id	UNIQUE
last_exported_at	TIMESTAMP
updated_at	TIMESTAMP
🧪 Running Tests
docker compose exec app pytest --cov=app

Coverage requirement: ≥ 70%

📊 Logging

Structured logs include:

Export job started

Export job completed

Export job failed

Rows exported

Duration

Example log:

{
  "event": "export_completed",
  "jobId": "123",
  "rowsExported": 100000,
  "duration": "3.2s"
}
🔐 Environment Variables

See .env.example

Example:

DATABASE_URL=postgresql://user:password@db:5432/mydatabase
PORT=8080
🧠 CDC Design Explanation (For Evaluation)
✔ Watermarking

Each consumer has its own watermark to prevent duplicate exports.

✔ Incremental Export

Exports only updated rows since the last watermark.

✔ Delta Export

Adds operation type (INSERT / UPDATE / DELETE).

✔ Asynchronous Processing

Uses FastAPI BackgroundTasks to avoid API blocking.

✔ Idempotent Seeding

Seed scripts prevent duplicate data.

✔ Containerized Deployment

Single-command startup using Docker Compose.

✅ How to Verify Task Requirements
Requirement	Verification
Docker Compose	docker compose up
100,000 users	SELECT COUNT(*) FROM users;
Soft deletes	SELECT COUNT(*) FROM users WHERE is_deleted=true;
Health API	curl /health
Full Export	POST /exports/full
Incremental Export	POST /exports/incremental
Delta Export	POST /exports/delta
Watermark	GET /exports/watermark
Logs	docker logs cdc-export-system-app-1
Tests	pytest --cov=app
🎯 Key Learning Outcomes

Change Data Capture (CDC) design patterns

Watermark-based stateful processing

Asynchronous long-running job handling

Dockerized production systems

Large dataset seeding and indexing

Backend system design for data pipelines

🏁 Conclusion

This project demonstrates a scalable, production-grade CDC export system using industry best practices such as watermarking, containerization, asynchronous processing, and structured logging.

It simulates real-world data synchronization pipelines used in:

Analytics systems

Search indexing

Data warehousing

Event-driven architectures
