from constants import SHUFERSAL_COUPONS, WOLT_COUPONS, CouponsKind

def optimized_algo(budget, kind, is_over_budget_allowed=False):
    options = get_options(kind)
    options.sort(reverse=True)
    dp = [0] + [-1] * budget  # Initialize a list to store the maximum value achievable for each sum

    for i in range(1, budget + 1):
        for option in options:
            if i - option >= 0 and dp[i - option] != -1:
                dp[i] = max(dp[i], dp[i - option] + option)

    result = []
    remaining = budget

    while remaining > 0:
        for option in options:
            if remaining - option >= 0 and dp[remaining - option] == dp[remaining] - option:
                result.append(option)
                remaining -= option
                break

    return result

def greedy_algo(budget, kind, is_over_budget_allowed=False):
    options = get_options(kind)
    options.sort(reverse=True)  # Sort options in descending order for optimization

    result = []
    current_sum = 0

    for value in options:
        while current_sum + value <= budget:
            result.append(value)
            current_sum += value

    return result

def get_options(kind):
    if kind == CouponsKind.SHUFERSAL:
        return SHUFERSAL_COUPONS
    elif kind == CouponsKind.WOLT:
        return WOLT_COUPONS
    else:
        raise Exception("Unsopported coupons kind") 