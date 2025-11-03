import pytest
import logging
from src.api.client import APIClient
from src.models.pet import Pet, Category, Tag
from src.models.user import User
from src.models.store import Order

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def api_client():
    """Fixture for API client"""
    return APIClient()

@pytest.fixture
def sample_pet():
    """Fixture for sample pet data"""
    return Pet(
        id=123456789,
        name="Test Dog",
        photoUrls=["http://test.com/image.jpg"],
        status="available"
    )

@pytest.fixture
def complex_pet():
    """Fixture for complex pet data"""
    return Pet(
        id=999888777,
        category=Category(id=1, name="Dogs"),
        name="Complex Pet",
        photoUrls=[
            "http://test.com/photo1.jpg",
            "http://test.com/photo2.jpg"
        ],
        tags=[
            Tag(id=1, name="friendly"),
            Tag(id=2, name="trained")
        ],
        status="available"
    )

@pytest.fixture
def sample_user():
    """Fixture for sample user data"""
    return User(
        id=1001,
        username="testuser",
        firstName="Test",
        lastName="User",
        email="test@example.com",
        password="password123",
        phone="+1234567890",
        userStatus=1
    )


@pytest.fixture
def sample_order():
    """Fixture for sample order data"""
    return Order(
        id=10001,
        petId=123456789,
        quantity=1,
        status="placed",
        complete=False
    )

@pytest.fixture
def created_pet(api_client, sample_pet):
    """Fixture that creates a pet and cleans up after test"""
    # Setup
    response = api_client.add_pet(sample_pet.dict())
    pet_id = response["id"]
    
    yield pet_id  # Provide pet_id to test
    
    # Teardown
    try:
        api_client.delete_pet(pet_id)
        logger.info(f"Cleaned up pet with ID: {pet_id}")
    except Exception as e:
        logger.warning(f"Failed to cleanup pet {pet_id}: {e}")

@pytest.fixture
def created_user(api_client, sample_user):
    """Fixture that creates a user and cleans up after test"""
    # Setup
    response = api_client.create_user(sample_user.dict())
    
    yield sample_user.username  # Provide username to test
    
    # Teardown
    try:
        api_client.delete_user(sample_user.username)
        logger.info(f"Cleaned up user: {sample_user.username}")
    except Exception as e:
        logger.warning(f"Failed to cleanup user {sample_user.username}: {e}")

@pytest.fixture
def created_order(api_client, sample_order):
    """Fixture that creates an order and cleans up after test"""
    # Setup
    response = api_client.place_order(sample_order.dict())
    order_id = response["id"]
    
    yield order_id  # Provide order_id to test
    
    # Teardown
    try:
        api_client.delete_order(order_id)
        logger.info(f"Cleaned up order with ID: {order_id}")
    except Exception as e:
        logger.warning(f"Failed to cleanup order {order_id}: {e}")

@pytest.fixture(autouse=True)
def slow_down_tests():
    """Slow down tests to avoid rate limiting"""
    yield
    import time
    time.sleep(0.5)
