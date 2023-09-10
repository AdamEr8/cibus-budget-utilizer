import requests
import json
from datetime import datetime
from abstract_order_controller import AbstractOrderController

# TODO: extract login and budget functionality to common class, Wolt needs it as well

class ShufersalOrderController(AbstractOrderController):
    def __init__(self, username, password, company):
        super().__init__()
        self.session = requests.session()
        self.username = username
        self.password = password
        self.company = company
        self.headers = {
            "Application-Id": "E5D5FEF5-A05E-4C64-AEBA-BA0CECA0E402"
        }
        self.session.headers.update(self.headers)
        self.mysodexo_url = "https://api.mysodexo.co.il/api/main.py"
        self.voucher_options = {}
    
    def _post_request(self, payload):
        return self.session.post(self.mysodexo_url, json=payload)
    
    def login(self):
        login_payload = {
            "type": "prx_login",
            "user": self.username,
            "password": self.password,
            "company": self.company,
            "remember": True
        }
        response = self._post_request(login_payload)
        if response.status_code != 200:
            print("Login failed. Status code:", response.status_code)
            exit()

        # Check if the login was successful
        login_response = response.json()
        if login_response.get("code") == 726:
            print("Login failed:", login_response.get("msg"))
            exit()

    def get_budget(self):
        get_budget_payload = {
            "type": "prx_get_budgets"
        }
        response = self._post_request(get_budget_payload)
        response_data = json.loads(response.text)
        current_budget = response_data['data'][0]['CurrBudget']
        
        return int(float(current_budget))
    
    def get_cart_info(self):
        get_cart_payload = {
            "type": "prx_get_cart"
        }
        response = self._post_request(get_cart_payload)
        if response.status_code != 200:
            print("Getting cart information failed. Status code:", response.status_code)
            exit()

        cart_data = response.json()
        return cart_data
    
    def fetch_voucher_options(self) -> None:
        # TODO: Fill other vouchers, or actually fetch them from the website and parse
        self.voucher_options = {
            100: {
                "category_id": 4723015,
                "dish_id": 4807364,
                "dish_price": 100,
                "co_owner_id": -1,
                "extra_list": []
            }
        }
    
    def add_voucher_to_cart(self, voucher_price):
        add_to_cart_payload = {
            "type": "prx_add_prod_to_cart",
            "order_type": 2,
            "dish_list": self.voucher_options[voucher_price]
        }
        response = response = self._post_request(add_to_cart_payload)
        if response.status_code != 200:
            print("Adding item to cart failed. Status code:", response.status_code)
            exit()
    

    def apply_order(self):
        apply_order_payload = {
            "type":"prx_apply_order",
            "order_time": datetime.now().strftime("%H:%M")
        }
        response = response = self._post_request(apply_order_payload)
        if response.status_code != 200:
            print("Applying order failed. Status code:", response.status_code)
            exit()

