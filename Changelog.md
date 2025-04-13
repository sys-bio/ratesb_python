# Changelog

All notable changes to this project will be documented in this file.

## [0.2.7] - Previous
- Supported Local Parameters in SBML

## [0.2.6]
- Created ReadTheDocs
- Bug fixes
- Improved test coverage to 99%
- Supressed python 3.12 string warning

## [0.2.5]
- Separated model reading from analysis
- Tested on 1054 biomodels and fixed bugs
- Added check_model method to allow users to use the package with one line
- Solved issue with running sympy with built-in symbols such as "S"

## [0.2.4]
- Updated instructions in README

## [0.2.3]
- Included .json files
- Fixed path finding issue

## [0.2.2]
- Bug fixes
- Created GitHub workflow for CI

## [0.2.1]
- Removed Analyzer.check()
- Added get_all_checks() to get info about all checks
- Improved testing to full coverage except for trivial ones
- Improved exception messages
- Allowed string of Antimony or SBML model as input
- Simplified the import statement
- Revised existing and added new method and class comments

## [0.2.0]
- Removed numpy dependency
- Updated rate law classification scheme
- No longer using SBMLKinetics for rate law classifications
- Restructured code for web integration

## [0.1.0]
- Initial release
- Used SBMLKinetics for rate law classifications

---

For the latest release notes, check the [GitHub Releases](https://github.com/sys-bio/ratesb_python/releases).
