from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "null", # For local file access (file://) in browsers during development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory game state
# This simple state does not distinguish between multiple clients.
# For a multi-user game, you would need proper session management or a database.
game_state = {
    "current_score": 0,
    "high_score": 0,
    "is_game_over": True,
    "game_id": 0 # A simple identifier for the current game session
}

class ScorePayload(BaseModel):
    score: int

@app.get("/state")
async def get_game_state():
    """Retrieves the current game state from the backend."""
    return game_state

@app.post("/start_game")
async def start_new_game():
    """Resets the current game score and flags the game as active."""
    global game_state
    game_state["current_score"] = 0
    game_state["is_game_over"] = False
    game_state["game_id"] += 1 # Increment game_id for a new session
    return {"message": "Game started", "game_id": game_state["game_id"]}

@app.post("/game_over")
async def end_game(payload: ScorePayload):
    """Updates the high score if the current score is higher and flags game as over."""
    global game_state
    final_score = payload.score
    game_state["current_score"] = final_score
    game_state["is_game_over"] = True
    if final_score > game_state["high_score"]:
        game_state["high_score"] = final_score
    return {"message": "Game over", "final_score": final_score, "high_score": game_state["high_score"]}

@app.get("/")
async def root():
    return {"message": "Snake Game Backend is running!"}