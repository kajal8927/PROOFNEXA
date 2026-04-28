# ProofNexa NLP Engine

Production-level Natural Language Processing service for the ProofNexa plagiarism detection system. Built with FastAPI, NLTK, and Scikit-Learn.

## Project Overview

The ProofNexa NLP Engine compares submitted texts against documents stored in MongoDB using advanced NLP techniques:
- **Fingerprinting (SHA-256)** for fast Jaccard overlap matching.
- **TF-IDF & Cosine Similarity** for broader semantic matching.
- **N-Gram Analysis** for phrase-level detection.

## Folder Structure

```text
nlp-engine/
├── app/
│   ├── config/
│   │   ├── config.py         # Centralized configuration
│   │   └── database.py       # MongoDB connection
│   ├── controllers/
│   │   └── analyze_controller.py # Request orchestrators
│   ├── routes/
│   │   └── analyze_routes.py     # API route handlers
│   ├── schemas/
│   │   └── analyze_schema.py     # Pydantic validation schemas
│   ├── services/
│   │   ├── database_service.py   # Mongo queries
│   │   ├── fingerprint_service.py# Hash generation
│   │   ├── ngram_service.py      # N-gram production
│   │   ├── preprocessing_service.py # Text cleanup/tokenization
│   │   └── similarity_service.py # Scores & algorithms
│   ├── utils/
│   │   └── logging.py        # Production logging
│   └── main.py               # Application entrypoint
├── tests/                    # Pytest coverage
├── .env                      # Local credentials
├── .env.example              # Environment templates
├── Dockerfile                # Production containerization
└── requirements.txt          # Vendor dependencies
```

## Installation & Setup

### Local Execution

1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start backend locally:
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker

1. Build:
   ```bash
   docker build -t proofnexa-nlp .
   ```
2. Run:
   ```bash
   docker run -p 8000:8000 --env-file .env proofnexa-nlp
   ```

## API Documentation

Full interactive swagger docs reside at `http://127.0.0.1:8000/api/docs`.

### 1. Health Check
- **GET** `/api/health`
- *Response*: `{"status": "healthy", "database": "connected", "version": "1.0.0"}`

### 2. Analyze Text
- **POST** `/api/analyze-text`
- *Request Body*:
  ```json
  {
    "text": "Document text extraction here...",
    "submissionId": "OptionalMongoDBId"
  }
  ```
- *Response*:
  ```json
  {
    "success": true,
    "similarity": 78.5,
    "riskLevel": "High",
    "matches": [
      {
        "sourceId": "mongo_id",
        "sourceName": "sample.pdf",
        "similarity": 45.2,
        "matchedText": "stored sentence match",
        "inputText": "input sentence match",
        "matchType": "ngram"
      }
    ],
    "processingTimeMs": 1200
  }
  ```

## Node.js Express Integration Example

```javascript
const axios = require('axios');

async function checkPlagiarism(text, submissionId) {
  try {
    const response = await axios.post('http://localhost:8000/api/analyze-text', {
      text: text,
      submissionId: submissionId
    });
    
    const { similarity, riskLevel, matches } = response.data;
    return { similarity, riskLevel, matches };
  } catch (error) {
    console.error('NLP Engine Request Failed:', error.response?.data || error.message);
    throw error;
  }
}
```

## Postman Testing Guide

### 1. Health Check
- **Method**: `GET`
- **URL**: `http://localhost:8000/api/health`
- **Expected Success Response**: `200 OK`
  ```json
  {
    "status": "healthy",
    "database": "connected",
    "version": "1.0.0"
  }
  ```

### 2. Compare Two Texts
- **Method**: `POST`
- **URL**: `http://localhost:8000/api/compare-two-texts`
- **Headers**: `Content-Type: application/json`
- **Body (Raw JSON)**:
  ```json
  {
    "text1": "The quick brown fox jumps over the lazy dog.",
    "text2": "A fast brown fox leaps over a lazy dog."
  }
  ```
- **Expected Response**: `200 OK` with similarity metrics.

### 3. Validation Error Response
- **Method**: `POST`
- **URL**: `http://localhost:8000/api/analyze-text`
- **Body**: `{"text": ""}`
- **Expected Response**: `422 Unprocessable Content`
  ```json
  {
    "success": false,
    "detail": "Validation error",
    "errors": [...]
  }
  ```

## Deployment Steps (Render/Any Cloud)

1. **Environment Variables**: Set the following in your platform's environment config:
   - `MONGO_URI` (Your production MongoDB Atlas URI)
   - `ALLOWED_ORIGINS` (Allowed origins like `https://yourfrontend.com`)
   - `PORT` (Defaults to `8000`)

2. **Runtime Environment**: Choose **Docker** deployment method. The `Dockerfile` automates all server execution constraints.

3. **Execution Port Mapping**: Ensure platform maps incoming web queries to the internal docker port `8000`.

## Security Standards Checklist
- [x] Open CORS restricted via strict `.env` mappings.
- [x] Content limits strictly monitored in `config.py`.
- [x] Log exposure truncated safely in `app.utils.logging`.
- [x] Avoidance of dangerous code blocks (`eval`, `exec`).

