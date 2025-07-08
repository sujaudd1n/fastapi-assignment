from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class Prompt(BaseModel):
    prompt: str


