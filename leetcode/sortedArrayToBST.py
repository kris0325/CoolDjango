class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def sortedArrayToBST(self, nums):
        self.call_count = 0
        
        def buildBST(left, right):
            self.call_count += 1
            if left > right:
                return None
            
            mid = (left + right) // 2
            root = TreeNode(nums[mid])
            root.left = buildBST(left, mid - 1)
            root.right = buildBST(mid + 1, right)
            return root
        
        root = buildBST(0, len(nums) - 1)
        return root, self.call_count

# 示例使用
nums = [1, 2, 3, 4, 5, 6, 7]
solution = Solution()
bst_root, function_calls = solution.sortedArrayToBST(nums)
print("递归函数调用次数:", function_calls)