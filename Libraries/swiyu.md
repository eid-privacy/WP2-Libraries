## swiyu - The Swiss E-ID ecosystem implementation

This file contains work notes on our demo project: https://github.com/eid-privacy/swiyu-demo

The goal of this project is to build an environment where we can test all the functionalities
supported by the SWIYU infrastructure.

### Project Summary

- We successfully managed to build a full practical demo based on the current open source libraries
  within the swiyu ecosystem (open-sourced by the swiyu team).
- We also incorporated Selective disclosure within the workflows.
- And based one of the workflows on swiyu's Beta ID which proves how easy it is to integrate
  this ecosystem.
- Two interesting point that need further investigation are:
  - Revokation which required an active OAuth2 token which requires a level of automation.
  - DID creation: the issuer/verifier onboarding process is a bit tedious, and probably needs
    some simplification or automation.

#### To-Do

-[x] added diploma VC -[x] added nginx proxy -[x] ported frontend of previous demo -[x] installed on eid.c4dt.org -[x] added verifier flow -[x] linked diploma credential with identity credential

## Weekly logs

### Week 18 - April 28th

**Tested the SWIYU application as a wallet holder**

- using this [SWIYU cookbook](https://swiyu-admin-ch.github.io/cookbooks/how-to-use-beta-id/)
  - Requested credential from [this PoC website](https://www.bcs.admin.ch/bcs-web/#/).
- Both Android and IOS applications are working on their respective stores.

### Remarks

- The process is a lot easier than before, specifically, the wallet holder only scans a QR code once, after the credential has been created.

- It’s unclear if the issuer is able in this case to issue other credentials to the holder without the holder scanning another QR code.
  - Indy: Connection is established first – very similar to a phone contact
  - SWIYU: QR code contains Credential information.

**Goal: Integrate our first E-ID testbed demo app (with Indy) with the new SWIYU infrastructure – Issuer workflow**

Steps:

1. Initial setup and creating a DID document
   - Followed the cookbook here
2. Install the backend for the issuer
   - Followed this cookbook here
   - Fill all environment variables coming from step 1
3. Make the server accessible from the local network
4. Connect with Wallet from phone

#### Remarks:

- Instructions were confusing and I had to repeat the process a couple of times.
- I wrote a script that helps reduce duplications but is still not automated fully.
- Backend had multiple issues:  
   Luckily, most of my issues have already been answered which helped a lot to move forward.

  _But it took a lot of time before connecting the problems I was facing with these on the list above._

At the end of this week, there’s a working backend that can issue credentials, but when creating the QR code, the SWIYU app doesn’t read it.

**Decision: based on last time experience, let’s use typescript to convert the credential offer link into a QR code that can be scanned from the browser.**

### Week 19 – May 5th

**Goal: Change the demo app to work with SWIYU**

1. Refactored the first couple of steps in the demo app to issue a credential to the new backend.
   - Now blocked by CORS
   - Injected QR code content directly, to circumvent CORS. However, app still rejects the credential.

2. Tried different configuration and tests with the app (android/ IOS), etc but to no avail.

#### Issues

- CORS remains an issue like the previous version, but it’s harder to fix because
  - The code is not available locally anymore.
  - Java spring is used which is not as easy to work with as Python/ Django.
  - I created a GitHub issue, and waiting for feedback

- Even with the QR code displayed from the demo app, it’s still being rejected by the app. Reason still unknown

#### Remarks:

- The workflow is very different between Indy and SWIYU, but SWIYU is obviously easier for the users.
- The app didn’t give a meaningful error message for rejecting QR code.
- SWIYU team made sure the backend services could be installed with a docker compose file and a .env file instead of the need to install the whole project.

**Decision: Cloning the IOS or the Android apps, and looking into the logs could help understand why the app rejects the QR code.**

### Week 20 – May 12th

**GOAL: Installing the mobile apps using sources (maybe using an emulator)**

**IOS:**

Many problems:

1. Missing command line tools (which the docs never mentioned):
   - Brew install xcodegen
   - Brew install swiftgen
   - Brew install swiftformat
2. Non-merged fixes and open issues
   - https://github.com/swiyu-admin-ch/eidch-ios-wallet/issues?q=is%3Aissue%20state%3Aclosed
   - https://github.com/swiyu-admin-ch/eidch-android-wallet/issues?q=is%3Aissue%20state%3Aclosed
3. Also, but not problematic it required a level of setup by the users, and the requirement of Xcode

#### >> Changing direction <<

One github issue mentioned that the problem is that the SWIYU app requires backend to be hosted on HTTPS.  
Solution: Having Nginx as reverse proxy for the backend servers.  
With some sys-admin work, the issuer environment is now working online!  
Visit online at: https://eid.c4dt.org  
Analyzing the requests that happen -from wallet to issuer server- after reading the QR code:

1. GET http://issuer-agent-oid4vci:8080/.well-known/openid-credential-issuer -- to get the details of the available credentials on this server
2. GET Request to http://issuer-agent-oid4vci:8080/.well-known/openid-configuration -- to get information on the token endpoint URLs.
3. POST http://issuer-agent-oid4vci:8080/api/v1/token -- trade pre-authorization token for a bearer token
4. POST http://issuer-agent-oid4vci:8080/api/v1/credential -- uses the bearer token to get the credential

#### Outcome of the week:

- Communication with the E-ID team on a couple of issues
- https://github.com/c4dt/SWIYU-demo
- Our test environment available on https://eid.c4dt.org

### Weeks 21 to 25

**GOALS:**

- Enhance issue workflow with no bugs.
- Move to verifier flow.
- Incorporate the swiyu team's Beta ID into the issuance flow.
- Prepare the whole demo.

I didn't keep up with traditional remarks as I was in a rust to meet the deadline for the workshop.
