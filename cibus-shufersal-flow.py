from pprint import pprint as pp
from greedy_voucher_generator import GreedyVoucherGenerator
from optimized_voucher_generator import OptimizedVoucherGenerator
from constants import SHUFERSAL_COUPONS
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
optimizedAlgo = OptimizedVoucherGenerator(budget, SHUFERSAL_COUPONS, allow_overdraft = True, max_voucher = 100)
voucher_prices = optimizedAlgo.genenrate_vouchers()

for voucher in voucher_prices:
    # Step 3: Add item to the cart (using default dish_id)
    soc.empty_cart()
    soc.add_voucher_to_cart(voucher)
    # Step 5: Apply order
    # TODO: soc.apply_order() # Apply_order (==Pay)
    


