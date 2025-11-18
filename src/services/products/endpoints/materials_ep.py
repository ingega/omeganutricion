# src/services/endpoints/materials_ep.py
from fastapi import Depends, Form, APIRouter
from sqlalchemy.orm import Session
from typing import List, Annotated
from src.services.products import crud, schemas
from src.services.products.database import get_db
from src.services.products.auth import get_current_user


router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Omega Nutricion API running"}

# -------------- materials endpoints  ----------------------- #


@router.post("/materials/", response_model=schemas.Material)
def create_material(material: Annotated[schemas.MaterialCreate, Form()],
                    current_user: schemas.User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    """
    This function creates a new material.
    :param material: payload with name, unit and cost of a material
    :param db: Session with db connection
    :return: a 200 response if successful, and data saved.
    """
    material_crud = crud.MaterialCrud(db=db)
    return material_crud.create_material(material=material)


@router.get("/materials/", response_model=List[schemas.Material])
def read_materials(db: Session = Depends(get_db)):
    material_crud = crud.MaterialCrud(db=db)
    return material_crud.get_materials()

@router.get("/materials/{material_id}")
def read_materials(material_id: int, db: Session = Depends(get_db)):
    material_crud = crud.MaterialCrud(db=db)
    return material_crud.get_material(material_id=material_id)

@router.patch("/materials/{material_id}", response_model=schemas.MaterialUpdate)
def partial_update_material(
        material_id: int,
        db: Session = Depends(get_db),
        name: Annotated[str | None, Form()] = None,
        unit: Annotated[str | None, Form()] = None,
        price: Annotated[str | None, Form()] = None,
        supplier_id: Annotated[str | None, Form()] = None,
):
    material_update = {}
    if name:
        material_update['name'] = name
    if unit:
        material_update['unit'] = unit
    if price:
        material_update['price'] = float(price)
    if supplier_id:
        material_update['supplier_id'] = int(supplier_id)

    material_update_data = schemas.MaterialUpdate(**material_update)
    material_crud = crud.MaterialCrud(db=db)

    return material_crud.update_material(
        material=material_update_data,
        material_id=material_id
    )


@router.delete("/materials/{material_id}", response_model=schemas.Material)
def delete_material(material_id: int, db: Session = Depends(get_db)):
    material_crud = crud.MaterialCrud(db=db)
    return material_crud.delete_material(material_id=material_id)


# -------------- suppliers endpoints  ----------------------- #


@router.post("/suppliers/", response_model=schemas.Supplier)
def create_supplier(supplier: Annotated[schemas.SupplierCreate, Form()],
                    db: Session = Depends(get_db)
                    ):
    supplier_crud = crud.SupplierCrud(db=db)
    return supplier_crud.create_supplier(supplier)

@router.get("/suppliers/", response_model=List[schemas.Supplier])
def read_suppliers(db: Session = Depends(get_db)):
    supplier_crud = crud.SupplierCrud(db=db)
    return supplier_crud.get_suppliers()

@router.get("/suppliers/{supplier_id}")
def read_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier_crud = crud.SupplierCrud(db=db)
    return supplier_crud.get_supplier(supplier_id=supplier_id)

@router.patch("/suppliers/{supplier_id}", response_model=schemas.SupplierUpdate)
def partial_update_supplier(
        supplier: schemas.SupplierUpdate,
        supplier_id: int,
        db: Session = Depends(get_db)
):
    supplier_crud = crud.SupplierCrud(db=db)
    return supplier_crud.update_supplier(supplier=supplier, supplier_id=supplier_id)

@router.delete("/suppliers/{supplier_id}", response_model=schemas.Supplier)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier_crud = crud.SupplierCrud(db=db)
    return supplier_crud.delete_supplier(supplier_id=supplier_id)