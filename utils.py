import os
import time
import json
from collections import defaultdict
from fastapi import HTTPException
from google import genai

if os.environ.get("LLM_API_KEY"):
    client = genai.Client(api_key=os.environ.get("LLM_API_KEY"))
else:
    client = None

request_log = defaultdict(list)
RATE_LIMIT = 5 
RATE_LIMIT_WINDOW = 60

def check_ratelimit(username):
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW

    request_log[username] = [t for t in request_log[username] if t > window_start]

    if len(request_log[username]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail=f'Rate limit exceeded. {RATE_LIMIT} req/m')

    request_log[username].append(now)

def save_history(prompt_history):
    with open(f"prompt-history.json", "w") as f:
        f.write(json.dumps(prompt_history))

def load_history():
    if os.path.exists("prompt-history.json"):
        with open(f"prompt-history.json") as f:
            try:
                return json.loads(f.read())
            except:
                return {}
    return {}

def get_llm_response(prompt):
    if client:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        ).text
    else:
        response = "Let me think"
    print(response)
    return response
