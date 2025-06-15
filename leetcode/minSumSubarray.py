"""
1. array 找连续k个element 和最小的 子nums
相似leetcode原题: LeetCode 209. 长度最小的子数组

"""


def minSumarry(nums: List[int], k: int) -> List[int]:
    if not nums or k > len(nums) or k <= 0:
        return None

    windown_sum = sum(nums[:k])
    min_sum = windown_sum
    start_index = 0

    for i in range(k, len(nums)):
        windown_sum = windown_sum - nums[i - k] + nums[i]
        if windown_sum < min_sum:
            min_sum = windown_sum
            start_index = i - k + 1
    return nums[start_index : start_index + k]
