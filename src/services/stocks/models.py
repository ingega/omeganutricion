



""" stock models """


class MaterialStockDB(Base):
    __tablename__ = "material_stock"
    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("material.id"))
    actual_balance = Column(Float)
    # relationships
    material = relationship(
        "MaterialDB", back_populates="material_stock"
    )


class ProductStockDB(Base):
    __tablename__ = "product_stock"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    actual_balance = Column(Integer)
    # relationships
    product = relationship(
        "ProductDB",
        back_populates="product_stock"
    )


class BatchStockDB(Base):
    __tablename__ = "batch_stock"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    actual_balance = Column(Float)
    # relationships
    product = relationship(
        "ProductDB", back_populates="batch_stock"
    )