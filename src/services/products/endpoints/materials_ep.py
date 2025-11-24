# src/services/products/endpoints/materials_ep.py
from fastapi import Depends, Form, APIRouter, HTTPException
from typing import List, Annotated
from sqlalchemy.orm import Session

from src.services.products import crud, schemas
from src.services.products.database import get_db
from src.services.products.auth import get_current_user
from src.services.products.endpoints.users_ep import ROLE_EXCEPTION


router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Omega Nutricion API is running"}

# -------------- materials endpoints  ----------------------- #


@router.post("/materials/", response_model=schemas.Material)
def create_material(material: Annotated[schemas.MaterialCreate, Form()],
                    current_user: schemas.User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    """
    **This function add a new material to db.**

    :param material: **payload with name, unit and cost of a material**
    :param db: **Session with db connection**
    :return: **a 200 response if successful, and data saved.**

    **Authorization level: 5**
    """
    if current_user.auth_level < 5:
        raise ROLE_EXCEPTION

    material_crud = crud.MaterialCrud(db=db)
    return material_crud.create_material(material=material)


@router.get("/materials/", response_model=List[schemas.Material])
def read_materials(current_user: schemas.User = Depends(get_current_user),
                   db: Session = Depends(get_db)
                   ) -> List[schemas.Material]:
    """
    **This function return a list of all materials.**

    :param db: **Session with db connection**
    :return: **a 200 response if successful, and a list of all materials.**

    **Authorization level: 4**
    """
    if current_user.auth_level < 4:
        raise ROLE_EXCEPTION
    material_crud = crud.MaterialCrud(db=db)
    return material_crud.get_materials()

@router.get("/materials/{material_id}")
def read_material(material_id: int,
                  current_user: schemas.User = Depends(get_current_user),
                  db: Session = Depends(get_db)
                  ):
    """
    **This function return the data of an individual material searched by id.**

    :param material_id: **the id of the material**
    :param db: **Session with db connection**
    :return: **a 200 response if successful, and the data of an individual material.**

    **Authorization level: 4**
    """
    if current_user.auth_level < 4:
        raise ROLE_EXCEPTION
    material_crud = crud.MaterialCrud(db=db)
    return material_crud.get_material(material_id=material_id)

@router.patch("/materials/{material_id}", response_model=schemas.MaterialUpdate)
def partial_update_material(
        material_id: int,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user),
        name: Annotated[str | None, Form()] = None,
        unit: Annotated[str | None, Form()] = None,
        price: Annotated[str | None, Form()] = None,
        supplier_id: Annotated[str | None, Form()] = None,
):
    """
    **This endpoint update an individual material by id.**

    :param material_id: **the id of the material -> mandatory**
    :param db: **Session with db connection -> mandatory**
    :param name: **the name of the material -> optional**
    :param unit: **the unit of the material -> optional**
    :param price: **the price of the material -> optional**
    :param supplier_id: **the supplier id of the material -> optional**
    :return: **a 200 response if successful, and the data of an individual material.**

    **Authorization level: 5 **
    """
    if current_user.auth_level < 5:
        raise ROLE_EXCEPTION
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
def delete_material(material_id: int,
                    current_user: schemas.User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    """
    **This endpoint delete an individual material by id.**
    :param material_id: **the id of the material -> mandatory**
    :param db: **Session with db connection -> mandatory**
    :return: **a 200 response if successful, and the data of an individual material.**
    **Authorization level: 6 **
    """
    if current_user.auth_level < 6:
        raise ROLE_EXCEPTION
    material_crud = crud.MaterialCrud(db=db)
    return material_crud.delete_material(material_id=material_id)


# -------------- packaging materials endpoints  ----------------------- #


@router.post("/package-materials/", response_model=schemas.PackageMaterial)
def create_package_material(package_material: Annotated[schemas.PackageMaterialCreate, Form()],
                    current_user: schemas.User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    """
    **This function add a new package material to db.**

    :param material: **payload with:**
     - name: **str, name of the package material -> mandatory**
     - supplier_id: **int, id of the supplier material -> optional**
    :param db: **Session with db connection -> mandatory**
    :return: **a 200 response if successful, and data saved.**

    **Authorization level: 5**
    """
    if current_user.auth_level < 5:
        raise ROLE_EXCEPTION

    package_material_crud = crud.PackageMaterialCrud(db=db)
    return package_material_crud.create_package_material(package_material=package_material)


@router.get("/package-materials/", response_model=List[schemas.PackageMaterial])
def read_package_materials(current_user: schemas.User = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    """
    **This function return a list of all package materials.**

    :param db: **Session with db connection**
    :return: **a 200 response if successful, and a list of all materials.**

    **Authorization level: 4**
    """
    if current_user.auth_level < 4:
        raise ROLE_EXCEPTION
    package_material_crud = crud.PackageMaterialCrud(db=db)
    return package_material_crud.get_package_materials()

@router.get("/package-materials/{package_material_id}")
def read_package_material(package_material_id: int,
                          current_user: schemas.User = Depends(get_current_user),
                          db: Session = Depends(get_db)
                          ):
    """
    **This function return the data of an individual package material searched by id.**

    :param package_material_id: **the id of the material**
    :param db: **Session with db connection**
    :return: **a 200 response if successful, and the data of an individual package material.**

    **Authorization level: 4**
    """
    if current_user.auth_level < 4:
        raise ROLE_EXCEPTION
    package_material_crud = crud.PackageMaterialCrud(db=db)
    return package_material_crud.get_package_material(package_material_id=package_material_id)

@router.patch("/package-materials/{package_material_id}", response_model=schemas.PackageMaterialUpdate)
def partial_update_package_material(
        package_material_id: int,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user),
        name: Annotated[str | None, Form()] = None,
        price: Annotated[str | None, Form()] = None,
        supplier_id: Annotated[str | None, Form()] = None,
):
    """
    **This endpoint update an individual material by id.**

    :param package_material_id: **the id of the packaging material -> mandatory**
    :param db: **Session with db connection -> mandatory**
    :param name: **the name of the material -> optional**
    :param price: **the price of the material -> optional**
    :param supplier_id: **the supplier id of the material -> optional**
    :return: **a 200 response if successful, and the data of an individual material.**

    **Authorization level: 5**
    """
    if current_user.auth_level < 5:
        raise ROLE_EXCEPTION
    package_material_update = {}
    if name:
        package_material_update['name'] = name
    if price:
        package_material_update['price'] = float(price)
    if supplier_id:
        package_material_update['supplier_id'] = int(supplier_id)

    package_material_update_data = schemas.PackageMaterialUpdate(**package_material_update)
    package_material_crud = crud.PackageMaterialCrud(db=db)

    return package_material_crud.update_package_material(
        package_material=package_material_update_data,
        package_material_id=package_material_id
    )


@router.delete("/package-materials/{package_material_id}", response_model=schemas.PackageMaterial)
def delete_material(package_material_id: int,
                    current_user: schemas.User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    """
    **This endpoint delete an individual package material by id.**
    :param package_material_id: **the id of the package material -> mandatory**
    :param db: **Session with db connection -> mandatory**
    :return: **a 200 response if successful, and the data of an individual package material.**
    **Authorization level: 6**
    """
    if current_user.auth_level < 6:
        raise ROLE_EXCEPTION
    package_material_crud = crud.PackageMaterialCrud(db=db)
    return package_material_crud.delete_package_material(package_material_id=package_material_id)


# -------------- suppliers endpoints  ----------------------- #


@router.post("/suppliers/", response_model=schemas.Supplier)
def create_supplier(supplier: Annotated[schemas.SupplierCreate, Form()],
                    current_user: schemas.User = Depends(get_current_user),
                    db: Session = Depends(get_db)
                    ):
    """
        **This function add a new supplier to db.**

        :param supplier: **payload with **
        - supplier_name. str -> mandatory,
        - supplier_address. str -> mandatory,
        - phone_1. str -> optional,
        - phone_2. str -> optional,
        - deliver. bool (The supplier deliver materials?) default: false
        :param db: **Session with db connection**
        :return: **a 200 response if successful, and data saved.**

        **Authorization level: 5**
        """
    if current_user.auth_level < 5:
        raise ROLE_EXCEPTION
    supplier_crud = crud.SupplierCrud(db=db)
    return supplier_crud.create_supplier(supplier)

@router.get("/suppliers/", response_model=List[schemas.Supplier])
def read_suppliers(current_user: schemas.User = Depends(get_current_user),
                   db: Session = Depends(get_db)
                   ):
    """
        **This function return a list of all suppliers.**

        :param db: **Session with db connection**
        :return: **a 200 response if successful, and a list of all suppliers.**

        **Authorization level: 4**
        """
    if current_user.auth_level < 4:
        raise ROLE_EXCEPTION
    supplier_crud = crud.SupplierCrud(db=db)
    return supplier_crud.get_suppliers()

@router.get("/suppliers/{supplier_id}")
def read_supplier(supplier_id: int,
                  current_user: schemas.User = Depends(get_current_user),
                  db: Session = Depends(get_db)
                  ):
    """
        **This function return the data of an individual supplier searched by id.**

        :param supplier_id: **the id of the supplier -> mandatory**
        :param db: **Session with db connection -> mandatory**
        :return: **a 200 response if successful, and the data of an individual supplier.**

        **Authorization level: 4**
        """
    if current_user.auth_level < 4:
        raise ROLE_EXCEPTION
    supplier_crud = crud.SupplierCrud(db=db)
    return supplier_crud.get_supplier(supplier_id=supplier_id)

@router.patch("/suppliers/{supplier_id}", response_model=schemas.SupplierUpdate)
def partial_update_supplier(
        supplier: schemas.SupplierUpdate,
        supplier_id: int,
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
        **This endpoint update an individual supplier by id.**

        :param supplier_id: **the id of the material -> mandatory**
        :param db: **Session with db connection -> mandatory**
        :return: **a 200 response if successful, and the data of an individual supplier.**

        **fields to update:**

        - supplier_name: **str, the name of the supplier -> optional**
        - supplier_address: **str, the address of the supplier -> optional**
        - phone_1: **str, main phone of the supplier -> optional**
        - phone_2: **str, additional phone of the supplier -> optional**
        - deliver: **bool, the supplier can deliver material? -> optional**

        **Authorization level: 5**
        """
    if current_user.auth_level < 5:
        raise ROLE_EXCEPTION
    supplier_crud = crud.SupplierCrud(db=db)
    return supplier_crud.update_supplier(supplier=supplier, supplier_id=supplier_id)

@router.delete("/suppliers/{supplier_id}", response_model=schemas.Supplier)
def delete_supplier(supplier_id: int,
                    current_user: schemas.User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    """
        **This endpoint delete an individual supplier by id.**
        :param material_id: **the id of the material -> mandatory**
        :param db: **Session with db connection -> mandatory**
        :return: **a 200 response if successful, and the data of an individual supplier.**
        **Authorization level: 6**
        """
    if current_user.auth_level < 6:
        raise ROLE_EXCEPTION
    supplier_crud = crud.SupplierCrud(db=db)
    return supplier_crud.delete_supplier(supplier_id=supplier_id)


# -------------- products endpoints  ----------------------- #


@router.post("/products/", response_model=schemas.Product)
def create_product(product: Annotated[schemas.ProductCreate, Form()],
                    current_user: schemas.User = Depends(get_current_user),
                    db: Session = Depends(get_db)
                    ):
    """
        **This endpoint add a new product to db.**

        :param product: **payload with:**
        - **product_name:** str -> mandatory,
        - **size:** float -> mandatory.
        :param db: **Session with db connection**
        :return: **a 200 response if successful, and data saved.**

        **Authorization level: 5**
        """
    if current_user.auth_level < 5:
        raise ROLE_EXCEPTION
    product_crud = crud.ProductCrud(db=db)
    return product_crud.create_product(product=product)

@router.get("/products/", response_model=List[schemas.Product])
def read_products(current_user: schemas.User = Depends(get_current_user),
                   db: Session = Depends(get_db)
                   ):
    """
        **This function return a list of all products.**

        :param db: **Session with db connection**
        :return: **a 200 response if successful, and a list of all products.**

        **Authorization level: 4**
        """
    if current_user.auth_level < 4:
        raise ROLE_EXCEPTION
    product_crud = crud.ProductCrud(db=db)
    return product_crud.get_products()

@router.get("/products/{product_id}")
def read_product(product_id: int,
                  current_user: schemas.User = Depends(get_current_user),
                  db: Session = Depends(get_db)
                  ):
    """
        **This function return the data of an individual product searched by id.**

        :param product_id: **the id of the product -> mandatory**
        :param db: **Session with db connection -> mandatory**
        :return: **a 200 response if successful, and the data of an individual product.**

        **Authorization level: 4**
        """
    if current_user.auth_level < 4:
        raise ROLE_EXCEPTION
    product_crud = crud.ProductCrud(db=db)
    return product_crud.get_product(product_id=product_id)

@router.patch("/products/{product_id}", response_model=schemas.ProductUpdate)
def partial_update_product(
        product: schemas.ProductUpdate,
        product_id: int,
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
        ):
    """
        **This endpoint update an individual product by id.**

        :param supplier_id: **the id of the material -> mandatory**
        :param db: **Session with db connection -> mandatory**
        :return: **a 200 response if successful, and the data of an individual supplier.**

        **fields to update:**

        - **name:** **str, the name of the product -> optional**
        - **size**: **float, the size of the product -> optional**

        **Authorization level: 5**
        """
    if current_user.auth_level < 5:
        raise ROLE_EXCEPTION
    product_crud = crud.ProductCrud(db=db)
    return product_crud.update_product(product=product, product_id=product_id)

@router.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int,
                    current_user: schemas.User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    """
        **This endpoint delete an individual product by id.**
        :param product_id: **the id of the product -> mandatory**
        :param db: **Session with db connection -> mandatory**
        :return: **a 200 response if successful, and the data of the deleted product.**
        **Authorization level: 6**
        """
    if current_user.auth_level < 6:
        raise ROLE_EXCEPTION
    product_crud = crud.ProductCrud(db=db)
    return product_crud.delete_product(product_id=product_id)
