from sqlalchemy.orm import Session
from app.models.game import Game


def add_game(db: Session, user_id: int, name: str, platform: str, path: str, cover: str = None):
    game = Game(
        user_id=user_id,
        name=name,
        platform=platform,
        path=path,
        cover=cover
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    return game


def get_games(db: Session, user_id: int):
    return db.query(Game).filter(Game.user_id == user_id).all()


def delete_game(db: Session, game_id: int, user_id: int):
    game = db.query(Game).filter(Game.id == game_id, Game.user_id == user_id).first()
    if not game:
        return None

    db.delete(game)
    db.commit()
    return True
