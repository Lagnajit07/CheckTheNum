# backend/core/game_manager.py

import uuid
from database.memory_db import games, connections
import asyncio

def create_new_game(host_name: str, number: str):
    game_id = str(uuid.uuid4())[:8]
    games[game_id] = {
        "host": host_name,
        "number": number,
        "players": [host_name],
        "guesses": [],
        "completed": False
    }
    connections[game_id] = set()
    return game_id


def join_existing_game(game_id: str, player_name: str):
    if game_id not in games:
        return None
    
    if player_name not in games[game_id]["players"]:
        games[game_id]["players"].append(player_name)
    
    return True


# def process_guess(game_id: str, player_name: str, guess: str):
#     game = games.get(game_id)
#     if not game or game["completed"]:
#         return None
    
#     number = game["number"]

#     correct_positions = sum(1 for i in range(4) if guess[i] == number[i])
#     correct_digits = sum(1 for c in guess if c in number) - correct_positions

#     completed = correct_positions == 4
#     if completed:
#         game["completed"] = True

#     game["guesses"].append({
#         "player": player_name,
#         "guess": guess,
#         "correct_digits": correct_digits,
#         "correct_positions": correct_positions
#     })

#     response = {
#         "type": "guess",
#         "player": player_name,
#         "guess": guess,
#         "correct_digits": correct_digits,
#         "correct_positions": correct_positions,
#         "completed": completed,
#         "steps": len(game["guesses"])
#     }

#     # Broadcast guess to WebSocket clients
#     for ws in connections[game_id]:
#         try:
#             asyncio.create_task(ws.send_json(response))
#         except:
#             pass

#     return response


def process_guess(game_id: str, player_name: str, guess: str):
    game = games.get(game_id)
    if not game or game["completed"]:
        return None
    
    secret = game["number"]
    correct_digits = 0
    correct_positions = 0

    for i in range(4):
        if guess[i] == secret[i]:
            correct_positions += 1
        if guess[i] in secret:
            correct_digits += 1

    completed = correct_positions == 4
    if completed:
        game["completed"] = True

    # Store guess
    game["guesses"].append({
        "player": player_name,
        "guess": guess,
        "correct_digits": correct_digits,
        "correct_positions": correct_positions
    })

    response = {
        "type": "guess",
        "player": player_name,
        "guess": guess,
        "correct_digits": correct_digits,
        "correct_positions": correct_positions,
        "completed": completed,
        "steps": len(game["guesses"])
    }

    # Broadcast guess to WebSocket clients
    for ws in connections[game_id]:
        try:
            asyncio.create_task(ws.send_json(response))
        except:
            pass

    return response
