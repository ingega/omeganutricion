import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from unittest.mock import Mock

# Import app and the real dependency
from src.services.products.main import app
from src.services.products.database import get_db
from src.services.products.database import Base as MockBase
from src.services.products.auth import get_current_user

# tables are necessary for creation in memory
from src.services.products.models import SupplierDB, MaterialDB, PackageMaterialDB, ProductDB

# the protected endpoints need auth, a Mock user is a good solution

MOCK_USER: dict = {
    'username': 'test',
    'full_name': 'Test User',
    'password': '',
    'email': '',
    'auth_level': 10
        }

# override auth
def override_auth():
    return Mock(**MOCK_USER)

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSession = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()

# now I need to override either, db and auth, using fixture

@pytest.fixture(scope='module')
def client():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_auth

    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

# create tables in setup, using pytest fixture
@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    MockBase.metadata.create_all(bind=engine)
    # I need add records to verify my endpoints
    db = TestingSession()
    db.add(SupplierDB(supplier_name="Test Supplier",
                      supplier_address="Test st, 123",
                      phone_1 = "123456",
                      phone_2 = "654321",
                      deliver=False
                      )
           )
    db.commit()
    # now a material
    db.add(MaterialDB(
        name="Test Material",
        unit="kilo",
        price=10,
        supplier_id=1
        )
    )
    db.commit()
    # package material
    db.add(PackageMaterialDB(
        name="Test Package Material",
        price=100,
        supplier_id=1
        )
    )
    db.commit()
    # product
    db.add(ProductDB(
        product_name="Test Product",
        size=1.2
    )
    )
    db.commit()
    yield
    MockBase.metadata.drop_all(bind=engine)


# ---  Tests --- #

# ---- material endpoints ------#
def test_read_materials(client):
    # database already has a record
    response_material = client.get("/materials/")
    assert response_material.status_code == 200
    data = response_material.json()
    assert len(data) == 1

def test_post_and_read_material(client):
    response_create_material = client.post("/materials/",
                                    data={"name": "New Material",
                                          "unit": "kilo",
                                          "price": 10,
                                          "supplier_id": 1
                                          })
    assert response_create_material.status_code == 200
    # verify the response content
    data = response_create_material.json()
    assert data.get("name") == "New Material"
    material_id = data.get("id")
    # now read the material
    response_read_material = client.get(f"/materials/{material_id}/")
    assert response_read_material.status_code == 200
    data = response_read_material.json()
    assert data.get("name") == "New Material"
    assert data.get("id") == material_id

def test_create_and_patch_material(client):
    # first create a material
    response_create_material = client.post("/materials/",
                                           data={"name": "New Material",
                                                 "unit": "kilo",
                                                 "price": 10,
                                                 "supplier_id": 1
                                                 })
    assert response_create_material.status_code == 200
    data = response_create_material.json()
    # now get the id
    material_id = data.get("id")
    # now patch this new material
    response_patch_material = client.patch(f"/materials/{material_id}",
                                           data={"name": "Patch Material",})
    # assert the response
    assert response_patch_material.status_code == 200
    # assert the patched data
    data = response_patch_material.json()
    assert data.get("name") == "Patch Material"
    # assert that other data is unchanged
    assert data.get("unit") == "kilo"
    assert data.get("price") == 10
    assert data.get("supplier_id") == 1

def test_create_and_delete_material(client):
    # first create a material
    response_create_material = client.post("/materials/",
                                           data={"name": "New Material",
                                                 "unit": "kilo",
                                                 "price": 10,
                                                 "supplier_id": 1
                                                 })
    assert response_create_material.status_code == 200
    data = response_create_material.json()
    # now get the id
    material_id = data.get("id")
    # now delete this new material
    response_delete_material = client.delete(f"/materials/{material_id}")
    # assert the response
    assert response_delete_material.status_code == 200
    # assert the data deleted
    data = response_delete_material.json()
    assert data.get("name") == "New Material"
    assert 'id' in data


