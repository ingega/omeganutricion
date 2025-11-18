# src/models.py
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.services.products.database import Base

# auth models

class UserDB(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    full_name = Column(String)
    email = Column(String)
    password = Column(String, nullable=False)  # hashed
    auth_level = Column(Integer)


# app main models


class SupplierDB(Base):
    __tablename__ = "supplier"
    id = Column(Integer, primary_key=True, index=True)
    supplier_name = Column(String, index=True)
    supplier_address = Column(String, index=True)
    phone_1 = Column(String)
    phone_2 = Column(String)
    deliver = Column(Boolean, server_default='false', nullable=False)

    # relations
    material = relationship(
        "MaterialDB", back_populates="supplier"
    )
    package_material = relationship(
        "PackageMaterialDB", back_populates="supplier"
    )


class MaterialDB(Base):
    __tablename__ = "material"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    unit = Column(String, index=True)
    price = Column(Float)
    supplier_id = Column(Integer, ForeignKey("supplier.id"))

    # relationships
    formula = relationship("FormulaDB", back_populates="material")
    supplier = relationship("SupplierDB", back_populates="material")


class PackageMaterialDB(Base):
    __tablename__ = 'package_material'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    supplier_id = Column(Integer, ForeignKey('supplier.id'))

    # foreign keys
    supplier = relationship("SupplierDB", back_populates='package_material')
    package_compose = relationship("PackageComposeDB", back_populates='package_material')


class ProductDB(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    size = Column(Float)

    # relationships
    formula = relationship("FormulaDB", back_populates="product")
    product_batch = relationship("ProductBatchDB", back_populates="product")
    package_compose = relationship("PackageComposeDB", back_populates="product")


class FormulaDB(Base):
    __tablename__ = "formula"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    material_id = Column(Integer, ForeignKey("material.id"))
    quantity = Column(Float)
    # relationships
    product = relationship("ProductDB", back_populates="formula")
    material = relationship(
        "MaterialDB", back_populates="formula"
    )


class PackageComposeDB(Base):
    __tablename__ = 'package_compose'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    package_material_id = Column(Integer, ForeignKey('package_material.id'))

    # foreign keys
    product = relationship("ProductDB", back_populates='package_compose')
    package_material = relationship("PackageMaterialDB", back_populates='package_compose')


class BatchDB(Base):
    __tablename__ = "batch"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    batch_id = Column(String, index=True)
    quantity = Column(Float)
    last_update = Column(DateTime(timezone=True), server_default=func.now())


class ProductBatchDB(Base):
    __tablename__ = "product_batch"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    product_batch_id = Column(String)
    pieces = Column(Float)
    last_update = Column(DateTime(timezone=True), server_default=func.now())

    # relations
    product = relationship("ProductDB", back_populates="product_batch")
