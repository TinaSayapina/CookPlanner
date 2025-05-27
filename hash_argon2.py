from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
ph = PasswordHasher()

def hash_password(password: str)-> str:
    return ph.hash(password)

def check_pw(password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, password)
    except VerifyMismatchError:
        return False
    except Exception:
        return False

# print(hashed)
# print(check_pw(123, hashed))