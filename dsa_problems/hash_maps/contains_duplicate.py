def contains_duplicate(nums: list[int]) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False


if __name__ == "__main__":
    assert contains_duplicate([1, 2, 3, 1]) == True, "basic duplicate failed"
    assert contains_duplicate([1, 2, 3, 4]) == False, "all unique failed"
    assert contains_duplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) == True, "many dups failed"
    assert contains_duplicate([5]) == False, "single element failed"
    assert contains_duplicate([5, 5]) == True, "immediate duplicate failed"
    assert contains_duplicate([-3, 2, -3, 7, 1]) == True, "negatives with duplicate failed"
    assert contains_duplicate([-3, 2, 7, 1, 0]) == False, "negatives without duplicate failed"

    print("All tests passed!")