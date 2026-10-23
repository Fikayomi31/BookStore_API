from fastapi import FastAPI


app = FastAPI(
    title="BookStore REST API",
    description="A simple REST API for managing a bookstore",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to the BookStore REST API!"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
