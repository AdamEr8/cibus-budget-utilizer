# cibus-budget-utilizer

1) open cmd and run: git clone https://github.com/AdamEr8/cibus-budget-utilizer.git

2) run: cd cibus-budget-utilizer

3) run: azd init (if not installed, install from here)

3.1) it will ask for environment name, write whatever you wish 

4) run: azd up

4.1) here it will ask you for the subscription and RG where you want to create the azure function, the name of the function and your credentials

5) run: func azure functionapp publish <YOUR_APP_NAME> (if func isn't installed in your computer, install from here)

 

and THAT'S IT, every Thursday at 15:00 UTC it will utilize your budget 

 

for fine tuning:

in the main.bicep file, you can configure the following values:
1)  "voucherGeneratorAlgo": 'Optimized' value will use one algo and 'Greedy' will use another voucher prices algo (if missing default is Greedy)
2) "allowOverdraft": for example if your budget is 199 and this is set to 'true' it will buy you in 200 if it false then it will utilize 190 shekels
3) "maxVoucher": the maximum value of the vouchers you would like to have (shufersal doesn't respect partial vouchers so 200 shekels voucher might be inconvenient) the default is 100

in the function.json file, you can configure the reoccurrence:
right now it's: "schedule": "0 0 15 * * 4" which means every Thursday at 15:00 UTC, if you would like another hour or day go for it 
