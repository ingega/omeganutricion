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
        db_supplier = self.db.query(models.SupplierDB).get(supplier_id)
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
        db_material = self.db.query(models.MaterialDB).get(material_id)
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

    def get_package_material(self, material_id: int):
        return self.db.query(models.PackageMaterialDB).filter(
            models.PackageMaterialDB.material_id == material_id
        ).first()

    def get_package_materials(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.PackageMaterialDB).offset(skip).limit(limit).all()

    def create_material(self,
                        package_material: schemas.PackageMaterialCreate
                        ):
        db_package_material = models.PackageMaterialDB(**package_material.model_dump())
        self.db.add(db_package_material)
        self.db.commit()
        self.db.refresh(db_package_material)
        return db_package_material

    def update_material(self, package_material_id: int,
                        package_material: schemas.PackageMaterialUpdate
                        ):
        db_package_material = self.db.query(models.PackageMaterialDB).get(package_material_id)
        update_data = package_material.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_package_material, key, value)

        self.db.add(db_package_material)
        self.db.commit()
        self.db.refresh(db_package_material)

        return db_package_material

    def delete_material(self, material_id: int):
        db_package_material = self.db.query(models.PackageMaterialDB).get(material_id)
        self.db.delete(db_package_material)
        self.db.commit()
        self.db.refresh(db_package_material)

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
        db_product = self.db.query(models.ProductDB).get(product_id)
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

    def update_formula(self,
                       formula: schemas.FormulaUpdate,
                       formula_id: int
                       ):
        db_formula = self.db.query(models.FormulaDB).get(formula_id)
        update_data = formula.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_formula, key, value)

        self.db.commit()
        self.db.refresh(db_formula)
        return db_formula

    def delete_formula(self, formula_id: int):
        db_formula = self.get_formula(formula_id=formula_id)

        if db_formula:
            self.db.delete(db_formula)
            self.db.commit()

        return db_formula

    """auxiliary functions"""

    def get_formula_weight(self, product_id: int):
        # get the formula by product
        formula = self.get_formula(product_id=product_id)
        if not formula:
            return None
        # calculate weight
        total_weight = 0
        for item in formula:
            total_weight += item.quantity
        return total_weight


class BatchCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_batch(self, batch_id: str):
        return self.db.query(models.BatchDB).filter(
            models.BatchDB.id == batch_id).first()

    def get_batches(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.BatchDB).offset(skip).limit(limit).all()

    def create_batch(self, batch: schemas.BatchCreate):
        """creates a batch requires enough materials to do it"""
        """
        1. Check if there's enough materials to do it
            a. Get the formula's materials list
                self.check_material_stock
            b. return the qty of each material for q batch
                self.check_formula_stock
            c. update batch stock
                self.update_stock_batch
            d. update materials stok
                self.update_material_stock
        """
        db_batch = models.BatchDB(**batch.model_dump())
        # 1.a get the formula's list
        formula_list = self.check_material_stock(db_batch.product_id, db_batch.quantity)
        # check if there's enough materials
        check_materials = self.check_formula_stock(formula_list)
        if not check_materials['outcome']:
            message = (f"{check_materials['message']} "
                       f"for product {check_materials['material_id']}")
            # return db as None
            return None, message
        self.db.add(db_batch)
        # the stock must be subtracted
        self.subtract_material(formula_list)
        self.db.commit()
        self.db.refresh(db_batch)
        # now updated the stock
        self.update_stock_batch(db_batch.product_id, db_batch.quantity)
        self.db.commit()
        self.db.refresh(db_batch)
        # return message as None
        return db_batch, None

    def update_batch(self,
                     batch: schemas.BatchUpdate,
                     batch_id: int
                     ):
        db_batch = self.db.query(models.BatchDB).get(batch_id)
        update_data = batch.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_batch, key, value)

        self.db.commit()
        self.db.refresh(db_batch)
        return db_batch

    def delete_batch(self, batch_id: int):
        db_batch = self.get_batch(batch_id=batch_id)

        if db_batch:
            self.db.delete(db_batch)
            self.db.commit()

        return db_batch

    def update_stock_batch(self,
                           product_id: int,
                           quantity: float
                           ):
        """At same time to add a record, the same quantity will be added.
        to the stock"""
        # 1. Find the record
        db_batch = self.db.query(
            models.BatchStockDB).filter(
            models.BatchStockDB.product_id == product_id
        ).first()
        # if exists, add the quantity, else, add the record
        if db_batch:
            db_batch.actual_balance += quantity
        else:
            db_batch = models.BatchStockDB(
                product_id=product_id,
                actual_balance=quantity
            )
            # add here, commit in the original function
            self.db.add(db_batch)

        return db_batch

    def check_material_stock(self, product_id: int, qty: float):
        """
        this function returns a list of materials used in a q batch
        of a p product
        """
        db_get_formula = self.db.query(
            models.FormulaDB).filter(
            models.FormulaDB.product_id == product_id).all()
        if db_get_formula:
            """
            strategy:
            1. loop to the formula items
            2. Save the value multiplied by qty.
            3. Return as a list of dict
            """
            material_list = []
            for item in db_get_formula:
                # quantity is for formula, qty for batch
                # the function returns the qty needed for a q batch
                item = {'material_id': item.material_id,
                        'quantity': item.quantity * qty}
                material_list.append(item)
            return material_list
        else:
            return HTTPException(status_code=404,
                                 detail="No formula's product found")

    def check_formula_stock(self, material_list: List[dict]):
        from src.main import debug_data
        """
        This function check if exists enough material to
        create the requested batch.
        strategy:
        1. iterate the material list
        2. check if there is enough material
        3. if it isn't, return False and the material_id
        """
        material_stock = MaterialStockCrud(db=self.db)
        final_response = {'message': 'insufficient stock',
                          'material_id': 0, "outcome": False}
        # Now I need to verify every material in material_list
        # with the actual_balance of this material
        for item in material_list:
            # find material
            debug_data(item, "item in check for stock")
            record_stock = material_stock.get_material(
                material_id=item['material_id'])
            debug_data(record_stock.material_id, "record_stock: material_id")
            debug_data(record_stock.actual_balance, "record_stock: actual_balance")
            if record_stock.actual_balance < item['quantity']:
                final_response['material_id'] = item['material_id']
                # final response already has the msg
                return final_response
        final_response['message'] = 'enough stock'
        final_response['outcome'] = True

        return final_response

    def subtract_material(self, material_list: list):
        """
        material_list: is list of dict with the values:
            material_id: the id of material
            quantity: the quantity of material
        This function subtracts material from stock, based in the list provided
        the list contains a material_id and quantity fields
        1. get the record for every material
        2. subtract material from stock
        """
        final_balance = []
        # the Model is updated directly in this function
        for item in material_list:
            # get the material
            material_to_update = self.db.query(models.MaterialStockDB).filter(
                models.MaterialStockDB.material_id == item['material_id']
            ).first()
            # update the quantity
            material_to_update.actual_balance -= item['quantity']
            # need the actual balance
            updated_item = {
                'material_id': item['material_id'],
                'quantity': material_to_update.actual_balance
            }
            final_balance.append(updated_item)
        # returns the actual balance
        return {'final_balance': final_balance}


class ProductBatchCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_product_batch(self, product_batch_id: str):
        return self.db.query(models.ProductBatchDB).filter(
            models.ProductBatchDB.id == product_batch_id).first()

    def get_product_batches(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.ProductBatchDB).offset(skip).limit(limit).all()

    def create_product_batch(self, product_batch: schemas.ProductBatchCreate):
        """creates a product batch requires enough material's batch to do it"""
        # ---------- Action Plan ---------------------#
        # In order to add product to the stock, is necessary:
        # 1. verify that is enough batch in stock
        # 2. subtract the batch stock used
        # 3. Finally add the product to the stock

        # ---------  code starts here ------------------------------------- #
        from src.main import debug_data
        # catch data from Form
        db_product = models.ProductBatchDB(**product_batch.model_dump())
        # 1 verify the batch stock
        verify_stock, message = self.verify_enough_batch(
            db_product.product_id, db_product.pieces)
        debug_data(verify_stock, "verify_stock")
        if message:
            return None, message
        # verify enough package material stock
        from .utils import verify_packaging_stock, subtract_packaging_material
        verify_packaging_material = verify_packaging_stock(db_product.product_id,
                                                           db_product.pieces, self.db)
        if not verify_packaging_material['error']:
            return None, verify_packaging_material['message']
        debug_data(verify_packaging_material, "verify_packaging_material")
        # once verified the stock, subtract from stock
        # in this point, all is set, now let's update the batch
        subtract_batch = self.subtract_material_batch(
            db_product.product_id, verify_stock['batch_qty'])
        # the stock of packaging must be updated too
        subtract_package_material = subtract_packaging_material()
        if not subtract_batch:
            message = "the function for subtract packaging stock failed"
            return None, message
        db_product.product_batch_id = utils.create_id()
        db_product.last_update = datetime.datetime.now()
        # and finally add the products to the stock
        self.update_product_stock(db_product.product_id, db_product.pieces)
        # add and commit all db objects
        self.db.add(db_product)
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product, None


    def update_batch(self,
                     batch: schemas.BatchUpdate,
                     batch_id: int
                     ):
        db_batch = self.db.query(models.BatchDB).get(batch_id)
        update_data = batch.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_batch, key, value)

        self.db.commit()
        self.db.refresh(db_batch)
        return db_batch

    def delete_batch(self, batch_id: int):
        db_batch = self.get_batch(batch_id=batch_id)

        if db_batch:
            self.db.delete(db_batch)
            self.db.commit()

        return db_batch

    def update_stock_batch(self,
                           product_id: int,
                           quantity: float
                           ):
        """At same time to add a record, the same quantity will be added.
        to the stock"""
        # 1. Find the record
        db_batch = self.db.query(
            models.BatchStockDB).filter(
            models.BatchStockDB.product_id == product_id
        ).first()
        from src.main import debug_data
        debug_data(db_batch)
        # if exists, add the quantity, else, add the record
        if db_batch:
            db_batch.actual_balance += quantity
        else:
            db_batch = models.BatchStockDB(
                product_id=product_id,
                actual_balance=quantity
            )
            self.db.add(db_batch)

        return db_batch

    """auxiliar functions"""

    def verify_enough_batch(self, product_id: int, pieces: int):
        from src.main import debug_data
        # get the query of batch
        db_batch = self.db.query(models.BatchStockDB).filter(
            models.BatchStockDB.product_id == product_id).first()
        if not db_batch:
            message = f"the product {product_id} is not in batch stock"
            return False, message
        # get the actual balance batch
        actual_balance = db_batch.actual_balance
        # get the size
        db_product = self.db.query(models.ProductDB).filter(
            models.ProductDB.id == product_id).first()
        if not db_product:
            message = f"the product {product_id} is not a valid product"
            return False, message
        # get the weight
        formula_crud = FormulaCrud(self.db)
        formula_weight = formula_crud.get_formula_weight(product_id)
        if not formula_weight:
            message = f"the product {product_id} is not in formulas"
            return False, message
        debug_data(db_product, "db_product")
        size = db_product.size
        debug_data(size, "size")
        batch_qty = (size * pieces) / formula_weight
        if actual_balance < batch_qty:
            message = f"there's not enough batch in stock for product {product_id}"
            return False, message
        # return the batch_qty, that is the relation between
        return {"batch_qty": batch_qty}, None

    def subtract_material_batch(self, product_id: int, qty: float):
        db_material_batch = self.db.query(models.BatchStockDB).filter(
            models.BatchStockDB.product_id == product_id
        ).first()
        if not db_material_batch:
            message = f"the product {product_id} is not in batch stock"
            return None, message
        db_material_batch.actual_balance -= qty
        self.db.add(db_material_batch)
        # commit is in main crud function
        return db_material_batch, None

    def update_product_stock(self,
                           product_id: int,
                           pieces: int
                           ):
        """At same time to add a record, the same quantity will be added.
        to the stock"""
        # 1. Find the record
        db_product_batch = self.db.query(
            models.ProductStockDB).filter(
            models.ProductStockDB.product_id == product_id
        ).first()
        # if exists, add the quantity, else, add the record
        if db_product_batch:
            db_product_batch.actual_balance += pieces
        else:
            db_product_batch = models.ProductStockDB(
                product_id=product_id,
                actual_balance=pieces
            )
            # add here, commit in the original function
            self.db.add(db_product_batch)
