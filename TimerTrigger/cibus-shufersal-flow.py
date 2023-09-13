import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

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

