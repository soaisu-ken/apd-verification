# APD (Alternating Power Difference) Verification Scripts

This repository provides numerical verification programs for the research paper:  
**"Analysis of Matrix Symmetry using APD (Alternating Power Difference): Conjectures and Closed-Form Formulas for the First Appearance Degree $m_1$."**

## Overview
These scripts calculate the **Alternating Power Difference (APD)** and the **First Appearance Degree ($m_1$)** for the function $f_A(\sigma) = \mathrm{tr}(AP_\sigma)$ defined on the symmetric group $S_n$. The purpose is to numerically verify the conjectures presented in the paper regarding various matrix structures.

## File Structure
This repository contains individual scripts for each matrix type analyzed in the study:

1. **`apd_identity.py`**: $n \times n$ Identity matrix $I_n$.
2. **`apd_circulant.py`**: $n \times n$ Standard Circulant matrix.
3. **`apd_shift_lattice.py`**: Quadratic lattice with $d$-shift per row.
4. **`apd_hilbert.py`**: $n \times n$ Hilbert matrix (uses exact rational arithmetic).
5. **`apd_multiplication.py`**: $n \times n$ Multiplication table lattice.
6. **`apd_vandermonde.py`**: $n \times n$ Vandermonde matrix.
7. **`apd_pascal.py`**: $n \times n$ Pascal matrix.

## Important Notes
* **Computational Complexity**: These scripts perform an exhaustive search of the symmetric group $S_n$ (complexity $O(n!)$). While calculations for $n \le 10$ complete within seconds, the execution time increases exponentially for $n \ge 11$.
* **Numerical Precision**: For the Hilbert matrix (`apd_hilbert.py`), the script uses the `fractions` module to ensure exact results without floating-point errors.
* **Customization**: You can adjust the range of calculation by modifying the `n_max` variable within each script.

## Author
**Kenichi Takemura**
