from fastapi import FastAPI
from src.services.products.database import Base, engine
from src.services.products.endpoints.materials_ep import router as materials_router
from src.services.products.endpoints.users_ep import router as users_router
from src.services.products.endpoints.formulas_ep import router as formulas_router

from src.services.products.auth import router as auth_router

# app
app = FastAPI()

# create tables for production microservice
Base.metadata.create_all(bind=engine)

# routers
app.include_router(materials_router)
app.include_router(formulas_router)
app.include_router(auth_router)
app.include_router(users_router)



if __name__ == '__main__':
    pass