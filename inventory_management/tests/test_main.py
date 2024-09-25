import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set up test database
os.environ['DATABASE_URL'] = "sqlite:///./test.db"

from app.main import app, get_db
from app.database import Base
from app.models import Inventory  # Ensure this model exists in your project

# Use the test database URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test functions for Inventory
def test_create_inventory_item():
    response = client.post(
        "/inventories/",  # Updated the endpoint to match your FastAPI routes
        json={"item_name": "Test Item", "quantity": 10}  # Adjusted attributes as per your Inventory schema
    )
    assert response.status_code == 200
    data = response.json()
    assert data["item_name"] == "Test Item"
    assert data["quantity"] == 10
    assert "id" in data

def test_read_inventory_items():
    response = client.get("/inventories/")  # Updated the endpoint to match your FastAPI routes
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_inventory_item():
    # First, create an inventory item
    create_response = client.post(
        "/inventories/",  # Updated the endpoint to match your FastAPI routes
        json={"item_name": "Read Test Item", "quantity": 5}  # Adjusted attributes as per your Inventory schema
    )
    created_item = create_response.json()

    # Now, try to read the item
    response = client.get(f"/inventories/{created_item['id']}")  # Updated the endpoint to match your FastAPI routes
    assert response.status_code == 200
    data = response.json()
    assert data["item_name"] == "Read Test Item"
    assert data["quantity"] == 5

def test_update_inventory_item():
    # First, create an inventory item
    create_response = client.post(
        "/inventories/",  # Updated the endpoint to match your FastAPI routes
        json={"item_name": "Update Test Item", "quantity": 10}  # Adjusted attributes as per your Inventory schema
    )
    created_item = create_response.json()

    # Now, update the item
    update_response = client.put(
        f"/inventories/{created_item['id']}",  # Updated the endpoint to match your FastAPI routes
        json={"item_name": "Updated Item", "quantity": 15}  # Adjusted attributes as per your Inventory schema
    )
    assert update_response.status_code == 200
    updated_item = update_response.json()
    assert updated_item["item_name"] == "Updated Item"
    assert updated_item["quantity"] == 15

def test_delete_inventory_item():
    # First, create an inventory item
    create_response = client.post(
        "/inventories/",  # Updated the endpoint to match your FastAPI routes
        json={"item_name": "Delete Test Item", "quantity": 8}  # Adjusted attributes as per your Inventory schema
    )
    created_item = create_response.json()

    # Now, delete the item
    delete_response = client.delete(f"/inventories/{created_item['id']}")  # Updated the endpoint to match your FastAPI routes
    assert delete_response.status_code == 200

    # Try to get the deleted item, should return 404
    get_response = client.get(f"/inventories/{created_item['id']}")  # Updated the endpoint to match your FastAPI routes
    assert get_response.status_code == 404

def test_read_non_existent_inventory_item():
    response = client.get("/inventories/9999")  # Assuming 9999 is a non-existent ID
    assert response.status_code == 404
