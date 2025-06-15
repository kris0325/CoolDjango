def max_subsequence_sum(nums):
    if not nums:
        return 0
    n = len(nums)
    # 初始化dp數組
    dp = [0] * n
    dp[0] = nums[0]
    dp[1] = max(nums[1], nums[0] + nums[1])

    for i in range(2, n):
        # 狀態轉移， 不選擇當前元素nums[i] | 選擇
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
    return dp[-1]


nums = [1, 2, -3, 4, 5]
print(max_subsequence_sum(nums))
