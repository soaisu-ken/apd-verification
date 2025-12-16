import math
import itertools

def factorial(n):
    # Calculates n!
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0:
        return 1
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res

def product_of_factorials(n_minus_1):
    # Calculates Product_{k=1}^{n-1} k!
    prod = 1
    for k in range(1, n_minus_1 + 1):
        prod *= factorial(k)
    return prod

def get_sign(p):
    # Calculates the sign of a permutation p (tuple or list)
    # Counts the number of inversions
    inversions = 0
    n = len(p)
    for i in range(n):
        for j in range(i + 1, n):
            if p[i] > p[j]:
                inversions += 1
    return 1 if inversions % 2 == 0 else -1

def get_vandermonde_diagonal_sum(p):
    # Calculates the diagonal sum T(sigma; V_n) for the standard Vandermonde matrix V_n
    # V_n[i, j] = i**(j-1)
    # The permutation p is 1-indexed (p[i] is the column index, i+1 is the row index)
    # i-th row is indexed from 1, so the row element is i+1
    # p[i] is the column index (1-based)
    
    diagonal_sum = 0
    # Iterate through the rows (i from 1 to n)
    for i, col_index in enumerate(p, 1):
        row_element = i       # Base value is i
        exponent = col_index - 1 # Exponent is j-1, where j = col_index
        diagonal_sum += (row_element ** exponent)
    
    return diagonal_sum

def calculate_apd_vandermonde(n, m):
    # Calculates the Alternating Power Difference APD_m(f_V)
    
    # S_n is generated as permutations of (1, 2, ..., n)
    elements = tuple(range(1, n + 1))
    
    apd_m = 0
    for p in itertools.permutations(elements):
        sign = get_sign(p)
        f_v = get_vandermonde_diagonal_sum(p)
        apd_m += sign * (f_v ** m)
    
    return apd_m

def verify_vandermonde_apd(n_max):
    results = {}
    print(f"--- Starting calculation for n=2 to n={n_max}...")
    
    for n in range(2, n_max + 1):
        
        # 1. Determine the vanishing interval and m1(f_V)
        m1 = 0
        zero_interval = []
        apd_m1 = None
        
        # We check m = 1 up to n-1 (Expected m1)
        for m in range(1, n):
            apd_m = calculate_apd_vandermonde(n, m)
            
            if apd_m == 0:
                zero_interval.append(str(m))
            
            if apd_m != 0 and m1 == 0:
                m1 = m
                apd_m1 = apd_m
        
        # If m1 is not found in the expected range, check the expected m1 (n-1)
        if m1 == 0:
            m = n - 1 # The expected first non-zero degree
            apd_m = calculate_apd_vandermonde(n, m)
            
            if apd_m != 0:
                 m1 = m
                 apd_m1 = apd_m
            # Note: If it's still zero, the conjecture is immediately false for this n, but we report the findings.
            
        # Format the zero interval
        if not zero_interval:
            zero_range_str = r"None" 
        else:
            first = int(zero_interval[0])
            last = int(zero_interval[-1])
            if last == first:
                zero_range_str = str(first)
            elif last > first:
                zero_range_str = f"{first}--{last}"
            else:
                zero_range_str = r"None" # Should not happen based on logic
                
        # 2. Calculate the expected value using the conjectured formula
        expected_m1 = n - 1
        # Formula: (n-1)! * Product_{k=1}^{n-1} k! * (n-1)!
        n_minus_1_fact = factorial(n - 1)
        prod_k_fact = product_of_factorials(n - 1)
        expected_apd = n_minus_1_fact * prod_k_fact * n_minus_1_fact
        
        results[n] = {
            'zero_interval': zero_range_str,
            'm1': m1,
            'apd_m1': apd_m1,
            'expected_apd': expected_apd,
            'verified': (m1 == expected_m1) and (apd_m1 == expected_apd)
        }
        
        print(f"--- Finished calculation for n={n}. m1={m1}, APD_{m1}={apd_m1}")
        
    return results

def format_latex_table(results):
    latex_output = [
        r"\begin{table}[h]",
        r"\centering",
        r"\caption{First Appearance Order and Value for Standard Vandermonde Matrix $V_n$ (Verification Results)}", # English Caption
        r"\label{tab:vandermonde-apd-verification}",
        r"\begin{tabular}{@{}cccc@{}}",
        r"\toprule",
        r"$n$ & Vanishing Interval & $m_1(f_V)$ & $\operatorname{APD}_{m_1}(f_V)$ \\", # English Column Headers
        r"\midrule"
    ]
    
    for n in sorted(results.keys()):
        data = results[n]
        m1 = data['m1']
        apd_m1 = data['apd_m1']
        expected_apd = data['expected_apd']
        zero_interval = data['zero_interval']
        
        # Format the APD value with comma separator
        apd_str = f"{apd_m1:,}".replace(",", r",")
        
        # Add a checkmark if verified
        if data['verified']:
            apd_str = r"\checkmark \, " + apd_str
        
        row = f"{n} & {zero_interval} & {m1} & {apd_str} \\\\"
        latex_output.append(row)

    latex_output.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}"
    ])
    
    return "\n".join(latex_output)

# Set n_max to 7 as requested. (n=7 takes a few minutes, n=8 takes a few hours)
n_max = 7 
verification_results = verify_vandermonde_apd(n_max)

# Generate LaTeX output
latex_table = format_latex_table(verification_results)

# Print the LaTeX code
print("\n" + r"% --- Generated LaTeX Table ---" + "\n")
print(latex_table)
