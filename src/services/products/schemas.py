from pydantic import BaseModel, Field, ConfigDict, SecretStr
from typing import List
from datetime import datetime

# ---- Auxiliar functions  ------- #
def create_id():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


# Pydantic Schemas (for API Data Validation) ------ #

# ---- auth schemas ----- #

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    password: str  # hashed password
    auth_level: int = 1

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    auth_level: int

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(UserBase):
    username: str | None = None
    email: str | None = None
    full_name: str | None = None
    password: str | None = None
    auth_level: int | None = None


# ------ Material  -------------- #


class MaterialBase(BaseModel):
    name: str
    unit: str
    price: float
    supplier_id: int


class MaterialCreate(MaterialBase):
    pass


class Material(MaterialBase):
    """
        Material provides the information of raw material
        used in the creation of a product.
        Fields: Id, Name, unit, price and supplier
        """
    id: int

    model_config = ConfigDict(from_attributes=True)


class MaterialUpdate(BaseModel):
    name: str | None = None
    unit: str | None = None
    price: float | None = None
    supplier_id: int | None = None


# summarize materials
class MaterialItem(BaseModel):
    product_id: int
    units: int
    size: float


# The main request body will be a list of these items
class MaterialRequest(BaseModel):
    items: List[MaterialItem]


# ------ PackageMaterial  -------------- #


class PackageMaterialBase(BaseModel):
    name: str
    price: float
    supplier_id: int


class PackageMaterialCreate(PackageMaterialBase):
    pass


class PackageMaterial(PackageMaterialBase):
    id: int


class PackageMaterialUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    supplier_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


# ------ Supplier  -------------- #


class SupplierBase(BaseModel):
    supplier_name: str
    supplier_address: str
    phone_1: str
    phone_2: str
    deliver: bool = False


class SupplierCreate(SupplierBase):
    pass


class Supplier(SupplierBase):
    id: int
    material: List[Material] = []

    model_config = ConfigDict(from_attributes=True)


class SupplierUpdate(BaseModel):
    supplier_name: str | None = None
    supplier_address: str | None = None
    phone_1: str | None = None
    phone_2: str | None = None
    deliver: bool | None = False


# ------ Product  -------------- #


class ProductBase(BaseModel):
    product_name: str
    size: float


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
    product_name: str | None = None
    size: float | None = None


# ------ Formula  -------------- #

class FormulaBase(BaseModel):
    product_id: int
    material_id: int
    quantity: float


class FormulaCreate(FormulaBase):
    pass


class Formula(FormulaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FormulaUpdate(BaseModel):
    product_id: int | None = None
    material_id: int | None = None
    quantity: float


# ------ Compose  -------------- #


class PackageComposeBase(BaseModel):
    product_id: int
    package_material_id: int


class PackageComposeCreate(PackageComposeBase):
    pass


class PackageCompose(PackageComposeBase):
    id: int


class PackageComposeUpdate(BaseModel):
    product_id: int | None = None
    package_material_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


# ------ Batch  -------------- #


class BatchBase(BaseModel):
    product_id: int
    quantity: float
    last_update: datetime


class BatchCreate(BatchBase):
    pass


class Batch(BatchBase):
    id: int
    batch_id: str = Field(default_factory=create_id)

    model_config = ConfigDict(from_attributes=True)


class BatchUpdate(BaseModel):
    product_id: int | None = None
    batch_id: int | None = None
    quantity: float
    last_update: datetime = datetime.now()


# ------ ProductBatch  -------------- #


class ProductBatchBase(BaseModel):
    product_id: int
    pieces: int


class ProductBatchCreate(ProductBatchBase):
    pass


class ProductBatch(ProductBatchBase):
    id: int
    product_batch_id: str
    last_update: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductBatchUpdate(BaseModel):
    id: int
    product_id: int | None = None
    pieces: int | None = None
    last_update: datetime

    model_config = ConfigDict(from_attributes=True)
