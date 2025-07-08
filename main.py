from secrets import token_urlsafe
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

users = {
    "sujauddin": "pssaword",
    "akash": "bluesky",
    "tousif": "tousifxyz"
}

login_tokens = {}

class User(BaseModel):
    username: str
    password: str

@app.post("/login/") 
async def login(user: User):
    if user.username not in users or user.password != users[user.username]:
        return HTTPException(status_code=401, detail="Wrong username or password")
    token = token_urlsafe(32)
    login_tokens[token] = user.username
    return {"token": token}

@app.post("/prompt/") 
async def prompt():
    return {"message": "Not implemented"}

@app.get("/history/") 
async def history():
    return {"message": "Not implemented"}
