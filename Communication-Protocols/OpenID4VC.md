
## OpenID4VC
OpenID for Verifiable Credentials (OID4VC) is a family of protocols enabling secure issuance and presentation of verifiable credentials using OpenID Connect standards. The main specifications are OID4VCI (Credential Issuance), OID4VP (Verifiable Presentation), and SIOPv2 (Self-Issued OpenID Provider v2). Below is a curated list of prominent open source libraries supporting these protocols.

## OID4VCI (OpenID for Verifiable Credential Issuance)

| Library / Repo                                                                            | Language        | Roles Supported      | Description                                                          | Maturity                                |
|-------------------------------------------------------------------------------------------|-----------------|----------------------|----------------------------------------------------------------------|-----------------------------------------|
| [~~walt.id waltid-ssikit~~](https://github.com/walt-id/waltid-ssikit)                     | ~~Kotlin/Java~~ | ~~Wallet, Issuer~~   | ~~Comprehensive SSI toolkit supporting OID4VCI, OID4VP, and SIOPv2~~ | **Deprecated**                          |
| [SpruceID oidc4vci-rs](https://github.com/spruceid/oidc4vci-rs)                           | Rust            | Issuer               | Implements OID4VCI for credential issuance                           | Weakly documented                       |
| [~~SpruceID oidc4vci-issuer~~](https://github.com/spruceid/oidc4vci-issuer)               | ~~Rust~~        | ~~Issuer~~           | ~~OID4VCI issuer implementation~~                                    | **Deprecated**                          |
| [Sphereon OpenID4VCI](https://github.com/Sphereon-Opensource/OpenID4VCI)                  | TypeScript      | Wallet, Issuer       | SDK for OID4VCI flows                                                | Very well-documented and well developed |
| [TrustBloc wallet-sdk](https://github.com/trustbloc/wallet-sdk)                           | Go              | Wallet               | APIs for wallets to receive credentials via OID4VCI                  | Too high level                          |
| [TrustBloc vcs](https://github.com/trustbloc/vcs)                                         | Go              | Issuer, Verifier     | Verifiable Credential Service with OID4VCI and OID4VP support        | Too high level                          |
| [Authlete oid4vci-demo](https://github.com/authlete/oid4vci-demo)                         | Ruby            | Issuer               | Demo implementation for OID4VCI                                      | Demo                                    |
| [blockchain-lab-um/oid4vc-monorepo](https://github.com/blockchain-lab-um/oid4vc-monorepo) | TypeScript      | Issuer, Verifier, RP | Modular OID4VC implementation                                        | Example                                 |


## OID4VP (OpenID for Verifiable Presentations)

| Library / Repo                                                                            | Language        | Roles Supported      | Description                                  | Maturity                     |
|-------------------------------------------------------------------------------------------|-----------------|----------------------|----------------------------------------------|------------------------------|
| [~~walt.id waltid-ssikit~~](https://github.com/walt-id/waltid-ssikit)                     | ~~Kotlin/Java~~ | ~~Wallet, Verifier~~ | ~~Supports OID4VP and EBSI/ESSIF use cases~~ | Deprecated                   |
| [SpruceID openid4vp](https://github.com/spruceid/openid4vp)                               | Rust            | Verifier             | Rust implementation of OID4VP                | little to no documentation   |
| [~~Sphereon SIOP-OpenID4VP~~](https://github.com/Sphereon-Opensource/SIOP-OpenID4VP)      | ~~TypeScript~~  | ~~Wallet, Verifier~~ | ~~SIOPv2 and OID4VP support~~                | Deprecated                   |
| [Sphereon ssi-sdk](https://github.com/Sphereon-Opensource/ssi-sdk)                        | TypeScript      | Wallet, Verifier     | SDK with OID4VP and SIOPv2 support           | **NEEDS MORE REVIEW**        |
| [Microsoft VC-SDK-Android](https://github.com/microsoft/VerifiableCredential-SDK-Android) | Java            | Wallet               | Android SDK for VCs and OID4VP               | high level - well documented |
| [Microsoft VC-SDK-iOS](https://github.com/microsoft/VerifiableCredential-SDK-iOS)         | Swift           | Wallet               | iOS SDK for VCs and OID4VP                   | high level - well-documented |
| [TrustBloc wallet-sdk](https://github.com/trustbloc/wallet-sdk)                           | Go              | Wallet               | OID4VP support for credential presentation   | well-documented              |

## SIOPv2 (Self-Issued OpenID Provider v2)
Sometimes offered by other OID4VP libraries, but doesn't have its own library.
ToDo: How does this fit within the E-ID eco-system. Any usecases?

### OpenID4VP over BLE
This is an important specification that covers the Bluetooth Low Energy transport layer for transmitting Verifiable Credentials.  
However, there's no available implementations for it so far, except for this one [talk](https://fosdem.org/2025/schedule/event/fosdem-2025-6575-sample-implementation-of-openid-4-verifiable-presentation-over-bluetooth-low-energy/) from FOSDEM 2025

## Notable framework

| Library / Repo                                                 | Language   | Description                                                                   |
|----------------------------------------------------------------|------------|-------------------------------------------------------------------------------|
| **[Veramo](https://github.com/decentralized-identity/veramo)** | TypeScript | automates lots of processes. Could be a useful reference for SWIYU automation |


## Summary Table

| Library/Repo                                   | Language    | OID4VCI | OID4VP | SIOPv2 | Roles                    |
|------------------------------------------------|-------------|---------|--------|--------|--------------------------|
| walt.id waltid-ssikit                          | Kotlin/Java | ✔       | ✔      | ✔      | Wallet, Issuer, Verifier |
| SpruceID oidc4vci-rs                           | Rust        | ✔       |        |        | Issuer                   |
| SpruceID openid4vp                             | Rust        |         | ✔      |        | Verifier                 |
| Sphereon OpenID4VCI                            | TypeScript  | ✔       |        |        | Wallet, Issuer           |
| Sphereon SIOP-OpenID4VP                        | TypeScript  |         | ✔      | ✔      | Wallet, Verifier         |
| TrustBloc wallet-sdk                           | Go          | ✔       | ✔      |        | Wallet                   |
| TrustBloc vcs                                  | Go          | ✔       | ✔      |        | Issuer, Verifier         |
| Authlete oid4vci-demo                          | Ruby        | ✔       |        |        | Issuer                   |
| Microsoft VerifiableCredential-SDK-Android/iOS | Java/Swift  |         | ✔      | ✔      | Wallet                   |
| blockchain-lab-um/oid4vc-monorepo              | TypeScript  | ✔       | ✔      |        | Issuer, Verifier, RP     |
