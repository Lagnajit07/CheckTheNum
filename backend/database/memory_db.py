# backend/database/memory_db.py

games = {}          # game_id → game data
connections = {}    # game_id → set of websocket connections
