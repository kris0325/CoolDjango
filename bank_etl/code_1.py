def findNumOfPairs(a, b):
    # Sort arrays in ascending order
    a.sort()
    b.sort()

    # Initialize pointers and pair count
    i = 0  # Pointer for a
    j = 0  # Pointer for b
    pairs = 0

    # Iterate while both pointers are within bounds
    while i < len(a) and j < len(b):
        if a[i] > b[j]:
            # Valid pair found
            pairs += 1
            i += 1
            j += 1
        else:
            # If a[i] <= b[j], try next a[i]
            i += 1

    return pairs


# Test code
if __name__ == '__main__':
    # Sample 0
    a = [1, 2, 3, 4, 5]
    b = [6, 5, 1, 1, 1]
    print(findNumOfPairs(a, b))  # Expected Output: 3

    # Sample 1
    a = [2, 3, 3]
    b = [3, 4, 5]
    print(findNumOfPairs(a, b))  # Expected Output: 0
