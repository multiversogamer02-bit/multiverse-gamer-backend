from fastapi import APIRouter

router = APIRouter()


@router.get("/validate")
def validate_license(key: str):
    """
    Este endpoint valida una licencia OFFLINE.
    Actualmente no está en uso porque el sistema 
    de planes online lo reemplaza.
    Pero lo dejamos funcional por compatibilidad futura.
    """

    if key == "MULTIVERSE-DEMO-001":
        return {"status": "valid", "plan": "BASIC"}

    return {"status": "invalid", "plan": None}