# ---- packaging material endpoints ------#

def test_read_packaging_materials(client):
    # database already has a record
    response_package_materials = client.get("/package-materials/")
    assert response_package_materials.status_code == 200
    data = response_package_materials.json()
    assert len(data) == 1

def test_post_and_read_package_material(client):
    response_create_package_material = client.post("/package-materials/",
                                    data={"name": "New Package Material",
                                          "price": 20,
                                          "supplier_id": 1
                                          }
                                           )
    assert response_create_package_material.status_code == 200
    # verify the response content
    data = response_create_package_material.json()
    assert data.get("name") == "New Package Material"
    package_material_id = data.get("id")
    # now read the package material
    response_read_package_material = client.get(f"/package-materials/{package_material_id}/")
    assert response_read_package_material.status_code == 200
    data = response_read_package_material.json()
    assert data.get("name") == "New Package Material"
    assert data.get("id") == package_material_id

def test_create_and_patch_package_material(client):
    # first create a package material
    response_create_package_material = client.post("/package-materials/",
                                           data={"name": "New Package Material",
                                                 "price": 50,
                                                 "supplier_id": 1
                                                 }
                                                   )
    assert response_create_package_material.status_code == 200
    data = response_create_package_material.json()
    # now get the id
    package_material_id = data.get("id")
    # now patch this new material
    response_patch_package_material = client.patch(f"/package-materials/{package_material_id}",
                                           data={"name": "Patch Package Material",}
                                                   )
    # assert the response
    assert response_patch_package_material.status_code == 200
    # assert the patched data
    data = response_patch_package_material.json()
    assert data.get("name") == "Patch Package Material"
    # assert that other data is unchanged
    assert data.get("price") == 50
    assert data.get("supplier_id") == 1

def test_create_and_delete_package_material(client):
    # first create a material
    response_create_package_material = client.post("/package-materials/",
                                           data={"name": "New Package Material",
                                                 "price": 40,
                                                 "supplier_id": 1
                                                 }
                                                   )
    assert response_create_package_material.status_code == 200
    data = response_create_package_material.json()
    # now get the id
    package_material_id = data.get("id")
    # now delete this new package material
    response_delete_package_material = client.delete(f"/package-materials/{package_material_id}")
    # assert the response
    assert response_delete_package_material.status_code == 200
    # assert the data deleted
    data = response_delete_package_material.json()
    assert data.get("name") == "New Package Material"
    assert 'id' in data


# ---- suplliers endpoints ------#

def test_read_suppliers(client):
    # database already has a record
    response_suppliers = client.get("/suppliers/")
    assert response_suppliers.status_code == 200
    data = response_suppliers.json()
    assert len(data) == 1

def test_post_and_read_supplier(client):
    response_create_supplier = client.post("/suppliers/",
                                    data={"supplier_name": "New Test Supplier",
                                          "supplier_address": "Street 123",
                                          "phone_1": "123",
                                          "phone_2": "321",
                                          "deliver": False
                                          }
                                           )
    assert response_create_supplier.status_code == 200
    # verify the response content
    data = response_create_supplier.json()
    # debug
    print(data)
    assert data.get("supplier_name") == "New Test Supplier"
    supplier_id = data.get("id")
    # now read the supplier
    response_read_supplier = client.get(f"/suppliers/{supplier_id}/")
    assert response_read_supplier.status_code == 200
    data = response_read_supplier.json()
    assert data.get("supplier_name") == "New Test Supplier"
    assert data.get("supplier_address") == "Street 123"
    assert data.get("phone_1") == "123"
    assert data.get("phone_2") == "321"
    assert data.get("deliver") == False
    assert data.get("id") == supplier_id

