from jwt import encode, decode
from dotenv import load_dotenv
import os
load_dotenv()

KEYWORD = os.getenv('KEYWORD') 

# Create token
def create_token(data: dict) -> str:
    token: str = encode(
        payload=data, # Content to token
        key=KEYWORD, # key word
        algorithm="HS256"
    )
    return token 

def validate_token(token: str) -> dict:
    data: dict = decode(token,key=KEYWORD, algorithms=['HS256'])
    return data