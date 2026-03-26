

def radix_sort(prices):
    """
    
    """
    if not prices:
        return []
        
    nums = [int(p * 100) for p in prices]
    max_num = max(nums)
    
    exp = 1  
    while max_num // exp > 0:
        
        buckets = [[] for _ in range(10)]
        
        
        for num in nums:
            index = (num // exp) % 10
            buckets[index].append(num)
        
        
        nums = []
        for bucket in buckets:
            nums.extend(bucket)
            
        exp *= 10  # 进到下一位
        
    
    return [n / 100 for n in nums]


if __name__ == "__main__":
    test_prices = [12.5, 5.0, 9.99, 25.0, 3.5]
    sorted_p = radix_sort(test_prices)
    print(f"Original Prices: {test_prices}")
    print(f"Sorted Prices:   {sorted_p}")
