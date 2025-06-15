def countMinimumOperations(arr):
    n = len(arr)

    # 找到最小元素的位置
    min_pos = arr.index(1)

    # 计算需要的循环左移次数
    shifts = min_pos

    # 计算需要的交换次数
    swaps = 0
    for i in range(n):
        if arr[(i + shifts) % n] != i + 1:
            swaps += 1

    # 总操作次数是左移次数加交换次数
    return shifts + swaps


# 示例
# arr = [5, 3, 2, 1, 4]
arr = [3, 1, 3, 2]
print(countMinimumOperations(arr))  # 输出 2
