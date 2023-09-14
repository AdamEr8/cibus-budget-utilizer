# cibus-budget-utilizer

## Prerequisites
1. azd CLI - [install](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd?tabs=winget-windows%2Cbrew-mac%2Cscript-linux&pivots=os-windows)
1. az CLI - [install](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
1. func - azure functions core utils - [install](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-csharp#install-the-azure-functions-core-tools)

## Setup

```bash
git clone https://github.com/AdamEr8/cibus-budget-utilizer.git
cd cibus-budget-utilizer
az login
az account set --subscription < YOUR_SUBSCRIPTION_HERE >
azd init  # It will ask for environment name, write whatever you wish
azd up  # Here it will ask you for the subscription and RG where you want to create the azure function, the name of the function and your credentials
func azure functionapp publish < YOUR_FUNCION_APP_NAME_HERE >
``` 

## Configurations
1. In the main.bicep file, you can configure the following values:
  1. "voucherGeneratorAlgo": 'Optimized' value will use one algo and 'Greedy' will use another voucher prices algo (Greedy if none provided).
  2. "allowOverdraft": If true, the minimum amount of out-of-pocket pay will be allowed when pruchasing coupons. If false, some cibus credit will remain and not be utilized.
  3. "maxVoucher": the maximum value of the vouchers you would like to have (shufersal doesn't respect partial vouchers so 200 shekels voucher might be inconvenient) the default is 100.
2. in the function.json file, you can configure the timing of function trigger. For further info, see [the official docs](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer?tabs=python-v2%2Cin-process%2Cnodejs-v4&pivots=programming-language-python#configuration)
