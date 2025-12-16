import math
import itertools

def factorial(n):
    # Calculates n!
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    return math.factorial(n)

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

def get_fixed_points(p):
    # Calculates the number of fixed points (fix(sigma))
    # Note: Permutations are 1-indexed, enumerate is 0-indexed, so we use i+1
    return sum(1 for i, x in enumerate(p, 1) if i == x)

def calculate_apd(n, m):
    # Calculates the Alternating Power Difference APD_m(fix)
    
    # S_n is generated as permutations of (1, 2, ..., n)
    elements = tuple(range(1, n + 1))
    
    apd_m = 0
    for p in itertools.permutations(elements):
        sign = get_sign(p)
        fix = get_fixed_points(p)
        apd_m += sign * (fix ** m)
    
    return apd_m

def verify_apd_identity(n_max):
    results = {}
    print(f"--- Starting calculation for n=2 to n={n_max}...")
    
    for n in range(2, n_max + 1):
        
        # 1. Determine the vanishing interval and m1(fix)
        m1 = 0
        zero_interval = []
        apd_m1 = None
        
        # Check m = 1 up to n-1
        for m in range(1, n):
            apd_m = calculate_apd(n, m)
            
            if apd_m == 0:
                zero_interval.append(str(m))
            
            if apd_m != 0 and m1 == 0:
                m1 = m
                apd_m1 = apd_m
            
        # Format the zero interval
        if not zero_interval:
            zero_range_str = r"None" # Changed from r"なし"
        else:
            # Check for contiguous range
            first = int(zero_interval[0])
            last = int(zero_interval[-1])
            
            if last == first:
                zero_range_str = str(first)
            elif last > first:
                zero_range_str = f"{first}--{last}"
            else:
                zero_range_str = r"None" # Should not happen based on logic
            
        # 2. Verify the conjecture
        expected_m1 = n - 1
        expected_apd = factorial(n)
        
        # APD is calculated as apd_m1, we just check the value and m1
        
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
        r"\caption{First Appearance Order and Value for Identity Matrix $I_n$ (Verification Results)}", # English Caption
        r"\label{tab:identity-apd-verification}",
        r"\begin{tabular}{@{}cccc@{}}",
        r"\toprule",
        r"$n$ & Vanishing Interval & $m_1(\operatorname{fix})$ & $\operatorname{APD}_{m_1}(\operatorname{fix})$ \\", # English Column Headers
        r"\midrule"
    ]
    
    # We start the loop from n=2 to match the structure of the original table's content
    
    for n in sorted(results.keys()):
        data = results[n]
        m1 = data['m1']
        apd_m1 = data['apd_m1']
        expected_apd = data['expected_apd']
        zero_interval = data['zero_interval']
        
        # Format the APD value with comma separator and expected value check
        if apd_m1 == expected_apd:
            # Note: LaTeX uses "," for thousands separator, so we must replace Python's ',' with r','
            apd_str = f"{apd_m1:,}".replace(",", r",") + r" = " + str(n) + r"!"
        else:
            # Should not happen if the conjecture is correct
            apd_str = f"{apd_m1:,}".replace(",", r",")
            
        row = f"{n} & {zero_interval} & {m1} & {apd_str} \\\\"
        latex_output.append(row)

    latex_output.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}"
    ])
    
    return "\n".join(latex_output)

# Run verification for n=2 to n=10 (n=10 takes significantly longer)
n_max = 10
verification_results = verify_apd_identity(n_max)

# Generate LaTeX output
latex_table = format_latex_table(verification_results)

# Print the LaTeX code
print(latex_table)