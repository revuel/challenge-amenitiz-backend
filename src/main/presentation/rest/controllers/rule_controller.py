""" REST controller: User Service """
from fastapi import APIRouter
from ....application.rules_service import RuleService, RuleEngine

router = APIRouter(
    prefix='/rules',
    tags=['rules'],
    dependencies=[],
    responses={404: {'description': 'Not found'}},
)


@router.get('/')
async def get_rules():
    """
    Lists all existing items
    Warnings:
        - No pagination implemented, use with caution
    Returns: JSON Array (through FastAPI decorator)

    """
    items_query = await RuleService().read_offer_rules()
    return items_query.all()


@router.post('/apply')
async def apply_rules_to_cart(cart_id: int):
    """
    Lists all existing items
    Warnings:
        - No pagination implemented, use with caution
    Returns: JSON Array (through FastAPI decorator)

    """
    cart = await RuleEngine().apply(cart_id)
    return cart
