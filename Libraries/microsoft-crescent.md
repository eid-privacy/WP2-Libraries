**Repository**: https://github.com/microsoft/crescent-credentials  
**Paper**: https://eprint.iacr.org/2024/2013.pdf  
**Announcement**: https://www.microsoft.com/en-us/research/blog/crescent-library-brings-privacy-to-digital-identity-systems/  
**Language:** Rust  
**License**: Apache-2.0

**Summary**

Crescent is a library to generate proofs of possession of JSON Web
Tokens (JWT) and mobile Driver's Licenses (mDL) credentials.
By creating a proof for a JWT or mDL, rather than sending it directly,
the credential holder may choose to keep some of the claims in the
credential private, while still providing the verifier with assurance
that the revealed claims are correct and that the underlying credential
is still valid.
