from fastapi import Request, HTTPException, status, Depends
from src.utils.settings import settings
from sqlalchemy.orm import Session
import jwt
from jwt import InvalidTokenError
from src.users.models import UserModel
from src.utils.db import get_db

# protected routes

def is_authenticate(request: Request, db: Session = Depends(get_db)):
    try:     
        token = request.headers.get("authorization") # Headers({'authorization': 'jwt eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOjMsImV4cCI6MTc5MjM5MDg4NX0.CeHiZF6sHS6AbX9KwxeaZRnJ1-KGeZ3AGbTphpwIRoA', 'cache-control': 'no-cache', 'postman-token': '2f3a9e66-2cc4-4204-83d9-92fe8abd1f18', 'host': '127.0.0.1:8000', 'user-agent': 'PostmanRuntime/2.11.2', 'accept': '*/*', 'accept-encoding': 'gzip, deflate, br', 'connection': 'keep-alive'})
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You Are Unauthorized")

        token = token.split(" ")[-1] # jwt eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOjMsImV4cCI6MTc5MjM5MDg4NX0.CeHiZF6sHS6AbX9KwxeaZRnJ1-KGeZ3AGbTphpwIRoA

        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        # print(data) # {'_id': 3, 'exp': 1792390885}
        user_id = data.get("_id")


        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You Are Unauthorized")

        return user

    except InvalidTokenError:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You Are Unauthorized")












