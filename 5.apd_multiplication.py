import math
import itertools
import sys

# Increase recursion limit if necessary for deep calculations
sys.setrecursionlimit(3000)

def factorial(n):
    """Calculates n! using exact integer arithmetic."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    return math.factorial(n)

def triangle_number(n):
    """Calculates the (n-1)-th Triangle number: T_{n-1} = n*(n-1)/2"""
    if n < 1:
        return 0
    return n * (n - 1) // 2

def get_sign(p):
    """Calculates the sign of a permutation p by counting inversions."""
    inversions = 0
    n = len(p)
    for i in range(n):
        for j in range(i + 1, n):
            if p[i] > p[j]:
                inversions += 1
    return 1 if inversions % 2 == 0 else -1

def calculate_multiplication_sum(p):
    """
    Calculates the function f_1(sigma) for the Multiplication Table M_n.
    f_1(sigma) = sum_{i=1}^n i * sigma(i)
    """
    sum_val = 0
    for i, sigma_i in enumerate(p, 1):
        # i is the row index, sigma_i (p[i-1]) is the column index
        sum_val += i * sigma_i
    return sum_val

def calculate_apd_multiplication(n, m):
    """Calculates the Alternating Power Difference APD_m for the Multiplication Table."""
    elements = tuple(range(1, n + 1))
    apd_m = 0
    for p in itertools.permutations(elements):
        sign = get_sign(p)
        f_val = calculate_multiplication_sum(p)
        apd_m += sign * (f_val ** m)
    return apd_m

def calculate_expected_apd(n):
    """
    Calculates the conjectured closed-form value:
    APD_{T_{n-1}}(M_n) = T_{n-1}! * prod_{k=1}^{n-1} k!
    """
    t_n_minus_1 = triangle_number(n)
    
    # Calculate T_{n-1}!
    expected_value = factorial(t_n_minus_1)
    
    # Calculate product of factorials: prod_{k=1}^{n-1} k!
    product_of_factorials = 1
    for k in range(1, n):
        product_of_factorials *= factorial(k)
        
    expected_value *= product_of_factorials
    return expected_value

def verify_multiplication_table(n_max):
    """Performs numerical verification for n=2 up to n_max."""
    results = {}
    print(f"--- Starting verification for Multiplication Table M_n (n=2 to {n_max}) ---")
    
    for n in range(2, n_max + 1):
        t_n_minus_1 = triangle_number(n)
        
        m1 = 0
        zero_interval = []
        apd_m1 = None
        
        # Check m from 1 up to T_{n-1}
        for m in range(1, t_n_minus_1 + 1):
            apd_m = calculate_apd_multiplication(n, m)
            
            if apd_m == 0:
                zero_interval.append(str(m))
            
            if apd_m != 0 and m1 == 0:
                m1 = m
                apd_m1 = apd_m
                
        # Format vanishing interval string
        if not zero_interval:
            vanishing_str = "None"
        else:
            first = zero_interval[0]
            last = zero_interval[-1]
            vanishing_str = f"1--{last}" if int(last) > int(first) else str(first)
            
        # Verify against conjecture
        expected_m1 = t_n_minus_1
        expected_apd = calculate_expected_apd(n)
        
        is_verified = (m1 == expected_m1) and (apd_m1 == expected_apd)
        
        results[n] = {
            'm1': m1,
            'vanishing_interval': vanishing_str,
            'apd_m1': apd_m1,
            'expected_apd': expected_apd,
            'verified': is_verified
        }
        print(f"n={n}: m1={m1}, Verified={is_verified}")
        
    return results

def format_latex_table(results):
    """Formats the results into a LaTeX table."""
    caption = "Verification of the First Appearance Degree $m_1$ for the Multiplication Table $M_n$"
    label = "tab:multiplication-apd-verification"
    
    latex = [
        r"\begin{table}[h]",
        r"\centering",
        f"\\caption{{{caption}}}",
        f"\\label{{{label}}}",
        r"\begin{tabular}{@{}cccc@{}}",
        r"\toprule",
        r"$n$ & $m_1(f_1)$ & Vanishing Interval & $\operatorname{APD}_{m_1}(f_1)$ \\",
        r"\midrule"
    ]
    
    for n in sorted(results.keys()):
        res = results[n]
        check = r"\checkmark \," if res['verified'] else ""
        apd_val = f"{res['apd_m1']:,}".replace(",", r",")
        
        row = f"{n} & {res['m1']} & {res['vanishing_interval']} & {check} {apd_val} \\\\"
        latex.append(row)
        
    footer = r"\footnotesize{*Note: Verification confirms that $m_1(f_1) = T_{n-1}$ and $\operatorname{APD}_{m_1}$ matches the conjectured formula $T_{n-1}! \cdot \prod_{k=1}^{n-1} k!$.}"
    
    latex.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\vspace{-0.5em}",
        footer,
        r"\end{table}"
    ])
    
    return "\n".join(latex)

if __name__ == "__main__":
    N_MAX = 7
    verification_data = verify_multiplication_table(N_MAX)
    print("\n" + "="*50)
    print("Generated LaTeX Table:")
    print("="*50 + "\n")
    print(format_latex_table(verification_data))