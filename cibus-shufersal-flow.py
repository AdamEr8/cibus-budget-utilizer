import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from pprint import pprint as pp
from greedy_voucher_generator import GreedyVoucherGenerator
from optimized_voucher_generator import OptimizedVoucherGenerator
from constants import SHUFERSAL_COUPONS
from shufersal_order_controller import ShufersalOrderController

def get_key_vault_secret(key_vault_url, secret_name):
    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
    try:
        secret = secret_client.get_secret(secret_name)
        cibus_pass_value = secret.value

        return cibus_pass_value

    except Exception as e:
        print(f"Error retrieving secret: {str(e)}")
        return None


# Define the login information
username = os.environ.get("cibusUserName")
company = os.environ.get("cibusCompany")
key_vault_name = os.environ.get("KeyVaultName")
key_vault_url = f"https://{key_vault_name}.vault.azure.net/"
password = get_key_vault_secret(key_vault_url, os.environ.get("CibusPassSecretName"))

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
    soc.add_voucher_to_cart(voucher)
    # Step 4: Get cart information
    cart_info = soc.get_cart_info()
    print("Cart info:")
    pp(cart_info)
    # Step 5: Apply order
    # TODO: Apply_order (==Pay)

