import json
import os
import time
from collections import defaultdict
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
request_log = defaultdict(list)

class User(BaseModel):
    username: str
    password: str

class Prompt(BaseModel):
    prompt: str

RATE_LIMIT = 5
RATE_LIMIT_WINDOW = 60

def check_ratelimit(username):
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW

    request_log[username] = [t for t in request_log[username] if t > window_start]

    if len(request_log[username]) >= RATE_LIMIT:
        raise HTTPException(status_code=422, detail='Rate limit exceeded')

    request_log[username].append(now)

def save_history():
    with open(f"prompt-history.json", "w") as f:
        f.write(json.dumps(prompt_history))

def load_history():
    if os.path.exists("prompt-history.json"):
        with open(f"prompt-history.json") as f:
            return json.loads(f.read())
    return {}

prompt_history.update(load_history())
        

def get_username(token = Header(..., alias="Authorization")):
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
    check_ratelimit(username)
    response = "dummy response for now"
    if username not in prompt_history:
        prompt_history[username] = []
    prompt_history[username].append({
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt.prompt,
        "response": response
        })
    save_history()
    print(prompt_history)
    return {"response": response}

@app.get("/history/") 
async def history(username = Depends(get_username)):
    return prompt_history.get(username, [])
