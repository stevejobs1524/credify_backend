from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel

app = FastAPI()

class InstagramAccount(BaseModel):
    username: str

@app.post("/verify")
async def verify_account(account: InstagramAccount):
    username = account.username
    url = f"https://www.instagram.com/{username}/?__a=1"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'graphql' in data:
            user_data = data['graphql']['user']
            is_private = user_data['is_private']
            is_verified = user_data['is_verified']
            
            if is_private:
                return {"status": "error", "message": "Account is private."}
            if is_verified:
                return {"status": "success", "message": "Account is verified."}
            else:
                return {"status": "error", "message": "Account is not verified."}
        else:
            raise HTTPException(status_code=404, detail="Account not found.")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

