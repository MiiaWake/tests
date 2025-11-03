import requests
import logging
from typing import Dict, Any, Optional, List, Union
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

from src.api.endpoints import Endpoints

class APIClient:
    """
    API Client for Petstore with retry mechanism and logging
    """
    
    def __init__(self, base_url: str = "https://petstore.swagger.io/v2", timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        
        # Setup retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Common headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def _log_request(self, method: str, url: str, **kwargs):
        """Log request details"""
        self.logger.info(f"Making {method} request to {url}")
        if 'json' in kwargs and kwargs['json']:
            self.logger.debug(f"Request body: {kwargs['json']}")
    
    def _log_response(self, response: requests.Response):
        """Log response details"""
        self.logger.info(f"Response status: {response.status_code}")
        if response.content:
            self.logger.debug(f"Response body: {response.text}")
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Base method for making HTTP requests"""
        url = f"{self.base_url}{endpoint}"
        
        self._log_request(method, url, **kwargs)
        
        start_time = time.time()
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            
            self._log_response(response)
            
            # Return JSON if content exists, else empty dict
            return response.json() if response.content else {}
            
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error: {e} - {response.text if 'response' in locals() else ''}")
            raise
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"Connection error: {e}")
            raise
        except requests.exceptions.Timeout as e:
            self.logger.error(f"Timeout error: {e}")
            raise
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error: {e}")
            raise
        finally:
            execution_time = time.time() - start_time
            self.logger.info(f"Request executed in {execution_time:.2f}s")
    
    # Pet endpoints
    def add_pet(self, pet_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new pet to the store"""
        return self._request("POST", Endpoints.PET, json=pet_data)
    
    def get_pet(self, pet_id: int) -> Dict[str, Any]:
        """Find pet by ID"""
        return self._request("GET", Endpoints.PET_BY_ID.format(pet_id=pet_id))
    
    def update_pet(self, pet_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing pet"""
        return self._request("PUT", Endpoints.PET, json=pet_data)
    
    def delete_pet(self, pet_id: int, api_key: str = "special-key") -> Dict[str, Any]:
        """Delete a pet"""
        headers = {"api_key": api_key}
        return self._request("DELETE", Endpoints.PET_BY_ID.format(pet_id=pet_id), headers=headers)
    
    def find_pets_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Finds Pets by status"""
        return self._request("GET", f"{Endpoints.PET_FIND_BY_STATUS}?status={status}"
Redirecting...
self.logger.info


)
    
    def upload_pet_image(self, pet_id: int, image_data: bytes, additional_metadata: str = "") -> Dict[str, Any]:
        """Uploads an image for a pet"""
        files = {'file': ('image.jpg', image_data, 'image/jpeg')}
        data = {'additionalMetadata': additional_metadata}
        return self._request("POST", Endpoints.PET_UPLOAD_IMAGE.format(pet_id=pet_id), files=files, data=data)
    
    # Store endpoints
    def place_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Place an order for a pet"""
        return self._request("POST", Endpoints.STORE_ORDER, json=order_data)
    
    def get_order(self, order_id: int) -> Dict[str, Any]:
        """Find purchase order by ID"""
        return self._request("GET", Endpoints.STORE_ORDER_BY_ID.format(order_id=order_id))
    
    def delete_order(self, order_id: int) -> Dict[str, Any]:
        """Delete purchase order by ID"""
        return self._request("DELETE", Endpoints.STORE_ORDER_BY_ID.format(order_id=order_id))
    
    def get_inventory(self) -> Dict[str, Any]:
        """Returns pet inventories by status"""
        return self._request("GET", Endpoints.STORE_INVENTORY)
    
    # User endpoints
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create user"""
        return self._request("POST", Endpoints.USER, json=user_data)
    
    def get_user(self, username: str) -> Dict[str, Any]:
        """Get user by user name"""
        return self._request("GET", Endpoints.USER_BY_USERNAME.format(username=username))
    
    def update_user(self, username: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Updated user"""
        return self._request("PUT", Endpoints.USER_BY_USERNAME.format(username=username), json=user_data)
    
    def delete_user(self, username: str) -> Dict[str, Any]:
        """Delete user"""
        return self._request("DELETE", Endpoints.USER_BY_USERNAME.format(username=username))
    
    def login_user(self, username: str, password: str) -> Dict[str, Any]:
        """Logs user into the system"""
        return self._request("GET", f"{Endpoints.USER_LOGIN}?username={username}&password={password}")
    
    def logout_user(self) -> Dict[str, Any]:
        """Logs out current logged in user session"""
        return self._request("GET", Endpoints.USER_LOGOUT)
    
    def create_users_with_list(self, users_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Creates list of users with given input array"""
        return self._request("POST", Endpoints.USER_CREATE_WITH_LIST, json=users_data)
