from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .controllers.user_controller import router as user_router
from .controllers.item_controller import router as item_router
from .controllers.cart_controller import router as cart_router
from .controllers.rule_controller import router as rule_router

app = FastAPI()
app.include_router(user_router)
app.include_router(item_router)
app.include_router(cart_router)
app.include_router(rule_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def root():
    """
    Dummy method to welcome new API users
    Returns: JSON (through FastAPI decorator)

    """
    return {'message': 'Welcome!'}
