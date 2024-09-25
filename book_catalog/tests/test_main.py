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
from app.models import Book

# Use the test database URLL
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

# Your test functions go here
def test_create_book():
    response = client.post(
        "/books/",
        json={"title": "Test Book", "author": "Test Author", "year": 2023}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Test Author"
    assert data["year"] == 2023
    assert "id" in data

def test_read_books():
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_book():
    # First, create a book
    create_response = client.post(
        "/books/",
        json={"title": "Read Test Book", "author": "Read Test Author", "year": 2023}
    )
    created_book = create_response.json()

    # Now, try to read the book
    response = client.get(f"/books/{created_book['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Read Test Book"
    assert data["author"] == "Read Test Author"
    assert data["year"] == 2023

def test_update_book():
    # First, create a book
    create_response = client.post(
        "/books/",
        json={"title": "Update Test Book", "author": "Update Test Author", "year": 2023}
    )
    created_book = create_response.json()

    # Now, update the book
    update_response = client.put(
        f"/books/{created_book['id']}",
        json={"title": "Updated Book", "author": "Updated Author", "year": 2024}
    )
    assert update_response.status_code == 200
    updated_book = update_response.json()
    assert updated_book["title"] == "Updated Book"
    assert updated_book["author"] == "Updated Author"
    assert updated_book["year"] == 2024

def test_delete_book():
    # First, create a book
    create_response = client.post(
        "/books/",
        json={"title": "Delete Test Book", "author": "Delete Test Author", "year": 2023}
    )
    created_book = create_response.json()

    # Now, delete the book
    delete_response = client.delete(f"/books/{created_book['id']}")
    assert delete_response.status_code == 200

    # Try to get the deleted book, should return 404
    get_response = client.get(f"/books/{created_book['id']}")
    assert get_response.status_code == 404

def test_read_non_existent_book():
    response = client.get("/books/9999")  # Assuming 9999 is a non-existent ID
    assert response.status_code == 404