from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.auth_deps import get_current_user
from app.crud.crud_game import add_game, get_games, delete_game

router = APIRouter()


@router.get("/list")
def list_games(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    games = get_games(db, current_user.id)
    return {
        "games": [
            {
                "id": g.id,
                "name": g.name,
                "platform": g.platform,
                "path": g.path,
                "cover": g.cover
            }
            for g in games
        ]
    }


@router.post("/add")
def add_new_game(
    data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    name = data.get("name")
    platform = data.get("platform")
    path = data.get("path")
    cover = data.get("cover")

    if not name or not platform or not path:
        raise HTTPException(status_code=400, detail="Faltan campos obligatorios.")

    game = add_game(db, current_user.id, name, platform, path, cover)
    return {"success": True, "game_id": game.id}


@router.delete("/delete/{game_id}")
def delete_existing_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    ok = delete_game(db, game_id, current_user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Juego no encontrado")

    return {"success": True}
