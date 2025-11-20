from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.auth_deps import get_current_user
from app.crud import crud_game
from app.schemas.game import GameCreate, GameResponse

router = APIRouter()


# ================================
#   GET — traer juegos del usuario
# ================================
@router.get("/", response_model=list[GameResponse])
def list_games(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud_game.get_games(db, user_id=current_user.id)


# ================================
#   POST — agregar juego (sync local)
# ================================
@router.post("/", response_model=GameResponse)
def add_game(
    payload: GameCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    game = crud_game.add_game(
        db=db,
        user_id=current_user.id,
        name=payload.name,
        platform=payload.platform,
        path=payload.path,
        cover=payload.cover
    )
    return game


# ================================
#   DELETE — borrar juego
# ================================
@router.delete("/{game_id}")
def delete_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted = crud_game.delete_game(
        db=db,
        game_id=game_id,
        user_id=current_user.id
    )

    if not deleted:
        raise HTTPException(status_code=404, detail="Game not found")

    return {"message": "Game deleted"}
