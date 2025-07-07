# DIDComm Open Source Libraries for SSI and E-ID Systems

First, let's understand the different components here:
- **DIDs** are the identifiers meant for a decentralized system.
- **DID Methods** are the rules for how those identifiers are created and used.
- **DIDComm** is the protocol that uses DIDs (from any method) to send secure messages between parties.

DIDComm is **agnostic to the DID method**—it works with any DID as long as the method supports the necessary cryptographic operations and endpoint discovery[4][6].

Here is a table summarizing the **differences between DIDComm, DID, and DID method**:

| Concept      | What It Is | Role in SSI/E-ID | Example | Relationship to Others |
|--------------|------------|------------------|---------|-----------------------|
| **DID** (Decentralized Identifier) | A globally unique identifier, such as `did:example:123456789abcdefghi` | Identifies an entity (person, org, device) in a decentralized way | `did:web:example.com` | Used as the address for secure communication and as the anchor for public keys and service endpoints |
| **DID Method** | A specification describing how a specific type of DID is created, resolved, updated, and deactivated | Defines how the DID works on a particular system or blockchain | `web`, `peer`, `ion`, `ebsi`, etc. | Each DID includes a method, e.g., `did:web:`, `did:peer:`, and the method determines how to interpret and manage that DID |
| **DIDComm** | A secure messaging protocol built on top of DIDs | Enables encrypted, private, end-to-end communication between entities identified by DIDs | Secure message exchange between Alice and Bob’s agents | Uses DIDs for addressing and keys; works with any DID method that supports required features |

### DIDComm v2 Library Ecosystem
The DIDComm v2 ecosystem has matured significantly, with **SICPA** being the primary contributor of cross-platform libraries, having made substantial **open source contributions** to both the **Hyperledger Foundation** and **OpenWallet Foundation**[1][2]. These libraries support the latest DIDComm v2 specification from the **Decentralized Identity Foundation**.
### Comprehensive Library Overview
#### **Core DIDComm v2 Libraries**

| Library                                                                    | Language    | Organization | Key Features                                                              |
|----------------------------------------------------------------------------|-------------|--------------|---------------------------------------------------------------------------|
| **[DIDComm Python](https://github.com/sicpa-dlab/didcomm-python)**         | Python      | SICPA        | Basic DIDComm v2 support, encryption, signing, peer-to-peer communication |
| **[DIDComm Rust](https://github.com/sicpa-dlab/didcomm-rust)**             | Rust        | SICPA        | Core implementation with WASM bindings for JS/TS and Swift wrappers       |
| **[DIDComm JavaScript/TypeScript](https://www.npmjs.com/package/didcomm)** | JS/TS       | SICPA        | WASM-based, browser and NodeJS compatible                                 |
| **[DIDComm JVM](https://github.com/sicpa-dlab/didcomm-jvm)**               | Java/Kotlin | SICPA        | Android support, multiple message formats                                 |
| **[DIDComm Swift](https://github.com/beatt83/didcomm-swift)**              | Swift       | beatt83      | Native iOS support, advanced routing capabilities                         |

#### **Enterprise & Framework Integration**

| Library                                                                                      | Language   | Organization          | Focus                                                        |
|----------------------------------------------------------------------------------------------|------------|-----------------------|--------------------------------------------------------------|
| **[Aries Cloud Agent Python](http://github.com/openwallet-foundation/acapy)**                | Python     | Hyperledger           | Enterprise agent framework with DIDComm v2 envelope handling |
| **[DIDComm Mediator Credo](http://github.com/openwallet-foundation/didcomm-mediator-credo)** | TypeScript | OpenWallet Foundation | Mediator services, message pickup protocols                  |
| **[Veramo DIDComm](https://github.com/decentralized-identity/veramo)**                       | TypeScript | Veramo Team           | Used in MetaMask plugin, SSI framework integration           |

### Key Technical Features

These libraries provide comprehensive support for:

- **Message Security**: End-to-end encryption using ECDH-ES+A256KW and ECDH-1PU+A256KW protocols[5][6]
- **Authentication**: Both anonymous (AnonCrypt) and authenticated (AuthCrypt) messaging[12]
- **Transport Agnostic**: Support for HTTP, WebSocket, Bluetooth, NFC, and other transport protocols[3]
- **Key Management**: X25519, Ed25519, P-256, P-384, and P-521 curve support[5]
- **Message Routing**: Advanced routing through mediators for mobile and constrained environments[9]

### DID:webvh and E-ID System Compatibility
**DID:webvh** (formerly Trust DID Web) is a **complementary technology** that **enhances** rather than replaces DIDComm libraries[13][14]. Here's the relationship:

#### **DID:webvh Specific Libraries**

| Library                                                                           | Language   | Organization |
|-----------------------------------------------------------------------------------|------------|--------------|
| **[did:webvh TypeScript](https://github.com/decentralized-identity/didwebvh-ts)** | TypeScript | DIF          |
| **[did:webvh Python](https://github.com/decentralized-identity/trustdidweb-py)**  | Python     | DIF          |
| **[did:webvh Rust](https://lib.rs/crates/did-webvh)**                             | Rust       | Multiple     |
| **[did:webvh Go](https://github.com/nuts-foundation/trustdidweb-go)**             | Go         |      -       |

##  Github project lists
- https://github.com/decentralized-identity/didcomm-messaging