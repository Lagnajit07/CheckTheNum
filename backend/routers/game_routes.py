# backend/routers/game_routes.py

from fastapi import APIRouter
from models.game_models import GameCreate, GameJoin, Guess
from core.game_manager import create_new_game, join_existing_game, process_guess

router = APIRouter()

@router.post("/create_game")
def create_game(data: GameCreate):
    game_id = create_new_game(data.host_name, data.number)
    return {"game_id": game_id}


@router.post("/join_game")
def join_game(data: GameJoin):
    ok = join_existing_game(data.game_id, data.player_name)
    if not ok:
        return {"error": "Invalid Game ID"}
    return {"message": "Joined game successfully"}


@router.post("/guess")
def make_guess(data: Guess):
    result = process_guess(data.game_id, data.player_name, data.guess)
    if not result:
        return {"error": "Invalid Game ID or Game Completed"}
    return result
