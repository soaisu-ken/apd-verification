import math
import itertools
import numpy as np

def factorial(n):
    # Calculates n!
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    return math.factorial(n)

def get_sign(p):
    # Calculates the sign of a permutation p (tuple or list)
    # Uses counting inversions to find the sign
    inversions = 0
    n = len(p)
    for i in range(n):
        for j in range(i + 1, n):
            if p[i] > p[j]:
                inversions += 1
    return 1 if inversions % 2 == 0 else -1

def create_circulant_matrix(n):
    # Creates the n x n standard circulant matrix C_n
    C = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            # (C_n)_{i,j} = ((j + i) mod n) + 1 (using 0-indexing for i, j)
            C[i, j] = ((j + i) % n) + 1
    return C

def get_perm_matrix(n, p):
    # Creates the n x n permutation matrix P_sigma for permutation p (1-indexed)
    P = np.zeros((n, n), dtype=int)
    # The (i+1)-th row (0-indexed i) corresponds to item i+1 being moved to position p[i]
    for i, target_val in enumerate(p):
        P[i, target_val - 1] = 1
    return P

def get_circulant_function_value(C_n, P_sigma):
    # Defines the function f_C(sigma) = Tr(C_n * P_sigma)
    product = C_n.dot(P_sigma)
    return np.trace(product)

def calculate_apd_circulant(n, m):
    # Calculates the Alternating Power Difference APD_m(C_n)

    elements = tuple(range(1, n + 1))
    C_n = create_circulant_matrix(n)

    apd_m = 0
    # Iterating over all n! permutations
    for p in itertools.permutations(elements):
        sign = get_sign(p)
        P_sigma = get_perm_matrix(n, p)

        # Function value f_C(sigma)
        f_value = get_circulant_function_value(C_n, P_sigma)

        # Summation
        apd_m += sign * (f_value ** m)

    return apd_m

def verify_apd_circulant_identity(n_max):
    results = {}
    for n in range(2, n_max + 1):
        print(f"--- Starting calculation for C_{n}...")

        # 1. Determine the vanishing interval and m1(C_n)
        m1 = 0
        zero_interval = []
        apd_m1 = None

        # Check m = 1 up to n-1
        for m in range(1, n):
            apd_m = calculate_apd_circulant(n, m)

            if apd_m == 0:
                zero_interval.append(str(m))

            if apd_m != 0 and m1 == 0:
                m1 = m
                apd_m1 = apd_m

        # Format the zero interval
        if not zero_interval:
            zero_range_str = r"None" # Changed from r"なし"
        else:
            first = int(zero_interval[0])
            last = int(zero_interval[-1])
            if last == first:
                zero_range_str = str(first)
            elif last > first:
                zero_range_str = f"{first}--{last}"
            else:
                zero_range_str = r"None" # Changed from r"なし"

        # 2. Store results
        results[n] = {
            'zero_interval': zero_range_str,
            'm1': m1,
            'apd_m1': apd_m1,
        }
        print(f"--- Finished calculation for C_{n}. m1={m1}, APD_{m1}={apd_m1}")

    return results

def format_circulant_latex_table(results):
    latex_output = [
        r"\begin{table}[h]",
        r"\centering",
        r"\caption{First Appearance Order and Value for Standard Circulant Matrix $C_n$ (Verification Results)}", # English Caption
        r"\label{tab:circulant-apd-verification}",
        r"\begin{tabular}{@{}cccc@{}}",
        r"\toprule",
        r"$n$ & Vanishing Interval & $m_1(C_n)$ & $\operatorname{APD}_{m_1}(C_n)$ \\",
        r"\midrule"
    ]

    for n in sorted(results.keys()):
        data = results[n]
        m1 = data['m1']
        apd_m1 = data['apd_m1']

        # Format the APD value with comma separator
        # Note: LaTeX uses "," for thousands separator, so we must replace Python's ',' with r','
        apd_str = f"{apd_m1:,}".replace(",", r",")

        row = f"{n} & {data['zero_interval']} & {m1} & {apd_str} \\\\"
        latex_output.append(row)

    latex_output.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}"
    ])

    return "\n".join(latex_output)

# Set n_max to 10
n_max = 10
verification_results = verify_apd_circulant_identity(n_max)

# Generate LaTeX output
latex_table = format_circulant_latex_table(verification_results)

# Print the LaTeX code
print(latex_table)
