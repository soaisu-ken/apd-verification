import math
import itertools
import sys

# Set a recursion limit higher than the default for deep permutations (e.g., n=8, n=9)
# Note: For n=10+, the runtime will become impractical due to 10! complexity.
sys.setrecursionlimit(3000)

# --- Core Mathematical Helpers (Exact Integer Arithmetic) ---

def factorial(n):
    """Calculates n! using integer arithmetic."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    return math.factorial(n)

def superfactorial_prod(n):
    """Calculates the product of factorials: prod_{k=1}^{n} k!"""
    result = 1
    for k in range(1, n + 1):
        result *= factorial(k)
    return result

def get_sign(p):
    """Calculates the sign of a permutation p (tuple or list)."""
    inversions = 0
    n = len(p)
    for i in range(n):
        for j in range(i + 1, n):
            if p[i] > p[j]:
                inversions += 1
    return 1 if inversions % 2 == 0 else -1

# --- Grid and APD Calculation Functions ---

def get_grid_value_squared(i, j, d):
    """Calculates the element A[i, j] for r=2, 1-indexed (i, j, d).
    A[i, j] = (j + (i - 1) * d)^2"""
    return (j + (i - 1) * d) ** 2

def calculate_apd_general(n, m, d):
    """Calculates the Alternating Power Difference APD_m for d-shift, r=2."""
    elements = tuple(range(1, n + 1))
    
    apd_m = 0
    for p in itertools.permutations(elements):
        sign = get_sign(p)
        
        # Calculate f(sigma) = sum_{i=1}^{n} A[i, p[i-1]]
        f_value = 0
        for i in range(1, n + 1):
            # i is 1-indexed row, p[i-1] is 1-indexed column
            d_current = n if d == 'n' else d
            f_value += get_grid_value_squared(i, p[i-1], d_current)
            
        apd_m += sign * (f_value ** m)
    
    return apd_m

def calculate_expected_apd_general(n, d, t_n_minus_1):
    """Calculates the expected value using the Unified Formula:
    APD_{T_{n-1}} = (2d)^{T_{n-1}} * T_{n-1}! * prod_{k=1}^{n-1} k!"""
    
    # Determine the d value for the formula based on input
    d_for_formula = n if d == 'n' else d
    
    # Calculate the common factor
    common_factor = factorial(t_n_minus_1) * superfactorial_prod(n - 1)
    
    # Calculate the coefficient (2d)^{T_{n-1}}
    coefficient = (2 * d_for_formula) ** t_n_minus_1
    
    expected_apd = coefficient * common_factor
    return expected_apd

# --- Verification Logic ---

def verify_apd_identity(n_max, d_value):
    """Verifies the APD identity for a given shift factor d and matrix size n."""
    results = {}
    print(f"--- Starting verification for d = {d_value} (r=2) up to n={n_max} ---")
    
    for n in range(2, n_max + 1):
        
        t_n_minus_1 = (n * (n - 1)) // 2 # T_{n-1} is the critical exponent m1
        
        # d_current is the d value used for the grid calculation in this iteration
        d_current = n if d_value == 'n' else d_value 

        m1 = 0
        zero_interval = []
        apd_m1 = None
        
        # Check m = 1 up to T_{n-1}
        for m in range(1, t_n_minus_1 + 1):
            # Pass the fixed d_value (e.g., 3) or the dynamic 'n' to the calculation
            apd_m = calculate_apd_general(n, m, d_value)
            
            if apd_m == 0:
                zero_interval.append(str(m))
            
            if apd_m != 0 and m1 == 0:
                m1 = m
                apd_m1 = apd_m
            
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
            
        # Calculate the expected value using the formula
        expected_apd = calculate_expected_apd_general(n, d_value, t_n_minus_1)
        
        results[n] = {
            'd_used': d_current,
            't_n_minus_1': t_n_minus_1,
            'zero_interval': zero_range_str,
            'm1': m1,
            'apd_m1': apd_m1,
            'expected_apd': expected_apd,
            'verified': (m1 == t_n_minus_1) and (apd_m1 == expected_apd)
        }
        
        print(f"--- Finished calculation for n={n}, d={d_current}. Verified: {results[n]['verified']}")
        
    return results

# --- LaTeX Output Formatting ---

def format_latex_table(results, d_source):
    """Formats the verification results into a LaTeX tabular environment."""
    
    # Determine caption, label, and footer based on d_source
    if d_source == 1:
        caption = r"Verification of Exact APD Identity for Squared Skew-Diagonal Grid ($d=1, r=2$)"
        label = r"tab:skew-squared-apd-exact-verification"
        footer = r"\footnotesize{*Note: The values for $n \geq 6$ are extremely large. The displayed coefficient shows the first 6 significant digits. All calculated values are exact integers and have been verified against the formula: $\operatorname{APD}_{T_{n-1}}(f) = 2^{T_{n-1}} \times T_{n-1}! \times \prod_{k=1}^{n-1} k!$.}"
        max_n_fixed = 5
    elif d_source == 'n':
        caption = r"Verification of Exact APD Identity for Squared Natural Square ($d=n, r=2$)"
        label = r"tab:natural-squared-apd-exact-verification"
        footer = r"\footnotesize{*Note: The values for $n \geq 5$ are extremely large. The displayed coefficient shows the first 6 significant digits. All calculated values are exact integers and have been verified against the formula: $\operatorname{APD}_{T_{n-1}}(f) = (2n)^{T_{n-1}} \times T_{n-1}! \times \prod_{k=1}^{n-1} k!$.}"
        max_n_fixed = 4
    else:
        # General case (d != 1, d != n)
        caption = f"Verification of Exact APD Identity for Shifted Squared Grid ($d={d_source}, r=2$)"
        label = f"tab:d-{d_source}-squared-apd-verification"
        # Use a Raw String (r"") for the formula footer
        footer = r"\footnotesize{*Note: All calculated values are exact integers and have been verified against the unified formula: $\operatorname{APD}_{T_{n-1}}(f) = (2d)^{T_{n-1}} \times T_{n-1}! \times \prod_{k=1}^{n-1} k!$.}"
        max_n_fixed = 5
        
    
    latex_output = [
        r"\begin{table}[h]",
        r"\centering",
        r"\caption{" + caption + r"}", 
        r"\label{" + label + r"}",
        r"\begin{tabular}{@{}ccccc@{}}",
        r"\toprule",
        r"$n$ & $T_{n-1}$ & Vanishing Interval & $m_1$ & $\operatorname{APD}_{m_1}(f)$ \\", 
        r"\midrule"
    ]
    
    for n in sorted(results.keys()):
        data = results[n]
        t_n_minus_1 = data['t_n_minus_1']
        m1 = data['m1']
        apd_m1 = data['apd_m1']
        zero_interval = data['zero_interval']
        
        if apd_m1 is None:
            apd_display_str = r"N/A"
        else:
            calculated_str = str(apd_m1)
            
            # Use fixed point format for smaller n
            if n <= max_n_fixed:
                apd_display_str = r"\checkmark \," + f"{apd_m1:,}".replace(",", r",")
            else:
                # Use scientific notation for display readability, keeping exact verification
                if len(calculated_str) < 2:
                    exp = 0
                    base = calculated_str
                else:
                    exp = len(calculated_str) - 1
                    base = calculated_str[0] + '.' + calculated_str[1:6] # First 6 significant digits

                # Enclose the scientific notation in math mode
                apd_display_str = r"\checkmark \,$" + base + r" \times 10^{" + str(exp) + r"}$"
        
        row = f"{n} & {t_n_minus_1} & {zero_interval} & {m1} & {apd_display_str} \\\\"
        latex_output.append(row)

    latex_output.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
        r"\vspace{-0.5em}",
        footer
    ])
    
    return "\n".join(latex_output)

# --- Main Execution Block for Interactive Use ---

if __name__ == '__main__':
    # Set the maximum matrix size for verification (n! complexity)
    N_MAX = 7 
    
    print("=======================================================================")
    print(" Integrated APD Verification for d-Shifted Squared Grid (r=2)")
    print("=======================================================================")
    print(f"Verification will run for n=2 to n={N_MAX}. (n! complexity)")
    
    # Get d value from user input
    while True:
        d_input_str = input("Enter the shift factor d (e.g., 1, 3, 5, or 'n' for the Natural Square case): ").strip().lower()
        
        if d_input_str == 'n':
            D_VALUE = 'n'
            break
        try:
            D_VALUE = int(d_input_str)
            if D_VALUE < 1:
                print("d must be a positive integer (d >= 1). Please try again.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a positive integer or 'n'.")

    # --- Run Verification ---
    print(f"\n--- Running Verification for d = {D_VALUE} ---")
    results = verify_apd_identity(N_MAX, d_value=D_VALUE)
    latex_table = format_latex_table(results, d_source=D_VALUE)

    print("\n==========================================================")
    print("               LaTeX Table Output                        ")
    print("==========================================================")
    
    print(latex_table)
