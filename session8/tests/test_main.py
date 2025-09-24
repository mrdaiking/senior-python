"""
Unit tests for FastAPI CRUD operations.
"""
import pytest
from fastapi import status


class TestUserCRUD:
    """Test user CRUD operations."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns correct response."""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "Welcome to Senior Python FastAPI!"
        assert data["status"] == "healthy"

    def test_create_user_success(self, client, sample_user):
        """Test creating a new user successfully."""
        response = client.post("/users/", json=sample_user)
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["name"] == sample_user["name"]
        assert data["email"] == sample_user["email"]
        assert data["is_active"] == sample_user["is_active"]
        assert "id" in data

    def test_create_user_duplicate_email(self, client, sample_user):
        """Test creating user with duplicate email fails."""
        # Create first user
        client.post("/users/", json=sample_user)

        # Try to create another user with same email
        response = client.post("/users/", json=sample_user)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]

    def test_list_users_empty(self, client):
        """Test listing users when none exist."""
        response = client.get("/users/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_users_with_data(self, client, sample_user):
        """Test listing users with existing data."""
        # Create a user first
        client.post("/users/", json=sample_user)

        response = client.get("/users/")
        assert response.status_code == status.HTTP_200_OK

        users = response.json()
        assert len(users) == 1
        assert users[0]["email"] == sample_user["email"]

    def test_get_user_success(self, client, sample_user):
        """Test getting a specific user successfully."""
        # Create user first
        create_response = client.post("/users/", json=sample_user)
        user_id = create_response.json()["id"]

        # Get the user
        response = client.get(f"/users/{user_id}")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == sample_user["email"]

    def test_get_user_not_found(self, client):
        """Test getting non-existent user returns 404."""
        response = client.get("/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "User not found" in response.json()["detail"]

    def test_update_user_success(self, client, sample_user):
        """Test updating user successfully."""
        # Create user first
        create_response = client.post("/users/", json=sample_user)
        user_id = create_response.json()["id"]

        # Update user
        updated_data = {
            "name": "Updated User",
            "email": "updated@example.com",
            "is_active": False,
        }
        response = client.put(f"/users/{user_id}", json=updated_data)
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["name"] == updated_data["name"]
        assert data["email"] == updated_data["email"]
        assert data["is_active"] == updated_data["is_active"]

    def test_update_user_not_found(self, client, sample_user):
        """Test updating non-existent user returns 404."""
        response = client.put("/users/999", json=sample_user)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user_success(self, client, sample_user):
        """Test deleting user successfully."""
        # Create user first
        create_response = client.post("/users/", json=sample_user)
        user_id = create_response.json()["id"]

        # Delete user
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["ok"] is True

        # Verify user is deleted
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user_not_found(self, client):
        """Test deleting non-existent user returns 404."""
        response = client.delete("/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_active_users(self, client):
        """Test getting only active users."""
        # Create active user
        active_user = {
            "name": "Active User",
            "email": "active@example.com",
            "is_active": True,
        }
        client.post("/users/", json=active_user)

        # Create inactive user
        inactive_user = {
            "name": "Inactive User",
            "email": "inactive@example.com",
            "is_active": False,
        }
        client.post("/users/", json=inactive_user)

        # Get active users
        response = client.get("/users/active")
        assert response.status_code == status.HTTP_200_OK

        users = response.json()
        assert len(users) == 1
        assert users[0]["email"] == active_user["email"]
        assert users[0]["is_active"] is True
