import os
from fastapi import HTTPException, Request 
from clerk_backend_api import Clerk, AuthenticateRequestOptions
from dotenv import load_dotenv

load_dotenv()

def authenticate_and_get_user(request: Request):
    clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))
    jwt_key=os.getenv("JWT_KEY")

    try:
        request_state = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=[
                    "http://10.10.10.158:5173",
                    "http://172.20.10.4:5173",
                    " http://localhost:5173",
                    "https://onction-dashboard.netlify.app"
                    ],
                jwt_key=jwt_key
            )   
        )
        if request_state.is_signed_in:
            user_id = request_state.payload.get("sub")
            return {"user_id": user_id}
        else:
            raise HTTPException(status_code=401, detail="Not signed in")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))









# def authenticate_and_get_user(request: Request):
#     clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))
#     jwt_key = os.getenv("JWT_KEY")
#     try:
#         if not jwt_key:
#             raise HTTPException(status_code=500, detail="JWT_KEY not configured")
        
#         request_state = clerk_sdk.authenticate_request(
#             request,
#             AuthenticateRequestOptions(
#                 authorized_parties=["http://10.10.10.158:5173"],
#                 jwt_key=jwt_key
#             )
#         )
        
#         print(f"Authentication state: is_signed_in={request_state.is_signed_in}, reason={request_state.reason}")
        
#         # Check authentication status
#         if not request_state.is_signed_in:
#             error_msg = f"User not authenticated"
#             if request_state.reason:
#                 error_msg += f": {request_state.reason}"
#             raise HTTPException(status_code=401, detail=error_msg)
        
#         # Validate payload exists
#         if not hasattr(request_state, 'payload') or not request_state.payload:
#             raise HTTPException(status_code=401, detail="No payload in authentication token")
        
#         # Extract user_id
#         user_id = request_state.payload.get("sub")
#         if not user_id:
#             # Try alternative fields
#             user_id = (
#                 request_state.payload.get("user_id") or 
#                 request_state.payload.get("id") or
#                 request_state.payload.get("clerk_user_id")
#             )
        
#         if not user_id:
#             available_keys = list(request_state.payload.keys())
#             raise HTTPException(
#                 status_code=401, 
#                 detail=f"No user ID found. Available payload keys: {available_keys}"
#             )
        
#         print(f"Successfully authenticated user: {user_id}")
        
#         # ALWAYS return a dictionary
#         return {
#             "user_id": user_id,
#             "session_id": request_state.payload.get("sid"),
#             "email": request_state.payload.get("email"),
#             "first_name": request_state.payload.get("given_name") or request_state.payload.get("first_name"),
#             "last_name": request_state.payload.get("family_name") or request_state.payload.get("last_name"),
#             "image_url": request_state.payload.get("picture") or request_state.payload.get("image_url"),
#             "issued_at": request_state.payload.get("iat"),
#             "expires_at": request_state.payload.get("exp")
#         }
        
#     except HTTPException:
#         # Re-raise HTTP exceptions
#         raise
#     except Exception as e:
#         print(f"Authentication exception: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")