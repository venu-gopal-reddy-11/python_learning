from fastapi import FastAPI

app = FastAPI()

@app.get("/name")
def get_name():
    return {"name": "FastAPI running locally"}

@app.post("/number")
def post_number(data: dict):
    return {"received": data.get("number")}

# ✅ Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# how to run this file 
# python main.py
