from src.users.dtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.users.models import UserModel
from fastapi import HTTPException, status, Request, BackgroundTasks
from pwdlib import PasswordHash
import jwt
from src.utils.settings import settings
from datetime import datetime, timedelta
from jwt.exceptions import InvalidTokenError
from src.utils.mail import send_email



password_hash = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
     return password_hash.verify(plain_password, hashed_password)



async def register(body: UserSchema, db: Session, bg_task: BackgroundTasks):
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(400, detail="Username already exist..") # username validation should be unique
    
    is_user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_user:
            raise HTTPException(400, detail="Email already exist..") # email validation
    
    # hash_password = get_password_hash(body.password)
    hashed_password = get_password_hash(body.password)

    new_user = UserModel(
        name = body.name,
        username = body.username,
        password = hashed_password,
        email = body.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    ## send email confirmation
    #res = await send_email([new_user.email])
    bg_task.add_task(send_email, [new_user.email])
 
    return new_user


def login_user(body: LoginSchema, db: Session):
     
     user = db.query(UserModel).filter(UserModel.username == body.username).first()
     if not user:
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You Entered Wrong Username")

     if not verify_password(body.password, user.password):
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You Entered Wrong Password")


     exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)
    #  exp_time = datetime.now() + timedelta(seconds=30)

     token = jwt.encode({"_id": user.id, "exp": exp_time.timestamp()}, settings.SECRET_KEY, settings.ALGORITHM) # one of _id or username shpuld be unique then it can generate token

     return {"token":token}



## api call then send token

def is_authenticate(request: Request, db: Session):
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
         








