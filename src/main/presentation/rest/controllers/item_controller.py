""" REST controller: User Service """
from fastapi import APIRouter
from ....application.item_service import ItemService


router = APIRouter(
    prefix='/items',
    tags=['items'],
    dependencies=[],
    responses={404: {'description': 'Not found'}},
)


@router.get('/')
async def get_items():
    """
    Lists all existing items
    Warnings:
        - No pagination implemented, use with caution
    Returns: JSON Array (through FastAPI decorator)

    """
    items_query = await ItemService().read_items()
    return list(items_query)


@router.post('/add_to_cart')
async def add_item_to_cart(item_id, cart_id):
    await ItemService().add_to_cart(item_id=item_id, cart_id=cart_id)


@router.post('/remove_from_cart')
async def add_item_to_cart(item_id, cart_id):
    await ItemService().remove_from_cart(item_id=item_id, cart_id=cart_id)
