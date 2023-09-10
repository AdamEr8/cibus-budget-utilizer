from pprint import pprint as pp
from coupons_generator import optimized_algo, greedy_algo
from constants import CouponsKind
from shufersal_order_controller import ShufersalOrderController

# Define the login information
username = "<YOUR USERNAME HERE>"
password = "<YOUR PASSWORD HERE>"
company = "מיקרוסופט"

# Step 1: Perform login and get the token cookie
soc = ShufersalOrderController(username, password, company)
soc.login()
# Step 2: Get the budget
budget = soc.get_budget()
print("Budget:", budget)
soc.fetch_voucher_options()
coupons_prices = greedy_algo(budget, CouponsKind.SHUFERSAL)

for price in coupons_prices:
    # Step 3: Add item to the cart (using default dish_id)
    soc.add_voucher_to_cart(price)

# Step 4: Get cart information
cart_info = soc.get_cart_info()
print("Cart info:")
pp(cart_info)
# Step 5: Apply order
# TODO: Apply_order (==Pay)
    


