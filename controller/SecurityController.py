from passlib.hash import pbkdf2_sha256
from models.User import User
from extensions import db

# Verifica el Login
async def verify_login(username, passwd):
    valid = False
    
    user = db.session.query(User).filter(User.username == username).first()
    if user:
        if await verify_passwd(passwd, user.passwd):
            valid = True

    return valid


# Encripta la contraseña
def encrypt_passwd(passwd):
    hash_passwd = pbkdf2_sha256.hash(passwd)
    return hash_passwd

# Verifica si la contraseña concuerda con la del hash
async def verify_passwd(passwd, hash):
    return pbkdf2_sha256.verify(passwd, hash)