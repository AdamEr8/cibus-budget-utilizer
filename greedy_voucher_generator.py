from abstract_voucher_generator import AbstractVoucherGenerator

class GreedyVoucherGenerator(AbstractVoucherGenerator):
    def __init__(self, budget, vouchers, allow_overdraft = False, max_voucher = None):
        super().__init__(budget, vouchers, allow_overdraft, max_voucher)

    def genenrate_vouchers(self):
        vouchers = self.get_vouchers_list(self.max_voucher)

        result = []
        current_sum = 0

        for value in vouchers:
            while current_sum + value <= self.budget:
                result.append(value)
                current_sum += value

        if self.allow_overdraft and current_sum < self.budget:
            result.append(min(vouchers))
            
        return result
