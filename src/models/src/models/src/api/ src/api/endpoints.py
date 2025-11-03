from enum import Enum

class Endpoints(str, Enum):
    # Pet endpoints
    PET = "/pet"
    PET_BY_ID = "/pet/{pet_id}"
    PET_FIND_BY_STATUS = "/pet/findByStatus"
    PET_UPLOAD_IMAGE = "/pet/{pet_id}/uploadImage"
    
    # Store endpoints
    STORE_INVENTORY = "/store/inventory"
    STORE_ORDER = "/store/order"
    STORE_ORDER_BY_ID = "/store/order/{order_id}"
    
    # User endpoints
    USER = "/user"
    USER_BY_USERNAME = "/user/{username}"
    USER_LOGIN = "/user/login"
    USER_LOGOUT = "/user/logout"
    USER_CREATE_WITH_LIST = "/user/createWithList"
