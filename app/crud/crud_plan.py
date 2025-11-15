from sqlalchemy.orm import Session
from app.models.plan import Plan


def get_plan_by_name(db: Session, name: str):
    return db.query(Plan).filter(Plan.name == name).first()


def get_all_plans(db: Session):
    return db.query(Plan).all()


def ensure_default_plans(db: Session):
    """
    Crea los planes por defecto si no existen.
    Esto garantiza que BASIC, PRO y ELITE estén creados.
    """

    default_plans = [
        ("BASIC", 1, 200, "Plan inicial"),
        ("PRO", 3, 999999, "Plan avanzado"),
        ("ELITE", 999999, 999999, "Plan sin límites")
    ]

    for name, max_sessions, max_games, desc in default_plans:
        if not get_plan_by_name(db, name):
            plan = Plan(
                name=name,
                max_sessions=max_sessions,
                max_games=max_games,
                description=desc
            )
            db.add(plan)

    db.commit()
