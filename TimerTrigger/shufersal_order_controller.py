from datetime import datetime
from TimerTrigger.cibus_budget_base_order_controller import CibusBudgetBaseOrderController


class ShufersalOrderController(CibusBudgetBaseOrderController):
    def __init__(self, username, password, company):
        super().__init__(username, password, company)
        self.voucher_options = {}

    def get_cart_info(self):
        get_cart_payload = {
            "type": "prx_get_cart"
        }
        response = self._post_sodexo_request(get_cart_payload)
        if response.status_code != 200:
            print("Getting cart information failed. Status code:",
                  response.status_code)
            exit()

        cart_data = response.json()
        return cart_data
    
    def empty_cart(self):
        empty_cart_payload = {
            "type": "prx_del_cart"
        }
        response = self._post_sodexo_request(empty_cart_payload)
        if response.status_code != 200:
            print("Emptying cart failed. Status code:",
                  response.status_code)
            exit()
    
    def fetch_voucher_options(self) -> None:
        # TODO: Fill other vouchers, or actually fetch them from the website and parse
        self.voucher_options = {
            30:         {
                "category_id": 4723030,
                "dish_id": 4723031,
                "dish_price": 30,
                "co_owner_id": -1,
                "extra_list": []
            },
            40: {
                "category_id": 4723030,
                "dish_id": 4723032,
                "dish_price": 40,
                "co_owner_id": -1,
                "extra_list": []
            },
            50: {
                "category_id": 4723030,
                "dish_id": 4723033,
                "dish_price": 50,
                "co_owner_id": -1,
                "extra_list": []
            },
            100: {
                "category_id": 4723030,
                "dish_id": 4807367,
                "dish_price": 100,
                "co_owner_id": -1,
                "extra_list": []
            },
            200: {
                "category_id": 4723030,
                "dish_id": 4807580,
                "dish_price": 200,
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
        response = self._post_sodexo_request(add_to_cart_payload)
        if response.status_code != 200:
            print("Adding item to cart failed. Status code:", response.status_code)
            exit()

    def apply_order(self):
        apply_order_payload = {
            "type": "prx_apply_order",
            "order_time": datetime.now().strftime("%H:%M")
        }
        response = self._post_sodexo_request(apply_order_payload)
        if response.status_code != 200:
            print("Applying order failed. Status code:", response.status_code)
            exit()
