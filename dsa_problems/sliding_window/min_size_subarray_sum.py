 #Minimum Size Subarray Sum - sliding window
# Approach:
# 1. Start l=0, r=0. Iterate r through array. Add nums[r] to sum_counter each step.
# 2. Check if sum_counter >= target.
# 3. If yes, compute current_length = r - l + 1. If current_length < min_length, update min_length.
# 4. Subtract nums[l] from sum_counter, then increment l. (Order matters — subtract BEFORE moving.)
# 5. After loop ends: if min_length is still infinity, return 0; else return min_length.