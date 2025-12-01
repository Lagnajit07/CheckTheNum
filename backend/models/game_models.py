# backend/models/game_models.py

from pydantic import BaseModel

class GameCreate(BaseModel):
    host_name: str
    number: str

class GameJoin(BaseModel):
    game_id: str
    player_name: str

class Guess(BaseModel):
    game_id: str
    player_name: str
    guess: str
