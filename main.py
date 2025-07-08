import json
from datetime import datetime
from secrets import token_urlsafe
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel

app = FastAPI()

users = {
    "sujauddin": "pssaword",
    "akash": "bluesky",
    "tousif": "tousifxyz"
}

login_tokens = {}
prompt_history = {}

class User(BaseModel):
    username: str
    password: str

class Prompt(BaseModel):
    prompt: str

async def get_username(token = Header(..., alias="Authorization")):
    token = token.split()[1]
    if token not in login_tokens:
        raise HTTPException(status_code=401, detail="token is not valid")
    return login_tokens[token]

@app.post("/login/") 
async def login(user: User):
    if user.username not in users or user.password != users[user.username]:
        return HTTPException(status_code=401, detail="Wrong username or password")
    token = token_urlsafe(32)
    login_tokens[token] = user.username
    return {"token": token}

@app.post("/prompt/") 
async def prompt(prompt: Prompt, username = Depends(get_username)):
    print(prompt_history)
    response = "dummy response for now"
    if username not in prompt_history:
        prompt_history[username] = []
    prompt_history[username].append({
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt.prompt,
        "response": response
        })
    with open(f"{username}-history.json", "w") as f:
        f.write(json.dumps(prompt_history[username]))
    return {"response": response}

@app.get("/history/") 
async def history(username = Depends(get_username)):
    return prompt_history.get(username, [])
