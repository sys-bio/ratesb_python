Default Rate Law Classifications
================================

Before the analysis, we classify each rate law into different categories (Xu, 2023). If a rate law does not belong to any of the default classes or the custom classification file provided, a warning will be raised.

The following categories are used for classifying rate laws:
- **Zeroth order (ZERO)**: No reactant or product in the rate law.
- **Uni-Directional Mass Action (UNDR)**: Direct, one-way reactions where all reactants influencing the rate law and resulting in a single product.
- **Uni-Directional Mass Action with an Activator (UNDR-A)**: Similar to UNDR but includes an essential activator.
- **Irreversible Enzymatic non-Mass Action Rate Law**: Features at least one enzyme and not all reactants in the rate law.
- **Bi-Directional Mass Action (BIDR)**: Covers reversible reactions with all reactants and products in the rate law.
- **Bi-Directional Mass Action with Activator(s) (BIDR-A)**: Reversible reactions with activators, including enzymes different from reactants and products.
- **Reversible Enzymatic non-Mass Action Rate Law**: For reversible reactions where not all reactants or products are in the rate law, including at least one enzyme.
- **Michaelis-Menten (MM)**: Describes enzymatic reactions based on substrate concentration, following specific Michaelis-Menten formulas without explicitly mentioning the enzyme.
- **Michaelis-Menten with explicit enzyme (MMcat)**: Michaelis-Menten model explicitly incorporating the enzyme in the reaction rate equation.
- **Allosteric and Inhibitors**: Michaelis-Menten format affected by allosteric effects or inhibitors, altering reaction rates through enzyme or substrate modulation.
- **Reversible Michaelis-Menten**: Accounts for reaction reversibility in Michaelis-Menten format.
- **Hill Equation**: Describes enzyme kinetics in cooperative binding scenarios, relating reaction rate to substrate concentration through a sigmoidal curve.

The details of the default rate law classifications can be found in the `source code`_.

.. _source code: https://github.com/sys-bio/ratesb_python/tree/main/ratesb_python/common
