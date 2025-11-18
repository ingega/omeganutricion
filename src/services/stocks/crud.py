# src/services/stocks/crud.py
from sqlalchemy.orm import Session
from .models import *
from .schemas import *


########### STOCK TABLES ######################


class MaterialStockCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_material(self, material_id: int):
        return self.db.query(MaterialStockDB).filter(
            MaterialStockDB.material_id == material_id).first()

    def get_materials(self, skip: int = 0, limit: int = 100):
        return self.db.query(
            MaterialStockDB).offset(skip).limit(limit).all()

    def create_material_stock(self, material: MaterialStockCreate):
        db_material = MaterialStockDB(**material.model_dump())
        self.db.add(db_material)
        self.db.commit()
        self.db.refresh(db_material)
        return db_material

    def update_material_stock(self,
                              material: MaterialStockUpdate,
                              material_id: int,
                              actual_balance: float
                              ):
        db_material = self.db.query(MaterialStockDB).get(material_id)
        update_data = material.model_dump(exclude_unset=True)
        update_data['actual_balance'] = actual_balance

        self.db.commit()
        self.db.refresh(db_material)
        return db_material

    def delete_supplier(self, supplier_id: int):
        db_supplier = self.get_supplier(supplier_id=supplier_id)

        if db_supplier:
            self.db.delete(db_supplier)
            self.db.commit()

        return db_supplier


class ProductStockCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_stock_product(self, product_id: int):
        return self.db.query(ProductStockDB).filter(
            ProductStockDB.id == product_id).first()

    def get_stock_products(self, skip: int = 0, limit: int = 100):
        return self.db.query(
            ProductStockDB).offset(skip).limit(limit).all()

    def create_product_stock(self,
                             product: FormProductStockCreate
                             ):
        """
        In order to add product to the stock, is necessary:
        1. verify that is enough batch in stock
        2. subtract the batch stock used
        3. Finally add the product to the stock
        """
        # catch data from Form
        db_product = ProductStockDB(**product.model_dump())
        # 1 verify the batch stock
        verify_stock, message = self.verify_enough_batch(
            db_product.product_id, db_product.actual_balance)
        if message:
            return None, message
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def update_stock_product(self,
                             product: FormProductStockUpdate,
                             product_id: int
                             ):
        db_product = self.db.query(ProductStockDB).get(product_id)
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)

        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def delete_product(self, product_id: int):
        db_product = self.get_stock_product(product_id=product_id)

        if db_product:
            self.db.delete(db_product)
            self.db.commit()

        return db_product


class FormProductStockCrud:
    pass