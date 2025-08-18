---
title: 'ratesb_python: A Python Package for Analyzing Rate Laws in Biological Models'
tags:
  - Python
  - SBML
  - Systems Biology
  - Kinetics
  - Rate Laws
authors:
  - name: Longxuan Fan
    orcid: 0009-0006-6523-8302
    affiliation: 1
  - name: Joseph L. Hellerstein
    affiliation: 2
  - name: Herbert M. Sauro
    affiliation: 3
affiliations:
  - name: Viterbi School of Engineering, University of Southern California, 3650 McClintock Avenue, Los Angeles, CA 90089, United States of America
    index: 1
  - name: eScience Institute, University of Washington, 3910 15th Ave NE, Seattle, WA 98195, United States of America
    index: 2
  - name: Department of Bioengineering, University of Washington, 3720 15th Ave NE, Seattle, WA 98195, United States of America
    index: 3
date: 14 October 2024
bibliography: paper.bib
---

# Summary

`ratesb_python` is a Python package that analyzes mechanistic models of biological systems that consist of networks of chemical reactions like $2 H_2 + O_2 \rightarrow 2 H_2O$ [with rate laws such as $k [h_2]^2 [O_2]$ that describe the rate at which the reaction proceeds]. The package focuses on rate laws of reactions, algebraic expressions that specify the rate at which reactants (e.g., $H_2, O_2$) are converted into products (e.g., $O_2$). ``ratesb_python`` analyzes rate laws to detect errors and warnings that affect the robustness and accuracy of models that use the SBML (Systems Biology Markup Language) community standard for model model descriptions [@Hucka2003].

# Statement of Need

Mechanistic models in systems biology are essential tools for simulating and understanding the intricacies of complex biological systems, and a wide variety of rate laws are used. One commonly used rate law is *mass action* in which the reaction rate is proportional to the product of the concentrations of the reactants. To illustrate, consider a reaction in which $m$ molecules of $A$ combine with $n$ molecules of $B$ to produce $r$ molecules of $C$, or $m A + n B \rightarrow r C$. The mass action rate law is $k\times[A]^m\times[B]^n$, where $[x]$ is the concentration of $x$ and $k$ are constants.

The  `ratesb_python` package evaluates rate laws against a library of predefined types to identify anomalies that may compromise the accuracy of mechanistic models. This process involves categorizing rate laws based on their mathematical characteristics and examining their performance within the context of the model. Such analysis enables `ratesb_python` to identify potential errors and warnings, including discrepancies in reactant usage or abnormal reaction fluxes. For example, if the rate law provided for the reaction $2 H_2 + O_2 \rightarrow 2 H_2O$ is $k_1 [H_2]^2 [O_2] [H_2O]^2$ (where $k_1$ is a constant), ``ratesb_python`` reports an error since there is no defined classification for the rate law since the products are included ($[H_2O]$).

Moreover, `ratesb_python` extends beyond symbolic comparisons employed by existing tools (such as SBMLKinetics [@Xu2023]) by providing a **modular and extensible classification framework** that supports both predefined and user-defined rate laws. While symbolic methods rely on hardcoded heuristics and expensive algebraic simplification, ratesb_python introduces a structured approach that separates normalization (e.g., power-lowering, constant removal) from classification, enabling more consistent and accurate results. More importantly, the algorithm is not restricted to a set of pre-coded equations, thereby enabling more flexible customization: users can readily define their own rate laws and instruct `ratesb_python` to check whether a provided rate law matches a generalized or custom-defined functional form. This functionality is especially beneficial for researchers who need to handle specialized or novel rate laws that do not necessarily fit the standard templates.

In simple scenearios-such as a Michaelis-Menten rate law $cell \times M \times V / (K + M)$ (where $V$ and $K$ are constants, $M$ is the reactant, and $cell$ is the compartment) with one reactant and no products, both `ratesb_python` and symbolic methods produce similar outcomes. However, for more complex rate laws, such as a reversible Michaelis-Menten formulation. However, in more complex examples like a reversible michaelis menten rate law: $$cell \times (V_{\mathit{max}} / K_{\mathit{m1}}) \times (S - P / K_{\mathit{eq}}) / (1 + S / K_{\mathit{m1}} + P / K_{\mathit{m2}})$$ (constants: $V_{\mathit{max}}$, $K_{\mathit{m1}}$, $K_{\mathit{eq}}$, $K_{\mathit{m1}}$, $K_{\mathit{m2}}$; reactant: $S$; product: $P$; compartment: $cell$), symbolic methods often default to generic classifications, while `ratesb_python` maintains accuracy. This demonstrates that the package is particularly valuable for ensuring stability and correctness in real-world, biologically meaningful models.

