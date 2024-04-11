class CryptomusError(Exception):
    def __init__(self, message: str) -> Exception:
        return super().__init__(message)
