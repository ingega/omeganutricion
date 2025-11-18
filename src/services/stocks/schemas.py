#src/services/stocks/schemas.py
from pydantic import BaseModel, ConfigDict

""" 
The schemas uses a base, a creation, a main and update schema
The schemas in this services are:
    MaterialStock: Balance of raw materials
    PackagingStock: Balance of packaging materials
    ProductStock: Balance of finished products
    BatchStock: Balance of prepared batches of formula for a product
"""

# stock_material
class MaterialStockBase(BaseModel):
    material_id: int
    actual_balance: float


class MaterialStockCreate(MaterialStockBase):
    pass


class MaterialStock(MaterialStockBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MaterialStockUpdate(BaseModel):
    material_id: int | None = None
    actual_balance: float


# product
class FormProductStockBase(BaseModel):
    product_id: int
    actual_balance: int


class FormProductStockCreate(FormProductStockBase):
    pass


class FormProductStock(FormProductStockBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FormProductStockUpdate(BaseModel):
    product_id: int | None = None
    actual_balance: int


# batch

class BatchStockBase(BaseModel):
    product_id: int
    actual_balance: float


class BatchStockCreate(BatchStockBase):
    pass


class BatchStock(BatchStockBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BatchStockUpdate(BaseModel):
    product_id: int | None = None
    actual_balance: float