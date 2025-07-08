import json
from collections import defaultdict
from datetime import datetime
from secrets import token_hex
from fastapi import FastAPI, HTTPException, Depends, Header
from models import User, Prompt
from utils import check_ratelimit, load_history, save_history, get_llm_response

app = FastAPI()

users = {
    "sujauddin": "password",
    "akash": "bluesky",
    "tousif": "tousifxyz"
}

login_tokens = {}
prompt_history = defaultdict(list)

prompt_history.update(load_history())

def get_username(token = Header(..., alias="Authorization")):
    try:
        token = token.split()[1]
    except:
        raise HTTPException(status_code=401, detail="token is not valid")
    if token not in login_tokens:
        raise HTTPException(status_code=401, detail="token is not valid")
    return login_tokens[token]

@app.post("/login/") 
async def login(user: User):
    if user.username not in users or user.password != users[user.username]:
        return HTTPException(status_code=401, detail="Wrong username or password")
    token = token_hex(32)
    login_tokens[token] = user.username
    return {"token": token}

@app.post("/prompt/") 
async def prompt(prompt: Prompt, username = Depends(get_username)):
    check_ratelimit(username)
    response = get_llm_response(prompt.prompt)
    prompt_history[username].append({
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt.prompt,
        "response": response
    })
    save_history(prompt_history)
    print(prompt_history)
    return {"response": response}

@app.get("/history/") 
async def history(username = Depends(get_username)):
    check_ratelimit(username)
    return prompt_history.get(username, [])
