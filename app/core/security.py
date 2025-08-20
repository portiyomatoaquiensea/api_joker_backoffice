
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
import os
from dotenv import load_dotenv
load_dotenv()

bearer_scheme = HTTPBearer(auto_error=True)

def get_current_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    # Here you can validate your JWT or token
    # Example: if using a static token for testing
    if not token or token != os.getenv("LOCAL_SECRET"):
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return token