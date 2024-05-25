Default Rate Law Classifications
================================

Before the analysis, we classify each rate law into different categories (Xu, 2023). If a rate law does not belong to any of the default classes or the custom classification file provided, a warning will be raised.

The following categories are used for classifying rate laws:

- **Zeroth order (ZERO)**: No reactant or product in the rate law.
  - **Description**: These reactions proceed at a constant rate regardless of the concentration of reactants or products.
  - **Example**:

    ::

       A -> B; k
       A = 10
       B = 0
       k = 0.1

- **Uni-Directional Mass Action (UNDR)**: Direct, one-way reactions where all reactants influencing the rate law and resulting in a single product.
  - **Description**: These reactions follow the law of mass action for reactants.
  - **Example**:

    ::

       A + B -> C; k*A*B
       A = 10
       B = 5
       C = 0
       k = 0.01

- **Uni-Directional Mass Action with an Activator (UNDR-A)**: Similar to UNDR but includes an essential activator.
  - **Description**: These reactions are influenced by the presence of an activator.
  - **Example**:

    ::

       A + B -> C; k*A*B*Activator
       A = 10
       B = 5
       C = 0
       Activator = 2
       k = 0.01

- **Bi-Directional Mass Action (BIDR)**: Covers reversible reactions with all reactants and products in the rate law.
  - **Description**: These reactions are reversible and follow the law of mass action.
  - **Example**:

    ::

       A + B -> C + D; k1*A*B - k2*C*D
       A = 10
       B = 5
       C = 2
       D = 1
       k1 = 0.01
       k2 = 0.005

- **Bi-Directional Mass Action with Activator(s) (BIDR-A)**: Reversible reactions with activators, including enzymes different from reactants and products.
  - **Description**: These reactions are reversible and influenced by activators or enzymes.
  - **Example**:

    ::

       A + B -> C + D; k1*A*B*Activator - k2*C*D
       A = 10
       B = 5
       C = 2
       D = 1
       Activator = 2
       k1 = 0.01
       k2 = 0.005

- **Michaelis-Menten (MM)**: Describes enzymatic reactions based on substrate concentration, following specific Michaelis-Menten formulas without explicitly mentioning the enzyme.
  - **Description**: These reactions follow Michaelis-Menten kinetics.
  - **Example**:

    ::

       S => P; Vmax*S/(Km + S)
       E = 1
       S = 10
       P = 0
       Vmax = 1
       Km = 5

- **Michaelis-Menten with explicit enzyme (MMcat)**: Michaelis-Menten model explicitly incorporating the enzyme in the reaction rate equation.
  - **Description**: These reactions explicitly include the enzyme in the Michaelis-Menten kinetics.
  - **Example**:

    ::

       S => P; Vmax*E*S/(Km + S)
       E = 1
       S = 10
       P = 0
       Vmax = 1
       Km = 5

- **Allosteric and Inhibitors**: Michaelis-Menten format affected by allosteric effects or inhibitors, altering reaction rates through enzyme or substrate modulation.
  - **Description**: These reactions are influenced by allosteric modulators or inhibitors.
  - **Example**:

    ::

       S => P; Vmax*S/(S + Km*(1 + Inhibitor/Ki))
       E = 1
       S = 10
       P = 0
       Inhibitor = 2
       Vmax = 1
       Km = 5
       Ki = 2

- **Reversible Michaelis-Menten**: Accounts for reaction reversibility in Michaelis-Menten format.
  - **Description**: These reactions are reversible and follow Michaelis-Menten kinetics.
  - **Example**:

    ::

       S => P; (Vf*S - Vr*P)/(Km + S)
       E = 1
       S = 10
       P = 0
       Vf = 1
       Vr = 0.5
       Km = 5

- **Hill Equation**: Describes enzyme kinetics in cooperative binding scenarios, relating reaction rate to substrate concentration through a sigmoidal curve.
  - **Description**: These reactions follow the Hill equation, describing cooperative binding.
  - **Example**:

    ::

       S => P; Vmax*S^n/(Kd^n + S^n)
       S = 10
       Vmax = 1
       Kd = 5
       n = 2

The details of the default rate law classifications can be found in the `source code`_.

.. _source code: https://github.com/sys-bio/ratesb_python/tree/main/ratesb_python/common
