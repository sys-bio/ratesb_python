Errors and Warnings
===================

`ratesb_python` generates detailed errors and warnings to help you ensure your models are robust and accurate.

### Errors
- **0001**: No rate law entered
- **0002**: Expecting reactant in rate law but not found

### Warnings
#### Common Warnings
- **1001**: Rate law contains only number
- **1002**: Unrecognized rate law from the standard list (and the custom list if given)
- **1003**: Flux is not increasing as reactant increases
- **1004**: Flux is not decreasing as product increases
- **1005**: Expecting boundary species reactant in rate law but not found
- **1006**: Expecting parameters to be constants

#### Reversibility
- **1010**: Irreversible reaction kinetic law contains products

#### Naming Conventions
- **1020**: We recommend that these parameters start with 'k'
- **1021**: We recommend that these parameters start with 'K'
- **1022**: We recommend that these parameters start with 'V'

#### Formatting Conventions
- **1030**: Elements of the same type are not ordered properly
- **1031**: Formatting convention not followed (compartment before parameters before species)
- **1032**: Denominator not in alphabetical order
- **1033**: Numerator and denominator not in alphabetical order
- **1034**: Numerator convention not followed and denominator not in alphabetical order
- **1035**: Denominator convention not followed
- **1036**: Numerator not in alphabetical order and denominator convention not followed
- **1037**: Numerator and denominator convention not followed

#### SBOTerm Annotations
- **1040**: Uni-directional mass action annotation not following recommended SBO terms
- **1041**: Uni-term with the moderator annotation not following recommended SBO terms
- **1042**: Bi-directional mass action or Bi-terms with the moderator annotation not following recommended SBO terms
- **1043**: Michaelis-Menten kinetics without an explicit enzyme annotation not following recommended SBO terms
- **1044**: Michaelis-Menten kinetics with an explicit enzyme annotation not following recommended SBO terms

For more details about warnings and errors, please refer to "View Error Codes" button in `RateSB`_.

.. _RateSB: https://sys-bio.github.io/ratesb/