def test_create_and_patch_supplier(client):
    # first create a new supplier
    response_create_supplier = client.post("/suppliers/",
                                           data={"supplier_name": "New Test Supplier",
                                                 "supplier_address": "Street 123",
                                                 "phone_1": "123",
                                                 "phone_2": "321",
                                                 "deliver": False
                                                 }
                                           )
    assert response_create_supplier.status_code == 200
    data = response_create_supplier.json()
    # get the id
    supplier_id = data.get("id")
    # patch this new supplier
    response_patch_supplier = client.patch(f"/suppliers/{supplier_id}",
                                           json={"supplier_name": "Patch Supplier",
                                                 "deliver": True
                                                 }
                                        )
    # assert the response
    assert response_patch_supplier.status_code == 200
    # assert the patched data
    data = response_patch_supplier.json()
    assert data.get("supplier_name") == "Patch Supplier"
    assert data.get("deliver") == True
    # assert that other data is unchanged
    assert data.get("supplier_address") == "Street 123"
    assert data.get("phone_1") == "123"
    assert data.get("phone_2") == "321"

def test_create_and_delete_supplier(client):
    # first create a supplier
    response_create_supplier = client.post("/suppliers/",
                                           data={"supplier_name": "Supplier to be deleted",
                                                 "supplier_address": "Street 123",
                                                 "phone_1": "123",
                                                 "phone_2": "321",
                                                 "deliver": False
                                                }
                                                   )
    assert response_create_supplier.status_code == 200
    data = response_create_supplier.json()
    # now get the id
    supplier_id = data.get("id")
    # now delete this new supplier
    response_delete_supplier = client.delete(f"/suppliers/{supplier_id}")
    # assert the response
    assert response_delete_supplier.status_code == 200
    # assert the data deleted
    data = response_delete_supplier.json()
    assert data.get("supplier_name") == "Supplier to be deleted"
    assert 'id' in data


# ---- products endpoints ------#

def test_read_products(client):
    # database already has a record
    response_products = client.get("/products/")
    assert response_products.status_code == 200
    data = response_products.json()
    # the in memory database just contains 1 item
    assert len(data) == 1
    first_record = data[0]
    assert first_record.get("product_name") == "Test Product"
    assert 'id' in first_record
    assert first_record.get("size") == 1.2

def test_post_and_read_product(client):
    response_create_product = client.post("/products/",
                                    data={"product_name": "New Test Product",
                                          "size": 1.75
                                          }
                                           )
    assert response_create_product.status_code == 200
    # verify the response content
    data = response_create_product.json()
    assert data.get("product_name") == "New Test Product"
    product_id = data.get("id")
    # now read the supplier
    response_read_product = client.get(f"/products/{product_id}/")
    assert response_read_product.status_code == 200
    data = response_read_product.json()
    assert data.get("product_name") == "New Test Product"
    assert data.get("size") == 1.75
    assert data.get("id") == product_id

def test_create_and_patch_product(client):
    # first create a new product
    response_create_product = client.post("/products/",
                                           data={"product_name": "Product to be patched",
                                                 "size": 1.0
                                                 }
                                           )
    assert response_create_product.status_code == 200
    data = response_create_product.json()
    # get the id
    product_id = data.get("id")
    # patch this new product
    response_patch_product = client.patch(f"/products/{product_id}",
                                           json={"product_name": "Patch Product"
                                                 }
                                        )
    # assert the response
    assert response_patch_product.status_code == 200
    # assert the patched data
    data = response_patch_product.json()
    assert data.get("product_name") == "Patch Product"
    # assert that other data is unchanged
    assert data.get("size") == 1.0


def test_create_and_delete_product(client):
    # first create a product
    response_create_product = client.post("/products/",
                                           data={"product_name": "Product to be deleted",
                                                 "size": 3.0
                                                }
                                                   )
    assert response_create_product.status_code == 200
    data = response_create_product.json()
    # now get the id
    product_id = data.get("id")
    # now delete this new product
    response_delete_product = client.delete(f"/products/{product_id}")
    # assert the response
    assert response_delete_product.status_code == 200
    # assert the data deleted
    data = response_delete_product.json()
    assert data.get("product_name") == "Product to be deleted"
    assert 'id' in data