import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

# Import app and the real dependency
from src.services.products.endpoints.endpoints import app
from src.services.products.database import get_db
from src.services.products.database import Base  # aliases avoids conflict between other Base objects

# tables are necessary for creation in memory
from src.services.products.models import SupplierDB, MaterialDB

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

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# create tables in setup, using pytest fixture
@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
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
    yield
    Base.metadata.drop_all(bind=engine)


# ---  Tests --- #
def test_read_materials():
    # database already has a record
    response_material = client.get("/materials/")
    assert response_material.status_code == 200
    data = response_material.json()
    assert len(data) == 1


def test_post_and_read_material():
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


