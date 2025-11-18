from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.auth_deps import get_current_user
from app.crud.crud_user import update_user_plan
from app.crud.crud_plan import get_plan_by_name, ensure_default_plans
from app.schemas.plan import PlanOut
from app.integrations.mercadopago import create_payment_preference

router = APIRouter()


@router.get("/info", response_model=PlanOut)
def get_plan_info(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Devuelve los datos del plan actual del usuario.
    """
    ensure_default_plans(db)

    plan = get_plan_by_name(db, current_user.plan)

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Plan no existe"
        )

    return plan


@router.post("/upgrade")
def upgrade_plan(
    target_plan: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Crea un pago en Mercado Pago y devuelve el link.
    """

    plan = get_plan_by_name(db, target_plan)

    if not plan:
        raise HTTPException(
            status_code=400,
            detail="El plan seleccionado no existe"
        )

    pref = create_payment_preference(current_user.id, target_plan)

    if not pref:
        raise HTTPException(
            status_code=500,
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
