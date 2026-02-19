from fastapi import FastAPI

app = FastAPI(title="YT Comment Microservice")

@app.get("/health")
def health():
    return {"status": "ok"}
