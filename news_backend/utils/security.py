import bcrypt

BCRYPT_MAX_PASSWORD_BYTES = 72

def _password_bytes(password: str) -> bytes:
  # bcrypt 只使用前 72 字节，passlib 旧版本也是同样行为
  return password.encode("utf-8")[:BCRYPT_MAX_PASSWORD_BYTES]

# 密码加密
def get_hash_password(password: str) -> str:
  return bcrypt.hashpw(_password_bytes(password), bcrypt.gensalt()).decode("utf-8")

# 密码验证：返回值为布尔
def verify_password(plain_password: str, hashed_password: str) -> bool:
  try:
    return bcrypt.checkpw(
      _password_bytes(plain_password),
      hashed_password.encode("utf-8")
    )
  except (TypeError, ValueError):
    return False
