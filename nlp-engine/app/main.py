from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.analyze_routes import router as analyze_router

app = FastAPI(
    title="ProofNexa NLP Engine",
    description="Text similarity and plagiarism detection service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {
        "success": True,
        "message": "ProofNexa NLP Engine is running"
    }

app.include_router(analyze_router, prefix="/api")