In practice, this structured design makes `ratesb_python` less prone to misclassification in complex biological models. For example, in our benchmark comparison (see Experimental Comparison), `ratesb_python` correctly identified reversible Michaelis-Menten kinetics as RMM and RMMcat, whereas SBMLKinetics defaulted to the generic form FR. Similarly, for bidirectional mass-action variants, `ratesb_python` distinguished structurally distinct cases (BIDR21, BIDR11), while symbolic methods collapsed them into the same generic class (BIDR). These results highlight that, although runtime may vary across examples, `ratesb_python` consistently produces specific and accurate classifications, especially in cases where symbolic approaches lose detail. By emphasizing robustness and adaptability, the package enhances confidence in model correctness, which is often more critical than raw execution speed in systems biology workflows.

# Software Description

`ratesb_python` analyzes rate laws to detect errors and warns about violations of best practices. Input to `ratesb_python` can be a file path to a model in the SBML or Antimony [@Smith2009] formats, or a string in the Antimony format. The output is text and/or Python objects. Control over inputs and outputs is managed by ``analyzer.py``.

Central to ``ratesb_python`` is the ability to classify rate laws according to widely used types such as: mass action, Michaelis-Menten, and zeroth order kinetics. ``ratesb_python`` relies heavily on approaches employed in SBMLKinetics [@Xu2023], which uses the ``sympy`` package to do symbolic analysis of rate laws. However, `ratesb_python` refines and extends these approaches by using a randomized polynomial identity test, providing a more efficient and customizable framework for classifying rate laws. This functionality is complemented by `custom_classifier.py`, which offers users the flexibility to define and classify rate laws via a structured JSON format. This adaptability is crucial for tailoring the tool to specific research requirements, highlighting `ratesb_python`'s commitment to user-defined customization. Default classifications are detailed in `default_classifier.json`.

Error and warning messages generated during the analysis are systematically managed within `messages.json`, ensuring users are well-informed of any issues detected during the examination process. The results of these analyses are succinctly presented through the `Results` class in `results.py`, providing users with a clear description of the findings. 

