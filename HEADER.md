# WP2 Libraries and Protocols

Welcome to the WP2 Libraries and Protocols repository! This is a living documentation project that catalogs and evaluates cryptographic libraries, communication protocols, and related tools in the Electronic Identification (E-ID) and Self-Sovereign Identity (SSI) ecosystem.

## Purpose

This repository serves as a comprehensive reference for developers, researchers, and organizations working with digital identity systems. We systematically evaluate libraries and protocols based on multiple criteria to help you make informed decisions for your projects.

## Repository Structure

- **Libraries/** - Existing documentation of cryptographic libraries (legacy format)
- **Communication-Protocols/** - Existing protocol documentation (legacy format)
- **Structured tables/** - New YAML-based entries with quality evaluations (see below)

---

## How to Add a New Entry

Adding a new entry is simple! Follow these steps:

### 1. Choose the Appropriate Table Directory

Navigate to the directory that best fits your entry (e.g., `example-table/`). If you need to create a new category, contact the maintainers.

### 2. Create a YAML File

Create a new file named `<library-or-protocol-name>.yaml` in the table directory. Use kebab-case for the filename (e.g., `my-awesome-library.yaml`).

### 3. Fill in the Template

Use this template for your YAML file:

```yaml
# REQUIRED FIELDS
name: "Library or Protocol Name"
organization: "Organization Name"  # Use "Independent" if not associated with an org
url: "https://github.com/organization/repository"
language: "Primary Programming Language"
purpose: "Brief description of what this library/protocol does and its main use cases"

# OPTIONAL FIELDS
note: "Additional context, observations, or important information"

# EVALUATION CRITERIA (all required, integers 1-5)
evaluation_criteria:
  software_structure: 4          # Software Structure / Architecture / Design / Engineering
  unit_tests_ci_cd: 3            # Unit Tests & CI/CD
  license_ownership: 5           # License, ownership and access
  amenity_to_change: 4           # Amenity to change (Issues, PRs)
  documentation: 3               # Documentation quality
  probable_support: 4            # Probable support on the next 2-3 years
```

### 4. Commit and Push

Commit your new YAML file and push to a feature branch. Create a pull request to the `main` branch. The README will be automatically generated when your PR is merged.

### 5. Local Testing (Optional but Recommended)

Before committing, you can test the README generation locally:

```bash
# Generate README
python3 scripts/generate_readme.py --verbose

# Or use Make
make generate-readme

# Validate without generating
python3 scripts/generate_readme.py --validate-only
```

---

## Evaluation Criteria Guide

Each entry is evaluated on **6 criteria** using a scale of **1 to 5**, where:
- **5** = Excellent
- **4** = Good
- **3** = Adequate
- **2** = Poor
- **1** = Very Poor / Non-existent

The **Quality Score** displayed in the tables is the mean (average) of all 6 criteria.

### 1. Software Structure / Architecture / Design / Engineering

Evaluates the overall code quality, architectural decisions, and engineering practices.

- **5 - Excellent**: Well-organized codebase, clear separation of concerns, follows design patterns, modular and extensible
- **4 - Good**: Generally well-structured with minor inconsistencies, mostly follows best practices
- **3 - Adequate**: Basic organization present, some technical debt, could benefit from refactoring
- **2 - Poor**: Disorganized code, unclear structure, difficult to navigate
- **1 - Very Poor**: Spaghetti code, no clear architecture, severely difficult to understand or maintain

### 2. Unit Tests & CI/CD

Assesses test coverage, quality of tests, and continuous integration/deployment setup.

- **5 - Excellent**: Comprehensive test coverage (>80%), integration tests, automated CI/CD pipeline, tests run on multiple platforms
- **4 - Good**: Good test coverage (60-80%), CI/CD present, most critical paths tested
- **3 - Adequate**: Basic tests present (30-60%), some CI setup, major features covered
- **2 - Poor**: Minimal tests (<30%), sporadic or no CI, many untested areas
- **1 - Very Poor**: No tests or CI/CD whatsoever

### 3. License, Ownership and Access

Evaluates licensing clarity, intellectual property considerations, and accessibility.

- **5 - Excellent**: Open source with permissive license (MIT, Apache 2.0, BSD), clear contributor guidelines, no dependencies on proprietary components
- **4 - Good**: Open source with copyleft license (GPL, LGPL), mostly clear licensing, minimal proprietary dependencies
- **3 - Adequate**: Open source but unclear licensing on some components, some restrictions
- **2 - Poor**: Restrictive license, uncertain ownership, significant proprietary dependencies
- **1 - Very Poor**: Closed source, very restrictive license, or unclear/contested ownership

### 4. Amenity to Change (Issues, PRs)

Measures how actively maintained the project is and how responsive maintainers are to issues and pull requests.

- **5 - Excellent**: Very active maintenance, issues triaged within days, PRs reviewed and merged promptly, welcoming to contributors
- **4 - Good**: Regular maintenance, issues addressed within weeks, PRs reviewed reasonably quickly
- **3 - Adequate**: Occasional maintenance, issues may take months to address, some PRs merged
- **2 - Poor**: Rarely maintained, many stale issues and PRs, slow or no responses
- **1 - Very Poor**: Abandoned project, no response to issues/PRs, maintainers unreachable

### 5. Documentation

Assesses the quality and completeness of documentation.

- **5 - Excellent**: Comprehensive docs with tutorials, API reference, examples, architecture diagrams, up-to-date
- **4 - Good**: Good documentation covering most use cases, API reference present, some examples
- **3 - Adequate**: Basic documentation present, covers core functionality, may lack examples or be outdated
- **2 - Poor**: Minimal documentation, incomplete API reference, missing critical information
- **1 - Very Poor**: No documentation or only README with basic info

### 6. Probable Support on the Next 2-3 Years

Predicts the likelihood of continued maintenance and support.

- **5 - Excellent**: Backed by large organization, active community, clear roadmap, financial support evident
- **4 - Good**: Active community, regular releases, maintainers committed, stable funding/backing
- **3 - Adequate**: Moderate activity, maintainers present but limited, some uncertainty about future
- **2 - Poor**: Low activity, uncertain future, maintainers rarely active, no clear backing
- **1 - Very Poor**: Project appears abandoned or on life support, highly unlikely to be maintained

---

## How the Automation Works

This repository uses GitHub Actions to automatically generate the main README.md:

1. When you push changes to YAML files, `HEADER.md`, `FOOTER.md`, or table READMEs, a workflow triggers
2. The workflow runs `scripts/generate_readme.py` to validate all entries and generate tables
3. On the `main` branch: The updated README is automatically committed
4. On pull requests: The workflow validates your changes and fails if there are errors

The workflow **does not** trigger on README.md changes itself, preventing infinite loops.

---

## Tables of Entries

Below are the tables of evaluated libraries and protocols. Each table is organized by category and automatically generated from the YAML entry files.

