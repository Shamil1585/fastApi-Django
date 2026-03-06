from fastapi import FastAPI

app = FastAPI(
    title="Blog API",
    description="Migrated from Django to FastAPI",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Blog API is running"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}