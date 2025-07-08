# FastAPI Prompt Application

A simple backend application that allows users to login,
submit text prompts, and get AI-style responses.

## Features

- User authentication with hardcoded credentials
- Prompt submission with random AI responses
- Prompt history tracking
- Basic error handling
- Basic Rate limiting
- Save history as JSON locally
- Integration with LLM

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
6. Optional: Export gemini api key `LLM_API_KEY` to use gemini LLM response
5. Run the application: `fastapi dev main.py`

## Files

- `main.py`: Entry point for the web app
- `utils.py`: Various utility functions such as rate limiting
- `models.py`: Models for users and prompts

## API Endpoints

### Login

```bash
curl -X POST "http://localhost:8000/login/" \
-H "Content-Type: application/json" \
-d '{"username":"sujauddin","password":"password"}'
``` 


### Submit prompt

```
curl -X POST "http://localhost:8000/prompt/" \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d '{"prompt":"What is the full form of LLM?"}'
```

### Get history

```
curl -X GET "http://localhost:8000/history/" \
-H "Authorization: Bearer <token>"
```

## Known limitations

- User credentials are hardcoded
- Uses basic authentication
- Uses in-memory storage for logins
