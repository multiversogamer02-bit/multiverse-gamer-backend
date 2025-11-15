from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.crud_user import get_user_by_id, update_user_plan
from app.crud.crud_plan import get_plan_by_name, ensure_default_plans
from app.schemas.plan import PlanOut
from app.core.security import decode_token
from app.integrations.mercadopago import create_payment_preference

router = APIRouter()


def get_current_user(db: Session, token: str):
    """
    Devuelve el usuario desde el JWT recibido.
    """
    payload = decode_token(token)
    user_id = payload.get("user_id")

    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return user


@router.get("/info", response_model=PlanOut)
def get_plan_info(db: Session = Depends(get_db), Authorization: str = None):
    """
    Devuelve los datos del plan actual del usuario.
    """

    if Authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token requerido"
        )

    token = Authorization.replace("Bearer ", "")
    user = get_current_user(db, token)

    ensure_default_plans(db)

    plan = get_plan_by_name(db, user.plan)

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan no existe"
        )

    return plan


@router.post("/upgrade")
def upgrade_plan(
    target_plan: str,
    db: Session = Depends(get_db),
    Authorization: str = None
):
    """
    Crea un pago en Mercado Pago y devuelve el link.
    """

    if Authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token requerido"
        )

    token = Authorization.replace("Bearer ", "")
    user = get_current_user(db, token)

    plan = get_plan_by_name(db, target_plan)

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El plan seleccionado no existe"
        )

    # Crear preferencia de pago MP
    pref = create_payment_preference(user.id, target_plan)

    if not pref:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear pago"
        )

    return {
        "init_point": pref["init_point"],
        "plan": target_plan
    }


@router.post("/apply")
def apply_plan_change(
    user_id: int,
    new_plan: str,
    db: Session = Depends(get_db)
):
    """
    Ruta interna utilizada por el WEBHOOK de Mercado Pago
    para actualizar el plan después del pago aprobado.
    """

    plan = get_plan_by_name(db, new_plan)

    if not plan:
        raise HTTPException(
            status_code=400,
            detail="Plan inválido"
        )

    user = update_user_plan(db, user_id, new_plan)

    return {"status": "ok", "user": user.username, "plan": new_plan}
