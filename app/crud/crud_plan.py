from sqlalchemy.orm import Session
from app.models.plan import Plan


def get_plan_by_name(db: Session, name: str):
    return db.query(Plan).filter(Plan.name == name).first()


def get_all_plans(db: Session):
    return db.query(Plan).all()


def ensure_default_plans(db: Session):
    """
    Carga o actualiza los planes oficiales de Multiverse Gamer
    con precios y límites del Prompt Maestro.
    """

    default_plans = [
        ("BASIC", 8000, 1, 200,
         "Acceso a todas las consolas. 1 sesión activa. 200 juegos máx."),

        ("PRO", 12000, 3, 999999,
         "Sesiones x3. Juegos ilimitados. Soporte prioritario y carátulas."),

        ("ELITE", 18000, 999999, 999999,
         "Sesiones ilimitadas. Soporte remoto. Todo ilimitado.")
    ]

    for name, price, max_sessions, max_games, description in default_plans:
        plan = get_plan_by_name(db, name)

        if not plan:
            plan = Plan(
                name=name,
                price=price,
                max_sessions=max_sessions,
                max_games=max_games,
                description=description
            )
            db.add(plan)
        else:
            # Actualiza si cambió algo
            plan.price = price
            plan.max_sessions = max_sessions
            plan.max_games = max_games
            plan.description = description

    db.commit()
