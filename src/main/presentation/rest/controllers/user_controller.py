""" REST controller: User Service """
from fastapi import APIRouter
from ....application.user_service import UserService

router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[],
    responses={404: {'description': 'Not found'}},
)


@router.get('/')
async def get_users():
    """
    Lists all existing users
    Warnings:
        - No pagination implemented, use with caution
    Returns: JSON Array (through FastAPI decorator)

    """
    user_query = await UserService().read_users()
    return [{**user.to_dict(), 'cart': user.cart[0].to_dict()} for user in user_query.all()]
