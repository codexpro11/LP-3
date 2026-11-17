from decimal import Decimal

gas_used = int(input("Gas used from receipt: "))
price_gwei = Decimal(input("Effective gas price in gwei: "))
value_eth = Decimal(input("Value transferred in ETH: "))
if gas_used < 0 or price_gwei < 0 or value_eth < 0:
    raise ValueError("Values cannot be negative")
fee_eth = Decimal(gas_used) * price_gwei / Decimal(10 ** 9)
print("Actual fee (ETH):", fee_eth)
print("Value + fee (ETH):", value_eth + fee_eth)
