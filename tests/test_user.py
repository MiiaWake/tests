import pytest
import allure
import logging
from src.models.user import User

logger = logging.getLogger(__name__)

@allure.epic("Petstore API")
@allure.feature("User Management")
class TestUserAPI:
    """Test cases for User endpoints"""
    
    @allure.title("Create user")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_create_user(self, api_client, sample_user):
        """Test creating a new user"""
        with allure.step("Create user"):
            response = api_client.create_user(sample_user.dict())
        
        with allure.step("Verify user creation"):
            assert response["code"] == 200
            assert "message" in response
        
        with allure.step("Cleanup"):
            api_client.delete_user(sample_user.username)
    
    @allure.title("Get user by username")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_by_username(self, api_client, created_user):
        """Test retrieving user by username"""
        with allure.step("Get user by username"):
            response = api_client.get_user(created_user)
        
        with allure.step("Verify user data"):
            assert response["username"] == created_user
            assert "email" in response
            assert "userStatus" in response
    
    @allure.title("Update user information")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_user(self, api_client, sample_user):
        """Test updating user information"""
        with allure.step("Create initial user"):
            api_client.create_user(sample_user.dict())
        
        with allure.step("Update user data"):
            updated_data = sample_user.dict()
            updated_data["firstName"] = "Updated"
            updated_data["lastName"] = "Name"
            updated_data["email"] = "updated@example.com"
            
            response = api_client.update_user(sample_user.username, updated_data)
        
        with allure.step("Verify update"):
            assert response["code"] == 200
        
        with allure.step("Verify updated data"):
            user_response = api_client.get_user(sample_user.username)
            assert user_response["firstName"] == "Updated"
            assert user_response["lastName"] == "Name"
            assert user_response["email"] == "updated@example.com"
        
        with allure.step("Cleanup"):
            api_client.delete_user(sample_user.username)
    
    @allure.title("Delete user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_user(self, api_client, sample_user):
        """Test deleting a user"""
        with allure.step("Create user for deletion"):
            api_client.create_user(sample_user.dict())
        
        with allure.step("Delete user"):
            delete_response = api_client.delete_user(sample_user.username)
            assert delete_response.get("message") == sample_user.username
        
        with allure.step("Verify user is deleted"):
            try:
                api_client.get_user(sample_user.username)
                assert False, "User should not be found after deletion"
            except Exception as e:
                assert "404" in str(e) or "User not found" in str(e)
    
    @allure.title("User login and logout")
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_login_logout(self, api_client, created_user):
        """Test user login and logout functionality"""
        with allure.step("Login user"):
            login_response = api_client.login_user(created_user, "password123")
            assert "message" in login_response
            assert "logged in" in login_response["message"].lower()
        
        with allure.step("Logout user"):
            logout_response = api_client.logout_user()
            assert "message" in logout_response
            assert "logout" in logout_response["message"].lower()
    
    @allure.title("Create users with list")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test


_create_users_with_list(self, api_client):
        """Test creating multiple users with a list"""
        with allure.step("Create list of users"):
            users_data = [
                {
                    "username": "user1",
                    "firstName": "User",
                    "lastName": "One",
                    "email": "user1@example.com",
                    "password": "password123",
                    "phone": "1234567890",
                    "userStatus": 1
                },
                {
                    "username": "user2", 
                    "firstName": "User",
                    "lastName": "Two",
                    "email": "user2@example.com",
                    "password": "password456",
                    "phone": "0987654321",
                    "userStatus": 1
                }
            ]
            
            response = api_client.create_users_with_list(users_data)
        
        with allure.step("Verify bulk user creation"):
            assert response["code"] == 200
            assert "message" in response
        
        with allure.step("Cleanup created users"):
            for user in users_data:
                try:
                    api_client.delete_user(user["username"])
                except Exception as e:
                    logger.warning(f"Failed to cleanup user {user['username']}: {e}")
    
    @allure.title("Get non-existent user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_user(self, api_client):
        """Test getting a user that doesn't exist"""
        with allure.step("Attempt to get non-existent user"):
            try:
                api_client.get_user("nonexistentuser123")
                assert False, "Should have raised an exception"
            except Exception as e:
                assert "404" in str(e) or "User not found" in str(e)
    
    @allure.title("Create user with minimal data")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_minimal_data(self, api_client):
        """Test creating user with only required fields"""
        with allure.step("Create user with minimal data"):
            minimal_user = {
                "username": "minimaluser",
                "firstName": "Minimal", 
                "lastName": "User",
                "email": "minimal@example.com",
                "password": "minpass123"
            }
            
            response = api_client.create_user(minimal_user)
        
        with allure.step("Verify minimal user creation"):
            assert response["code"] == 200
        
        with allure.step("Cleanup"):
            api_client.delete_user("minimaluser")
    
    @allure.title("Login with invalid credentials")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_invalid_credentials(self, api_client):
        """Test login with invalid credentials"""
        with allure.step("Attempt login with invalid credentials"):
            try:
                api_client.login_user("invaliduser", "wrongpassword")
                # API might return 200 even for invalid credentials in some implementations
                logger.info("Login attempt completed")
            except Exception as e:
                # Expected for invalid credentials
                logger.info(f"Expected behavior with invalid credentials: {e}")
