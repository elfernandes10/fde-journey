 #Minimum Size Subarray Sum - sliding window
# Approach:
# 1. Start l=0, r=0. Iterate r through array. Add nums[r] to sum_counter each step.
# 2. Check if sum_counter >= target.
# 3. If yes, compute current_length = r - l + 1. If current_length < min_length, update min_length.
# 4. Subtract nums[l] from sum_counter, then increment l. (Order matters — subtract BEFORE moving.)
# 5. After loop ends: if min_length is still infinity, return 0; else return min_length.

def min_subarray_len(nums: list[int], target: int) -> int:
    l = 0
    min_length = float('inf')
    current_sum = 0
    n = len(nums)

    for r in range(n):
        current_sum += nums[r]
        
        while current_sum >= target:
            current_length = r - l + 1
            if current_length < min_length:
                min_length = current_length
            current_sum -= nums[l]
            l += 1

    if min_length == float('inf'):
        return 0
    else:
        return min_length
    

if __name__ == "__main__":
    assert min_subarray_len([2, 3, 1, 2, 4, 3], 7) == 2, "basic case failed"
    assert min_subarray_len([1, 4, 4], 4) == 1, "single element meets target failed"
    assert min_subarray_len([1, 1, 1, 1, 1, 1, 1, 1], 11) == 0, "sum never reaches target failed"
    assert min_subarray_len([1, 2, 3, 4, 5], 11) == 3, "shortest at end failed"
    assert min_subarray_len([10], 5) == 1, "single element exceeds target failed"
    assert min_subarray_len([1], 5) == 0, "single element below target failed"
    assert min_subarray_len([5, 1, 3, 5, 10, 7, 4, 9, 2, 8], 15) == 2, "larger test failed"
    
    print("All tests passed!")