Check Reference
===============

This section provides detailed references for all checks performed by `ratesb_python`, including examples to help you understand each check, why it is important, and under what circumstances users might encounter these errors and warnings.
`ratesb_python` generates detailed errors and warnings to help you ensure your models are robust and accurate. Below are all the checks, categorized as errors and warnings, along with examples illustrating common mistakes that trigger these checks.

Errors
~~~~~~
- **0001: No rate law entered**
  - **Description**: This error occurs when a reaction in the model does not have an associated rate law.
  - **Example**: If a reaction "A -> B" is defined without specifying a rate law, this error will be raised.
  - **Solution**: Ensure that every reaction in your model has a defined rate law, such as "A -> B; k*A".

- **0002: Expecting reactant in rate law but not found**
  - **Description**: This error is triggered when a rate law is expected to include a reactant, but the reactant is missing.
  - **Example**: For the reaction "A -> B", if the rate law is defined as "k", this error will be raised because "A" is expected in the rate law.
  - **Solution**: Include the reactant in the rate law, for example, "A -> B; k*A".

Common Warnings
~~~~~~~~~~~~~~~
- **1001: Rate law contains only number**
  - **Description**: A rate law consisting of only a number is flagged because it implies a constant flux, which might not be realistic.
  - **Example**: "A -> B; 5" where "5" is a constant number.
  - **Solution**: Use a more realistic rate law that includes reactants or parameters, like "A -> B; k*A".

- **1002: Unrecognized rate law from the standard list (and the custom list if given)**
  - **Description**: This warning indicates that the rate law does not match any recognized patterns from the standard or custom classification lists.
  - **Example**: An unusual or incorrectly formatted rate law.
  - **Solution**: Check the rate law for typos or incorrect formats and ensure it matches recognized patterns.

- **1003: Flux is not increasing as reactant increases**
  - **Description**: This warning suggests that the rate law does not appropriately reflect that the flux should increase with increasing reactant concentration.
  - **Example**: "A -> B; k" without the reactant "A" in the rate law.
  - **Solution**: Modify the rate law to include the reactant, like "A -> B; k*A".

- **1004: Flux is not decreasing as product increases**
  - **Description**: Indicates that the rate law does not account for the product concentration's influence on the reaction rate.
  - **Example**: "A -> B; k*A" without considering the product "B".
  - **Solution**: Adjust the rate law to reflect the product's influence, if applicable.

- **1005: Expecting boundary species reactant in rate law but not found**
  - **Description**: This warning is raised when a boundary species is expected in the rate law but is missing.
  - **Example**: For a reaction involving a boundary species "S", if the rate law does not include "S", this warning is triggered.
  - **Solution**: Include the boundary species in the rate law.

- **1006: Expecting parameters to be constants**
  - **Description**: Parameters in the rate law should be constants, and this warning is triggered if they are not.
  - **Example**: Using a variable instead of a constant parameter.
  - **Solution**: Ensure all parameters in the rate law are constants.


Reversibility
~~~~~~~~~~~~~
- **1010: Irreversible reaction kinetic law contains products**
  - **Description**: This warning indicates that an irreversible reaction's rate law incorrectly includes products.
  - **Example**: "A <-> B; k1*A - k2*B" for an irreversible reaction.
  - **Solution**: Remove the product term from the rate law for irreversible reactions.

Naming Conventions
~~~~~~~~~~~~~~~~~~
- **1020: We recommend that these parameters start with 'k'**
  - **Description**: Suggests following the naming convention for parameters to start with 'k'.
  - **Example**: Parameter named "rate" instead of "k_rate".
  - **Solution**: Rename the parameter to follow the convention, like "k_rate".

- **1021: We recommend that these parameters start with 'K'**
  - **Description**: Suggests following the naming convention for parameters to start with 'K'.
  - **Example**: Parameter named "dissociation" instead of "K_dissociation".
  - **Solution**: Rename the parameter to follow the convention, like "K_dissociation".

- **1022: We recommend that these parameters start with 'V'**
  - **Description**: Suggests following the naming convention for parameters to start with 'V'.
  - **Example**: Parameter named "max_rate" instead of "V_max_rate".
  - **Solution**: Rename the parameter to follow the convention, like "V_max_rate".

