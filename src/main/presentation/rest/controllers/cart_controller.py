""" REST controller: Prefill Service """
from fastapi import APIRouter
from ....application.cart_service import CartService


router = APIRouter(
    prefix='/carts',
    tags=['carts'],
    dependencies=[],
    responses={404: {'description': 'Not found'}},
)


@router.get('/')
async def get_carts():
    """
    Lists all existing carts
    Warnings:
        - No pagination implemented, use with caution
    Returns: JSON Array (through FastAPI decorator)

    """
    carts_query = await CartService().read_carts()
    return carts_query.all()


@router.get('/id/')
async def get_cart(cart_id):
    """
    Finds a specific Cart by ID
    Returns: JSON Array (through FastAPI decorator)

    """
    cart_query = await CartService().read_cart({'id': cart_id})
    cart = cart_query.first()
    if cart is not None:
        return {**cart.to_dict(), 'items': [cart_item.item.to_dict() for cart_item in cart.items]}


@router.post('/')
async def post_cart(user_id):
    """
    Lists all existing carts
    Warnings:
        - No pagination implemented, use with caution
    Returns: JSON Array (through FastAPI decorator)

    """
    await CartService().create_cart(user_id=user_id)
