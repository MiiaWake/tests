import pytest
import allure
import logging
from src.models.store import Order, Inventory

logger = logging.getLogger(__name__)

@allure.epic("Petstore API")
@allure.feature("Store Management")
class TestStoreAPI:
    """Test cases for Store endpoints"""
    
    @allure.title("Place order for pet")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_place_order(self, api_client, sample_order):
        """Test placing an order for a pet"""
        with allure.step("Place order"):
            response = api_client.place_order(sample_order.dict())
        
        with allure.step("Verify order placement"):
            assert response["id"] == sample_order.id
            assert response["petId"] == sample_order.petId
            assert response["quantity"] == sample_order.quantity
            assert response["status"] == sample_order.status
            assert response["complete"] == sample_order.complete
            assert "shipDate" in response
        
        with allure.step("Cleanup"):
            api_client.delete_order(sample_order.id)
    
    @allure.title("Get order by ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_order_by_id(self, api_client, created_order):
        """Test retrieving order by ID"""
        with allure.step("Get order by ID"):
            response = api_client.get_order(created_order)
        
        with allure.step("Verify order data"):
            assert response["id"] == created_order
            assert "petId" in response
            assert "quantity" in response
            assert "status" in response
            assert "complete" in response
    
    @allure.title("Delete order")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_order(self, api_client, sample_order):
        """Test deleting an order"""
        with allure.step("Create order for deletion"):
            api_client.place_order(sample_order.dict())
        
        with allure.step("Delete order"):
            delete_response = api_client.delete_order(sample_order.id)
            assert delete_response.get("message") == str(sample_order.id)
        
        with allure.step("Verify order is deleted"):
            try:
                api_client.get_order(sample_order.id)
                assert False, "Order should not be found after deletion"
            except Exception as e:
                assert "404" in str(e) or "Order not found" in str(e)
    
    @allure.title("Get store inventory")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_get_inventory(self, api_client):
        """Test retrieving store inventory"""
        with allure.step("Get inventory"):
            response = api_client.get_inventory()
        
        with allure.step("Verify inventory structure"):
            assert isinstance(response, dict)
            # Inventory should have status counts
            expected_statuses = ["available", "pending", "sold"]
            for status in expected_statuses:
                if status in response:
                    assert isinstance(response[status], int)
                    assert response[status] >= 0
    
    @allure.title("Place order with different statuses - Parameterized")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("status", ["placed", "approved", "delivered"])
    def test_place_order_different_statuses(self, api_client, status):
        """Test placing orders with different statuses"""
        with allure.step(f"Place order with status: {status}"):
            order_data = {
                "id": 20000,
                "petId": 123456789,
                "quantity": 2,
                "status": status,
                "complete": False
            }
            
            response = api_client.place_order(order_data)
        
        with allure.step("Verify order status"):
            assert response["status"] == status
        
        with allure.step("Cleanup"):
            api_client.delete_order(20000)
    
    @allure.title(


"Get non-existent order")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_order(self, api_client):
        """Test getting an order that doesn't exist"""
        with allure.step("Attempt to get non-existent order"):
            try:
                api_client.get_order(999999999)
                assert False, "Should have raised an exception"
            except Exception as e:
                assert "404" in str(e) or "Order not found" in str(e)
    
    @allure.title("Place order with maximum quantity")
    @allure.severity(allure.severity_level.NORMAL)
    def test_place_order_max_quantity(self, api_client):
        """Test placing order with maximum allowed quantity"""
        with allure.step("Place order with max quantity"):
            order_data = {
                "id": 30000,
                "petId": 123456789,
                "quantity": 100,  # Maximum according to schema
                "status": "placed",
                "complete": False
            }
            
            response = api_client.place_order(order_data)
        
        with allure.step("Verify max quantity order"):
            assert response["quantity"] == 100
        
        with allure.step("Cleanup"):
            api_client.delete_order(30000)
