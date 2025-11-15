from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.integrations.mercadopago import get_payment_status
from app.crud.crud_user import update_user_plan

router = APIRouter()


@router.post("/mercadopago")
async def mp_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Webhook oficial de Mercado Pago.
    Mercado Pago llama a este endpoint cuando el pago cambia de estado.
    """

    data = await request.json()

    if "data" not in data or "id" not in data["data"]:
        return {"status": "ignored"}

    payment_id = data["data"]["id"]

    # Consultar el estado del pago
    payment_info = get_payment_status(payment_id)

    if not payment_info:
        return {"status": "error"}

    status_mp = payment_info.get("status")
    external = payment_info.get("external_reference")

    if not external:
        return {"status": "no external reference"}

    # external_reference = "userId_PLAN"
    user_id, plan = external.split("_")

    if status_mp == "approved":
        update_user_plan(db, int(user_id), plan)
        return {"status": "plan updated", "user": user_id, "plan": plan}

    return {"status": "pending", "payment": status_mp}
