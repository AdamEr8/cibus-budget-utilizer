from TimerTrigger.abstract_voucher_generator import AbstractVoucherGenerator

class OptimizedVoucherGenerator(AbstractVoucherGenerator):
    def __init__(self, budget, vouchers, allow_overdraft = False, max_voucher = None):
        super().__init__(budget, vouchers, allow_overdraft, max_voucher)

    def genenrate_vouchers(self):
        vouchers = self.get_vouchers_list(self.max_voucher)
        possible_values = self.budget + min(vouchers)
        dp = [0] + [-1] * possible_values  # Initialize a list to store the maximum value achievable for each sum

        for i in range(1, possible_values + 1):
            for option in vouchers:
                if i - option >= 0 and dp[i - option] != -1:
                    dp[i] = max(dp[i], dp[i - option] + option)

        result = []
        remaining = self.closest_to_budget(dp, self.budget, self.allow_overdraft)

        while remaining > 0:
            for option in vouchers:
                if remaining - option >= 0 and dp[remaining - option] == dp[remaining] - option:
                    result.append(option)
                    remaining -= option
                    break

        return result
    
    def closest_to_budget(self, dp, budget, allow_overdraft):
        filter_condition = lambda x: x != -1
        filtered_list = [item for item in dp if filter_condition(item)]
        filtered_list.sort()
        closest_value = None

        for value in filtered_list:
            if value <= budget and (closest_value is None or budget - value < budget - closest_value):
                closest_value = value
        if allow_overdraft and filtered_list.index(closest_value) < len(filtered_list) - 1 and closest_value < budget:
            closest_value = filtered_list[filtered_list.index(closest_value) + 1]
            
        return closest_value