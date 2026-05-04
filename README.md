# ai-MillenOps-ai# Smart Ops AI Service

![Status](https://img.shields.io/badge/Status-In%20Development-yellow)
![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20FastAPI%20%7C%20scikit--learn-blue)
![AI Layer](https://img.shields.io/badge/AI%20Layer-Independent%20Microservice-purple)

## Overview

`smart-ops-ai-service` is the independent AI microservice for the **AI-Powered Smart Facility & Support Operations System**.

The service is built with **Python**, **FastAPI**, and **scikit-learn**.

It provides AI-powered predictions, classifications, recommendations, and insights to the main NestJS backend.

The NestJS backend remains the source of truth.

This AI service does not directly modify:

- Tickets
- Bookings
- Rooms
- Visitors
- HR records
- Payroll records
- Database state

It only returns:

- Predictions
- Classifications
- Recommendations
- Confidence scores
- Explanations
- Model versions

---

## AI Architecture Summary

```txt
Main AI Service Layer: 1
AI Domains: 4
AI Capability Layers: 12
```

## AI Domains

1. Support AI
2. Facility AI
3. Visitor AI
4. HR & Workforce AI

---

## System Relationship

```mermaid
flowchart TD
    A[NestJS Backend] --> B[BullMQ AI Inference Queue]
    B --> C[AI Processor]
    C --> D[FastAPI AI Service]
    D --> E[AI Prediction / Recommendation]
    E --> F[NestJS Backend]
    F --> G[(PostgreSQL)]
    F --> H[AIInsight Records]
    F --> I[Dashboard Suggestions]
    I --> J[Human Accept / Override / Ignore]
```

---

## General AI Flow

```mermaid
flowchart TD
    A[Core Platform Data] --> B[AI Service Layer]
    B --> C[Predictions]
    B --> D[Classifications]
    B --> E[Recommendations]
    B --> F[Alerts]
    B --> G[Insights]

    C --> H[NestJS Backend]
    D --> H
    E --> H
    F --> H
    G --> H

    H --> I[Dashboards]
    H --> J[Notifications]
    H --> K[Reports]
    H --> L[Workflow Suggestions]
```

---

## Current Build Focus

We are starting with the first AI capability:

```txt
Ticket Categorization AI
```

This belongs to:

```txt
Support AI
```

First endpoint:

```txt
POST /v1/tickets/classify
```

---

## AI Capability Map

```mermaid
flowchart TD
    A[Smart Ops AI Service] --> B[Support AI]
    A --> C[Facility AI]
    A --> D[Visitor AI]
    A --> E[HR & Workforce AI]

    B --> B1[Ticket Categorization AI]
    B --> B2[Priority Suggestion AI]
    B --> B3[Intelligent Routing AI]
    B --> B4[Repeat Issue Detection AI]
    B --> B5[Anomaly Detection AI]

    C --> C1[No-Show Prediction AI]
    C --> C2[Smart Room Release AI]
    C --> C3[Facility Usage Forecasting AI]
    C --> C4[Behavioural Profiling AI]
    C --> C5[Natural Language Assistant AI]

    D --> D1[Visitor Matching AI]

    E --> E1[HR & Workforce Intelligence AI]
```

---

## Project Structure

```txt
smart-ops-ai-service/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   │
│   ├── common/
│   │   ├── responses.py
│   │   ├── text_cleaning.py
│   │   └── model_loader.py
│   │
│   ├── modules/
│   │   │
│   │   ├── tickets/
│   │   │   ├── classification/
│   │   │   │   ├── router.py
│   │   │   │   ├── schemas.py
│   │   │   │   ├── rules.py
│   │   │   │   ├── model.py
│   │   │   │   ├── service.py
│   │   │   │   ├── training/
│   │   │   │   │   ├── train.py
│   │   │   │   │   └── datasets/
│   │   │   │   │       └── tickets.csv
│   │   │   │   └── models/
│   │   │   │       └── .gitkeep
│   │   │   │
│   │   │   ├── priority/
│   │   │   │   └── README.md
│   │   │   │
│   │   │   └── routing/
│   │   │       └── README.md
│   │   │
│   │   ├── bookings/
│   │   │   └── no_show/
│   │   │       └── README.md
│   │   │
│   │   ├── rooms/
│   │   │   └── repeat_issue/
│   │   │       └── README.md
│   │   │
│   │   ├── anomalies/
│   │   │   └── detection/
│   │   │       └── README.md
│   │   │
│   │   ├── visitors/
│   │   │   └── matching/
│   │   │       └── README.md
│   │   │
│   │   ├── workforce/
│   │   │   └── insight/
│   │   │       └── README.md
│   │   │
│   │   └── nlp/
│   │       └── assistant/
│   │           └── README.md
│   │
│   └── tests/
│       ├── test_health.py
│       └── test_ticket_classification.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Module Build Order

```mermaid
flowchart TD
    A[Start AI Service] --> B[Ticket Categorization AI]
    B --> C[Priority Suggestion AI]
    C --> D[Intelligent Routing AI]
    D --> E[No-Show Prediction AI]
    E --> F[Repeat Issue Detection AI]
    F --> G[Anomaly Detection AI]
    G --> H[Visitor Matching AI]
    H --> I[Facility Usage Forecasting AI]
    I --> J[HR & Workforce Intelligence AI]
    J --> K[Natural Language Assistant AI]
```

---

## Current Module: Ticket Categorization AI

### Purpose

Ticket Categorization AI reads support ticket text and predicts the correct issue category.

### Supported Categories

```txt
IT
AV / Projector
Network
Access Control
HVAC / Facility
Workspace / Meeting Room
Visitor-related
General Service
```

### Input Data

```txt
Ticket title
Ticket description
Room context
Booking context
Department
Safe metadata
```

### Output

```txt
Suggested category
Alternative categories
Confidence score
Explanation
Model version
```

---

## Ticket Categorization Flow

```mermaid
flowchart TD
    A[Ticket Created in NestJS] --> B[AI_INFERENCE_QUEUE]
    B --> C[AiProcessor]
    C --> D[POST /v1/tickets/classify]
    D --> E[Ticket Categorization AI]
    E --> F[Predicted Category]
    F --> G[NestJS Backend]
    G --> H[Store AIInsight]
    H --> I[Support Dashboard]
    I --> J[Human Accepts / Overrides / Ignores]
```

---

## Endpoint

```txt
POST /v1/tickets/classify
```

### Example Request

```json
{
  "ticketId": "ticket_001",
  "title": "Projector not working",
  "description": "The projector in Boardroom A is not displaying",
  "roomName": "Boardroom A",
  "bookingLinked": true,
  "department": "Operations",
  "metadata": {
    "bookingId": "booking_001",
    "roomEquipment": ["projector", "screen"],
    "activeMeeting": true
  }
}
```

### Example Response

```json
{
  "success": true,
  "capability": "TICKET_CLASSIFICATION",
  "confidence": 0.88,
  "recommendation": {
    "category": "AV / Projector",
    "alternativeCategories": [
      {
        "category": "IT",
        "confidence": 0.31
      }
    ]
  },
  "explanation": "The ticket mentions projector display failure in a meeting room.",
  "modelVersion": "baseline-rules-v1"
}
```

---

## Training Strategy

The first implementation starts with:

```txt
baseline-rules-v1
```

This is a rule-based classifier.

Later, after enough labelled ticket data exists, the service will train a scikit-learn model:

```txt
TF-IDF + Logistic Regression
```

---

## Training Data Sources

```mermaid
flowchart TD
    A[Training Data Sources] --> B[Internal System Tickets]
    A --> C[Accepted AI Suggestions]
    A --> D[Overridden AI Suggestions]
    A --> E[Resolved Tickets]
    A --> F[Public Support Ticket Datasets]
    A --> G[Synthetic Starter Examples]

    B --> H[Best Production Data]
    C --> H
    D --> H
    E --> H

    F --> I[Bootstrap Only]
    G --> J[Testing Only]
```

---

## Training Data Format

```csv
title,description,roomName,bookingLinked,department,finalCategory
Projector not working,Projector in Boardroom A is not displaying,Boardroom A,true,Operations,AV / Projector
Wi-Fi is down,Internet is not working in meeting room,Meeting Room 2,true,IT,Network
AC not cooling,The room is too hot,Boardroom B,false,Admin,HVAC / Facility
Door access failed,My access card cannot open the boardroom door,Boardroom A,false,Security,Access Control
Laptop cannot login,User cannot login to company laptop,,false,IT,IT
Room is dirty,Meeting room has dirty tables and chairs,Meeting Room 1,false,Admin,Workspace / Meeting Room
Visitor cannot find host,Guest arrived but host cannot be identified,Reception,false,Front Desk,Visitor-related
General assistance needed,Need help with an operational request,,false,Operations,General Service
```

---

## Model Training Flow

```mermaid
flowchart TD
    A[Labelled Ticket Data] --> B[Clean and Normalize Text]
    B --> C[Combine Ticket Fields]
    C --> D[Train/Test Split]
    D --> E[TF-IDF Vectorizer]
    E --> F[Logistic Regression Classifier]
    F --> G[Evaluate Model]
    G --> H{Performance Good?}
    H -->|Yes| I[Save Model as ticket_classifier.joblib]
    H -->|No| J[Collect More Data / Improve Labels]
    I --> K[FastAPI Loads Model]
    K --> L[Use Trained Model for Classification]
```

---

## Model Fallback Strategy

```mermaid
flowchart TD
    A[Classification Request] --> B{Trained Model Exists?}
    B -->|Yes| C[Use Trained Model]
    B -->|No| D[Use Rule-Based Classifier]

    C --> E{Model Prediction Works?}
    E -->|Yes| F[Return Model Prediction]
    E -->|No| D

    D --> G[Return baseline-rules-v1 Result]
```

---

## Human Review Flow

```mermaid
flowchart TD
    A[AI Suggestion Created] --> B[Stored in AIInsight]
    B --> C[Shown to Support Coordinator]
    C --> D{Human Decision}
    D -->|Accept| E[Mark AIInsight as Accepted]
    D -->|Override| F[Mark AIInsight as Overridden]
    D -->|Ignore| G[Mark AIInsight as Ignored]

    F --> H[Store Override Reason]
    H --> I[Use Override as Future Training Label]
    E --> J[Use Accepted Suggestion as Training Label]
```

---

## Setup

Create virtual environment:

```bash
python -m venv venv
```

Activate on Windows:

```bash
venv\Scripts\activate
```

Install packages:

```bash
pip install fastapi uvicorn scikit-learn pandas joblib pydantic python-dotenv numpy pytest httpx
```

Create requirements file:

```bash
pip freeze > requirements.txt
```

---

## Environment Variables

Create `.env`:

```env
APP_NAME=Smart Ops AI Service
APP_ENV=development
APP_VERSION=1.0.0
PORT=8000
DEFAULT_MODEL_VERSION=baseline-rules-v1
TICKET_CLASSIFIER_MODEL_PATH=app/modules/tickets/classification/models/ticket_classifier.joblib
```

---

## Run Service

```bash
uvicorn app.main:app --reload --port 8000
```

Health check:

```txt
http://localhost:8000/health
```

Swagger docs:

```txt
http://localhost:8000/docs
```

---

## Test Manually

Use Swagger or curl.

### Projector Test

```json
{
  "ticketId": "ticket_001",
  "title": "Projector not working",
  "description": "The projector in Boardroom A is not displaying",
  "roomName": "Boardroom A",
  "bookingLinked": true,
  "department": "Operations"
}
```

Expected category:

```txt
AV / Projector
```

### Network Test

```json
{
  "ticketId": "ticket_002",
  "title": "Wi-Fi is down",
  "description": "Internet is not working in the meeting room",
  "roomName": "Meeting Room 2",
  "bookingLinked": true,
  "department": "IT"
}
```

Expected category:

```txt
Network
```

### HVAC Test

```json
{
  "ticketId": "ticket_003",
  "title": "AC not cooling",
  "description": "The room is too hot and the air conditioner is not working",
  "roomName": "Boardroom B",
  "bookingLinked": false,
  "department": "Admin"
}
```

Expected category:

```txt
HVAC / Facility
```

---

## Run Tests

```bash
pytest
```

---

## Train Model

Run:

```bash
python app/modules/tickets/classification/training/train.py
```

If there is not enough real data, the service should continue using:

```txt
baseline-rules-v1
```

---

## Deployment Concept

The AI service is deployed separately from the NestJS backend.

```mermaid
flowchart TD
    A[Frontend] --> B[NestJS Backend]
    B --> C[Redis / BullMQ]
    C --> D[Smart Ops AI Service]
    D --> B
    B --> E[(PostgreSQL)]
```

In local development:

```txt
Frontend: http://localhost:5173
NestJS Backend: http://localhost:5000
AI Service: http://localhost:8000
PostgreSQL: localhost:5432
Redis: localhost:6379
```

Backend `.env`:

```env
AI_SERVICE_URL=http://localhost:8000
AI_QUEUE_ENABLED=true
AI_CONFIDENCE_THRESHOLD=0.70
```

In Docker deployment:

```env
AI_SERVICE_URL=http://smart-ops-ai-service:8000
```

---

## AI Safety Rules

```txt
1. AI only recommends.
2. NestJS remains the source of truth.
3. AI does not directly modify database records.
4. AI results must be stored in AIInsight.
5. Every AI response must include confidence.
6. Every AI response must include explanation.
7. Every AI response must include modelVersion.
8. Low-confidence results require manual review.
9. Human override must always be available.
10. Failed AI calls must not break core workflows.
```

---

## Future Modules

The following modules will be added later inside the same AI service.

### Priority Suggestion AI

```txt
POST /v1/tickets/priority
```

Suggests:

```txt
Low
Medium
High
Critical
```

### Intelligent Routing AI

```txt
POST /v1/tickets/routing
```

Recommends best technician, developer, or team.

### No-Show Prediction AI

```txt
POST /v1/bookings/no-show
```

Predicts booking no-show risk.

### Repeat Issue Detection AI

```txt
POST /v1/rooms/repeat-issue
```

Detects recurring room or asset problems.

### Anomaly Detection AI

```txt
POST /v1/anomalies/detect
```

Detects unusual operational patterns.

### Visitor Matching AI

```txt
POST /v1/visitors/match
```

Matches visitors to hosts, bookings, or meetings.

### Workforce Insight AI

```txt
POST /v1/workforce/insight
```

Detects workforce availability and shift pressure risks.

### Natural Language Assistant AI

```txt
POST /v1/nlp/parse-command
```

Parses natural language commands for bookings and tickets.

---

## Final Goal

The goal of this service is to provide a safe AI layer for the main platform.

The first completed capability is:

```txt
Ticket Categorization AI
```

The service will grow module by module while keeping one FastAPI server and one integration point with the NestJS backend.
