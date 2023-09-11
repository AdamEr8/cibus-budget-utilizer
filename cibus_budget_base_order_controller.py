import requests
import json
from abstract_order_controller import AbstractOrderController

# Base Class for controllers that use budget from Cibus (which for us is everything...)
class CibusBudgetBaseOrderController(AbstractOrderController):
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
    
    def _post_sodexo_request(self, payload):
        return self.session.post(self.mysodexo_url, json=payload)
    
    def login(self):
        login_payload = {
            "type": "prx_login",
            "user": self.username,
            "password": self.password,
            "company": self.company,
            "remember": True
        }
        response = self._post_sodexo_request(login_payload)
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
        response = self._post_sodexo_request(get_budget_payload)
        response_data = json.loads(response.text)
        current_budget = response_data['data'][0]['CurrBudget']
        
        return int(float(current_budget))