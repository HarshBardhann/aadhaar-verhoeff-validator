# Integration guide

> **Important limitation:** This tool validates the format and Verhoeff checksum of an Aadhaar-formatted number. It does not confirm that the number was issued by UIDAI, exists in official records, is active, or belongs to any individual. A checksum-valid number may be entirely fabricated. Do not use this tool as a substitute for official Aadhaar verification or identity authentication.

All examples use the synthetic number `123456789010`. Check for exactly 12 ASCII digits, reject malformed input instead of trying to fix it, and always run the check on the backend even if a frontend already does.

## Python backend (FastAPI)

```python
from fastapi import FastAPI
from pydantic import BaseModel

from aadhaar_validator import validate_aadhaar_checksum

app = FastAPI()


class Request(BaseModel):
    number: str


@app.post("/validate")
def validate(body: Request):
    format_valid = len(body.number) == 12 and body.number.isascii() and body.number.isdigit()
    checksum_valid = format_valid and validate_aadhaar_checksum(body.number)
    return response(format_valid, checksum_valid)
```

Install FastAPI separately (`pip install fastapi uvicorn`), save the file as `app.py`, and run `uvicorn app:app --reload`. FastAPI is only an example here; it is not a project dependency.

## Browser form and API layer

```js
const { validateAadhaarChecksum } = require("./verhoeff");

form.addEventListener("submit", (event) => {
  if (!validateAadhaarChecksum(input.value)) event.preventDefault();
});
```

Treat this as feedback only. A backend handler (Express or anything else) still has to call the same module, checking `typeof value === "string"` first. Run `node integrations/javascript/example.js` for the standalone proof.

## API response contract

The helper below builds a local result. It must not be presented as a UIDAI response:

```python
def response(format_valid, checksum_valid):
    if not format_valid:
        message = "Input format is invalid. No official issuance or identity verification was performed."
    elif not checksum_valid:
        message = "Checksum validation failed. This does not independently establish whether the identifier was issued by UIDAI."
    else:
        message = "Checksum validation passed. UIDAI issuance and identity have not been verified."
    return {"format_valid": format_valid, "checksum_valid": checksum_valid,
            "uidai_issuance_verified": False, "identity_verified": False, "message": message}
```

Format valid, checksum valid:

```json
{"format_valid":true,"checksum_valid":true,"uidai_issuance_verified":false,"identity_verified":false,"message":"Checksum validation passed. UIDAI issuance and identity have not been verified."}
```

Format valid, checksum invalid:

```json
{"format_valid":true,"checksum_valid":false,"uidai_issuance_verified":false,"identity_verified":false,"message":"Checksum validation failed. This does not independently establish whether the identifier was issued by UIDAI."}
```

Malformed input:

```json
{"format_valid":false,"checksum_valid":false,"uidai_issuance_verified":false,"identity_verified":false,"message":"Input format is invalid. No official issuance or identity verification was performed."}
```

Treat failures as ordinary validation results, avoid echoing values into logs, rate-limit public endpoints where that matters, and don't build enumeration or identity-discovery features on top of this check.
