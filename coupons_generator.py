def optimized_algo(budget, vouchers, allow_overdraft = False):
    vouchers.sort(reverse=True)
    possible_values = budget + min(vouchers)
    dp = [0] + [-1] * possible_values  # Initialize a list to store the maximum value achievable for each sum

    for i in range(1, possible_values + 1):
        for option in vouchers:
            if i - option >= 0 and dp[i - option] != -1:
                dp[i] = max(dp[i], dp[i - option] + option)

    result = []
    remaining = closest_to_budget(dp, budget, allow_overdraft)

    while remaining > 0:
        for option in vouchers:
            if remaining - option >= 0 and dp[remaining - option] == dp[remaining] - option:
                result.append(option)
                remaining -= option
                break

    return result

def greedy_algo_maximized(budget, vouchers):
    vouchers.sort(reverse=True)  # Sort options in descending order for optimization

    result = []
    current_sum = 0

    for value in vouchers:
        while current_sum + value <= budget:
            result.append(value)
            current_sum += value

    return result

def closest_to_budget(dp, budget, allow_overdraft):
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