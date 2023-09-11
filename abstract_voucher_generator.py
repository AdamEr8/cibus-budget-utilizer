from abc import ABC, abstractmethod

class AbstractVoucherGenerator(ABC):
    def __init__(self, budget, vouchers, allow_overdraft = False, max_voucher = None):
        self.budget = budget
        self.vouchers = vouchers
        self.allow_overdraft = allow_overdraft
        self.max_voucher = max_voucher

    @abstractmethod
    def genenrate_vouchers(self):
        pass

    def get_vouchers_list(self, max_voucher):
        self.vouchers.sort(reverse=True)  # Sort options in descending order for optimization
        filter_condition = lambda x: not max_voucher or x <= max_voucher  # Filter out options that are too expensive
        
        return list(filter(filter_condition, self.vouchers))