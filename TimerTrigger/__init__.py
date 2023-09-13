import logging
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from TimerTrigger.shufersal_order_controller import ShufersalOrderController
from TimerTrigger.greedy_voucher_generator import GreedyVoucherGenerator
from TimerTrigger.optimized_voucher_generator import OptimizedVoucherGenerator
from TimerTrigger.constants import SHUFERSAL_COUPONS

import azure.functions as func

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

def CreateShuferSalOrderController():
    # Define the login information
    username = os.environ.get("cibusUserName")
    company = os.environ.get("cibusCompany")
    key_vault_name = os.environ.get("keyVaultName")
    cibus_pass_secret_name = os.environ.get("cibusPassSecretName")
    key_vault_url = f"https://{key_vault_name}.vault.azure.net/"
    password = get_key_vault_secret(key_vault_url, cibus_pass_secret_name)
    logging.info(f"username: {username}, company: {company}, cibus_pass_secret_name: {cibus_pass_secret_name} readed from environment variables")


    # Step 1: Perform login and get the token cookie
    return ShufersalOrderController(username, password, company)

def main(mytimer: func.TimerRequest) -> None:
    soc = CreateShuferSalOrderController()
    soc.login()
    # Step 2: Get the budget
    budget = soc.get_budget()
    logging.info(f"Budget: {budget}")
    budget = 30
    soc.fetch_voucher_options()
    algo_type = os.environ.get("voucherGeneratorAlgo")
    allow_overdraft = os.environ.get("allowOverdraft").lower() == "true"
    max_voucher = int(os.environ.get("maxVoucher"))
    logging.info(f"algo_type: {algo_type}, allow_overdraft: {allow_overdraft}, max_voucher: {max_voucher} readed from environment variables")
    if algo_type == "Optimized":
        algo = OptimizedVoucherGenerator(budget, SHUFERSAL_COUPONS, allow_overdraft = allow_overdraft, max_voucher = 100)
    else:
        algo = GreedyVoucherGenerator(budget, SHUFERSAL_COUPONS, allow_overdraft = max_voucher, max_voucher = 100)
    voucher_prices = algo.genenrate_vouchers()
    logging.info(f"Voucher prices: {voucher_prices}")

    for voucher in voucher_prices:
        # Step 3: Add item to the cart (using default dish_id)
        soc.add_voucher_to_cart(voucher)
        # Step 4: Get cart information
        cart_info = soc.get_cart_info()
        logging.info(f"Cart info: {cart_info}")
        # Step 5: Apply order
        soc.apply_order()