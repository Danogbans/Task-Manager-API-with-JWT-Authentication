import pytest
from django.contrib.auth.models import User
from tasks.serializers import UserSerializer


@pytest.mark.django_db
def test_user_serializer_valid_data():
    """Test UserSerializer with valid data."""
    
    valid_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123"
    }
    
    serializer = UserSerializer(data=valid_data)
    
    assert serializer.is_valid(), serializer.errors  # Ensure data is valid
    user_instance = serializer.save()
    
    assert user_instance.username == valid_data["username"]
    assert user_instance.email == valid_data["email"]
    assert user_instance.check_password(valid_data["password"])  # Password should be hashed


@pytest.mark.django_db
def test_user_serializer_missing_fields():
    """Test UserSerializer with missing required fields."""
    
    invalid_data = {
        "username": "testuser"
        # Missing 'email' and 'password'
    }
    
    serializer = UserSerializer(data=invalid_data)
    
    assert not serializer.is_valid()  # Validation should fail
    assert "password" in serializer.errors  # Password is required


@pytest.mark.django_db
def test_user_serializer_password_write_only():
    """Ensure that the password is write-only and not returned in response."""

    user = User.objects.create_user(username="hiddenuser", email="hidden@example.com", password="hiddenpass")
    serializer = UserSerializer(user)

    assert "password" not in serializer.data  