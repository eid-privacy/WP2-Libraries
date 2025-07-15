**Repository**: https://github.com/zkcrypto/bulletproofs
**Language:** Rust
**License**: MIT

**Features:**

- Single and aggregated range proofs
- Multi-party computation for rangeproof aggregation
- Programmable constraint system API (experimental)
- Uses Ristretto and curve25519-dalek **note: this is pretty restrictive**

**Additional Information:**

- Fastest Bulletproofs implementation
- 2x faster verification than libsecp256k1-based implementation
- Uses Merlin transcripts for proof composition
- Experimental yoloproofs feature for R1CS API
- Requires nightly Rust
- AVX2 backend support for improved performance
