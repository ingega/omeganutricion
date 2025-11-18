import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from src.services.products.config import settings
from src.services.products.models import UserDB
from src.services.products.database import get_db



# router is necessary for token ep

router = APIRouter()

# constants

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
TIME_EXPIRATION = 30  # minutes


class APIError(Exception):
    pass

password_hash = PasswordHash.recommended()

# hash functions

def password_hashed(password: str) -> str:
    hashed = password_hash.hash(password)
    return hashed

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    pwdlib (pwd_context) contains a function that verifies password against hashed password
    :param plain_password: plain password
    :param hashed_password: hashed password
    :return: bool value indicating whether password matches hashed password
    """
    return password_hash.verify(plain_password, hashed_password)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(username: str,
             db: Session):
    """
    1. import session local
    2. query the username
    3. Launch the logical
    """

    user_query = db.query(UserDB).filter(UserDB.username == username).first()
    if not user_query:
        raise HTTPException(status_code=404, detail="User not found")

    return user_query


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user(username, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(password, user.password):
        print(password, password_hashed(password), user.password, sep="\n")
        raise HTTPException(status_code=401,
                            detail="Incorrect password",
                            headers={"WWW-Authenticate": "Bearer"}
                            )

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=TIME_EXPIRATION)
    to_encode['exp'] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    This function rescue the username from a codify token,
    with this, we can validate the token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        # payload rescue the information within the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=400, detail="username missing in payload")
    except InvalidTokenError as e:
        credentials_exception.detail = "Could not validate credentials: " + str(e)
        raise credentials_exception
    user = get_user(username=username, db=db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"not username: {username} in database",
                                headers={"WWW-Authenticate": "Bearer"}
                                )
    return user


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                    db: Session = Depends(get_db)
                                 ):
    """
    Handles user login, authenticates credentials, and issues a JWT access token.
    """
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)

    if not user:
        return HTTPException(status_code=401,
                             detail="Incorrect username or password",
                             headers={"WWW-Authenticate": "Bearer"}
                             )

    return {"access_token": create_access_token(data={"sub": user.username}),
            "token_type": "bearer"}