Formatting Conventions
~~~~~~~~~~~~~~~~~~~~~~
- **1030: Elements of the same type are not ordered properly**
  - **Description**: Elements in the rate law should be ordered properly.
  - **Example**: "k*B*A" instead of "k*A*B".
  - **Solution**: Order the elements properly, like "k*A*B".

- **1031: Formatting convention not followed (compartment before parameters before species)**
  - **Description**: Suggests following the convention of placing compartments before parameters before species in the rate law.
  - **Example**: "A*k*compartment" instead of "compartment*k*A".
  - **Solution**: Reformat the rate law to follow the convention.

- **1032: Denominator not in alphabetical order**
  - **Description**: Terms in the denominator should be in alphabetical order.
  - **Example**: "k/(B*A)" instead of "k/(A*B)".
  - **Solution**: Order the terms alphabetically, like "k/(A*B)".

- **1033: Numerator and denominator not in alphabetical order**
  - **Description**: Both numerator and denominator should have terms in alphabetical order.
  - **Example**: "k*A/B" instead of "k*A/B".
  - **Solution**: Ensure both numerator and denominator terms are ordered alphabetically.

- **1034: Numerator convention not followed and denominator not in alphabetical order**
  - **Description**: Both numerator and denominator conventions are not followed.
  - **Example**: "k*B/A*C" instead of "k*A/B*C".
  - **Solution**: Follow the proper conventions for both numerator and denominator.

- **1035: Denominator convention not followed**
  - **Description**: Suggests following the convention for terms in the denominator.
  - **Example**: Incorrect ordering or inclusion of terms in the denominator.
  - **Solution**: Adjust the denominator to follow the convention.

- **1036: Numerator not in alphabetical order and denominator convention not followed**
  - **Description**: Both numerator and denominator conventions are not followed.
  - **Example**: Incorrect ordering or inclusion of terms in both numerator and denominator.
  - **Solution**: Adjust both numerator and denominator to follow the conventions.

- **1037: Numerator and denominator convention not followed**
  - **Description**: Suggests following conventions for both numerator and denominator.
  - **Example**: Incorrect ordering or inclusion of terms.
  - **Solution**: Follow the conventions for both numerator and denominator.

SBOTerm Annotations
~~~~~~~~~~~~~~~~~~~
- **1040: Uni-directional mass action annotation not following recommended SBO terms**
  - **Description**: The annotation for uni-directional mass action does not follow recommended SBO terms.
  - **Example**: Incorrect SBO term used for uni-directional mass action.
  - **Solution**: Use the recommended SBO term for uni-directional mass action.

- **1041: Uni-term with the moderator annotation not following recommended SBO terms**
  - **Description**: The annotation for uni-term with a moderator does not follow recommended SBO terms.
  - **Example**: Incorrect SBO term used for uni-term with a moderator.
  - **Solution**: Use the recommended SBO term for uni-term with a moderator.

- **1042: Bi-directional mass action or Bi-terms with the moderator annotation not following recommended SBO terms**
  - **Description**: The annotation for bi-directional mass action or bi-terms with a moderator does not follow recommended SBO terms.
  - **Example**: Incorrect SBO term used for bi-directional mass action or bi-terms with a moderator.
  - **Solution**: Use the recommended SBO term for bi-directional mass action or bi-terms with a moderator.

- **1043: Michaelis-Menten kinetics without an explicit enzyme annotation not following recommended SBO terms**
  - **Description**: The annotation for Michaelis-Menten kinetics without an explicit enzyme does not follow recommended SBO terms.
  - **Example**: Incorrect SBO term used for Michaelis-Menten kinetics without an explicit enzyme.
  - **Solution**: Use the recommended SBO term for Michaelis-Menten kinetics without an explicit enzyme.

- **1044: Michaelis-Menten kinetics with an explicit enzyme annotation not following recommended SBO terms**
  - **Description**: The annotation for Michaelis-Menten kinetics with an explicit enzyme does not follow recommended SBO terms.
  - **Example**: Incorrect SBO term used for Michaelis-Menten kinetics with an explicit enzyme.
  - **Solution**: Use the recommended SBO term for Michaelis-Menten kinetics with an explicit enzyme.
For more details about warnings and errors, please refer to the "View Error Codes" button in `RateSB`_.

.. _RateSB: https://sys-bio.github.io/ratesb/