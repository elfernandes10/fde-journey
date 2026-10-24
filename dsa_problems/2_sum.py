def two_sum(nums: list[int], target: int) -> list[int]:
    lookup_dict = {}  # {number: index}

    for i, num in enumerate(nums):
        remainder = target - num
        if remainder in lookup_dict:
            return [lookup_dict[remainder], i]
        lookup_dict[num] = i
    
    return []  # unreachable per problem constraints, but defensive


if __name__ == "__main__":
    # From the problem
    assert two_sum([2, 7, 11, 15], 9) == [0, 1], "classic case failed"
    assert two_sum([3, 2, 4], 6) == [1, 2], "second case failed"
    assert two_sum([3, 3], 6) == [0, 1], "duplicates case failed"
    
    # Negatives
    assert two_sum([-1, -2, -3, -4, -5], -8) == [2, 4], "negatives failed"
    
    # Target of zero
    assert two_sum([-3, 4, 3, 90], 0) == [0, 2], "target zero failed"
    
    # Larger input, pair at the end
    assert two_sum([1, 5, 7, 2, 9, 3], 5) == [3, 5], "pair at end failed"
    
    print("All tests passed!")