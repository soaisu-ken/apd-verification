import math
import itertools
from datetime import datetime

# --- Utility Functions ---

def factorial(n):
    # Calculates n!
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    return math.factorial(n)

def binomial_coefficient(n, k):
    # Calculates nCk (n choose k)
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    if k > n // 2:
        k = n - k
    
    # Use math.comb for Python 3.8+ compatibility, or manual calculation if needed
    try:
        return math.comb(n, k)
    except AttributeError:
        # Fallback for older Python versions
        res = 1
        for i in range(k):
            res = res * (n - i) // (i + 1)
        return res

def get_pascal_matrix_element(i, j):
    # Calculates P_n[i, j] = (i+j-2) C (i-1)
    # The sum of indices is i+j. The top parameter is sum - 2.
    n_param = i + j - 2
    k_param = i - 1
    return binomial_coefficient(n_param, k_param)

def get_pascal_diagonal_sum(n, p):
    # Calculates the diagonal sum f_P(sigma) for the Pascal Matrix P_n
    # p is the permutation (1-indexed)
    
    diagonal_sum = 0
    # Iterate through the rows (i from 1 to n)
    for i, col_index in enumerate(p, 1):
        j = col_index # j = sigma(i)
        
        # P_n[i, j] = (i+j-2) C (i-1)
        element = get_pascal_matrix_element(i, j)
        diagonal_sum += element
    
    return diagonal_sum

def get_sign(p):
    # Calculates the sign of a permutation p (tuple or list)
    inversions = 0
    n = len(p)
    for i in range(n):
        for j in range(i + 1, n):
            if p[i] > p[j]:
                inversions += 1
    return 1 if inversions % 2 == 0 else -1

# --- Main APD Calculation Function ---

def calculate_apd_pascal(n, m):
    # Calculates the Alternating Power Difference APD_m(f_P)
    
    # S_n is generated as permutations of (1, 2, ..., n)
    elements = tuple(range(1, n + 1))
    
    apd_m = 0
    for p in itertools.permutations(elements):
        sign = get_sign(p)
        f_p = get_pascal_diagonal_sum(n, p)
        apd_m += sign * (f_p ** m)
        
    return apd_m

# --- Verification Logic ---

def verify_apd_pascal_matrix(n_max):
    results = {}
    print(f"--- Starting Pascal Matrix APD calculation for n=2 to n={n_max}...")
    
    for n in range(2, n_max + 1):
        start_time = datetime.now()
        
        # 1. Determine the vanishing interval and m1(f_P)
        m1 = 0
        zero_interval = []
        apd_m1 = None
        
        # Search for m1 from m=1 up to n
        # Since Pascal Matrix is complex, we might need to check beyond n-1
        # Let's check up to 2*n for now, or just n to maintain speed.
        
        # Check m = 1 up to n-1 (Max m to check = n)
        # We check one step beyond the known vanishing interval (n-1 for V_n, I_n)
        m_max_check = n
        
        for m in range(1, m_max_check + 1):
            apd_m = calculate_apd_pascal(n, m)
            
            if apd_m == 0:
                zero_interval.append(str(m))
            
            if apd_m != 0 and m1 == 0:
                m1 = m
                apd_m1 = apd_m
                # Once m1 is found, we stop the search for APD values
                break
                
        # Format the zero interval
        if not zero_interval:
            zero_range_str = r"None"
        else:
            first = int(zero_interval[0])
            last = int(zero_interval[-1])
            if last == first:
                zero_range_str = str(first)
            else:
                zero_range_str = f"{first}--{last}"
                
        end_time = datetime.now()
        duration = end_time - start_time
        
        # 2. Record the result
        # Note: We do NOT assume a simple formula like n! yet, 
        # but check the actual value.
        
        results[n] = {
            'zero_interval': zero_range_str,
            'm1': m1,
            'apd_m1': apd_m1,
            'duration': duration
        }
        
        print(f"--- Finished calculation for n={n} (Duration: {duration}).")
        print(f"n={n}: Vanishing Interval={zero_range_str}, m1={m1}, APD_{m1}={apd_m1:,}")
        
    return results

def format_latex_table_pascal(results):
    latex_output = [
        r"\begin{table}[h]",
        r"\centering",
        r"\caption{First Appearance Order and Value for Pascal Matrix $P_n$ (Verification Results)}",
        r"\label{tab:pascal-apd-verification}",
        r"\begin{tabular}{@{}cccc@{}}",
        r"\toprule",
        r"$n$ & Vanishing Interval & $m_1(f_P)$ & $\operatorname{APD}_{m_1}(f_P)$ \\",
        r"\midrule"
    ]
    
    for n in sorted(results.keys()):
        data = results[n]
        m1 = data['m1']
        apd_m1 = data['apd_m1']
        zero_interval = data['zero_interval']
        
        # Format the APD value with comma separator
        if isinstance(apd_m1, int):
            apd_str = f"{apd_m1:,}".replace(",", r",")
        else:
            apd_str = str(apd_m1)
            
        row = f"{n} & {zero_interval} & {m1} & {apd_str} \\\\"
        latex_output.append(row)

    latex_output.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}"
    ])
    
    return "\n".join(latex_output)

# --- Execution ---

n_max = 7 # Set to 7 for reasonable runtime
verification_results = verify_apd_pascal_matrix(n_max)

# Generate LaTeX output
latex_table = format_latex_table_pascal(verification_results)

# Print the LaTeX code
print("\n" + "="*50)
print("PASCAL MATRIX APD RESULTS")
print("="*50)
print(latex_table)
