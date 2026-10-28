def max_profit(prices: list[int]) -> int:
    min_price = prices[0]
    max_so_far = 0

    for price in prices[1:]:
        current_profit = price - min_price
        if current_profit > max_so_far:
            max_so_far = current_profit
        if price < min_price:
            min_price = price

    return max_so_far


if __name__ == "__main__":
    assert max_profit([7, 1, 5, 3, 6, 4]) == 5, "basic case failed"
    assert max_profit([7, 6, 4, 3, 1]) == 0, "descending failed"
    assert max_profit([1]) == 0, "single element failed"
    assert max_profit([1, 2]) == 1, "two increasing failed"
    assert max_profit([2, 1]) == 0, "two decreasing failed"
    assert max_profit([3, 3, 3, 3]) == 0, "all same failed"
    assert max_profit([1, 2, 3, 4, 5]) == 4, "strictly ascending failed"
    assert max_profit([0, 5, 2, 8]) == 8, "zero start failed"
    
    print("All tests passed!")