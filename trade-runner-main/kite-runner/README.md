# kite-runner
Kite Platform access interface

### Prerequisites Library
* python 3.8 or above
* kiteconnect library
* selenium library

### Prerequisites Files
* Save User & App credentials in "keystrings/kite/PRIVATE.KEY" in format:
  * username:encryp_password:TOTP_KEY:APP_NAME:APP_Key:APP_SECRET:PASS_KEY

### How to generate daily access-token
* Run **access-token.py**.
* access-token.py reads **PRIVATE.KEY** from above mentioned PATHS.
* access-token.py generates access-token in **keystrings/kite/ACCESS.TOK**.

### How to connect to Kite and query stock
* Run **run.py**.
* run.py reads access-token from above **keystrings/kite/ACCESS.TOK**.



\*  Password must be saved using SHA256 algorithm in PRIVATE.KEY. Use keystrings/keygen.py to generate password in encrypted format.
\* PASS_KEY is optional. Do not pass PASS_KEY if password is not encrypted.
