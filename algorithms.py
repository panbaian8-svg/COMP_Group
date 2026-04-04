def radix_sort(prices):
    """
    Sorts a list of prices in ascending order using the Radix Sort algorithm.
    Note: Since Radix Sort typically handles integers, prices are multiplied 
    by 100 to process them as cents.
    """
    if not prices:
        return []
        
    # Convert floats to integers (e.g., 12.50 -> 1250) for bitwise/digit processing
    nums = [int(p * 100) for p in prices]
    max_num = max(nums)
    
    # exp represents the current digit position (1, 10, 100, etc.)
    exp = 1  
    while max_num // exp > 0:
        
        # Create 10 buckets for digits 0-9
        buckets = [[] for _ in range(10)]
        
        # Distribution stage: Place numbers into buckets based on the current digit
        for num in nums:
            index = (num // exp) % 10
            buckets[index].append(num)
        
        # Collection stage: Reconstruct the list from buckets in order
        nums = []
        for bucket in buckets:
            nums.extend(bucket)
            
        # Move to the next significant digit
        exp *= 10  
        
    # Convert integers back to float prices
    return [n / 100 for n in nums]

if __name__ == "__main__":
    test_prices = [12.5, 5.0, 9.99, 25.0, 3.5]
    sorted_p = radix_sort(test_prices)
    print(f"Original Prices: {test_prices}")
    print(f"Sorted Prices:   {sorted_p}")

# Alias for compatibility with main_project.py
radix_sort_prices = radix_sort