**Error Code Rationale and Organization**  
`ratesb_python` employs *grouped error codes* to systematically guide users in identifying and addressing issues with rate law classification. This ensures that common issues (e.g., missing reactants, invalid product usage, or typographical mistakes) are clearly distinguished from more severe problems (e.g., completely undefined rate laws). The codes also serve developers by providing a standardized mechanism for adding new checks or extending existing ones. Detailed explanations of these codes, along with examples, can be found both in the `messages.json` file and in the [official documentation](https://longxf-ratesb-python.readthedocs-hosted.com/en/latest/). By grouping related issues under specific ranges of codes, `ratesb_python` makes it easier for users to trace potential errors to their underlying causes and for developers to introduce new error or warning categories without breaking the existing structure.

Below is a summary of the error and warning codes along with their brief descriptions:

+------------+---------+---------------------------------------------------------------+
| Code       | Type    | Brief Description                                             |
|            |         |                                                               |
+:==========:+:=======:+:=============================================================:+
| 1-2        | Errors  | Issues with missing rate laws or expected reactants.          |
+------------+---------+---------------------------------------------------------------+
| 1001       | Warning | Numeric-only rate law.                                        |
+------------+---------+---------------------------------------------------------------+
| 1002       | Warning | Rate law unrecognized.                                        |
+------------+---------+---------------------------------------------------------------+
| 1003-1004  | Warning | Flux relationship issues with reactants and products.         |
+------------+---------+---------------------------------------------------------------+
| 1005       | Warning | Missing boundary species reactant.                            |
+------------+---------+---------------------------------------------------------------+
| 1006       | Warning | Non-constant parameters in rate law.                          |
+------------+---------+---------------------------------------------------------------+
| 1010       | Warning | Products in irreversible reaction rate law.                   |
+------------+---------+---------------------------------------------------------------+
| 1020-1022  | Warning | Naming conventions for parameters not followed.               |
+------------+---------+---------------------------------------------------------------+
| 1030-1037  | Warning | Issues with ordering and formatting conventions in rate laws. |
+------------+---------+---------------------------------------------------------------+
| 1040-1044  | Warning | Annotations not following recommended SBO terms.              |
+============+=========+===============================================================+
| Error and warning messages to aid in rate law analysis.                              |
+======================================================================================+

# Experimental Comparison

To evaluate classification correctness and stability, we compared `ratesb_python` against `SBMLKinetics` on a curated benchmark of eight representative SBML models, covering common rate law types such as mass action, Michaelis-Menten, and reversible kinetics. Each model was analyzed using both tools, and we recorded the classification results and execution time. The results are summarized below:

+----------------------------+------------------+------------------+----------------+----------------+
| Model                      | RatesB Time (s)  | SBMLK Time (s)   | RatesB Class   | SBMLK Class    |
+:==========================:+:================:+:================:+:==============:+:==============:+
| bidirectional_bidr21.xml   | 0.08692          | 0.01483          | **BIDR21**     | **BIDR**       |
+----------------------------+------------------+------------------+----------------+----------------+
| bidirectional_bidr_a11.xml | 0.02487          | 0.01403          | **BIDR11**     | **BIDR**       |
+----------------------------+------------------+------------------+----------------+----------------+
| mass_action_undr1.xml      | 0.00531          | 0.01044          | **UNDR1**      | **UNDR**       |
+----------------------------+------------------+------------------+----------------+----------------+
| mass_action_undr2.xml      | 0.01189          | 0.01087          | **UNDR2**      | **UNDR**       |
+----------------------------+------------------+------------------+----------------+----------------+
| michaelis_menten_mm.xml    | 0.14586          | 0.01429          | **MM**         | **MM**         |
+----------------------------+------------------+------------------+----------------+----------------+
| michaelis_menten_mmcat.xml | 0.16496          | 0.06787          | **MM**         | **MM**         |
+----------------------------+------------------+------------------+----------------+----------------+
| reversible_mm_rmm.xml      | 0.22132          | 1.23374          | **RMM**        | _FR_           |
+----------------------------+------------------+------------------+----------------+----------------+
| reversible_mm_rmmcat.xml   | 0.28556          | 0.02395          | **RMMcat**     | _FR_           |
+============================+==================+==================+================+================+
| Comparative classification and timing results for `ratesb_python` and `SBMLKinetics`.              |
+====================================================================================================+

Correct classifications are shown in bold, while incorrect or generic classifications are shown in italics.

These results show that while execution time varies depending on the example, the more important outcome is classification stability: `SBMLKinetics` often defaults to generic forms such as FR or fails to distinguish structurally distinct cases, whereas `ratesb_python` consistently produces specific and accurate classifications. This reliability is crucial when analyzing complex biological models, where correctness matters more than raw runtime. To further illustrate this point, future work will include visualizations (e.g., plotting correctness versus model complexity) to better capture the relationship between stability and model size. Scripts to reproduce this benchmark, including model files, wrapper code, and output summaries, are publicly available at the [Github Repository](https://github.com/sys-bio/ratesb_python/tree/main/benchmark) to ensure transparency and replicability.

# Integration with Other Tools and API Capabilities

`ratesb_python` is designed as a flexible, modular API and standalone tool, enabling integration with various systems biology tools to facilitate rate law analysis in biological modeling projects. Its development in ``Python`` ensures compatibility with prevalent scientific computing tools, allowing it to be added to existing systems or tailored for specific applications. It works well with tools that are widely used in the SBML community, such as ``libantimony`` and ``libsbml``. Additionally, `ratesb_python` serves an educational purpose, offering a practical tool for computational biology courses where students can learn about rate law analysis by interacting with and modifying the API.

# Future Work

Future developments for `ratesb_python` include enriching the library of checks, optimizing the performance of classification algorithms improving visualization of classification outcomes, and expanding the benchmark set to cover a broader spectrum of biologically relevant models. In particular, plotting classification correctness and stability against model complexity will provide a clearer picture of where existing tools struggle. Performance optimization of classification algorithms remains a secondary goal, but the primary focus is on strengthening correctness, robustness, and usability for researchers.

---
bibliography: paper.bib
---
