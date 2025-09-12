#!/usr/bin/env python3
"""
LCM Calculation Problem Solution

Problem: Given positive integers n and y, count all sequences a₁, a₂, ..., aₙ 
such that lcm(a₁, a₂, ..., aₙ) = y. Output the result modulo 10⁹ + 7.

Algorithm: Uses inclusion-exclusion principle
1. All elements in the sequence must be divisors of y
2. For LCM to equal y exactly, for each prime p^k in y's factorization,
   at least one element must have exactly p^k as its highest power of p
3. Use inclusion-exclusion to count valid sequences

Time Complexity: O(d^n × 2^p) where d is number of divisors and p is number of distinct primes
Space Complexity: O(p) for storing prime factors

Input Format: ACM contest style
- First line: T (number of test cases)
- Next T lines: n y (sequence length and target LCM)

Example:
Input:
2
2 6
3 9

Output:
9
19
"""

MOD = 10**9 + 7

def prime_factors(n):
    """
    Get prime factorization of n as a dictionary {prime: power}
    """
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

def power_mod(base, exp, mod):
    """
    Calculate (base^exp) % mod efficiently
    """
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def count_sequences(n, y):
    """
    Count sequences of length n where LCM equals y
    Using inclusion-exclusion principle
    
    Algorithm:
    1. Find all divisors of y (these are the only possible values for elements)
    2. Use inclusion-exclusion to count sequences where LCM = y exactly
    3. Total sequences with all elements dividing y - sequences with LCM < y
    """
    if y == 1:
        return 1 if n >= 1 else 0
    
    # Get prime factorization of y
    factors = prime_factors(y)
    primes = list(factors.keys())
    num_primes = len(primes)
    
    # Edge case: if y has too many distinct prime factors, 
    # inclusion-exclusion might be too slow (2^num_primes iterations)
    if num_primes > 20:  # Reasonable limit for contest problems
        return 0  # This shouldn't happen in typical contest constraints
    
    # Count total divisors of y
    divisor_count = 1
    for power in factors.values():
        divisor_count *= (power + 1)
    
    # Total sequences where all elements divide y
    total_sequences = power_mod(divisor_count, n, MOD)
    
    # Use inclusion-exclusion to subtract sequences where LCM < y
    # For each subset of primes, calculate sequences where the LCM 
    # is missing the highest power of those primes
    result = total_sequences
    
    for mask in range(1, 1 << num_primes):
        # Calculate number of divisors when reducing powers of selected primes
        reduced_divisor_count = 1
        
        for i in range(num_primes):
            prime = primes[i]
            power = factors[prime]
            
            if mask & (1 << i):
                # Reduce this prime's power by 1 (exclude highest power)
                reduced_divisor_count *= max(1, power)
            else:
                # Keep all powers of this prime
                reduced_divisor_count *= (power + 1)
        
        sequences = power_mod(reduced_divisor_count, n, MOD)
        
        # Apply inclusion-exclusion: alternate adding and subtracting
        if bin(mask).count('1') % 2 == 1:
            result = (result - sequences + MOD) % MOD
        else:
            result = (result + sequences) % MOD
    
    return result

def main():
    """
    Main function to handle ACM contest input/output
    Constraints: 1 ≤ T ≤ 10³, 1 ≤ n ≤ 10⁵, 1 ≤ y ≤ 10⁹
    """
    T = int(input().strip())
    
    for _ in range(T):
        n, y = map(int, input().strip().split())
        
        # Input validation for contest constraints
        if not (1 <= n <= 10**5 and 1 <= y <= 10**9):
            print(0)  # Invalid input, output 0
            continue
            
        result = count_sequences(n, y)
        print(result)

if __name__ == "__main__":
    main()