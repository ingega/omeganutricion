# src/crud.py
import datetime
from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session
from http.client import HTTPException
from src import utils
from src.services.products import models, schemas
from src.services.products.auth import password_hashed


"""
This module contains all CRUD classes, every class contains:
    Create a new object
    Read a single object
    Read the entire model
    Update a single object
    Delete a single object
Some methods uses special function to update Stocks
    BatchCreate: update the BatchMaterialStock (microservice)
    BatchProductCreate: update the BatchProductStock (microservice) 
"""


# user tables

class UserCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int):
        user_info = self.db.query(models.UserDB).filter(
            models.UserDB.id == user_id).first()
        if not user_info:
            return None
        return user_info

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.UserDB).offset(skip).limit(limit).all()

    def create_user(self, user: schemas.UserCreate):
        db_user = models.UserDB(**user.model_dump())
        # the password must be hashed
        plain_password = user.password
        hashed_password = password_hashed(plain_password)
        db_user.password = hashed_password
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self,
                    user: schemas.UserUpdate,
                    user_id: int
                    ):
        db_user = self.db.query(models.UserDB).get(user_id)
        update_data = user.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(db_user, key, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        db_user = self.get_user(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()

        return db_user

#########  MAIN TABLES    ###############

class SupplierCrud:
    """
    This class handles the supplier data:
        supplier name: The commercial or personal name of the supplier.
        supplier address: The main addres of the supplier.
        phone 1: The main phone number of the supplier.
        phone 2: A secondary phone number of the supplier.
        deliver: Indicates if the supplier can deliver the materials in the client address.
    """
    def __init__(self, db: Session):
        """
        Initialize the CRUD class.
        :param db:session of the actual db
        """
        self.db = db

    def get_supplier(self, supplier_id: int):
        """
        This method returns the data of an individual supplier.
        :param supplier_id: Id of the supplier.
        :return: supplier object
        """
        return self.db.query(models.SupplierDB).filter(
            models.SupplierDB.id == supplier_id).first()

    def get_suppliers(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.SupplierDB).offset(skip).limit(limit).all()

    def create_supplier(self, supplier: schemas.SupplierCreate):
        db_supplier = models.SupplierDB(**supplier.model_dump())
        self.db.add(db_supplier)
        self.db.commit()
        self.db.refresh(db_supplier)
        return db_supplier

    def update_supplier(self,
                        supplier: schemas.SupplierUpdate,
                        supplier_id: int
                        ):
        db_supplier = self.db.get(models.SupplierDB, supplier_id)
        update_data = supplier.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_supplier, key, value)

        self.db.commit()
        self.db.refresh(db_supplier)
        return db_supplier

    def delete_supplier(self, supplier_id: int):
        db_supplier = self.get_supplier(supplier_id=supplier_id)

        if db_supplier:
            self.db.delete(db_supplier)
            self.db.commit()

        return db_supplier


class MaterialCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_material(self, material_id: int):
        # testing in memory db, requieres maintain data, even after a close
        # using make_transient is possible
        material = self.db.query(models.MaterialDB).filter(
            models.MaterialDB.id == material_id).first()
        return material

    def get_materials(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.MaterialDB).offset(skip).limit(limit).all()

    def create_material(self, material: schemas.MaterialCreate):
        db_material = models.MaterialDB(**material.model_dump())
        self.db.add(db_material)
        self.db.commit()
        self.db.refresh(db_material)
        return db_material

    def update_material(self,
                        material: schemas.MaterialUpdate,
                        material_id: int
                        ):
        db_material = self.db.get(models.MaterialDB, material_id)
        update_data = material.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_material, key, value)

        self.db.commit()
        self.db.refresh(db_material)
        return db_material

    def delete_material(self, material_id: int):
        db_material = self.get_material(material_id=material_id)

        if db_material:
            self.db.delete(db_material)
            self.db.commit()

        return db_material


class PackageMaterialCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_package_material(self, package_material_id: int):
        return self.db.query(models.PackageMaterialDB).filter(
            models.PackageMaterialDB.id == package_material_id
        ).first()

    def get_package_materials(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.PackageMaterialDB).offset(skip).limit(limit).all()

    def create_package_material(self,
                        package_material: schemas.PackageMaterialCreate
                        ):
        db_package_material = models.PackageMaterialDB(**package_material.model_dump())
        self.db.add(db_package_material)
        self.db.commit()
        self.db.refresh(db_package_material)
        return db_package_material

    def update_package_material(self, package_material_id: int,
                        package_material: schemas.PackageMaterialUpdate
                        ):
        db_package_material = self.db.get(models.PackageMaterialDB, package_material_id)
        update_data = package_material.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_package_material, key, value)

        self.db.add(db_package_material)
        self.db.commit()
        self.db.refresh(db_package_material)

        return db_package_material

    def delete_package_material(self, package_material_id: int):
        db_package_material = self.db.get(models.PackageMaterialDB, package_material_id)
        self.db.delete(db_package_material)
        self.db.commit()

        return db_package_material


class ProductCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_product(self, product_id: int):
        return self.db.query(models.ProductDB).filter(
            models.ProductDB.id == product_id).first()

    def get_products(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.ProductDB).offset(skip).limit(limit).all()

    def create_product(self, product: schemas.ProductCreate):
        db_product = models.ProductDB(**product.model_dump())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def update_product(self,
                       product: schemas.ProductUpdate,
                       product_id: int
                       ):
        db_product = self.db.get(models.ProductDB, product_id)
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)

        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def delete_product(self, product_id: int):
        db_product = self.get_product(product_id=product_id)

        if db_product:
            self.db.delete(db_product)
            self.db.commit()

        return db_product


class FormulaCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_formula(self, product_id: int):
        return self.db.query(models.FormulaDB).filter(
            models.FormulaDB.product_id == product_id).all()

    def get_formulas(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.FormulaDB).offset(skip).limit(limit).all()

    def create_formula(self, formula: schemas.FormulaCreate):
        db_formula = models.FormulaDB(**formula.model_dump())
        self.db.add(db_formula)
        self.db.commit()
        self.db.refresh(db_formula)
        return db_formula

    def update_formula_row(self,
                       product_id: int,
                       material_id: int,
                       quantity: float
                       ):
        """
        The index in a formula is the product_id, so, updating a formula, is updating a
        row in the formula table.
        :param product_id: the id of the product to be updated
        :param material_id: the id of the material
        :param quantity: the new quantity
        :return: a tuple with a message and None | query object
        """
        message = ""
        db_formula = self.db.query(models.FormulaDB).filter(
            models.FormulaDB.product_id == product_id
            & models.FormulaDB.material_id == material_id).first()
        if not db_formula:
            message = (f"There is no row with material_id {material_id} "
                       f"and product_id {product_id} in formula table")
            return None, message
        # edit the quantity
        db_formula.quantity = quantity
        self.db.commit()
        self.db.refresh(db_formula)
        return db_formula, message

    def delete_formula_row(self, product_id: int, material_id: int):
        message = ""
        db_formula = self.db.query(models.FormulaDB).filter(
            models.FormulaDB.product_id == product_id
            & models.FormulaDB.material_id == material_id).first()
        if not db_formula:
            message = (f"There is no row with material_id {material_id} "
                       f"and product_id {product_id} in formula table")
            return None, message

        self.db.delete(db_formula)
        self.db.commit()

        return db_formula, message


class PackageComposeCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_package_compose(self, product_id: int):
        return self.db.query(models.FormulaDB).filter(
            models.PackageComposeDB.product_id == product_id).all()

    def get_composes(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.PackageComposeDB).offset(skip).limit(limit).all()

    def add_package_compose_row(self, package_compose: schemas.PackageComposeCreate):
        db_compose = models.PackageComposeDB(**package_compose.model_dump())
        self.db.add(db_compose)
        self.db.commit()
        self.db.refresh(db_compose)
        return db_compose

    def delete_package_compose_row(self, product_id: int, package_material_id: int):
        message = ""
        db_compose = self.db.query(models.PackageComposeDB).filter(
            models.PackageComposeDB.product_id == product_id
            & models.PackageMaterialDB.package_material_id
            == package_material_id).first()
        if not db_compose:
            message = (f"There is no row with package_material_id {package_material_id} "
                       f"and product_id {product_id} in package compose table")
            return None, message

        self.db.delete(db_compose)
        self.db.commit()

        return db_compose, message