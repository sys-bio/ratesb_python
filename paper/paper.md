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

Mechanistic models in systems biology are essential tools for simulating and understanding the intricacies of complex biological systems, and a wide variety of rate laws are used. One commonly used rate law is *mass action* in which the reaction rate is proportional to the product of the concentrations of the reactants. To illustrate, consider a reaction in which $m$ molecules of $A$ combine with $n$ molecules of $B$ to produce $r$ molecules of $C$, or $m A + n B \rightarrow r C$. The mass action rate law is $k*[A]^m*[B]^n$, where $[x]$ is the concentration of $x$ and $k$ is a constant.

The  `ratesb_python` package evaluates rate laws against a library of predefined types to identify anomalies that may compromise the accuracy of mechanistic models. This process involves categorizing rate laws based on their mathematical characteristics and examining their performance within the context of the model. Such analysis enables `ratesb_python` to identify potential errors and warnings, including discrepancies in reactant usage or abnormal reaction fluxes. For example, if the rate law provided for the reaction $2 H_2 + O_2 \rightarrow 2 H_2O$ is $k_1 [H_2]^2 [O_2] [H_2O]^2$ (where $k_1$ is a constant), ``ratesb_python`` reports an error since there is no defined classification for the rate law since the products are included ($[H_2O]$).

# Software Description

`ratesb_python` analyzes rate laws to detect errors and warns about violations of best practices. Input to ``ratesb_python`` can be a file path to a model in the SBML or Antimony [@Smith2009] formats, or a string in the Antimony format. The output is text and/or Python objects. Control over inputs and outputs is managed by ``analyzer.py``.

Central to ``ratesb_python`` is the ability to classify rate laws according to widely used types such as: mass action, Michaelis-Menten, and zeroth order kinetics. ``ratesb_python`` relies heavily on approaches employed in SBMLKinetics [@Xu2023], which uses the ``sympy`` package to do symbolic analysis of rate laws. `ratesb_python` refines and extends these approaches to increase the accuracy of classification and to improve performance.

This functionality is complemented by `custom_classifier.py`, which offers users the flexibility to define and classify rate laws via a structured JSON format. This adaptability is crucial for tailoring the tool to specific research requirements, highlighting `ratesb_python`'s commitment to user-defined customization. Default classifications are detailed in `default_classifier.json`.

Error and warning messages generated during the analysis are systematically managed within `messages.json`, ensuring users are well-informed of any issues detected during the examination process. The results of these analyses are succinctly presented through the `Results` class in `results.py`, providing users with a clear description of the findings. Here is a summary of the error and warning codes along with their descriptions:

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


# Integration with Other Tools and API Capabilities

`ratesb_python` is designed as a flexible, modular API and standalone tool, enabling integration with various systems biology tools to facilitate rate law analysis in biological modeling projects. Its development in ``Python`` ensures compatibility with prevalent scientific computing tools, allowing it to be added to existing systems or tailored for specific applications. It works well with tools that are widely used in the SBML community, such as ``libantimony`` and ``libsbml``. Additionally, `ratesb_python` serves an educational purpose, offering a practical tool for computational biology courses where students can learn about rate law analysis by interacting with and modifying the API.

# Future Work

Future developments for `ratesb_python` include enriching the library of checks and optimizing the performance of classification algorithms. The goal is to expand the tool's capabilities, making it a more comprehensive resource for developers and researchers alike, and to introduce customization options for error and warning management, further enhancing its utility in systems biology.

---
bibliography: paper.bib
---
