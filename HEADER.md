# WP2 Libraries and Protocols

Welcome to the WP2 Libraries and Protocols repository! This is a living documentation project that catalogs and evaluates cryptographic libraries, communication protocols, and related tools in the Electronic Identification (E-ID) and Self-Sovereign Identity (SSI) ecosystem.

## Purpose

This repository serves as a comprehensive reference for developers, researchers, and organizations working with digital identity systems. We systematically evaluate libraries and protocols based on multiple criteria to help you make informed decisions for your projects.

## Deliverables - 2025-09-07

- D2.1 - Basic cryptographic libraries for the underlying mathematical
  - Done: [Libraries/](./Libraries) and the [Zero-Knowledge Libraries](#zero-knowledge-libraries) table below
- D2.2 - ZKP libraries
  - Done: [Zero-Knowledge Libraries](#zero-knowledge-libraries) table below
- D2.3 - ZKP circuit libraries
  - Done: [Zero-Knowledge Circuit Frameworks](#zero-knowledge-circuit-frameworks) table below
- G2.1 - The algorithms found in [WP1](https://github.com/eid-privacy/WP1-Algorithms) are represented in the libraries, or their absence is marked in the report.
  - Done: the libraries chosen for the proof-of-concepts, Docknetwork and Noir, are discussed in the
    [MS2 report](https://github.com/eid-privacy/MS2-Minimal-Viable-Project/releases/download/2026-10-22_13-38/eid_privacy-101.292-IP-ICT-ms2-report-2026-10-22_13-38.pdf), section _Frameworks used for our Proof-of-Concepts_.
    See also the blog posts
    [Resources on Zero-knowledge Systems and Proofs](https://eid-privacy.github.io/wp2/2025/09/17/privacy-enhancing-resources.html) and
    [Choosing a Cryptographic Library for Anonymous Credentials](https://eid-privacy.github.io/wp2/2026/01/27/docknetwork-crypto-library.html).
    Later related work is collected in [zkp-vault](https://github.com/eid-privacy/zkp-vault)

## Repository Structure

- **Libraries/** - Existing documentation of cryptographic libraries (legacy format)
- **Communication-Protocols/** - Existing protocol documentation (legacy format)
- **Structured tables/** - New YAML-based entries with quality evaluations (see below)

---

## Tables of Entries

Below are the tables of evaluated libraries and protocols. Each table is organized by category and automatically generated from the YAML entry files.
