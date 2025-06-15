from typing import List


def moveZeroes(nums: List[int]) -> None:
    non_zero = 0
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[non_zero], nums[i] = nums[i], nums[non_zero]
            non_zero += 1


if __name__ == "__main__":

    # 测试用例1：常规情况
    nums1 = [0, 1, 0, 3, 12]
    moveZeroes(nums1)

    print(nums1)
