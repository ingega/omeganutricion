#src/services/products/endpoints/formulas_ep.py
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import Annotated, List

from src.services.products import schemas, crud
from src.services.products.database import get_db
from src.services.products.auth import get_current_user
from src.services.products.endpoints.users_ep import ROLE_EXCEPTION


router = APIRouter()


# -------------- formula endpoints  ----------------------- #


@router.post("/formulas/", response_model=schemas.Formula)
def create_formula(formula: Annotated[schemas.FormulaCreate, Form()],
                    current_user: schemas.User = Depends(get_current_user),
                    db: Session = Depends(get_db)
                    ):
    """
        **This endpoint add a new formula to db.**

        :param formula: **payload with:**
        - **product_id:** int -> mandatory. <The id of the formula's product>
        - **material_id:** int -> mandatory. <The id of the material in formula>
        - **quantity:** float -> mandatory. <The quantity of material in formula>

        :param db: **Session with db connection**

        :return: **a 200 response if successful, and data saved.**

        **Authorization level: 6**
        """
    if current_user.auth_level < 6:
        raise ROLE_EXCEPTION
    formula_crud = crud.FormulaCrud(db=db)
    return formula_crud.create_formula(formula=formula)

@router.get("/formulas/", response_model=List[schemas.Formula])
def read_formulas(current_user: schemas.User = Depends(get_current_user),
                   db: Session = Depends(get_db)
                   ):
    """
        **This function return a list of all formulas in the db.**

        :param db: **Session with db connection**
        :return: **a 200 response if successful, and a list of all formulas.**

        **Authorization level: 6**
        """
    if current_user.auth_level < 6:
        raise ROLE_EXCEPTION
    formula_crud = crud.FormulaCrud(db=db)
    return formula_crud.get_formulas()

@router.get("/formulas/{product_id}")
def read_formula(product_id: int,
                  current_user: schemas.User = Depends(get_current_user),
                  db: Session = Depends(get_db)
                  ):
    """
        **This function return a list of materials per formula, filtered by product id.**

        :param product_id: **the id of the formula's product -> mandatory**

        :param db: **Session with db connection -> mandatory**

        :return: **a 200 response if successful, and the data of an individual product.**

        **Authorization level: 6**
        """
    if current_user.auth_level < 6:
        raise ROLE_EXCEPTION
    formula_crud = crud.FormulaCrud(db=db)
    return formula_crud.get_formula(product_id=product_id)

@router.patch("/formulas/{product_id}{material_id}", response_model=schemas.FormulaUpdate)
def update_formula_row(
        product_id: int,
        material_id: int,
        quantity: Annotated[float, Form()],
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
        ):
    """
        **This endpoint update a formula's.**
        - with a product_id and material id could edit the quantity of material in formula.

        :param product_id: **the id of the formula's product -> mandatory**

        :param material_id: **the id of the formula's material -> mandatory**

        :param quantity: **the quantity of material in formula.**

        :param db: **Session with db connection -> mandatory**

        :return: **a 200 response if successful, and the data of an individual supplier.**


        **Authorization level: 6**
        """
    if current_user.auth_level < 6:
        raise ROLE_EXCEPTION
    formula_crud = crud.FormulaCrud(db=db)
    result, message = formula_crud.update_formula_row(
        product_id=product_id, material_id=material_id, quantity=quantity)
    if not result:
        raise HTTPException(status_code=404, detail=message)

    return result

@router.delete("/formulas/{product_id}{material_id}", response_model=schemas.Supplier)
def delete_formula_row(product_id: int,
                   material_id: int,
                   current_user: schemas.User = Depends(get_current_user),
                   db: Session = Depends(get_db)
                   ):
    """
        **This endpoint delete a row in formula table**
        :param product_id: **the id of the product -> mandatory**
        :param material_id: **the id of the formula's material -> mandatory**
        :param db: **Session with db connection -> mandatory**
        :return: **a 200 response if successful, and the data of the deleted row.**
        **Authorization level: 7**
        """
    if current_user.auth_level < 7:
        raise ROLE_EXCEPTION
    formula_crud = crud.FormulaCrud(db=db)
    result, message = formula_crud.delete_formula_row(product_id=product_id, material_id=material_id)
    if not result:
        raise HTTPException(status_code=404, detail=message)
    return result


# -------------- package compose endpoints  ----------------------- #


@router.post("/package-compose/", response_model=schemas.PackageCompose)
def add_package_compose_row(compose: Annotated[schemas.PackageComposeCreate, Form()],
                    current_user: schemas.User = Depends(get_current_user),
                    db: Session = Depends(get_db)
                    ):
    """
        **This endpoint add a new row to the package compose table.**

        :param compose: **payload with:**
        - **product_id:** int -> mandatory. <The id of the formula's product>
        - **material_id:** int -> mandatory. <The id of the material in formula>

        :param db: **Session with db connection**

        :return: **a 200 response if successful, and data saved.**

        **Authorization level: 6**
        """
    if current_user.auth_level < 6:
        raise ROLE_EXCEPTION
    compose_crud = crud.PackageComposeCrud(db=db)
    return compose_crud.add_package_compose_row(package_compose=compose)

@router.get("/package-compose/", response_model=List[schemas.PackageCompose])
def read_composes(current_user: schemas.User = Depends(get_current_user),
                   db: Session = Depends(get_db)
                   ):
    """
        **This function return a list of all package composes in the db.**

        :param db: **Session with db connection**
        :return: **a 200 response if successful, and a list of all formulas.**

        **Authorization level: 6**
        """
    if current_user.auth_level < 6:
        raise ROLE_EXCEPTION
    compose_crud = crud.PackageComposeCrud(db=db)
    return compose_crud.get_composes()

@router.get("/package-compose/{product_id}")
def read_compose(product_id: int,
                  current_user: schemas.User = Depends(get_current_user),
                  db: Session = Depends(get_db)
                  ):
    """
        **This function return a list of materials per pacakge compose, filtered by product id.**

        :param product_id: **the id of the package compose product -> mandatory**

        :param db: **Session with db connection -> mandatory**

        :return: **a 200 response if successful, and the data of an individual compose.**

        **Authorization level: 6**
        """
    if current_user.auth_level < 6:
        raise ROLE_EXCEPTION
    compose_crud = crud.PackageComposeCrud(db=db)
    return compose_crud.get_package_compose(product_id=product_id)

@router.delete("/package-compose/{product_id}{package_material_id}",
               response_model=schemas.PackageCompose)
def delete_package_compose_row(product_id: int,
                   package_material_id: int,
                   current_user: schemas.User = Depends(get_current_user),
                   db: Session = Depends(get_db)
                   ):
    """
        **This endpoint delete a row in package compose table**

        :param product_id: **the id of the product -> mandatory**

        :param package_material_id: **the id of the formula's material -> mandatory**

        :param db: **Session with db connection -> mandatory**

        :return: **a 200 response if successful, and the data of the deleted row.**

        **Authorization level: 7**
        """
    if current_user.auth_level < 7:
        raise ROLE_EXCEPTION
    compose_crud = crud.PackageComposeCrud(db=db)
    result, message = compose_crud.delete_package_compose_row(
        product_id=product_id, package_material_id=package_material_id)
    if not result:
        raise HTTPException(status_code=404, detail=message)
    return result