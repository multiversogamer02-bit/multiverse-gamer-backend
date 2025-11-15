import requests
from app.core.config import settings


def create_payment_preference(user_id: int, target_plan: str):
    """
    Crea la preferencia de pago en Mercado Pago.
    """

    url = "https://api.mercadopago.com/checkout/preferences"

    headers = {
        "Authorization": f"Bearer {settings.MP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "items": [
            {
                "title": f"Multiverse Gamer - {target_plan}",
                "quantity": 1,
                "currency_id": "ARS",
                "unit_price": (
                    8000 if target_plan == "BASIC" else
                    12000 if target_plan == "PRO" else
                    18000
                )
            }
        ],
        "external_reference": f"{user_id}_{target_plan}",
        "notification_url": "https://TU-BACKEND-RENDER.onrender.com/webhooks/mercadopago"
    }

    try:
        res = requests.post(url, json=payload, headers=headers)
        res.raise_for_status()
        return res.json()

    except Exception as e:
        print("Error Mercado Pago:", e)
        return None


def get_payment_status(payment_id: str):
    """
    Consulta el estado del pago.
    """

    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"

    headers = {
        "Authorization": f"Bearer {settings.MP_ACCESS_TOKEN}"
    }

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        return res.json()

    except:
        return None
