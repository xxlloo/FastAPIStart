from passlib.context import CryptContext


class PasswordUtil:
    def __init__(self):
        # 创建密码上下文，可以同时支持多种加密算法
        self.pwd_context = CryptContext(
            schemes=["bcrypt", "pbkdf2_sha256", "sha256_crypt"], deprecated="auto"
        )

    def encrypt_bcrypt(self, password: str) -> str:
        """使用 bcrypt 算法加密密码"""
        return self.pwd_context.hash(password)

    def verify_bcrypt(self, password: str, hashed: str) -> bool:
        """验证 bcrypt 加密的密码"""
        return self.pwd_context.verify(password, hashed)

    def encrypt_sha256(self, password: str) -> str:
        """使用 SHA-256 算法加密密码"""
        return self.pwd_context.hash(password)

    def verify_sha256(self, password: str, hashed: str) -> bool:
        """验证 SHA-256 加密的密码"""
        return self.pwd_context.verify(password, hashed)

    def encrypt_pbkdf2(self, password: str) -> str:
        """使用 PBKDF2 算法加密密码"""
        return self.pwd_context.hash(password)

    def verify_pbkdf2(self, password: str, hashed: str) -> bool:
        """验证 PBKDF2 加密的密码"""
        return self.pwd_context.verify(password, hashed)


# 示例
if __name__ == "__main__":
    util = PasswordUtil()

    password = "Qwe123"

    # 加密
    hashed_bcrypt = util.encrypt_bcrypt(password)
    hashed_sha256 = util.encrypt_sha256(password)
    hashed_pbkdf2 = util.encrypt_pbkdf2(password)

    print(f"bcrypt: {hashed_bcrypt}")
    print(f"sha256: {hashed_sha256}")
    print(f"pbkdf2: {hashed_pbkdf2}")

    # 验证
    print(util.verify_bcrypt(password, hashed_bcrypt))  # True
    print(util.verify_sha256(password, hashed_sha256))  # True
    print(util.verify_pbkdf2(password, hashed_pbkdf2))  # True
