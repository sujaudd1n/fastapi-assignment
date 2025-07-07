from fastapi import FastAPI

app = FastAPI()

@app.post("/login/") 
async def login():
    return {"message": "Not implemented"}

@app.post("/prompt/") 
async def prompt():
    return {"message": "Not implemented"}

@app.get("/history/") 
async def history():
    return {"message": "Not implemented"}
